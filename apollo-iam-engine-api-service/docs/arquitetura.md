# Apollo IAM Engine — Arquitetura Tecnica

**Versao:** 1.0.0  
**Padrao:** Clean Architecture + DDD  
**Autor:** Elias Andrade — O2 Data Solutions

---

## Visao Geral

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INTERFACE LAYER                              │
│                                                                     │
│  ┌──────────────────────────┐   ┌──────────────────────────────┐   │
│  │  FastAPI — API REST      │   │  Starlette — WebApp Admin    │   │
│  │  /auth, /admin/*         │   │  Jinja2 templates            │   │
│  │  /admin/policies/*       │   │  Dashboard responsivo        │   │
│  │  /health                 │   │  http://localhost:8080       │   │
│  └────────────┬─────────────┘   └──────────────────────────────┘   │
│               │ Middlewares: CORS, RateLimit, SecurityHeaders,      │
│               │ RequestQueue, RequestLog                            │
└───────────────┼─────────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                              │
│                                                                     │
│  Services: PolicyService, AuthService (via use cases)              │
│  Use Cases: LoginUseCase, LogoutUseCase, RefreshUseCase,           │
│             ValidateUseCase, DeleteUserUseCase, ...                │
│  DTOs: LoginInputDTO, TokenOutputDTO, UserCreateDTO, ...           │
└───────────────┬─────────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────────┐
│                        DOMAIN LAYER                                 │
│                                                                     │
│  Entities: User, Role, Permission, Group, Policy,                  │
│            RbacAttribute, CustomEntityType, CustomEntityValue      │
│  Value Objects: TokenPayload, Email, Password                      │
│  Ports: UserRepository, RoleRepository, PermissionRepository,      │
│         GroupRepository, RbacAttributeRepository,                  │
│         TokenService, PasswordHasher, AuditLogger                  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Apollo Policy Language (APL) Engine v3                      │  │
│  │  src/domain/policy/policy_dsl.py                             │  │
│  │                                                              │  │
│  │  PolicyEngine.evaluate(EvalContext) -> EvalResult            │  │
│  │  PolicyEngine.explain(EvalContext)  -> dict (trace)          │  │
│  │  PolicyEngine.simulate(policies, ctx) -> dict (what-if)      │  │
│  │  16 operadores, AND/OR, glob, hierarquia, templating         │  │
│  │  Time-based: valid_from, valid_until, time_window            │  │
│  │  Context schema validation, conflict resolution score        │  │
│  │  Regex seguro: timeout 0.5s, limite 256 chars (ReDoS)        │  │
│  │  Policy composition: global -> tenant -> user                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└───────────────┬─────────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                             │
│                                                                     │
│  Database:                                                          │
│    SQLAlchemy 2.x + SQLite WAL                                      │
│    PRAGMA cache_size=-32768 (32 MB)                                 │
│    PRAGMA mmap_size=536870912 (512 MB)                              │
│    PRAGMA wal_autocheckpoint=1000                                   │
│    expire_on_commit=False (evita re-SELECT pos-commit)              │
│    joinedload() em todas as queries com relacionamentos             │
│                                                                     │
│  Cache (in-memory, LRU+TTL, thread-safe):                          │
│    token_cache          4096 entries  TTL 30s                       │
│    blacklist_cache      8192 entries  TTL 120s                      │
│    user_enrichment_cache 512 entries  TTL 300s                      │
│    decision_cache       8192 entries  TTL 60s  (APL)               │
│    metrics_cache           4 entries  TTL 5s                        │
│    settings_cache          4 entries  TTL 60s                       │
│                                                                     │
│  Security:                                                          │
│    JwtTokenService (HS256, decode com cache L1)                     │
│    BcryptPasswordHasher                                             │
│    SqliteTokenBlacklist (L1 cache + L2 SQLite)                      │
│    SecurityHeadersMiddleware                                        │
│    RateLimitMiddleware (sliding window por IP + por tenant v3)      │
│    RequestQueueMiddleware (backpressure)                            │
│    PEPMiddleware (Policy Enforcement Point ASGI v3)                 │
│    mTLS (TLS 1.2+, ECDHE+AES-GCM, ECDHE+CHACHA20)                 │
│                                                                     │
│  Logging:                                                           │
│    EventLogger: fila assincrona + background thread                 │
│    Saidas: JSON (NDJSON), YAML, Markdown, SQLite                    │
│    DecisionAudit: tabela dedicada para decisoes APL                 │
│    LogHooks: funcoes tipadas por dominio                            │
│    ConsoleLogger: output colorido (rich/colorama)                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Autenticacao

```
POST /auth/token  {username, password}
        │
        ▼
  LoginUseCase
        │
        ├─ UserRepository.find_by_username()          [idx: username]
        │
        ├─ PasswordHasher.verify(plain, hashed)       [bcrypt — lento intencional]
        │
        ├─ _enrich_from_db(user_id)
        │    ├─ user_enrichment_cache.get(user_id)    [L1 — TTL 300s]
        │    │    HIT  → retorna imediatamente
        │    │    MISS → consulta DB
        │    │
        │    ├─ SELECT roles, permissions via joinedload()
        │    ├─ SELECT user_rbac_values WHERE user_id = ?   [idx: user_id]
        │    ├─ SELECT user_custom_entities WHERE user_id = ? [idx: user_id]
        │    └─ user_enrichment_cache.set(user_id, data, ttl=300)
        │
        ├─ JwtTokenService.create_access_token(payload)
        │    payload: {sub, user_id, is_superuser, roles, permissions,
        │              group, group_id, user_type, user_level,
        │              user_level_rank, rbac, abac, exp, iat, jti}
        │
        └─ AuditLogger.log(auth.login_success)
                │
                └─ EventLogger.log_event() → fila assincrona → background thread
                                           → SQLite (apollo_log.db)
                                           → JSON/YAML/MD (async)

Response: {access_token, refresh_token, token_type, expires_in}
```

---

## Fluxo de Validacao de Token

```
POST /auth/validate  {token}
        │
        ▼
  JwtTokenService.decode_token(token)
        │
        ├─ token_cache.get(sha256(token)[:32])        [L1 — TTL 30s]
        │    HIT  → retorna TokenPayload imediatamente (< 0.1ms)
        │    MISS → continua
        │
        ├─ jwt.decode(token, secret_key, algorithms=["HS256"])
        │
        ├─ SqliteTokenBlacklist.is_revoked(jti)
        │    ├─ blacklist_cache.get(jti)              [L1 — TTL 120s]
        │    │    HIT  → retorna bool imediatamente
        │    │    MISS → SELECT FROM token_blacklist WHERE jti = ?  [idx: jti]
        │    └─ blacklist_cache.set(jti, result)
        │
        ├─ token_cache.set(key, payload, ttl=min(remaining, 30))
        │
        └─ retorna TokenPayload
```

---

## Fluxo de Avaliacao APL

```
POST /admin/policies/evaluate
  {subject, action, resource, tenant_id, subject_id, use_cache}
        │
        ▼
  PolicyService.evaluate()
        │
        ├─ DecisionCache.get(tenant_id, subject_id, action, resource)
        │    chave: SHA-256(tenant_id:subject_id:action:resource)
        │    HIT  → retorna EvalResult imediatamente (< 1ms)
        │    MISS → continua
        │
        ├─ PolicyEngine.evaluate(EvalContext)
        │    │
        │    ├─ filtra policies por tenant_id
        │    │    (tenant_id == ctx.tenant_id) OR (tenant_id IS NULL)
        │    │    [idx: ix_policies_tenant_enabled_prio]
        │    │
        │    ├─ filtra por enabled=True
        │    │
        │    ├─ v3: verifica time validity (valid_from, valid_until, time_window)
        │    │
        │    ├─ ordena por priority ASC (menor = maior prioridade)
        │    │
        │    ├─ para cada policy:
        │    │    ├─ action_match(ctx.action, policy.actions)   [glob]
        │    │    ├─ resource_match(ctx.resource, policy.resources) [hierarquico]
        │    │    ├─ resolve_templates(conditions, ctx)         [{{subject_id}}, etc]
        │    │    ├─ evaluate_conditions(conditions, ctx)       [16 operadores]
        │    │    ├─ v3: schema_validation(policy.context_schema, ctx)
        │    │    │
        │    │    ├─ effect=deny  → candidato deny (maior conflict_score vence)
        │    │    └─ effect=allow → candidato allow (maior conflict_score vence)
        │    │
        │    ├─ deny candidates → vence o de maior conflict_score
        │    │    conflict_score = scope_score(user=300,tenant=200,global=100) + weight
        │    │
        │    └─ sem match → default DENY
        │
        ├─ DecisionCache.set(key, result, ttl=60)
        │
        ├─ log_decision() → SQLite decision_audit (async)
        │
        └─ retorna EvalResult {allowed, effect, matched_policy, reason}
```

---

## Modelo de Dados

```
users
  id (PK)
  username (UNIQUE, idx)
  email (UNIQUE, idx)
  hashed_password
  is_active (idx)
  is_superuser (idx)
  group_id (FK groups.id, idx)
  type_id  (FK user_types.id, idx)
  level_id (FK user_levels.id, idx)
  created_at, updated_at

user_roles (M2M)
  user_id (FK, idx)
  role_id (FK, idx)

user_rbac_values (M2M + value)
  user_id      (FK, idx)
  attribute_id (FK, idx)
  value

user_custom_entities
  user_id          (idx)
  entity_type_slug (idx)
  entity_value_id
  assigned_at
  UNIQUE(user_id, entity_type_slug)

roles
  id (PK)
  name (UNIQUE, idx)
  is_active (idx)

role_permissions (M2M)
  role_id       (FK, idx)
  permission_id (FK, idx)

permissions
  id (PK)
  name (UNIQUE, idx)
  resource (idx)
  action   (idx)
  INDEX(resource, action)

groups
  id (PK)
  name (UNIQUE, idx)
  is_active (idx)

rbac_attributes
  id (PK)
  key (UNIQUE, idx)
  is_active (idx)
  INDEX(key, is_active)

custom_entity_types
  id (PK)
  slug (UNIQUE, idx)
  is_active (idx)

custom_entity_values
  id (PK)
  entity_type_slug (idx)
  INDEX(entity_type_slug, is_active)

policies
  id (PK)
  name (idx)
  tenant_id (idx)
  enabled   (idx)
  priority
  scope     (idx)
  subject_id (idx)
  INDEX(tenant_id, enabled, priority)   ← query principal do engine
  INDEX(scope, enabled)

audit_logs
  id (PK)
  actor    (idx)
  action   (idx)
  resource (idx)
  status   (idx)
  created_at (idx)
  INDEX(actor, status)
  INDEX(resource, status)

token_blacklist
  jti (PK, idx)
  revoked_at

settings
  id (PK, singleton)
  access_token_expire_minutes
  refresh_token_expire_days
  allow_registration
  max_login_attempts
  lockout_minutes

-- banco separado: data/apollo_log.db --

event_log
  seq (PK, autoincrement)
  uid (UNIQUE)
  hash (SHA-256 integridade)
  timestamp (idx)
  event     (idx)
  actor     (idx)
  tenant_id (idx)
  status    (idx)
  INDEX(actor, status)
  INDEX(tenant_id, event)

decision_audit
  seq (PK, autoincrement)
  uid (UNIQUE, idx)
  timestamp  (idx)
  actor      (idx)
  subject_id (idx)
  tenant_id  (idx)
  action     (idx)
  decision   (idx)
  INDEX(tenant_id, decision)
  INDEX(subject_id, action)
```

---

## Camada de Cache — Detalhamento

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cache Architecture                           │
│                                                                 │
│  token_cache                                                    │
│    key:   SHA-256(token_raw)[:32]                               │
│    value: TokenPayload serializado                              │
│    TTL:   min(token_remaining_seconds, 30s)                     │
│    size:  4096 entries (LRU)                                    │
│    uso:   evita jwt.decode() + blacklist check a cada request   │
│                                                                 │
│  blacklist_cache                                                │
│    key:   jti (UUID do token)                                   │
│    value: True (revogado) | False (nao revogado)                │
│    TTL:   3600s (revogado) | 30s (nao revogado)                 │
│    size:  8192 entries (LRU)                                    │
│    uso:   evita SELECT na token_blacklist a cada request        │
│                                                                 │
│  user_enrichment_cache                                          │
│    key:   user_id                                               │
│    value: {roles, permissions, rbac, abac, group, level}        │
│    TTL:   300s (5 minutos)                                      │
│    size:  512 entries (LRU)                                     │
│    uso:   evita 4+ queries no login                             │
│                                                                 │
│  decision_cache                                                 │
│    key:   SHA-256(tenant_id:subject_id:action:resource:subject) │
│    value: _DecisionEntry {allowed, effect, matched_policy, ...} │
│    TTL:   60s (default) | configuravel por policy_id            │
│    size:  8192 entries (LRU)                                    │
│    uso:   evita avaliacao APL completa (engine em memoria)      │
│    v3:    chave inclui subject completo — sem decisoes erradas  │
│    isolamento: chave inclui tenant_id — sem vazamento           │
│                                                                 │
│  metrics_cache / db_kpis_cache / settings_cache                 │
│    TTL:   5s / 10s / 60s                                        │
│    uso:   evita COUNT(*) e psutil a cada request de dashboard   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Middlewares (ordem de execucao)

```
Request
  │
  ▼
CORSMiddleware          — headers CORS, preflight OPTIONS
  │
  ▼
RequestQueueMiddleware  — backpressure: fila de 100 req, timeout 30s
  │                       retorna 503 se fila cheia
  ▼
RateLimitMiddleware     — sliding window por IP + por tenant (v3)
  │                       /auth/token: 10/min IP | 50/min tenant
  │                       global: 200/min IP | 600/min tenant
  ▼
SecurityHeadersMiddleware — X-Content-Type-Options, X-Frame-Options,
  │                         HSTS, CSP, X-XSS-Protection
  ▼
RequestLogMiddleware    — log de cada request/response no EventLogger
  │
  ▼
PEPMiddleware (opcional) — Policy Enforcement Point
  │                        avalia APL antes do handler
  │                        retorna 403 + X-APL-Decision se negado
  ▼
Router (FastAPI)
  │
  ▼
Response
```

---

## Multi-Tenant

Isolamento logico via `tenant_id` em:

| Componente | Como usa tenant_id |
|---|---|
| `PolicyModel` | Coluna `tenant_id` — policies por tenant |
| `EvalContext` | Campo `tenant_id` — contexto de avaliacao |
| `DecisionCache` | Incluido na chave SHA-256 — sem vazamento |
| `EventLogger` | Campo `tenant_id` em todos os eventos |
| `decision_audit` | Coluna `tenant_id` — auditoria por tenant |

Policies com `tenant_id=NULL` sao **globais** — aplicam a todos os tenants.  
Policies de tenant especifico sobrescrevem as globais (scope hierarchy).

---

## Event Logger — Arquitetura Assincrona

```
log_event() chamado no request handler
        │
        ├─ INSERT no SQLite (apollo_log.db) — sincrono, com _db_lock
        │    autoincrement elimina SELECT MAX(seq)
        │
        └─ _file_queue.put_nowait(entry)   — nao bloqueia o request
                │
                ▼
        background thread (daemon)
                │
                ├─ open(apollo_events.json, "a") → NDJSON
                ├─ open(apollo_events.yaml, "a") → YAML docs
                └─ open(apollo_events.md,   "a") → Markdown table

Beneficio: file I/O (lento) nao impacta latencia dos requests.
Fila: maxsize=10000 — descarta silenciosamente se cheia (nao bloqueia).
```

---

## Seguranca — Resumo

| Mecanismo | Implementacao |
|---|---|
| Autenticacao | JWT HS256, access + refresh token |
| Senhas | Bcrypt (salt automatico, custo alto intencional) |
| Token revogacao | Blacklist persistida + cache L1 (TTL 3600s) |
| Transport | mTLS TLS 1.2+, ECDHE+AES-GCM, ECDHE+CHACHA20 |
| Rate limiting IP | Sliding window por IP, por rota |
| Rate limiting tenant | Sliding window por X-Tenant-ID, por rota (v3) |
| Headers | HSTS, CSP, X-Frame-Options, X-Content-Type-Options |
| Backpressure | RequestQueueMiddleware (503 se fila cheia) |
| PEP | PEPMiddleware ASGI — avalia APL antes do handler (v3) |
| Auditoria | EventLogger imutavel, SHA-256 por entrada |
| Policy | Deny explicito sempre vence, default deny |
| Multi-tenant | Isolamento por tenant_id em policies, cache e rate limit |
| Regex | Timeout 0.5s + limite 256 chars (ReDoS protection v3) |

---

*Elias Andrade — O2 Data Solutions*

---

## Novidades v3 — APL Engine

### Conflict Resolution Score

Quando multiplas policies conflitam (ex: 2 allows ou 2 denies aplicaveis),
o engine usa `conflict_score` para determinar qual vence:

```
conflict_score = scope_score + weight

scope_score:
  scope=user   -> 300  (mais especifico)
  scope=tenant -> 200
  scope=global -> 100  (menos especifico)

weight: configuravel por policy (default 0)
```

O resultado inclui `conflict_score` da policy vencedora para auditoria.

### Time-Based Policies

```json
{
  "valid_from":  "2026-01-01T00:00:00Z",
  "valid_until": "2026-12-31T23:59:59Z",
  "time_window": "08:00-18:00"
}
```

- `valid_from` / `valid_until`: ISO 8601 UTC — policy ativa apenas nesse periodo
- `time_window`: janela horaria diaria (suporta janela que cruza meia-noite: "22:00-06:00")
- Policies fora do periodo sao puladas e listadas em `EvalResult.time_skipped`
- Operadores `time_before` e `time_after` para condicoes baseadas em hora atual

### Context Schema Validation

```json
{
  "context_schema": {
    "user_level": "int",
    "roles": "list",
    "department": "string",
    "is_active": "bool"
  }
}
```

- Valida tipos dos campos do contexto em runtime
- Nao bloqueia a avaliacao — registra violacoes em `EvalResult.schema_violations`
- Util para detectar bugs silenciosos de coercao de tipo

### Regex Seguro (ReDoS Protection)

```python
_REGEX_EXECUTOR = ThreadPoolExecutor(max_workers=4)
_REGEX_MAX_LEN  = 256   # tamanho maximo do pattern
_REGEX_TIMEOUT  = 0.5   # segundos — mata regex catastrofico
```

- Pattern com mais de 256 chars e rejeitado imediatamente
- Execucao em thread separada com timeout de 0.5s
- Regex catastrofico (catastrophic backtracking) e morto sem derrubar o processo

### Policy Simulation / Sandbox

```
POST /admin/policies/simulate
  policies: [lista de policies temporarias]
  subject, action, resource, tenant_id, subject_id

POST /admin/policies/simulate/batch
  policies: [lista de policies temporarias]
  contexts: [lista de contextos a testar]
```

- Zero persistencia — nao altera o engine global, nao grava audit
- Retorna resultado completo com traces por condicao
- Ideal para: CI/CD de policies, test suite, dry-run antes de ativar

### Policy Enforcement Point (PEP)

```python
from src.infrastructure.security.pep_middleware import PEPMiddleware, PEPRule

app.add_middleware(PEPMiddleware, rules=[
    PEPRule(
        path_prefix="/api/cotacoes",
        action="cotacao:read",
        resource_template="cotacao/{path_suffix}",
        tenant_id_header="X-Tenant-ID",
        skip_superuser=True,
        methods=["GET", "POST", "PUT", "DELETE"],
    ),
])
```

Headers adicionados na resposta:
```
X-APL-Decision: allow | deny | no_match
X-APL-Policy:   <policy_id que decidiu>
```

---

*Elias Andrade — O2 Data Solutions*

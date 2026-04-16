# 🏰 Apollo IAM Engine — Arquitetura

> *"O Castelo de Ooo tem muitas camadas — cada uma protege a próxima!"*

**Padrão:** Clean Architecture + DDD  
**Versão:** 2.0

---

## Visão Geral

```
╔══════════════════════════════════════════════════════════════════╗
║                    🌐 Interface Layer                            ║
║  ┌─────────────────────┐    ┌──────────────────────────────┐    ║
║  │   FastAPI (API)     │    │   Starlette (WebApp)         │    ║
║  │  /auth, /admin      │    │   Dashboard UI               │    ║
║  │  /admin/policies    │    │   Templates Jinja2           │    ║
║  └──────────┬──────────┘    └──────────────────────────────┘    ║
╚═════════════╪════════════════════════════════════════════════════╝
              │
╔═════════════▼════════════════════════════════════════════════════╗
║                  🧠 Application Layer                            ║
║  Services: AuthService, RbacService, PolicyService              ║
║  Use Cases: Login, Logout, Refresh, Validate, Check             ║
║  DTOs: LoginInputDTO, TokenOutputDTO, ...                       ║
╚═════════════╪════════════════════════════════════════════════════╝
              │
╔═════════════▼════════════════════════════════════════════════════╗
║                   💎 Domain Layer                                ║
║  Entities: User, Role, Permission, Group, Policy                ║
║  Value Objects: TokenPayload, Email, Password                   ║
║  Ports: UserRepository, TokenService, PasswordHasher            ║
║  ┌─────────────────────────────────────────────────────────┐    ║
║  │  🔮 Apollo Policy Language (APL) Engine                 │    ║
║  │  PolicyEngine, EvalContext, EvalResult                  │    ║
║  │  14 operadores, AND/OR, glob, multi-tenant              │    ║
║  └─────────────────────────────────────────────────────────┘    ║
╚═════════════╪════════════════════════════════════════════════════╝
              │
╔═════════════▼════════════════════════════════════════════════════╗
║               🔧 Infrastructure Layer                            ║
║  DB: SQLAlchemy + SQLite (WAL mode, 8MB cache, mmap 256MB)      ║
║  Cache: MemoryCache (LRU+TTL), DecisionCache (SHA-256 key)      ║
║  Security: JwtService, BcryptHasher, TokenBlacklist, mTLS       ║
║  Logging: EventLogger (JSON+YAML+MD+SQLite), LogHooks           ║
║  Repositories: SqliteUserRepo, SqliteRoleRepo, ...              ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Camadas

### Domain (núcleo — o coração do castelo)
- Sem dependências externas
- Entidades puras com lógica de negócio
- Ports (interfaces) para inversão de dependência
- **PolicyEngine**: motor de avaliação APL completamente independente

### Application (o cérebro)
- Orquestra use cases
- Depende apenas do Domain
- Services são fachadas para os use cases

### Infrastructure (os alicerces)
- Implementações concretas dos ports
- SQLAlchemy para persistência
- Cache em memória (LRU + TTL) — múltiplas instâncias especializadas
- JWT, Bcrypt, mTLS, Rate Limiting

### Interface (as portas do castelo)
- FastAPI para API REST
- Starlette para WebApp
- Middlewares: CORS, RateLimit, SecurityHeaders, RequestQueue, RequestLog

---

## Fluxo de Autenticação

```
POST /auth/token
  │
  ├─ LoginUseCase
  │    ├─ UserRepository.find_by_username()
  │    ├─ PasswordHasher.verify()  ← bcrypt (intencional lento)
  │    ├─ _enrich_from_db() → roles, permissions, RBAC, ABAC
  │    │    └─ user_enrichment_cache (TTL 5min, LRU 512)
  │    └─ JwtTokenService.create_access_token()
  │         └─ payload: sub, roles, permissions, abac, rbac, level
  │
  └─ TokenOutputDTO → { access_token, refresh_token, expires_in }
```

---

## Fluxo de Avaliação APL

```
POST /admin/policies/evaluate
  │
  ├─ PolicyService.evaluate()
  │    │
  │    ├─ DecisionCache.get(tenant_id, subject_id, action, resource)
  │    │    └─ chave: SHA-256(tenant:subject:action:resource)
  │    │    └─ HIT → retorna imediatamente (< 1ms)
  │    │
  │    ├─ PolicyEngine.evaluate(EvalContext)  ← MISS
  │    │    ├─ filtra por tenant_id (global ou específico)
  │    │    ├─ filtra por action (glob match)
  │    │    ├─ filtra por resource (glob match)
  │    │    ├─ avalia condições (AND/OR, 14 operadores)
  │    │    ├─ Deny explícito → retorna imediatamente
  │    │    └─ primeiro Allow por prioridade
  │    │
  │    └─ DecisionCache.set() → armazena com TTL
  │
  └─ EvalResult → { allowed, effect, matched_policy, reason }
```

---

## Cache Architecture

```
╔══════════════════════════════════════════════════════════════╗
║                    ⚡ Cache Layer (BMO Turbo)                ║
║                                                              ║
║  token_cache           (4096 entries, TTL 30s)               ║
║  blacklist_cache       (8192 entries, TTL 120s)              ║
║  user_enrichment_cache (512  entries, TTL 300s)              ║
║  decision_cache        (8192 entries, TTL 60s)  ← APL        ║
║  metrics_cache         (4    entries, TTL 5s)                ║
║  settings_cache        (4    entries, TTL 60s)               ║
╚══════════════════════════════════════════════════════════════╝
```

Todos os caches são **LRU + TTL**, thread-safe via `threading.Lock`.  
`decision_cache` usa chave **SHA-256(tenant_id:subject_id:action:resource)**.

---

## Segurança

### mTLS
```
Cliente → [client.crt + client.key] → Servidor
Servidor → [server.crt] → verifica CA
CA → [ca.crt] → raiz de confiança interna
TLS 1.2+ | ECDHE+AES-GCM | ECDHE+CHACHA20
```

### Rate Limiting (sliding window por IP)
| Rota | Limite |
|---|---|
| `/auth/token` | 10 req/min |
| `/auth/check` | 60 req/min |
| `/admin/*` | 120 req/min |
| Global | 200 req/min |

---

## Banco de Dados

SQLite com otimizações WAL:
- `PRAGMA journal_mode=WAL` — leituras não bloqueiam escritas
- `PRAGMA synchronous=NORMAL` — performance + segurança
- `PRAGMA cache_size=-8192` — 8 MB de cache de páginas
- `PRAGMA mmap_size=268435456` — 256 MB memory-mapped I/O
- `PRAGMA busy_timeout=30000` — 30s timeout em lock

### Tabelas Principais
```
users ──────────── user_roles ──────── roles
  │                                      │
  ├── user_rbac_values ── rbac_attributes│
  │                                      │
  └── user_custom_entities          role_permissions ── permissions

groups, user_types, user_levels
policies (APL — tenant_id, effect, priority, conditions)
audit_logs, token_blacklist, settings
```

### Banco de Logs Separado
`data/apollo_log.db` — tabela `event_log` com migração automática de schema.

---

## Multi-Tenant

Isolamento lógico via `tenant_id` em:
- `PolicyModel.tenant_id` — policies por tenant
- `EvalContext.tenant_id` — contexto de avaliação
- `DecisionCache` — chave SHA-256 inclui tenant_id
- `EventLogger` — todos os eventos têm tenant_id opcional

Policies sem `tenant_id` são **globais** (aplicam a todos os tenants).

---

## Event Logger

Saídas simultâneas para cada evento:
```
logs/json/apollo_events.json   (NDJSON — uma linha por entrada)
logs/yaml/apollo_events.yaml   (documentos YAML separados por ---)
logs/md/apollo_events.md       (tabela Markdown incremental)
data/apollo_log.db             (SQLite dedicado — tabela event_log)
```

Campos: `seq`, `uid`, `hash` (SHA-256), `timestamp`, `event`, `actor`,  
`resource`, `resource_id`, `tenant_id`, `session_id`, `status`,  
`duration_ms`, `tags`, `detail`.

---

*O2 Data Solutions — "O Castelo de Ooo tem muitas camadas!"*

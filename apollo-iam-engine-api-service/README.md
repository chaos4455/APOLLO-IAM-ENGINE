# Apollo IAM Engine

**Servico centralizado de Identity and Access Management (IAM) para arquiteturas de microsservicos.**

Desenvolvido por **Elias Andrade — O2 Data Solutions**

---

## O que e o Apollo IAM Engine

Apollo IAM Engine e um servico IAM completo e autonomo, projetado para ser o guardiao central de autenticacao e autorizacao em arquiteturas de microsservicos. Em vez de cada servico implementar sua propria logica de acesso, todos delegam para o Apollo — um unico ponto de verdade para identidade, roles, permissoes, atributos e policies declarativas.

O projeto implementa Clean Architecture + DDD com separacao clara entre Domain, Application, Infrastructure e Interface. O nucleo e a **Apollo Policy Language (APL)**, uma engine declarativa proprietaria que avalia policies em JSON ou YAML com 16 operadores, templating dinamico, hierarquia de recursos, composicao de policies e cache de decisao em memoria.

---

## Stack Tecnica

| Componente | Tecnologia | Versao |
|---|---|---|
| Runtime | Python | 3.10+ |
| Framework HTTP | FastAPI | 0.110+ |
| ASGI Server | Uvicorn | 0.27+ |
| ORM | SQLAlchemy | 2.x |
| Banco principal | SQLite WAL / PostgreSQL-ready | — |
| Banco de logs | SQLite dedicado (apollo_log.db) | — |
| Auth | JWT HS256 (python-jose) | 3.x |
| Hashing | Bcrypt | 4.x |
| Transport security | mTLS TLS 1.2+ ECDHE+AES-GCM | — |
| Cache L1 | In-memory LRU+TTL (MemoryCache) | proprietario |
| Cache APL | DecisionCache SHA-256 multi-tenant | proprietario |
| Policy engine | Apollo Policy Language (APL) v3 | proprietario |
| Admin UI | Starlette + Jinja2 dark theme | — |
| Validacao | Pydantic v2 | 2.x |
| Config | pydantic-settings | 2.x |
| Metricas | psutil | 5.x |
| Output | rich / colorama | latest |

---

## Inicio Rapido

```bash
# 1. instalar dependencias
pip install -r requirements.txt

# 2. copiar e configurar variaveis de ambiente
cp .env.example .env

# 3. iniciar servidor HTTP (desenvolvimento)
python run-init-api-engine.py

# 4. iniciar com mTLS (producao)
MTLS_ENABLED=true python run-init-api-engine.py
```

### Endpoints disponiveis apos iniciar

| Servico | URL | Descricao |
|---|---|---|
| API REST | http://localhost:8000 | API principal |
| Swagger UI | http://localhost:8000/docs | Documentacao interativa |
| ReDoc | http://localhost:8000/redoc | Documentacao alternativa |
| Admin UI | http://localhost:8080/admin | Painel administrativo (admin/admin) |
| mTLS API | https://localhost:8443 | API com mutual TLS |
| mTLS WebApp | https://localhost:8444 | Admin UI com mutual TLS |
| Health | http://localhost:8000/health | Health check |

---

## Variaveis de Ambiente

```env
# Seguranca — OBRIGATORIO alterar em producao
SECRET_KEY=sua-chave-secreta-minimo-32-chars-aleatorios
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin

# Banco de dados
DATABASE_URL=sqlite:///./data/apollo_iam.db

# Tokens JWT
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# mTLS
MTLS_ENABLED=false

# Aplicacao
APP_NAME=Apollo IAM Engine
APP_VERSION=1.0.0
```

Gerar SECRET_KEY segura:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
# ou
openssl rand -hex 32
```

---

## Testes

```bash
# Suite funcional completa — 132 steps, 18 secoes, 100% pass rate
python project-production-test.py

# Stress test — rampa 1 -> 500 requisicoes simultaneas
python benchmark-stress.py
```

### Resultado da ultima execucao (run_20260417_195127)

| Metrica | Valor |
|---|---|
| Total steps | 132 |
| Passed | 132 |
| Failed | 0 |
| Pass rate | 100.0% |
| Latencia media | 2090.8 ms |
| Latencia P50 | 2057.6 ms |
| Latencia P90 | 2284.5 ms |
| Latencia P95 | 2309.8 ms |
| Latencia P99 | 2474.9 ms |

> Latencia inclui overhead mTLS + bcrypt. Endpoints sem I/O retornam em menos de 1ms.

---

## Docker

```bash
# build
docker build -t apollo-iam-engine .

# run
docker-compose up -d

# logs
docker-compose logs -f apollo-iam
```

```yaml
# docker-compose.yml (resumo)
services:
  apollo-iam:
    build: .
    ports:
      - "8000:8000"
      - "8080:8080"
      - "8443:8443"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=sqlite:///./data/apollo_iam.db
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./certs:/app/certs
```

---

## Arquitetura

O projeto segue Clean Architecture com 4 camadas:

```
INTERFACE LAYER
  FastAPI (API REST)          Starlette (Admin UI)
  /auth, /admin/*, /health    Dashboard responsivo dark theme
         |
APPLICATION LAYER
  PolicyService               Use Cases: Login, Logout, Refresh
  CRUD + evaluate + simulate  Validate, DeleteUser, ...
         |
DOMAIN LAYER
  Entities: User, Role, Permission, Group, Policy
  Ports: UserRepository, TokenService, PasswordHasher
  APL Engine: PolicyEngine, EvalContext, EvalResult
         |
INFRASTRUCTURE LAYER
  SQLAlchemy + SQLite WAL     MemoryCache LRU+TTL
  JwtTokenService             DecisionCache SHA-256
  BcryptPasswordHasher        EventLogger async
  RateLimitMiddleware         PEPMiddleware
  mTLS                        SecurityHeadersMiddleware
```

### Estrutura de Pastas

```
apollo-iam-engine-api-service/
|
+-- src/
|   +-- domain/
|   |   +-- entities/           User, Role, Permission, Group, Policy, ...
|   |   +-- value_objects/      TokenPayload, Email, Password
|   |   +-- ports/              UserRepository, TokenService, AuditLogger, ...
|   |   +-- exceptions/         AuthExceptions, UserExceptions, RbacExceptions
|   |   +-- policy/
|   |       +-- policy_dsl.py   APL Engine v3 — PolicyEngine, EvalContext, EvalResult
|   |
|   +-- application/
|   |   +-- use_cases/
|   |   |   +-- auth/           LoginUseCase, LogoutUseCase, RefreshUseCase, ...
|   |   |   +-- users/          CreateUserUseCase, DeleteUserUseCase, ...
|   |   +-- services/
|   |   |   +-- policy_service.py  CRUD + evaluate + explain + simulate + reload
|   |   +-- dtos/               LoginInputDTO, TokenOutputDTO, UserCreateDTO, ...
|   |
|   +-- infrastructure/
|   |   +-- database/
|   |   |   +-- connection.py   Engine SQLAlchemy, PRAGMAs, indices, init_db()
|   |   |   +-- models/         UserModel, RoleModel, PolicyModel, AuditLogModel, ...
|   |   |   +-- migrations/     Alembic
|   |   +-- repositories/       SqliteUserRepo, SqliteRoleRepo, SqliteAuditLogRepo, ...
|   |   +-- cache/
|   |   |   +-- memory_cache.py     MemoryCache LRU+TTL thread-safe (6 instancias)
|   |   |   +-- decision_cache.py   DecisionCache SHA-256 multi-tenant
|   |   +-- security/
|   |   |   +-- jwt_service.py              JwtTokenService (cache L1)
|   |   |   +-- token_blacklist.py          SqliteTokenBlacklist (L1+L2)
|   |   |   +-- password_hasher_impl.py     BcryptPasswordHasher
|   |   |   +-- pep_middleware.py           Policy Enforcement Point (v3)
|   |   |   +-- rate_limit_middleware.py    Sliding window IP + tenant (v3)
|   |   |   +-- security_headers_middleware.py
|   |   |   +-- request_queue_middleware.py Backpressure
|   |   +-- logging/
|   |   |   +-- event_logger.py     Log universal async (fila + background thread)
|   |   |   +-- log_hooks.py        Funcoes tipadas por dominio
|   |   |   +-- log_middleware.py   RequestLogMiddleware
|   |   |   +-- console_logger.py   Output colorido
|   |   +-- config/
|   |       +-- settings.py         Configuracoes via .env (pydantic-settings)
|   |
|   +-- interface/
|       +-- api/
|       |   +-- main.py             FastAPI app, lifespan, middlewares, handlers
|       |   +-- dependencies.py     get_current_user, require_superuser, require_role, ...
|       |   +-- routes/
|       |       +-- auth.py         /auth/token, /refresh, /logout, /validate, /check
|       |       +-- admin/
|       |           +-- users.py, roles.py, permissions.py, groups.py
|       |           +-- rbac_attributes.py, settings.py, audit_logs.py
|       |           +-- user_types.py, user_levels.py, custom_entities.py
|       |           +-- metrics.py, policies.py
|       +-- webapp/
|           +-- main.py             Starlette Admin UI
|           +-- templates/          Jinja2 (base, dashboard, users, roles, ...)
|           +-- static/css/         main.css, variables.css (dark theme responsivo)
|           +-- static/js/          main.js, api.js
|
+-- certs/
|   +-- ca/                         ca.crt, ca.key
|   +-- server/                     server.crt, server.key
|   +-- client/                     client.crt, client.key, client.p12
|
+-- config/
|   +-- security.yaml               Configuracao mTLS e rate limiting
|
+-- data/
|   +-- apollo_iam.db               Banco principal (SQLite WAL)
|   +-- apollo_log.db               Banco de logs (SQLite WAL, separado)
|
+-- logs/
|   +-- json/apollo_events.json     NDJSON (uma linha por evento)
|   +-- yaml/apollo_events.yaml     YAML docs separados por ---
|   +-- md/apollo_events.md         Tabela Markdown incremental
|
+-- docs/                           Documentacao tecnica completa
+-- benchmark-stress-logs/          Relatorios de stress test
+-- project-test-run-setup-logs/    Relatorios de testes funcionais
+-- benchmark-stress.py             Suite de stress test (rampa 1->500)
+-- project-production-test.py      Suite funcional (132 steps, 18 secoes)
+-- run-init-api-engine.py          Inicializador (HTTP + mTLS)
+-- requirements.txt
+-- pyproject.toml
+-- alembic.ini
+-- Dockerfile
+-- docker-compose.yml
+-- .env.example
```

---

## Capacidades Completas

### Autenticacao e Tokens

- Login com username/password retorna JWT HS256 (access + refresh token)
- Payload do token inclui: roles, permissions, group, user_type, user_level, rbac, abac
- Refresh token com rotacao automatica
- Logout com blacklist persistida no banco + cache L1 (TTL 3600s)
- Validacao de token com payload completo decodificado
- Cache de decode JWT em memoria (L1 TTL 30s) — evita jwt.decode() a cada request
- Verificacao de blacklist em dois niveis: L1 cache (TTL 120s) + L2 SQLite

### RBAC — Role-Based Access Control

- Roles com permissoes granulares no formato `{resource}:{action}`
- Multiplas roles por usuario
- Grupos de usuarios com atribuicao direta
- Atributos RBAC customizaveis (key-value, incluidos no payload JWT)
- User types para classificacao de usuarios (ex: funcionario, externo, parceiro)
- User levels com rank numerico para hierarquia (ex: junior=1, senior=3, lead=4)
- Assign/revoke de roles e permissoes via API REST

### ABAC — Attribute-Based Access Control

- Custom entity types com slug unico (ex: regiao, cargo, contrato, filial)
- Valores por tipo configurados em runtime (ex: sul, sudeste, nordeste)
- Atribuicao de entidades a usuarios (1 por tipo, com unicidade garantida)
- Avaliacao combinada RBAC+ABAC no endpoint /auth/check
- Entidades incluidas no payload JWT como atributos abac

### Apollo Policy Language (APL) v3

Engine declarativa proprietaria para controle de acesso baseado em policies.

**16 operadores:**
eq, neq, gt, gte, lt, lte, in, not_in, contains, not_contains,
starts_with, ends_with, regex, exists, not_exists, time_before, time_after

**Recursos:**
- Policies em JSON ou YAML
- Efeito allow/deny (deny sempre vence, independente de prioridade)
- Condicoes compostas AND/OR
- Templating dinamico: {{subject_id}}, {{tenant_id}}, {{subject.X}}
- Resource-level com glob patterns e hierarquia de caminhos
- Prioridade configuravel (menor numero = maior prioridade)
- Multi-tenant via tenant_id com isolamento logico garantido
- Policy composition: scope global -> tenant -> user com heranca de condicoes
- Cache de decisao LRU+TTL, chave SHA-256 do contexto completo, 8192 entradas
- Audit trail de todas as decisoes (tabela decision_audit dedicada)
- Explain endpoint para rastreamento completo por condicao
- **v3: Time-based policies** — valid_from, valid_until, time_window (HH:MM-HH:MM)
- **v3: Context schema validation** — context_schema por policy com validacao de tipos
- **v3: Conflict resolution score** — weight + scope_score para desempate explicito
- **v3: Regex seguro** — timeout 0.5s via ThreadPoolExecutor, limite 256 chars (ReDoS protection)
- **v3: Simulate/sandbox** — POST /simulate e /simulate/batch para what-if sem persistir
- **v3: Cache key completa** — hash inclui subject completo, nao apenas IDs

### Policy Enforcement Point (PEP) — v3

Middleware ASGI que aplica avaliacao APL automaticamente em rotas configuradas:

```python
app.add_middleware(PEPMiddleware, rules=[
    PEPRule(
        path_prefix="/api/cotacoes",
        action="cotacao:read",
        resource_template="cotacao/{path_suffix}",
        tenant_id_header="X-Tenant-ID",
    ),
])
```

- Intercepta requests antes do handler
- Extrai JWT, monta subject, avalia APL
- Retorna 403 com X-APL-Decision e X-APL-Policy nos headers
- Superuser bypass configuravel
- Zero modificacao nos handlers existentes

### Seguranca

- mTLS para comunicacao entre servicos (TLS 1.2+, ECDHE+AES-GCM, ECDHE+CHACHA20)
- Rate limiting por IP (sliding window) com regras por rota
- **v3: Rate limiting por tenant** via X-Tenant-ID header — previne monopolizacao
- Security headers: HSTS, CSP, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- Backpressure via RequestQueueMiddleware (503 se fila cheia)
- Audit log imutavel com SHA-256 de integridade por entrada
- Bcrypt para senhas (custo alto intencional — protecao contra brute force)
- Default deny em todas as policies APL

### Observabilidade

- Event logger universal com fila assincrona (background thread — nao bloqueia requests)
- Saidas simultaneas: JSON NDJSON, YAML, Markdown, SQLite
- Log hooks tipados por dominio (auth, policy, user, role, group, entity, settings)
- Metricas de sistema via /admin/metrics/ (CPU, memoria, disco, rede, processo)
- Cache stats via /admin/metrics/cache e /admin/policies/cache/stats
- Decision audit trail via /admin/policies/decisions/audit
- Auto-refresh de metricas no dashboard (5s)

### Admin UI

- Dashboard responsivo dark theme (mobile-first, CSS custom sem frameworks)
- Sidebar com toggle mobile (hamburger + overlay)
- Gerenciamento completo: usuarios, roles, permissoes, grupos, atributos RBAC
- Gerenciamento de policies APL com toggle ativo/inativo
- Visualizacao de metricas em tempo real (CPU, memoria, disco, rede, KPIs)
- Event logs com filtros client-side e paginacao
- Audit logs com paginacao
- Modais responsivos para criacao de recursos
- Formularios com validacao client-side

---

## API — Endpoints Completos

### Auth

| Metodo | Endpoint | Descricao | Auth |
|---|---|---|---|
| POST | /auth/token | Login — retorna JWT access + refresh | Nao |
| POST | /auth/refresh | Renovar access token | Nao |
| POST | /auth/logout | Revogar token (blacklist) | Bearer |
| POST | /auth/validate | Validar token + payload completo | Nao |
| POST | /auth/check | Verificar RBAC+ABAC para sistemas externos | Nao |

### Apollo Policy Language (APL)

| Metodo | Endpoint | Descricao | Auth |
|---|---|---|---|
| POST | /admin/policies/ | Criar policy (JSON estruturado) | Superuser |
| GET | /admin/policies/ | Listar policies (filtros: tenant_id, scope) | Bearer |
| POST | /admin/policies/raw | Criar policy via JSON/YAML raw string | Superuser |
| GET | /admin/policies/{id} | Obter policy por ID | Bearer |
| DELETE | /admin/policies/{id} | Remover policy | Superuser |
| PATCH | /admin/policies/{id}/toggle | Ativar/desativar policy | Superuser |
| POST | /admin/policies/evaluate | Avaliar contexto de acesso | Bearer |
| POST | /admin/policies/explain | Rastreamento completo da avaliacao | Bearer |
| POST | /admin/policies/reload | Recarregar engine do banco | Superuser |
| GET | /admin/policies/cache/stats | Stats do decision cache | Bearer |
| GET | /admin/policies/decisions/audit | Audit trail de decisoes | Bearer |
| POST | /admin/policies/simulate | Simulacao what-if (sem persistir) | Bearer |
| POST | /admin/policies/simulate/batch | Simulacao em massa | Bearer |

### Usuarios

| Metodo | Endpoint | Descricao |
|---|---|---|
| GET | /admin/users/ | Listar usuarios (skip, limit) |
| POST | /admin/users/ | Criar usuario |
| GET | /admin/users/{id} | Obter usuario por ID |
| PUT | /admin/users/{id} | Atualizar usuario |
| DELETE | /admin/users/{id} | Remover usuario (cascade) |
| POST | /admin/users/{id}/toggle-status | Alternar is_active |
| POST | /admin/users/{id}/reset-password | Redefinir senha |

### Roles e Permissoes

| Metodo | Endpoint | Descricao |
|---|---|---|
| GET/POST | /admin/roles/ | Listar/criar roles |
| DELETE | /admin/roles/{id} | Remover role |
| POST | /admin/roles/{id}/assign-user/{uid} | Atribuir role a usuario |
| DELETE | /admin/roles/{id}/revoke-user/{uid} | Revogar role de usuario |
| GET/POST | /admin/permissions/ | Listar/criar permissoes |
| DELETE | /admin/permissions/{id} | Remover permissao |
| POST | /admin/permissions/{id}/assign-role/{rid} | Atribuir permissao a role |

### Grupos, RBAC, Entidades

| Metodo | Endpoint | Descricao |
|---|---|---|
| GET/POST | /admin/groups/ | Listar/criar grupos |
| DELETE | /admin/groups/{id} | Remover grupo |
| POST | /admin/groups/{id}/assign-user/{uid} | Atribuir usuario ao grupo |
| GET/POST | /admin/rbac/ | Listar/criar atributos RBAC |
| DELETE | /admin/rbac/{id} | Remover atributo (cascade) |
| POST | /admin/rbac/assign/{uid} | Atribuir valor de atributo a usuario |
| GET/POST | /admin/custom-entities/types | Listar/criar tipos de entidade ABAC |
| GET/PUT/DELETE | /admin/custom-entities/types/{slug} | CRUD tipo de entidade |
| GET/POST | /admin/custom-entities/{slug}/values | Listar/criar valores |
| GET/PUT/DELETE | /admin/custom-entities/{slug}/values/{id} | CRUD valor |
| POST | /admin/custom-entities/assign/{uid} | Atribuir entidade a usuario |
| DELETE | /admin/custom-entities/assign/{uid}/{slug} | Desatribuir entidade |
| GET | /admin/custom-entities/user/{uid} | Listar entidades do usuario |

### User Types, Levels, Settings, Audit, Metrics

| Metodo | Endpoint | Descricao |
|---|---|---|
| GET/POST | /admin/user-types/ | Listar/criar tipos de usuario |
| GET/PUT/DELETE | /admin/user-types/{id} | CRUD tipo de usuario |
| GET/POST | /admin/user-levels/ | Listar/criar niveis de usuario |
| GET/PUT/DELETE | /admin/user-levels/{id} | CRUD nivel de usuario |
| GET/PUT | /admin/settings/ | Ler/atualizar configuracoes |
| GET | /admin/audit/ | Audit logs (filtros: actor, status) |
| GET | /admin/metrics/ | Metricas completas do sistema |
| GET | /admin/metrics/logs | Event logs com paginacao |
| GET | /admin/metrics/cache | Stats de todos os caches |
| GET | /health | Health check |

---

## Apollo Policy Language (APL) v3 — Exemplos Rapidos

### Policy basica allow

```json
{
  "name": "Vendedores — acesso a cotacoes",
  "effect": "allow",
  "priority": 10,
  "tenant_id": "tenant-empresa-abc",
  "actions": ["cotacao:create", "cotacao:read"],
  "resources": ["cotacao/*"],
  "conditions": [
    {"field": "roles", "op": "contains", "value": "vendedor"},
    {"field": "user_level", "op": "gte", "value": 2}
  ],
  "condition_logic": "AND"
}
```

### Deny explicito (prioridade absoluta)

```json
{
  "name": "Negar usuarios bloqueados",
  "effect": "deny",
  "priority": 1,
  "actions": ["*"],
  "resources": ["*"],
  "conditions": [
    {"field": "blocked", "op": "eq", "value": true}
  ]
}
```

### Time-based policy (v3)

```json
{
  "name": "Acesso apenas em horario comercial",
  "effect": "allow",
  "priority": 50,
  "actions": ["relatorio:export"],
  "resources": ["relatorio/*"],
  "time_window": "08:00-18:00",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2026-12-31T23:59:59Z",
  "conditions": [
    {"field": "roles", "op": "contains", "value": "gerente"}
  ]
}
```

### Templating dinamico

```json
{
  "name": "Usuario acessa apenas seus proprios recursos",
  "effect": "allow",
  "priority": 20,
  "actions": ["cotacao:*"],
  "resources": ["cotacao/*"],
  "conditions": [
    {"field": "owner_id", "op": "eq", "value": "{{subject_id}}"},
    {"field": "tenant", "op": "eq", "value": "{{tenant_id}}"}
  ]
}
```

### Simulacao what-if (sandbox)

```bash
POST /admin/policies/simulate
{
  "policies": [
    {
      "name": "Teste — nova policy",
      "effect": "allow",
      "actions": ["cotacao:create"],
      "resources": ["cotacao/*"],
      "conditions": [
        {"field": "roles", "op": "contains", "value": "vendedor"}
      ]
    }
  ],
  "subject": {"roles": ["vendedor"], "user_level": 2},
  "action": "cotacao:create",
  "resource": "cotacao/123",
  "tenant_id": "tenant-abc"
}
```

### Avaliacao com explain

```bash
POST /admin/policies/explain
{
  "subject": {"roles": ["vendedor"], "department": "sales", "user_level": 3},
  "action": "cotacao:create",
  "resource": "empresa/123/cotacao/456",
  "tenant_id": "tenant-abc",
  "subject_id": "user-uuid"
}
```

Retorna rastreamento completo: cada policy testada, cada condicao avaliada,
valores de template resolvidos, motivo de aprovacao/rejeicao.

---

## Cache Architecture

```
token_cache
  key:   SHA-256(token_raw)[:32]
  value: TokenPayload serializado
  TTL:   min(token_remaining, 30s)
  size:  4096 entries LRU
  uso:   evita jwt.decode() + blacklist check a cada request

blacklist_cache
  key:   jti (UUID do token)
  value: True (revogado) | False (nao revogado)
  TTL:   3600s (revogado) | 30s (nao revogado)
  size:  8192 entries LRU
  uso:   evita SELECT na token_blacklist a cada request

user_enrichment_cache
  key:   user_id
  value: {roles, permissions, rbac, abac, group, level}
  TTL:   300s (5 minutos)
  size:  512 entries LRU
  uso:   evita 4+ queries no login

decision_cache (APL)
  key:   SHA-256(tenant_id:subject_id:action:resource:subject_json)
  value: DecisionEntry {allowed, effect, matched_policy, reason}
  TTL:   60s default | configuravel por policy_id
  size:  8192 entries LRU
  uso:   evita avaliacao APL completa (engine em memoria)
  v3:    chave inclui subject completo — sem decisoes erradas

metrics_cache     TTL 5s   — evita psutil a cada request
db_kpis_cache     TTL 10s  — evita COUNT(*) no dashboard
settings_cache    TTL 60s  — evita SELECT na tabela settings
```

---

## Banco de Dados — Indices

Todos os indices criados automaticamente no `init_db()`:

```
users:                ix_users_username, ix_users_email, ix_users_is_active,
                      ix_users_group_id, ix_users_is_superuser, ix_users_type_level

user_roles:           ix_user_roles_user_id, ix_user_roles_role_id
user_rbac_values:     ix_user_rbac_values_user_id, ix_user_rbac_values_attr_id
user_custom_entities: ix_user_custom_entities_user_id, ix_user_custom_entities_slug
                      ix_user_custom_entities_user_slug (composto)

roles:                ix_roles_name, ix_roles_is_active
role_permissions:     ix_role_permissions_role_id, ix_role_permissions_perm_id

permissions:          ix_permissions_name, ix_permissions_resource,
                      ix_permissions_action, ix_permissions_resource_action (composto)

policies:             ix_policies_name, ix_policies_tenant_id, ix_policies_enabled,
                      ix_policies_scope, ix_policies_subject_id,
                      ix_policies_tenant_enabled_prio (composto — query principal do engine)
                      ix_policies_scope_enabled (composto)

audit_logs:           ix_audit_logs_actor, ix_audit_logs_action, ix_audit_logs_resource,
                      ix_audit_logs_status, ix_audit_logs_created_at,
                      ix_audit_logs_actor_status (composto)
                      ix_audit_logs_resource_status (composto)

token_blacklist:      ix_token_blacklist_jti (hot path — cada request autenticado)

event_log:            ix_event_log_actor_status, ix_event_log_tenant_event (compostos)
decision_audit:       ix_decision_audit_tenant_decision, ix_decision_audit_subject_action
```

SQLite PRAGMAs aplicados em cada conexao:
```
PRAGMA journal_mode=WAL          leituras nao bloqueiam escritas
PRAGMA synchronous=NORMAL        performance + seguranca
PRAGMA cache_size=-32768         32 MB de cache de paginas
PRAGMA mmap_size=536870912       512 MB memory-mapped I/O
PRAGMA wal_autocheckpoint=1000   checkpoint a cada 1000 paginas
PRAGMA optimize                  atualiza estatisticas do query planner
PRAGMA foreign_keys=ON           integridade referencial
PRAGMA busy_timeout=30000        30s timeout em lock
```

---

## Seguranca

### Rate Limiting

Sliding window por IP. IPs locais (127.0.0.1, ::1) nunca sao limitados.

| Rota | Limite IP | Janela |
|---|---|---|
| /auth/token | 10 req | 60s |
| /auth/refresh | 20 req | 60s |
| /auth/check | 60 req | 60s |
| /auth/* | 30 req | 60s |
| /admin/metrics | 60 req | 60s |
| /admin/* | 120 req | 60s |
| Global | 200 req | 60s |

**v3 — Rate limit por tenant** (header X-Tenant-ID):

| Rota | Limite Tenant | Janela |
|---|---|---|
| /admin/policies/evaluate | 500 req | 60s |
| /auth/check | 300 req | 60s |
| /auth/token | 50 req | 60s |
| /admin/* | 600 req | 60s |

### mTLS

```
Habilitado via: MTLS_ENABLED=true
Portas:         8443 (API), 8444 (WebApp)
TLS versao:     1.2+
Cipher suites:  ECDHE+AES-GCM, ECDHE+CHACHA20
Desabilitados:  RC4, 3DES, NULL, EXPORT, MD5, SSLv2, SSLv3
Certificados:   certs/ca/, certs/server/, certs/client/
```

### Security Headers

Aplicados em todas as respostas via SecurityHeadersMiddleware:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

### Codigos de Status

| Codigo | Significado |
|---|---|
| 200 | Sucesso |
| 201 | Criado |
| 204 | Sem conteudo (delete) |
| 400 | Requisicao invalida |
| 401 | Nao autenticado (token invalido, expirado ou revogado) |
| 403 | Sem permissao (nao e superuser ou PEP negou) |
| 404 | Recurso nao encontrado |
| 409 | Conflito (UNIQUE constraint) |
| 422 | Erro de validacao Pydantic |
| 429 | Rate limit excedido (IP ou tenant) |
| 500 | Erro interno |
| 503 | Servico indisponivel (request queue cheia) |

---

## Middlewares — Ordem de Execucao

```
Request
  |
  v
CORSMiddleware              headers CORS, preflight OPTIONS
  |
  v
RequestQueueMiddleware      backpressure: fila 100 req, timeout 30s, 503 se cheia
  |
  v
RateLimitMiddleware         sliding window por IP + por tenant (v3)
  |
  v
SecurityHeadersMiddleware   HSTS, CSP, X-Frame-Options, X-Content-Type-Options
  |
  v
RequestLogMiddleware        log de cada request/response no EventLogger
  |
  v
PEPMiddleware (opcional)    Policy Enforcement Point — avalia APL antes do handler
  |
  v
Router FastAPI
  |
  v
Response
```

---

## Multi-Tenant

Isolamento logico via tenant_id em todos os componentes:

| Componente | Isolamento |
|---|---|
| PolicyModel | Coluna tenant_id — policies por tenant |
| EvalContext | Campo tenant_id — contexto de avaliacao |
| DecisionCache | Incluido na chave SHA-256 — sem vazamento entre tenants |
| EventLogger | Campo tenant_id em todos os eventos |
| decision_audit | Coluna tenant_id — auditoria por tenant |
| RateLimitMiddleware | Rate limit separado por tenant (v3) |

Policies com tenant_id=null sao globais — aplicam a todos os tenants.
Policies de tenant especifico sobrescrevem as globais (scope hierarchy).

---

## Componentes Criticos

| Componente | Arquivo | Responsabilidade |
|---|---|---|
| APL Engine v3 | src/domain/policy/policy_dsl.py | 16 ops, glob, hierarquia, templates, time-based, schema, conflict score |
| Decision Cache | src/infrastructure/cache/decision_cache.py | LRU+TTL, SHA-256 contexto completo, multi-tenant |
| Policy Service | src/application/services/policy_service.py | CRUD + evaluate + explain + simulate + reload |
| JWT Service | src/infrastructure/security/jwt_service.py | Decode com cache L1, blacklist L1+L2 |
| Token Blacklist | src/infrastructure/security/token_blacklist.py | Revogacao com cache em memoria |
| PEP Middleware | src/infrastructure/security/pep_middleware.py | Policy Enforcement Point ASGI (v3) |
| Rate Limiter | src/infrastructure/security/rate_limit_middleware.py | Sliding window IP + tenant (v3) |
| Event Logger | src/infrastructure/logging/event_logger.py | Log assincrono multi-saida (fila + background thread) |
| Memory Cache | src/infrastructure/cache/memory_cache.py | LRU+TTL thread-safe (6 instancias) |
| DB Connection | src/infrastructure/database/connection.py | SQLite WAL, PRAGMAs, indices, init |
| Dependencies | src/interface/api/dependencies.py | get_current_user, require_superuser, require_role, require_abac |

---

## Suite de Testes Funcionais

`project-production-test.py` — 19 secoes, 132 steps:

| Secao | Descricao |
|---|---|
| 1 | Health check |
| 2 | Auth: login, refresh, validate, logout, token invalido |
| 3 | Roles: criar, listar |
| 4 | Permissions: criar, listar |
| 5 | Users: criar, login, listar |
| 6 | RBAC: assign roles e permissions |
| 7 | ABAC: atributos RBAC, check combinado |
| 8 | APL: policies JSON/YAML, reload, evaluate, toggle, explain, audit, cache stats |
| 9 | Decision cache: TTL, LRU, hit rate, isolamento por tenant |
| 10 | Multi-tenant: isolamento logico |
| 11 | User types e levels: CRUD completo |
| 12 | Custom entities (ABAC): CRUD + assign/unassign |
| 13 | Settings: GET/PUT |
| 14 | Audit logs: listagem e filtros |
| 15 | Groups: CRUD + assign user |
| 16 | Metrics: KPIs, /logs, /cache |
| 17 | APL operadores avancados (neq) |
| 18 | Users: toggle-status, reset-password, GET por ID |
| 19 | Cleanup: remocao de todos os recursos de teste |

---

## SLOs — Service Level Objectives

| Metrica | Target | Observacao |
|---|---|---|
| Disponibilidade | 99.9% | |
| Latencia P99 login | < 500 ms | Bcrypt e intencional |
| Latencia P99 validate | < 50 ms | JWT decode + cache L1 |
| Latencia P99 check | < 100 ms | JWT + RBAC/ABAC |
| Latencia P99 APL eval (cache miss) | < 10 ms | Engine em memoria |
| Latencia P99 APL eval (cache hit) | < 1 ms | SHA-256 lookup |
| Cache hit rate (token) | > 85% | Workload normal |
| Cache hit rate (decision) | > 90% | Workload repetitivo |

---

## Dependencias

```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
python-jose[cryptography]>=3.3.0
bcrypt>=4.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
pyyaml>=6.0.0
httpx>=0.27.0
psutil>=5.9.0
rich>=13.0.0
colorama>=0.4.6
starlette>=0.36.0
jinja2>=3.1.0
python-multipart>=0.0.9
alembic>=1.13.0
```

---

## Roadmap

- [ ] PostgreSQL como banco principal (substituir SQLite em producao)
- [ ] Redis para cache distribuido (multi-instancia horizontal)
- [ ] OIDC/OAuth2 provider (SSO — Google, Azure AD, Keycloak)
- [ ] Policy versioning e rollback (historico de mudancas)
- [ ] APL editor visual no Admin UI (drag-and-drop de condicoes)
- [ ] Webhooks para eventos de autorizacao (allow/deny em tempo real)
- [ ] SDK cliente Python e Node.js
- [ ] Exportacao/importacao de policies (backup/restore JSON/YAML)
- [ ] Integracao com LDAP/Active Directory
- [ ] Correlation ID distribuido (tracing entre microsservicos)
- [ ] Policy dry-run com diff (comparar antes/depois de ativar)
- [ ] Metricas Prometheus/OpenMetrics
- [ ] Dashboard Grafana pre-configurado
- [ ] CLI para gerenciamento de policies (apollo-iam-cli)
- [ ] Suporte a PostgreSQL row-level security para multi-tenant fisico

---

## Documentacao

| Documento | Descricao |
|---|---|
| docs/arquitetura.md | Arquitetura tecnica completa, fluxos, modelo de dados |
| docs/api-reference.md | Referencia completa de todos os endpoints |
| docs/policy-dsl.md | Apollo Policy Language v3 — referencia completa |
| docs/produto.md | Documento de produto, capacidades, SLOs, roadmap |
| docs/projeto.md | Visao geral, estrutura de pastas, componentes |
| docs/seguranca.md | Modelo de seguranca, mTLS, rate limiting, audit |
| docs/stress-test.md | Metodologia e interpretacao do stress test |

---

*Elias Andrade — O2 Data Solutions*

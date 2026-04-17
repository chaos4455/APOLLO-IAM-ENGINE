# Apollo IAM Engine — Visao Geral do Projeto

**Versao:** 1.0.0  
**Organizacao:** O2 Data Solutions  
**Autor:** Elias Andrade  
**Stack:** Python 3.10+, FastAPI, SQLAlchemy, SQLite WAL, JWT HS256, mTLS, bcrypt

---

## O que e

Apollo IAM Engine e um servico centralizado de **Identity & Access Management (IAM)** para arquiteturas de microsservicos. Ele fornece:

- Autenticacao JWT com access + refresh token
- RBAC completo (roles, permissoes, grupos, atributos, tipos, niveis)
- ABAC via custom entities (tipos e valores configurados em runtime)
- **Apollo Policy Language (APL)** — engine declarativa proprietaria com 14 operadores
- Cache de decisao em memoria (LRU+TTL, SHA-256, multi-tenant)
- Multi-tenant com isolamento logico por `tenant_id`
- mTLS para comunicacao segura entre servicos
- Audit log completo e imutavel (JSON, YAML, Markdown, SQLite)
- Admin UI responsivo (dark theme, mobile-first)

---

## Estrutura de Pastas

```
apollo-iam-engine-api-service/
|
+-- src/
|   +-- domain/
|   |   +-- entities/          # User, Role, Permission, Group, Policy, ...
|   |   +-- value_objects/     # TokenPayload, Email, Password
|   |   +-- ports/             # Interfaces: UserRepository, TokenService, ...
|   |   +-- exceptions/        # AuthExceptions, UserExceptions, RbacExceptions
|   |   +-- policy/
|   |       +-- policy_dsl.py  # APL Engine: PolicyEngine, EvalContext, EvalResult
|   |
|   +-- application/
|   |   +-- use_cases/
|   |   |   +-- auth/          # LoginUseCase, LogoutUseCase, RefreshUseCase, ...
|   |   |   +-- users/         # CreateUserUseCase, DeleteUserUseCase, ...
|   |   +-- services/
|   |   |   +-- policy_service.py  # CRUD + evaluate + reload + explain
|   |   +-- dtos/              # LoginInputDTO, TokenOutputDTO, UserCreateDTO, ...
|   |
|   +-- infrastructure/
|   |   +-- database/
|   |   |   +-- connection.py  # Engine SQLAlchemy, PRAGMAs, indices, init_db()
|   |   |   +-- base.py        # Base declarativa SQLAlchemy
|   |   |   +-- models/        # UserModel, RoleModel, PolicyModel, ...
|   |   |   +-- migrations/    # Alembic (schema migrations)
|   |   +-- repositories/      # SqliteUserRepo, SqliteRoleRepo, ...
|   |   +-- cache/
|   |   |   +-- memory_cache.py    # MemoryCache (LRU+TTL, thread-safe)
|   |   |   +-- decision_cache.py  # DecisionCache (SHA-256 key, multi-tenant)
|   |   +-- security/
|   |   |   +-- jwt_service.py             # JwtTokenService (decode com cache L1)
|   |   |   +-- token_blacklist.py         # SqliteTokenBlacklist (L1+L2)
|   |   |   +-- password_hasher_impl.py    # BcryptPasswordHasher
|   |   |   +-- security_headers_middleware.py
|   |   |   +-- rate_limit_middleware.py   # Sliding window por IP
|   |   |   +-- request_queue_middleware.py # Backpressure
|   |   +-- logging/
|   |   |   +-- event_logger.py    # Log universal (fila assincrona + background thread)
|   |   |   +-- log_hooks.py       # Funcoes tipadas por dominio
|   |   |   +-- log_middleware.py  # RequestLogMiddleware
|   |   |   +-- console_logger.py  # Output colorido (rich/colorama)
|   |   +-- config/
|   |   |   +-- settings.py        # Configuracoes via .env (pydantic-settings)
|   |   +-- seed/
|   |       +-- seed_admin.py      # Cria usuario admin na inicializacao
|   |       +-- seed_roles.py      # Roles padrao
|   |       +-- seed_permissions.py # Permissoes padrao
|   |
|   +-- interface/
|       +-- api/
|       |   +-- main.py            # FastAPI app, lifespan, middlewares, exception handlers
|       |   +-- dependencies.py    # get_current_user, require_superuser, require_role, ...
|       |   +-- routes/
|       |       +-- auth.py        # /auth/token, /refresh, /logout, /validate, /check
|       |       +-- admin/
|       |           +-- users.py, roles.py, permissions.py, groups.py
|       |           +-- rbac_attributes.py, settings.py, audit_logs.py
|       |           +-- user_types.py, user_levels.py, custom_entities.py
|       |           +-- metrics.py, policies.py
|       +-- webapp/
|           +-- main.py            # Starlette app (Admin UI)
|           +-- templates/         # Jinja2 templates (base, dashboard, users, ...)
|           +-- static/
|               +-- css/           # main.css, variables.css (dark theme responsivo)
|               +-- js/            # main.js, api.js
|
+-- certs/
|   +-- ca/                        # ca.crt, ca.key
|   +-- server/                    # server.crt, server.key
|   +-- client/                    # client.crt, client.key, client.p12
|
+-- config/
|   +-- security.yaml              # Configuracao mTLS e rate limiting
|
+-- data/
|   +-- apollo_iam.db              # Banco principal (SQLite WAL)
|   +-- apollo_log.db              # Banco de logs (SQLite WAL, separado)
|
+-- logs/
|   +-- json/apollo_events.json    # NDJSON (uma linha por evento)
|   +-- yaml/apollo_events.yaml    # YAML docs separados por ---
|   +-- md/apollo_events.md        # Tabela Markdown incremental
|
+-- docs/                          # Documentacao tecnica completa
+-- benchmark-stress-logs/         # Relatorios de stress test
+-- project-test-run-setup-logs/   # Relatorios de testes funcionais
|
+-- benchmark-stress.py            # Suite de stress test (rampa 1->500)
+-- project-production-test.py     # Suite de testes funcionais (132 steps, 18 secoes)
+-- run-init-api-engine.py         # Inicializador do servidor (HTTP + mTLS)
+-- requirements.txt
+-- pyproject.toml
+-- alembic.ini
+-- Dockerfile
+-- docker-compose.yml
+-- .env.example
```

---

## Fluxo Principal

```
Cliente externo
    |
    +-- POST /auth/token          -> JWT (access + refresh)
    |
    +-- POST /auth/check          -> {allowed: true/false, reason}
    |        (RBAC + ABAC)
    |
    +-- POST /admin/policies/evaluate -> {allowed, matched_policy, reason}
             (APL engine)
```

---

## Dependencias Principais

| Pacote | Versao | Uso |
|---|---|---|
| fastapi | 0.110+ | Framework HTTP |
| uvicorn | 0.27+ | ASGI server |
| sqlalchemy | 2.x | ORM + queries |
| python-jose | 3.x | JWT HS256 |
| bcrypt | 4.x | Password hashing |
| pydantic-settings | 2.x | Configuracao via .env |
| pyyaml | 6.x | Suporte YAML nas policies APL |
| httpx | 0.27+ | Cliente HTTP (testes) |
| psutil | 5.x | Metricas de sistema |
| rich / colorama | latest | Output colorido no terminal |
| starlette | 0.36+ | WebApp Admin UI |
| jinja2 | 3.x | Templates HTML |

---

## Como Rodar

```bash
# instalar dependencias
pip install -r requirements.txt

# iniciar servidor (HTTP dev, porta 8000 + 8080)
python run-init-api-engine.py

# iniciar com mTLS (porta 8443 + 8444)
MTLS_ENABLED=true python run-init-api-engine.py

# rodar suite funcional completa (132 steps, 18 secoes)
python project-production-test.py

# rodar stress test (rampa 1->500 req simultaneos)
python benchmark-stress.py
```

---

## Configuracao (.env)

```env
# Seguranca
SECRET_KEY=sua-chave-secreta-minimo-32-chars
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin

# Banco
DATABASE_URL=sqlite:///./data/apollo_iam.db

# Tokens
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# mTLS
MTLS_ENABLED=false

# App
APP_NAME=Apollo IAM Engine
APP_VERSION=1.0.0
```

---

## Componentes Criticos

| Componente | Arquivo | Responsabilidade |
|---|---|---|
| APL Engine | `src/domain/policy/policy_dsl.py` | Avaliacao de policies (14 ops, glob, hierarquia, templates) |
| Decision Cache | `src/infrastructure/cache/decision_cache.py` | Cache LRU+TTL, SHA-256, multi-tenant |
| Policy Service | `src/application/services/policy_service.py` | CRUD + evaluate + explain + reload |
| JWT Service | `src/infrastructure/security/jwt_service.py` | Decode com cache L1, blacklist L1+L2 |
| Token Blacklist | `src/infrastructure/security/token_blacklist.py` | Revogacao com cache em memoria |
| Event Logger | `src/infrastructure/logging/event_logger.py` | Log assincrono multi-saida |
| Memory Cache | `src/infrastructure/cache/memory_cache.py` | LRU+TTL thread-safe (6 instancias) |
| DB Connection | `src/infrastructure/database/connection.py` | SQLite WAL, PRAGMAs, indices, init |
| Dependencies | `src/interface/api/dependencies.py` | get_current_user, require_superuser, require_role, require_abac |

---

## Suite de Testes Funcionais

`project-production-test.py` — 18 secoes, 132 steps:

| Secao | Descricao |
|---|---|
| 1 | Health check |
| 2 | Auth: login, refresh, validate, logout |
| 3 | Roles: CRUD |
| 4 | Permissions: CRUD |
| 5 | Users: CRUD + login |
| 6 | RBAC: assign roles e permissions |
| 7 | ABAC: atributos RBAC e check combinado |
| 8 | APL: policies JSON/YAML, reload, evaluate, toggle, explain, audit |
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

*Elias Andrade — O2 Data Solutions*

# 🌟 Apollo IAM Engine — Visão Geral do Projeto

> *"Hora de Aventura no Reino de Ooo IAM — onde Finn e Jake protegem cada token!"*

**Versão:** 2.0  
**Organização:** O2 Data Solutions  
**Stack:** Python 3.10+, FastAPI, SQLAlchemy, SQLite (prod: PostgreSQL), JWT HS256, mTLS

---

## O que é

Apollo IAM Engine é um serviço centralizado de **Identity & Access Management (IAM)** — o guardião do Reino de Ooo. Ele protege todos os recursos do reino com:

- Autenticação JWT com refresh token
- RBAC (Role-Based Access Control) completo
- ABAC (Attribute-Based Access Control) via custom entities
- **Apollo Policy Language (APL)** — engine declarativa proprietária
- Cache de decisão em memória com TTL por policy (LRU + SHA-256)
- Multi-tenant com isolamento lógico por `tenant_id`
- mTLS para comunicação segura entre serviços
- Audit log completo e imutável de todas as ações

---

## Objetivos

1. Centralizar autenticação e autorização de múltiplos sistemas
2. Fornecer `/auth/check` para sistemas externos verificarem acesso
3. Suportar políticas declarativas (APL) em JSON e YAML
4. Escalar horizontalmente com cache de decisão eficiente
5. Garantir rastreabilidade via audit log e event logger

---

## Estrutura de Pastas

```
apollo-iam-engine-api-service/
├── src/
│   ├── domain/           # Entidades, value objects, ports, Policy DSL (APL)
│   ├── application/      # Use cases, services, DTOs
│   ├── infrastructure/   # DB, cache, security, logging, repositories
│   └── interface/        # API (FastAPI), WebApp (Starlette)
├── certs/                # Certificados mTLS (CA, server, client)
├── config/               # security.yaml
├── data/                 # SQLite databases (apollo_iam.db, apollo_log.db)
├── logs/                 # Logs estruturados (JSON, YAML, MD)
├── docs/                 # Documentação do projeto
├── benchmark-stress-logs/      # Relatórios de stress test
├── project-test-run-setup-logs/ # Relatórios de testes funcionais
├── benchmark-stress.py         # Suite de stress test (rampa 1→500)
├── project-production-test.py  # Suite de testes funcionais (18 seções)
└── run-init-api-engine.py      # Inicializador do servidor
```

---

## Fluxo Principal

```
Cliente → POST /auth/token          → JWT (access + refresh)
       → POST /auth/check           → allowed: true/false (RBAC+ABAC)
       → POST /admin/policies/evaluate → avaliação APL declarativa
```

---

## Dependências Principais

| Pacote | Uso |
|---|---|
| fastapi | Framework HTTP |
| sqlalchemy | ORM + migrations |
| pyjwt | JWT signing/verification |
| bcrypt | Password hashing |
| httpx | Cliente HTTP assíncrono |
| pydantic | Validação de dados |
| rich / colorama | Output colorido no terminal |
| pyyaml | Suporte YAML nas policies APL |

---

## Como Rodar

```bash
# instalar dependências
pip install -r requirements.txt

# iniciar servidor (HTTP dev)
python run-init-api-engine.py

# rodar testes funcionais completos (18 seções)
python project-production-test.py

# rodar stress test (rampa 1→500 req simultâneos)
python benchmark-stress.py
```

---

## Configuração (.env)

```env
SECRET_KEY=sua-chave-secreta-32chars
DATABASE_URL=sqlite:///./data/apollo_iam.db
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
MTLS_ENABLED=false
```

---

## Componentes Principais

| Componente | Arquivo | Descrição |
|---|---|---|
| APL Engine | `src/domain/policy/policy_dsl.py` | Motor de avaliação de policies |
| Decision Cache | `src/infrastructure/cache/decision_cache.py` | Cache LRU+TTL thread-safe |
| Policy Service | `src/application/services/policy_service.py` | CRUD + avaliação + reload |
| Policy Routes | `src/interface/api/routes/admin/policies.py` | REST endpoints APL |
| Event Logger | `src/infrastructure/logging/event_logger.py` | Log universal multi-saída |
| Log Hooks | `src/infrastructure/logging/log_hooks.py` | Funções de log por domínio |

---

*O2 Data Solutions — "Matemática!" — BMO*

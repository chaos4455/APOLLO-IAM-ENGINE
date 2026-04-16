# 🍕 Apollo IAM Engine — Documento de Produto

> *"Jake estica os braços para alcançar todos os microsserviços do reino!"*

**Versão:** 2.0  
**Status:** Produção  
**Owner:** O2 Data Solutions

---

## Proposta de Valor

Apollo IAM Engine resolve o problema de **fragmentação de autenticação e autorização** em arquiteturas de microsserviços. Em vez de cada serviço implementar sua própria lógica de acesso, todos delegam para o Apollo — o guardião central do Reino de Ooo.

---

## Personas

| Persona | Necessidade |
|---|---|
| Dev de microsserviço | Verificar se um token tem acesso via `/auth/check` |
| Admin de sistema | Gerenciar usuários, roles, permissões e policies via API |
| Arquiteto de segurança | Definir policies declarativas em JSON/YAML (APL) |
| Auditor | Consultar audit logs de todas as ações do sistema |
| Arquiteto multi-tenant | Isolar policies e decisões por `tenant_id` |

---

## Funcionalidades

### Autenticação
- Login com username/password → JWT (access + refresh)
- Refresh token automático
- Logout com blacklist de token (persistida + cache)
- Validação de token com payload completo (roles, permissions, ABAC)

### RBAC
- Roles com permissões granulares (`resource:action`)
- Atribuição de múltiplas roles por usuário
- Grupos de usuários
- Atributos RBAC customizáveis (key-value)
- User types e user levels com rank numérico

### ABAC
- Custom entities com tipos e valores
- Atributos dinâmicos por usuário
- Avaliação combinada RBAC+ABAC no `/auth/check`

### Apollo Policy Language (APL)
- Policies declarativas em **JSON ou YAML**
- Efeito **Allow/Deny explícito** (deny sempre vence)
- **14 operadores** de condição (eq, neq, gt, gte, lt, lte, in, not_in, contains, not_contains, starts_with, ends_with, regex, exists, not_exists)
- Condições compostas **AND/OR**
- Resource-level com **glob patterns** (`cotacao/*`, `admin:*`)
- **Prioridade de regras** configurável (menor número = maior prioridade)
- **Multi-tenant** via `tenant_id` com isolamento lógico
- **Cache de decisão** com TTL por policy, LRU eviction, chave SHA-256

### Segurança
- mTLS para comunicação entre serviços
- Rate limiting por IP e rota (sliding window)
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Audit log imutável de todas as ações
- Bcrypt para senhas

### Observabilidade
- Event logger universal (JSON, YAML, MD, SQLite)
- Log hooks tipados por domínio (auth, policy, user, role, etc.)
- Métricas de sistema via `/admin/metrics/`
- Cache stats via `/admin/policies/cache/stats`

---

## Endpoints Principais

| Endpoint | Método | Descrição |
|---|---|---|
| `/auth/token` | POST | Login → JWT |
| `/auth/refresh` | POST | Renovar token |
| `/auth/logout` | POST | Revogar token |
| `/auth/validate` | POST | Validar token + payload |
| `/auth/check` | POST | Verificar RBAC+ABAC |
| `/admin/policies/` | POST | Criar policy APL |
| `/admin/policies/raw` | POST | Criar policy via JSON/YAML raw |
| `/admin/policies/evaluate` | POST | Avaliar policy APL |
| `/admin/policies/reload` | POST | Recarregar engine do banco |
| `/admin/policies/cache/stats` | GET | Stats do cache de decisão |
| `/admin/users/` | GET/POST | Gerenciar usuários |
| `/admin/roles/` | GET/POST | Gerenciar roles |
| `/admin/permissions/` | GET/POST | Gerenciar permissões |
| `/health` | GET | Health check |

---

## SLOs (Service Level Objectives)

| Métrica | Target |
|---|---|
| Disponibilidade | 99.9% |
| Latência P99 login | < 500 ms |
| Latência P99 validate | < 50 ms |
| Latência P99 check | < 100 ms |
| Latência P99 policy eval (cache miss) | < 10 ms |
| Latência P99 policy eval (cache hit) | < 5 ms |

---

## Roadmap

- [ ] PostgreSQL como banco principal
- [ ] Redis para cache distribuído
- [ ] OIDC/OAuth2 provider
- [ ] Policy versioning e rollback
- [ ] Dashboard web de policies (APL editor visual)
- [ ] Webhooks para eventos de autorização
- [ ] SDK cliente (Python, Node.js)
- [ ] Policy dry-run (simular sem persistir)
- [ ] Batch evaluate (múltiplos contextos em uma chamada)

---

*O2 Data Solutions — "Hora de Aventura no Reino de Ooo IAM"*

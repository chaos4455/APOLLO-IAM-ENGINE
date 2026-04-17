# Apollo IAM Engine — Documento de Produto

**Versao:** 1.0.0  
**Status:** Producao  
**Autor:** Elias Andrade — O2 Data Solutions

---

## Proposta de Valor

Apollo IAM Engine resolve o problema de **fragmentacao de autenticacao e autorizacao** em arquiteturas de microsservicos.

Em vez de cada servico implementar sua propria logica de acesso, todos delegam para o Apollo — o guardiao central. Um unico ponto de verdade para identidade, roles, permissoes, atributos e policies declarativas.

---

## Personas

| Persona | Necessidade Principal |
|---|---|
| Dev de microsservico | Verificar acesso via `POST /auth/check` sem implementar logica propria |
| Admin de sistema | Gerenciar usuarios, roles, permissoes e policies via API REST ou Admin UI |
| Arquiteto de seguranca | Definir policies declarativas em JSON/YAML (APL) com 14 operadores |
| Auditor | Consultar audit trail completo e imutavel de todas as acoes |
| Arquiteto multi-tenant | Isolar policies e decisoes por `tenant_id` com garantia de nao-vazamento |

---

## Capacidades

### Autenticacao
- Login com username/password → JWT HS256 (access + refresh token)
- Refresh token com rotacao automatica
- Logout com blacklist de token (persistida + cache L1 TTL 3600s)
- Validacao de token com payload completo (roles, permissions, RBAC, ABAC)
- Cache de decode JWT (L1 TTL 30s) — evita jwt.decode() a cada request

### RBAC (Role-Based Access Control)
- Roles com permissoes granulares no formato `{resource}:{action}`
- Multiplas roles por usuario
- Grupos de usuarios
- Atributos RBAC customizaveis (key-value, incluidos no JWT)
- User types (classificacao de usuarios)
- User levels com rank numerico (hierarquia de nivel)

### ABAC (Attribute-Based Access Control)
- Custom entity types com slug unico (ex: `regiao`, `cargo`, `contrato`)
- Valores por tipo (ex: `sul`, `sudeste`, `nordeste`)
- Atribuicao de entidades a usuarios (1 por tipo)
- Avaliacao combinada RBAC+ABAC no `/auth/check`

### Apollo Policy Language (APL) v3
- Policies declarativas em **JSON ou YAML**
- Efeito **Allow/Deny explicito** (deny sempre vence, independente de prioridade)
- **16 operadores** de condicao (incluindo `time_before`, `time_after`)
- Condicoes compostas **AND/OR**
- **Templating dinamico** em valores: `{{subject_id}}`, `{{subject.X}}`
- Resource-level com **glob patterns** e **hierarquia de caminhos**
- **Prioridade configuravel** (menor numero = maior prioridade)
- **Multi-tenant** via `tenant_id` com isolamento logico garantido
- **Policy composition**: `scope=global` → `tenant` → `user` com heranca
- **Cache de decisao** LRU+TTL, chave SHA-256 do contexto completo, 8192 entradas
- **Audit trail** de todas as decisoes (tabela `decision_audit` dedicada)
- **Explain endpoint** para rastreamento completo por condicao (debug/audit)
- **v3: Time-based policies** — `valid_from`, `valid_until`, `time_window` (HH:MM-HH:MM)
- **v3: Context schema validation** — `context_schema` por policy com validacao de tipos em runtime
- **v3: Conflict resolution score** — `weight` + `scope_score` para desempate explicito entre policies conflitantes
- **v3: Regex seguro** — timeout 0.5s via ThreadPoolExecutor, limite 256 chars (protecao ReDoS)
- **v3: Simulate/sandbox** — `POST /simulate` e `/simulate/batch` para what-if sem persistir nada
- **v3: Cache key completa** — hash inclui subject completo, nao apenas IDs (sem decisoes erradas)
- **v3: Audit estruturado** — `evaluated_policies`, `conflict_score`, `schema_violations`, `time_skipped`, `timestamp`

### Policy Enforcement Point (PEP) — v3
- Middleware ASGI plug-and-play para qualquer rota FastAPI/Starlette
- Intercepta requests, extrai JWT, monta subject, avalia APL automaticamente
- Retorna 403 com `X-APL-Decision` e `X-APL-Policy` nos headers de resposta
- Superuser bypass configuravel por regra
- Zero modificacao nos handlers existentes
- Configuracao declarativa via `PEPRule` (path_prefix, action, resource_template)

### Seguranca
- mTLS para comunicacao entre servicos (TLS 1.2+, ECDHE+AES-GCM)
- Rate limiting por IP e rota (sliding window)
- **v3: Rate limiting por tenant** via `X-Tenant-ID` header — previne monopolizacao do servico
- Security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)
- Backpressure via RequestQueueMiddleware (503 se fila cheia)
- Audit log imutavel com SHA-256 de integridade por entrada
- Bcrypt para senhas (custo alto intencional — protecao contra brute force)
- Default deny em todas as policies APL

### Observabilidade
- Event logger universal: JSON (NDJSON), YAML, Markdown, SQLite
- Escrita em arquivo via fila assincrona (background thread — nao bloqueia requests)
- Log hooks tipados por dominio (auth, policy, user, role, group, etc.)
- Metricas de sistema via `/admin/metrics/` (CPU, memoria, disco, rede, processo)
- Cache stats via `/admin/metrics/cache` e `/admin/policies/cache/stats`
- Decision audit trail via `/admin/policies/decisions/audit`

### Admin UI
- Dashboard responsivo (dark theme, mobile-first)
- Gerenciamento completo de usuarios, roles, permissoes, grupos
- Gerenciamento de policies APL com toggle ativo/inativo
- Visualizacao de metricas em tempo real (auto-refresh 5s)
- Event logs com filtros client-side
- Audit logs com paginacao

---

## Resultados de Teste (Suite Funcional)

Ultima execucao: `run_20260417_195127`

| Metrica | Valor |
|---|---|
| Total de steps | 132 |
| Passed | 132 |
| Failed | 0 |
| Pass rate | 100.0% |
| Latencia media | 2090.8 ms |
| Latencia P50 | 2057.6 ms |
| Latencia P90 | 2284.5 ms |
| Latencia P95 | 2309.8 ms |
| Latencia P99 | 2474.9 ms |

> Nota: latencia inclui overhead de TLS (mTLS habilitado) e bcrypt no login.
> Endpoints sem I/O de banco retornam em < 1ms (latencia 0.0ms no relatorio = operacao local).

---

## Endpoints Principais

| Endpoint | Metodo | Descricao |
|---|---|---|
| `/health` | GET | Health check |
| `/auth/token` | POST | Login → JWT |
| `/auth/refresh` | POST | Renovar token |
| `/auth/logout` | POST | Revogar token |
| `/auth/validate` | POST | Validar token + payload completo |
| `/auth/check` | POST | Verificar RBAC+ABAC (para sistemas externos) |
| `/admin/policies/` | POST/GET | Criar/listar policies APL |
| `/admin/policies/raw` | POST | Criar policy via JSON/YAML raw |
| `/admin/policies/evaluate` | POST | Avaliar contexto de acesso |
| `/admin/policies/explain` | POST | Rastreamento completo da avaliacao |
| `/admin/policies/reload` | POST | Recarregar engine do banco |
| `/admin/policies/cache/stats` | GET | Stats do decision cache |
| `/admin/policies/decisions/audit` | GET | Audit trail de decisoes |
| `/admin/policies/simulate` | POST | Simulacao what-if (sem persistir) |
| `/admin/policies/simulate/batch` | POST | Simulacao em massa (multiplos contextos) |
| `/admin/users/` | GET/POST | Gerenciar usuarios |
| `/admin/roles/` | GET/POST | Gerenciar roles |
| `/admin/permissions/` | GET/POST | Gerenciar permissoes |
| `/admin/groups/` | GET/POST | Gerenciar grupos |
| `/admin/rbac/` | GET/POST | Gerenciar atributos RBAC |
| `/admin/user-types/` | GET/POST | Gerenciar tipos de usuario |
| `/admin/user-levels/` | GET/POST | Gerenciar niveis de usuario |
| `/admin/custom-entities/types` | GET/POST | Gerenciar tipos de entidade ABAC |
| `/admin/custom-entities/{slug}/values` | GET/POST | Gerenciar valores de entidade |
| `/admin/settings/` | GET/PUT | Configuracoes do sistema |
| `/admin/audit/` | GET | Audit logs |
| `/admin/metrics/` | GET | Metricas do sistema |
| `/admin/metrics/logs` | GET | Event logs |
| `/admin/metrics/cache` | GET | Stats de todos os caches |

---

## SLOs (Service Level Objectives)

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

*Elias Andrade — O2 Data Solutions*

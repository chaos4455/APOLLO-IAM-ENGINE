# Apollo IAM Engine — API Reference

**Versao:** 1.0.0  
**Base URL HTTP:**  `http://localhost:8000`  
**Base URL mTLS:**  `https://localhost:8443`  
**Swagger UI:**     `/docs`  
**ReDoc:**          `/redoc`  
**Autor:** Elias Andrade — O2 Data Solutions

---

## Autenticacao

Todos os endpoints protegidos requerem:

```http
Authorization: Bearer <access_token>
```

O token e um JWT HS256 com payload:

```json
{
  "sub": "username",
  "user_id": "uuid",
  "is_superuser": false,
  "roles": ["vendedor"],
  "permissions": ["cotacao:create", "cotacao:read"],
  "group": "comercial",
  "group_id": "uuid",
  "user_type": "funcionario",
  "user_level": "senior",
  "user_level_rank": 3,
  "rbac": {"department": "sales"},
  "abac": {"regiao": "sul"},
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "uuid"
}
```

---

## Health

### GET /health

Verifica disponibilidade do servico.

**Response 200:**
```json
{
  "status": "ok",
  "service": "Apollo IAM Engine",
  "version": "1.0.0"
}
```

---

## Auth

### POST /auth/token

Login com username/password. Retorna JWT access + refresh token.

**Content-Type:** `application/x-www-form-urlencoded`

**Request:**
```
username=admin&password=admin
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Erros:**
- `401` — credenciais invalidas ou usuario inativo
- `429` — rate limit excedido (10 req/min por IP)

---

### POST /auth/refresh

Renova o access token usando o refresh token.

**Request:**
```json
{"refresh_token": "eyJ..."}
```

**Response 200:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

### POST /auth/logout

Revoga o token atual (adiciona jti na blacklist).

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{"detail": "Token revogado."}
```

---

### POST /auth/validate

Valida um token e retorna o payload completo decodificado.

**Request:**
```json
{"token": "eyJ..."}
```

**Response 200:**
```json
{
  "sub": "usuario1",
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "is_superuser": false,
  "roles": ["vendedor"],
  "permissions": ["cotacao:create", "cotacao:read"],
  "group": "comercial",
  "group_id": "uuid",
  "user_type": "funcionario",
  "user_level": "senior",
  "user_level_rank": 3,
  "rbac": {"department": "sales"},
  "abac": {"regiao": "sul"},
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "uuid"
}
```

**Erros:**
- `401` — token invalido, expirado ou revogado

---

### POST /auth/check

Verifica se um token tem acesso com base em criterios RBAC+ABAC.  
Endpoint para sistemas externos delegarem verificacao de acesso ao Apollo.

**Request:**
```json
{
  "token": "eyJ...",
  "require_roles": ["vendedor"],
  "require_all_roles": null,
  "require_permissions": ["cotacao:create"],
  "require_abac": {"department": "sales"},
  "require_level_gte": 3
}
```

| Campo | Tipo | Descricao |
|---|---|---|
| `token` | string | JWT a verificar |
| `require_roles` | list[str]\|null | Pelo menos uma das roles |
| `require_all_roles` | list[str]\|null | Todas as roles obrigatorias |
| `require_permissions` | list[str]\|null | Pelo menos uma das permissoes |
| `require_abac` | dict\|null | Atributos ABAC exigidos (todos) |
| `require_level_gte` | int\|null | Nivel minimo (rank) |

**Response 200:**
```json
{
  "allowed": true,
  "reason": "ok",
  "subject": "usuario1",
  "roles": ["vendedor"],
  "permissions": ["cotacao:create", "cotacao:read"],
  "abac": {"department": "sales"},
  "user_level_rank": 3
}
```

**Response 200 (negado):**
```json
{
  "allowed": false,
  "reason": "ABAC negado: 'department' esperado='finance' atual='sales'",
  "subject": "usuario1",
  "roles": ["vendedor"],
  "permissions": [],
  "abac": {"department": "sales"},
  "user_level_rank": 3
}
```

---

## Policies (APL)

### POST /admin/policies/

Cria uma policy estruturada (JSON).

**Request:**
```json
{
  "id": "pol-vendedor-cotacao",
  "name": "Vendedores — acesso a cotacoes",
  "description": "Permite criar e ler cotacoes para vendedores senior",
  "version": "2.0",
  "tenant_id": "tenant-empresa-abc",
  "scope": "tenant",
  "subject_id": null,
  "inherits": [],
  "effect": "allow",
  "priority": 10,
  "actions": ["cotacao:create", "cotacao:read"],
  "resources": ["cotacao/*", "empresa/*/cotacao/*"],
  "conditions": [
    {"field": "roles",      "op": "contains", "value": "vendedor"},
    {"field": "user_level", "op": "gte",      "value": 3},
    {"field": "department", "op": "eq",       "value": "{{subject.department}}"}
  ],
  "condition_logic": "AND",
  "enabled": true
}
```

**Response 201:** policy criada (mesmo schema)

---

### POST /admin/policies/raw

Cria policy via string JSON ou YAML raw.

**Request:**
```json
{
  "format": "yaml",
  "content": "name: Negar bloqueados\neffect: deny\npriority: 1\nactions:\n  - '*'\nresources:\n  - '*'\nconditions:\n  - field: blocked\n    op: eq\n    value: true\n"
}
```

---

### GET /admin/policies/

Lista policies com filtros opcionais.

**Query params:**
- `tenant_id` — filtra por tenant (inclui globais)
- `scope` — `global` | `tenant` | `user`

**Response 200:** `list[PolicyDict]`

---

### GET /admin/policies/{policy_id}

Retorna policy por ID.

**Response 200:** `PolicyDict`  
**Response 404:** policy nao encontrada

---

### DELETE /admin/policies/{policy_id}

Remove policy e invalida o decision cache.

**Response 204:** sem conteudo

---

### PATCH /admin/policies/{policy_id}/toggle?enabled=false

Ativa ou desativa uma policy. Recarrega o engine e invalida o cache.

**Response 200:**
```json
{"policy_id": "pol-vendedor-cotacao", "enabled": false}
```

---

### POST /admin/policies/evaluate

Avalia uma policy para um contexto de acesso.

**Request:**
```json
{
  "subject": {
    "roles": ["vendedor"],
    "department": "sales",
    "user_level": 3,
    "is_active": true
  },
  "action": "cotacao:create",
  "resource": "empresa/123/cotacao/456",
  "tenant_id": "tenant-empresa-abc",
  "subject_id": "user-uuid-123",
  "use_cache": true
}
```

**Response 200 (allow):**
```json
{
  "allowed": true,
  "effect": "allow",
  "matched_policy": "pol-vendedor-cotacao",
  "reason": "Permitido pela policy 'Vendedores — acesso a cotacoes' (id=pol-vendedor-cotacao, scope=tenant).",
  "decision": "allow"
}
```

**Response 200 (deny explicito):**
```json
{
  "allowed": false,
  "effect": "deny",
  "matched_policy": "pol-negar-bloqueados",
  "reason": "Negado pela policy 'Negar bloqueados' (id=pol-negar-bloqueados, scope=tenant).",
  "decision": "deny"
}
```

**Response 200 (default deny):**
```json
{
  "allowed": false,
  "effect": null,
  "matched_policy": null,
  "reason": "Nenhuma policy aplicavel encontrada (default deny).",
  "decision": "no_match"
}
```

---

### POST /admin/policies/explain

Retorna rastreamento completo da avaliacao (debug/audit).  
Mesmo payload do `/evaluate`.

**Response 200:**
```json
{
  "decision": {
    "allowed": true,
    "matched_policy": "pol-vendedor-cotacao",
    "reason": "...",
    "composition_chain": ["pol-base-global", "pol-vendedor-cotacao"]
  },
  "context": {
    "action": "cotacao:create",
    "resource": "empresa/123/cotacao/456",
    "tenant_id": "tenant-empresa-abc",
    "subject_id": "user-uuid-123"
  },
  "steps": [
    {
      "policy_id": "pol-base-global",
      "policy_name": "Base Global",
      "scope": "global",
      "effect": "allow",
      "priority": 1000,
      "action_match": true,
      "resource_match": true,
      "conditions_result": true,
      "applicable": true,
      "conditions": [
        {
          "field": "is_active",
          "op": "eq",
          "value_template": true,
          "value_resolved": true,
          "actual": true,
          "result": true
        }
      ]
    }
  ]
}
```

---

### POST /admin/policies/reload

Recarrega todas as policies habilitadas do banco no engine em memoria.

**Response 200:**
```json
{"loaded": 7}
```

---

### GET /admin/policies/cache/stats

Estatisticas do decision cache.

**Response 200:**
```json
{
  "size": 42,
  "max_size": 8192,
  "hits": 1337,
  "misses": 42,
  "hit_rate": 0.9694,
  "default_ttl": 60.0
}
```

---

### GET /admin/policies/decisions/audit

Consulta o audit trail de decisoes de policy.

**Query params:**
- `tenant_id` — filtra por tenant
- `subject_id` — filtra por sujeito
- `decision` — `allow` | `deny` | `no_match`
- `action` — filtra por acao
- `limit` (default 100)
- `offset` (default 0)

**Response 200:** `list[DecisionAuditEntry]`

---

## Usuarios

### GET /admin/users/

Lista usuarios com paginacao.

**Query params:** `skip=0`, `limit=100`

**Response 200:** `list[UserResponse]`

```json
[{
  "id": "uuid",
  "username": "joao.silva",
  "email": "joao@empresa.com",
  "full_name": "Joao Silva",
  "is_active": true,
  "is_superuser": false,
  "group_id": "uuid",
  "type_id": "uuid",
  "level_id": "uuid",
  "roles": ["vendedor"],
  "created_at": "2026-01-01T00:00:00",
  "updated_at": "2026-01-01T00:00:00"
}]
```

---

### POST /admin/users/

Cria usuario.

**Request:**
```json
{
  "username": "joao.silva",
  "password": "Senha123!",
  "email": "joao@empresa.com",
  "full_name": "Joao Silva",
  "is_active": true,
  "is_superuser": false,
  "group_id": null,
  "type_id": null,
  "level_id": null,
  "role_names": ["vendedor"]
}
```

**Response 201:** `UserResponse`  
**Response 409:** username ou email ja existe

---

### GET /admin/users/{user_id}

Retorna usuario por ID.

---

### PUT /admin/users/{user_id}

Atualiza campos do usuario.

**Request:**
```json
{
  "email": "novo@empresa.com",
  "full_name": "Joao Silva Jr",
  "is_active": true,
  "group_id": "uuid",
  "type_id": "uuid",
  "level_id": "uuid"
}
```

---

### DELETE /admin/users/{user_id}

Remove usuario e todas as suas associacoes (roles, rbac values, custom entities).

**Response 204:** sem conteudo

---

### POST /admin/users/{user_id}/toggle-status

Alterna `is_active` do usuario.

**Response 200:**
```json
{"is_active": false}
```

---

### POST /admin/users/{user_id}/reset-password

Redefine a senha do usuario.

**Request:**
```json
{"new_password": "NovaSenha456!"}
```

**Response 200:**
```json
{"detail": "Senha redefinida."}
```

---

## Roles

### GET /admin/roles/

Lista todas as roles com suas permissoes.

**Response 200:**
```json
[{
  "id": "uuid",
  "name": "vendedor",
  "description": "Vendedor do sistema",
  "is_active": true,
  "permissions": ["cotacao:create", "cotacao:read"]
}]
```

---

### POST /admin/roles/

Cria role.

**Request:**
```json
{"name": "vendedor", "description": "Vendedor do sistema"}
```

**Response 201:** `RoleResponse`

---

### DELETE /admin/roles/{role_id}

Remove role.

**Response 204**

---

### POST /admin/roles/{role_id}/assign-user/{user_id}

Atribui role a usuario.

**Response 200:** `{}`

---

### DELETE /admin/roles/{role_id}/revoke-user/{user_id}

Revoga role de usuario.

**Response 200:** `{}`

---

## Permissoes

### GET /admin/permissions/

Lista permissoes.

**Response 200:**
```json
[{
  "id": "uuid",
  "name": "cotacao:create",
  "resource": "cotacao",
  "action": "create",
  "description": "Criar cotacao"
}]
```

---

### POST /admin/permissions/

Cria permissao.

**Request:**
```json
{
  "name": "cotacao:create",
  "resource": "cotacao",
  "action": "create",
  "description": "Criar cotacao"
}
```

---

### DELETE /admin/permissions/{perm_id}

Remove permissao.

**Response 204**

---

### POST /admin/permissions/{perm_id}/assign-role/{role_id}

Atribui permissao a role.

**Response 200:** `{}`

---

## Grupos

### GET /admin/groups/

Lista grupos.

---

### POST /admin/groups/

Cria grupo.

**Request:**
```json
{"name": "comercial", "description": "Time comercial"}
```

---

### DELETE /admin/groups/{group_id}

Remove grupo.

**Response 204**

---

### POST /admin/groups/{group_id}/assign-user/{user_id}

Atribui usuario ao grupo.

**Response 200:** `{}`

---

## Atributos RBAC

### GET /admin/rbac/

Lista atributos RBAC.

**Response 200:**
```json
[{
  "id": "uuid",
  "key": "department",
  "label": "Departamento",
  "value_type": "string",
  "description": "Departamento do usuario",
  "is_active": true
}]
```

---

### POST /admin/rbac/

Cria atributo RBAC.

**Request:**
```json
{
  "key": "department",
  "label": "Departamento",
  "value_type": "string",
  "description": "Departamento do usuario"
}
```

---

### DELETE /admin/rbac/{attr_id}

Remove atributo e todos os valores atribuidos a usuarios.

**Response 204**

---

### POST /admin/rbac/assign/{user_id}

Atribui valor de atributo RBAC a usuario.

**Request:**
```json
{
  "attribute_key": "department",
  "value": "sales"
}
```

**Response 200:** `{}`

---

## User Types

### GET /admin/user-types/
### POST /admin/user-types/

```json
{"name": "funcionario", "description": "Funcionario padrao"}
```

### GET /admin/user-types/{type_id}
### PUT /admin/user-types/{type_id}
### DELETE /admin/user-types/{type_id}

---

## User Levels

### GET /admin/user-levels/
### POST /admin/user-levels/

```json
{"name": "senior", "rank": 3, "description": "Nivel senior"}
```

### GET /admin/user-levels/{level_id}
### PUT /admin/user-levels/{level_id}
### DELETE /admin/user-levels/{level_id}

---

## Custom Entities (ABAC)

### GET /admin/custom-entities/types
### POST /admin/custom-entities/types

```json
{"slug": "regiao", "label": "Regiao", "description": "Regiao geografica"}
```

### GET /admin/custom-entities/types/{slug}
### PUT /admin/custom-entities/types/{slug}
### DELETE /admin/custom-entities/types/{slug}

### GET /admin/custom-entities/{slug}/values
### POST /admin/custom-entities/{slug}/values

```json
{"name": "sul", "description": "Regiao Sul"}
```

### GET /admin/custom-entities/{slug}/values/{value_id}
### PUT /admin/custom-entities/{slug}/values/{value_id}
### DELETE /admin/custom-entities/{slug}/values/{value_id}

### POST /admin/custom-entities/assign/{user_id}

```json
{
  "entity_type_slug": "regiao",
  "entity_value_id": "uuid-do-valor"
}
```

### DELETE /admin/custom-entities/assign/{user_id}/{slug}

Remove entidade ABAC do usuario.

**Response 204**

### GET /admin/custom-entities/user/{user_id}

Lista entidades ABAC atribuidas ao usuario.

**Response 200:**
```json
[{
  "entity_type_slug": "regiao",
  "entity_value_id": "uuid",
  "entity_value_name": "sul",
  "assigned_at": "2026-01-01T00:00:00"
}]
```

---

## Settings

### GET /admin/settings/

**Response 200:**
```json
{
  "access_token_expire_minutes": 60,
  "refresh_token_expire_days": 7,
  "allow_registration": false,
  "max_login_attempts": 5,
  "lockout_minutes": 15
}
```

### PUT /admin/settings/

**Request:** campos opcionais (apenas os que deseja alterar)

```json
{
  "access_token_expire_minutes": 90,
  "max_login_attempts": 3
}
```

---

## Audit Logs

### GET /admin/audit/

Lista logs de auditoria. Le do `event_log` (apollo_log.db) com fallback para `audit_logs`.

**Query params:**
- `skip` (default 0)
- `limit` (default 100)
- `actor` — filtra por ator
- `status` — `success` | `failure`

**Response 200:**
```json
[{
  "id": "1",
  "actor": "admin",
  "action": "auth.login_success",
  "resource": "auth",
  "resource_id": null,
  "status": "success",
  "created_at": "2026-01-01T00:00:00",
  "tenant_id": null,
  "duration_ms": "45.2"
}]
```

---

## Metricas

### GET /admin/metrics/

Metricas completas do sistema: CPU, memoria, disco, rede, processo, KPIs do banco, logs recentes.

**Response 200:**
```json
{
  "timestamp": "2026-04-17T22:56:19Z",
  "uptime_s": 227,
  "uptime_fmt": "0h 3m 47s",
  "platform": "Windows",
  "python": "3.11.0",
  "cpu": {
    "percent": 3.6,
    "count_logical": 4,
    "count_physical": 4,
    "freq_mhz": 2400.0,
    "per_core": [2.1, 4.5, 3.2, 4.6]
  },
  "memory": {
    "total_mb": 16324.3,
    "used_mb": 10634.1,
    "available_mb": 5690.2,
    "percent": 65.1,
    "swap_total_mb": 4096.0,
    "swap_used_mb": 512.0,
    "swap_percent": 12.5
  },
  "disk": {
    "total_gb": 476.94,
    "used_gb": 200.12,
    "free_gb": 276.82,
    "percent": 41.9
  },
  "db": {
    "users": 9,
    "roles": 7,
    "permissions": 20,
    "groups": 2,
    "rbac_attrs": 2,
    "audit_logs": 150,
    "user_types": 1,
    "user_levels": 4,
    "token_blacklist": 3
  },
  "logs": {
    "total": 1836,
    "success": 1746,
    "failure": 89,
    "logins": 38,
    "recent": [...]
  }
}
```

### GET /admin/metrics/logs

Lista event logs com paginacao.

**Query params:** `skip=0`, `limit=200`

### GET /admin/metrics/cache

Estatisticas de todos os caches em memoria.

**Response 200:**
```json
{
  "token":           {"size": 5, "max_size": 4096, "hits": 110, "misses": 13, "hit_rate": 0.894},
  "blacklist":       {"size": 3, "max_size": 8192, "hits": 95,  "misses": 8,  "hit_rate": 0.922},
  "user_enrichment": {"size": 4, "max_size": 512,  "hits": 42,  "misses": 4,  "hit_rate": 0.913},
  "metrics":         {"size": 1, "max_size": 4,    "hits": 12,  "misses": 3,  "hit_rate": 0.800},
  "db_kpis":         {"size": 2, "max_size": 4,    "hits": 8,   "misses": 2,  "hit_rate": 0.800},
  "settings":        {"size": 1, "max_size": 4,    "hits": 5,   "misses": 1,  "hit_rate": 0.833}
}
```

---

## Codigos de Status

| Codigo | Significado |
|---|---|
| 200 | Sucesso |
| 201 | Criado |
| 204 | Sem conteudo (delete bem-sucedido) |
| 400 | Requisicao invalida / erro de integridade |
| 401 | Nao autenticado (token invalido, expirado ou revogado) |
| 403 | Sem permissao (nao e superuser) |
| 404 | Recurso nao encontrado |
| 409 | Conflito (registro ja existe — UNIQUE constraint) |
| 422 | Erro de validacao Pydantic |
| 429 | Rate limit excedido |
| 500 | Erro interno do servidor |
| 503 | Servico indisponivel (request queue cheia) |

---

*Elias Andrade — O2 Data Solutions*

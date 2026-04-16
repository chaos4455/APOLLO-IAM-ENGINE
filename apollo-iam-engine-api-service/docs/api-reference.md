# 🗺️ Apollo IAM Engine — API Reference

> *"O mapa do tesouro do Reino de Ooo — todos os endpoints documentados!"*

**Base URL:** `http://localhost:8000` (HTTP) | `https://localhost:8443` (mTLS)  
**Docs interativos:** `/docs` (Swagger) | `/redoc` (ReDoc)

---

## Autenticação

Todos os endpoints protegidos requerem:
```
Authorization: Bearer <access_token>
```

---

## Auth

### POST /auth/token
Login com username/password.

**Request** (form-data):
```
username=admin&password=admin
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

### POST /auth/refresh
Renovar access token.

**Request:**
```json
{"refresh_token": "eyJ..."}
```

---

### POST /auth/logout
Revogar token atual.

**Headers:** `Authorization: Bearer <token>`

---

### POST /auth/validate
Validar token e retornar payload completo.

**Request:**
```json
{"token": "eyJ..."}
```

**Response 200:**
```json
{
  "sub": "admin",
  "user_id": "uuid",
  "is_superuser": true,
  "roles": ["admin"],
  "permissions": ["users:read", "users:write"],
  "group": null,
  "user_type": null,
  "user_level": null,
  "user_level_rank": 0,
  "rbac": {},
  "abac": {},
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "uuid"
}
```

---

### POST /auth/check
Verificar RBAC+ABAC para sistemas externos.

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

---

## Policies (APL)

### POST /admin/policies/
Criar policy estruturada (JSON).

**Request:**
```json
{
  "name": "Vendedores — cotação",
  "description": "Acesso ao módulo de cotação",
  "effect": "allow",
  "priority": 10,
  "actions": ["cotacao:create", "cotacao:read"],
  "resources": ["cotacao/*"],
  "conditions": [
    {"field": "roles", "op": "contains", "value": "vendedor"},
    {"field": "user_level", "op": "gte", "value": 3}
  ],
  "condition_logic": "AND",
  "tenant_id": "tenant-abc",
  "enabled": true
}
```

**Response 201:**
```json
{
  "id": "uuid-gerado",
  "name": "Vendedores — cotação",
  "effect": "allow",
  ...
}
```

---

### POST /admin/policies/raw
Criar policy via string JSON ou YAML.

**Request:**
```json
{
  "format": "yaml",
  "content": "name: Minha Policy\neffect: allow\nactions:\n  - '*'\nresources:\n  - '*'\n"
}
```

---

### POST /admin/policies/evaluate
Avaliar policy para um contexto.

**Request:**
```json
{
  "subject": {
    "roles": ["vendedor"],
    "department": "sales",
    "user_level": 3
  },
  "action": "cotacao:create",
  "resource": "cotacao/123",
  "tenant_id": "tenant-abc",
  "subject_id": "user-uuid",
  "use_cache": true
}
```

**Response 200:**
```json
{
  "allowed": true,
  "effect": "allow",
  "matched_policy": "pol-vendedor-cotacao",
  "reason": "Permitido pela policy 'Vendedores — cotação' (id=pol-vendedor-cotacao)."
}
```

**Response (no match):**
```json
{
  "allowed": false,
  "effect": null,
  "matched_policy": null,
  "reason": "Nenhuma policy aplicável encontrada (default deny)."
}
```

---

### GET /admin/policies/
Listar policies.

**Query params:** `?tenant_id=tenant-abc`

---

### GET /admin/policies/{policy_id}
Obter policy por ID.

---

### DELETE /admin/policies/{policy_id}
Remover policy (superuser only). `204 No Content`

---

### PATCH /admin/policies/{policy_id}/toggle?enabled=false
Ativar/desativar policy.

**Response 200:**
```json
{"policy_id": "uuid", "enabled": false}
```

---

### POST /admin/policies/reload
Recarregar todas as policies do banco no engine.

**Response 200:**
```json
{"loaded": 42}
```

---

### GET /admin/policies/cache/stats
Stats do cache de decisão.

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

## Usuários

### GET /admin/users/
Listar usuários. `?skip=0&limit=100`

### POST /admin/users/
Criar usuário.
```json
{
  "username": "joao",
  "password": "Senha123!",
  "email": "joao@empresa.com",
  "full_name": "João Silva",
  "is_active": true
}
```

### GET /admin/users/{user_id}
### PUT /admin/users/{user_id}
### DELETE /admin/users/{user_id}
### POST /admin/users/{user_id}/toggle-status
### POST /admin/users/{user_id}/reset-password

---

## Roles

### GET /admin/roles/
### POST /admin/roles/
```json
{"name": "vendedor", "description": "Vendedor do sistema"}
```
### DELETE /admin/roles/{role_id}
### POST /admin/roles/{role_id}/assign/{user_id}
### DELETE /admin/roles/{role_id}/revoke/{user_id}

---

## Permissões

### GET /admin/permissions/
### POST /admin/permissions/
```json
{"name": "cotacao:create", "resource": "cotacao", "action": "create"}
```
### DELETE /admin/permissions/{perm_id}
### POST /admin/permissions/{perm_id}/assign/{role_id}

---

## Grupos

### GET /admin/groups/
### POST /admin/groups/
### DELETE /admin/groups/{group_id}
### POST /admin/groups/{group_id}/assign/{user_id}

---

## RBAC Attributes

### GET /admin/rbac-attributes/
### POST /admin/rbac-attributes/
```json
{"key": "department", "label": "Departamento", "description": "Dept do usuário"}
```
### POST /admin/rbac-attributes/{attr_id}/assign/{user_id}
```json
{"value": "sales"}
```

---

## User Types & Levels

### GET /admin/user-types/
### POST /admin/user-types/
```json
{"name": "funcionario", "description": "Funcionário padrão"}
```

### GET /admin/user-levels/
### POST /admin/user-levels/
```json
{"name": "senior", "rank": 3, "description": "Nível sênior"}
```

---

## Custom Entities (ABAC)

### GET /admin/custom-entities/types/
### POST /admin/custom-entities/types/
```json
{"slug": "regiao", "name": "Região", "description": "Região geográfica"}
```
### POST /admin/custom-entities/types/{slug}/values/
```json
{"name": "sul", "description": "Região Sul"}
```

---

## Settings

### GET /admin/settings/
### PUT /admin/settings/
```json
{"max_login_attempts": 5, "session_timeout": 3600}
```

---

## Audit Logs

### GET /admin/audit-logs/
`?skip=0&limit=50`

---

## Metrics

### GET /admin/metrics/
Métricas do sistema (usuários, roles, permissões, cache stats, etc.)

---

## Health

### GET /health
```json
{"status": "ok", "service": "Apollo IAM Engine", "version": "1.0.0"}
```

---

## Códigos de Status

| Código | Significado |
|---|---|
| 200 | Sucesso |
| 201 | Criado |
| 204 | Sem conteúdo (delete) |
| 400 | Requisição inválida |
| 401 | Não autenticado |
| 403 | Sem permissão |
| 404 | Não encontrado |
| 409 | Conflito (já existe) |
| 422 | Erro de validação Pydantic |
| 429 | Rate limit excedido |
| 500 | Erro interno |
| 503 | Serviço indisponível (request queue cheia) |

---

*O2 Data Solutions — "O mapa do tesouro do Reino de Ooo!"*

# Apollo Policy Language (APL) v2 — Referencia Completa

**Versao:** 2.0  
**Engine:** `src/domain/policy/policy_dsl.py`  
**Cache:** `src/infrastructure/cache/decision_cache.py`  
**Service:** `src/application/services/policy_service.py`  
**Autor:** Elias Andrade — O2 Data Solutions

---

## Visao Geral

APL e uma linguagem declarativa de policies para controle de acesso.  
Cada policy define: quem pode fazer o que, em qual recurso, sob quais condicoes.

```
Policy = {effect} + {actions} + {resources} + {conditions} + {priority}
```

O engine avalia policies em ordem de prioridade (menor numero = maior prioridade).  
**Deny explicito sempre vence Allow**, independente de prioridade.  
**Default deny**: sem policy aplicavel = acesso negado.

---

## Estrutura Completa

### JSON
```json
{
  "id": "pol-vendedor-cotacao",
  "name": "Vendedores — acesso a cotacoes",
  "description": "Permite criar e ler cotacoes para vendedores senior",
  "version": "2.0",
  "tenant_id": "tenant-empresa-abc",
  "scope": "tenant",
  "subject_id": null,
  "inherits": ["pol-base-global"],
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

### YAML
```yaml
id: pol-vendedor-cotacao
name: "Vendedores — acesso a cotacoes"
version: "2.0"
tenant_id: tenant-empresa-abc
scope: tenant
inherits:
  - pol-base-global
effect: allow
priority: 10
actions:
  - cotacao:create
  - cotacao:read
resources:
  - cotacao/*
  - empresa/*/cotacao/*
conditions:
  - field: roles
    op: contains
    value: vendedor
  - field: user_level
    op: gte
    value: 3
  - field: department
    op: eq
    value: "{{subject.department}}"
condition_logic: AND
enabled: true
```

---

## Campos

| Campo | Tipo | Default | Descricao |
|---|---|---|---|
| `id` | string | UUID gerado | Identificador unico da policy |
| `name` | string | obrigatorio | Nome descritivo |
| `description` | string | `""` | Descricao detalhada |
| `version` | string | `"2.0"` | Versao do schema |
| `tenant_id` | string\|null | `null` | Tenant; `null` = global (todos os tenants) |
| `scope` | enum | `"tenant"` | `global` \| `tenant` \| `user` |
| `subject_id` | string\|null | `null` | Para `scope=user`: ID do sujeito especifico |
| `inherits` | list[string] | `[]` | IDs de policies pai (heranca de condicoes) |
| `effect` | enum | `"allow"` | `allow` \| `deny` |
| `priority` | int | `100` | Menor numero = maior prioridade |
| `actions` | list[string] | `["*"]` | Acoes (suportam glob: `cotacao:*`, `*`) |
| `resources` | list[string] | `["*"]` | Recursos (hierarquico + glob) |
| `conditions` | list[Condition] | `[]` | Condicoes de acesso |
| `condition_logic` | enum | `"AND"` | `AND` (todas) \| `OR` (qualquer uma) |
| `enabled` | bool | `true` | Ativa/desativa sem remover |

---

## Os 14 Operadores

| Operador | Tipo | Descricao | Exemplo |
|---|---|---|---|
| `eq` | qualquer | Igual (com coercao de tipo) | `{"field": "status", "op": "eq", "value": "active"}` |
| `neq` | qualquer | Diferente | `{"field": "status", "op": "neq", "value": "blocked"}` |
| `gt` | numerico | Maior que | `{"field": "user_level", "op": "gt", "value": 2}` |
| `gte` | numerico | Maior ou igual | `{"field": "user_level", "op": "gte", "value": 3}` |
| `lt` | numerico | Menor que | `{"field": "risk_score", "op": "lt", "value": 50}` |
| `lte` | numerico | Menor ou igual | `{"field": "risk_score", "op": "lte", "value": 100}` |
| `in` | lista | Valor esta na lista | `{"field": "region", "op": "in", "value": ["sul", "sudeste"]}` |
| `not_in` | lista | Valor nao esta na lista | `{"field": "status", "op": "not_in", "value": ["blocked", "suspended"]}` |
| `contains` | lista/string | Lista contem o valor | `{"field": "roles", "op": "contains", "value": "vendedor"}` |
| `not_contains` | lista/string | Lista nao contem | `{"field": "roles", "op": "not_contains", "value": "blocked"}` |
| `starts_with` | string | Comeca com | `{"field": "email", "op": "starts_with", "value": "admin"}` |
| `ends_with` | string | Termina com | `{"field": "email", "op": "ends_with", "value": "@empresa.com"}` |
| `regex` | string | Expressao regular (re.match) | `{"field": "username", "op": "regex", "value": "^[a-z]+\\.[a-z]+$"}` |
| `exists` | qualquer | Campo nao e nulo | `{"field": "department", "op": "exists"}` |
| `not_exists` | qualquer | Campo e nulo | `{"field": "blocked_at", "op": "not_exists"}` |

---

## Templating Dinamico

Qualquer `value` em uma condicao pode conter `{{variavel}}`.  
A variavel e resolvida em tempo de avaliacao a partir do contexto.

### Variaveis disponiveis

| Template | Resolve para |
|---|---|
| `{{subject_id}}` | `ctx.subject_id` |
| `{{tenant_id}}` | `ctx.tenant_id` |
| `{{action}}` | `ctx.action` |
| `{{resource}}` | `ctx.resource` |
| `{{subject.X}}` | `ctx.subject["X"]` |
| `{{extra.X}}` | `ctx.extra["X"]` |

### Exemplos

```json
// Usuario so acessa seus proprios recursos
{"field": "owner_id", "op": "eq", "value": "{{subject_id}}"}

// Recurso deve pertencer ao tenant do contexto
{"field": "resource_tenant", "op": "eq", "value": "{{tenant_id}}"}

// Email deve terminar com dominio do subject
{"field": "email", "op": "ends_with", "value": "@{{subject.company_domain}}"}

// Interpolacao parcial em string
{"field": "resource", "op": "starts_with", "value": "empresa/{{subject.company_id}}/"}
```

---

## Match de Recursos (Hierarquico + Glob)

Recursos sao caminhos hierarquicos. O match e feito em qualquer segmento ancestral.

### Como funciona

```
Pattern:  "empresa/*/cotacao/*"
Recurso:  "empresa/123/departamento/5/cotacao/9"

O engine testa o recurso completo e todos os seus sufixos:
  "empresa/123/departamento/5/cotacao/9"  → fnmatch("empresa/*/cotacao/*") → MATCH
  "empresa/123/cotacao/9"                 → fnmatch("empresa/*/cotacao/*") → MATCH
  "cotacao/9"                             → fnmatch("empresa/*/cotacao/*") → nao bate
```

### Exemplos de patterns

| Pattern | Bate em |
|---|---|
| `*` | Qualquer recurso |
| `cotacao/*` | `cotacao/123`, `empresa/abc/cotacao/123` |
| `empresa/*/cotacao/*` | `empresa/123/cotacao/9`, `empresa/abc/cotacao/xyz` |
| `empresa/123/*` | Qualquer recurso dentro de `empresa/123` |
| `*/relatorio/*` | Qualquer relatorio em qualquer empresa |
| `admin/*` | Qualquer recurso admin |

---

## Policy Composition (Heranca e Scope)

### Scopes

| Scope | Descricao | Prioridade de override |
|---|---|---|
| `global` | Aplica a todos os tenants | Base (menor) |
| `tenant` | Aplica a um tenant especifico | Media |
| `user` | Aplica a um `subject_id` especifico | Maxima (override) |

### Cascata de avaliacao

```
scope=global  (base — vale para todos os tenants)
      |
      v  tenant pode sobrescrever
scope=tenant  (regras especificas do tenant)
      |
      v  user pode sobrescrever
scope=user    (regras individuais — override maximo)

Deny explicito em QUALQUER scope -> nega imediatamente.
Allow mais especifico (user > tenant > global) vence.
```

### Heranca de condicoes (`inherits`)

```json
// Policy base global — condicoes minimas para qualquer acesso
{
  "id": "pol-base-global",
  "scope": "global",
  "effect": "allow",
  "priority": 1000,
  "actions": ["*"],
  "resources": ["*"],
  "conditions": [
    {"field": "is_active",  "op": "eq",        "value": true},
    {"field": "blocked_at", "op": "not_exists"}
  ]
}

// Policy de tenant herda a base e adiciona condicao propria
{
  "id": "pol-tenant-vendedor",
  "scope": "tenant",
  "tenant_id": "tenant-abc",
  "inherits": ["pol-base-global"],
  "effect": "allow",
  "priority": 100,
  "actions": ["cotacao:*"],
  "resources": ["cotacao/*"],
  "conditions": [
    {"field": "roles", "op": "contains", "value": "vendedor"}
    // is_active e blocked_at herdados do pai
    // se redefinir "is_active" aqui, sobrescreve o pai
  ]
}

// Policy de usuario especifico — override maximo
{
  "id": "pol-user-joao",
  "scope": "user",
  "subject_id": "user-joao-123",
  "tenant_id": "tenant-abc",
  "inherits": ["pol-tenant-vendedor"],
  "effect": "allow",
  "priority": 10,
  "actions": ["cotacao:*", "relatorio:read"],
  "resources": ["*"],
  "conditions": []
}
```

### Regras de merge de condicoes

1. Condicoes do pai sao herdadas
2. Se o filho define a mesma `field`, **sobrescreve** a do pai
3. Campos nao redefinidos sao **mantidos** do pai
4. Ciclos de heranca sao detectados e ignorados

---

## Algoritmo de Avaliacao

```python
def evaluate(ctx: EvalContext) -> EvalResult:
    # 1. filtra policies aplicaveis ao tenant
    candidates = [p for p in policies
                  if p.tenant_id == ctx.tenant_id or p.tenant_id is None]

    # 2. filtra por enabled
    candidates = [p for p in candidates if p.enabled]

    # 3. ordena por prioridade (menor = maior prioridade)
    candidates.sort(key=lambda p: p.priority)

    allow_candidate = None

    for policy in candidates:
        # 4. verifica match de action (glob)
        if not action_match(ctx.action, policy.actions):
            continue

        # 5. verifica match de resource (hierarquico + glob)
        if not resource_match(ctx.resource, policy.resources):
            continue

        # 6. resolve templates nas condicoes
        resolved_conditions = resolve_templates(policy.conditions, ctx)

        # 7. avalia condicoes (AND ou OR)
        cond_ok = evaluate_conditions(resolved_conditions, ctx, policy.condition_logic)
        if not cond_ok:
            continue

        # 8. deny explicito -> retorna imediatamente
        if policy.effect == "deny":
            return EvalResult(allowed=False, effect="deny",
                              matched_policy=policy.id, ...)

        # 9. primeiro allow por prioridade
        if allow_candidate is None:
            allow_candidate = policy

    # 10. retorna allow ou default deny
    if allow_candidate:
        return EvalResult(allowed=True, effect="allow",
                          matched_policy=allow_candidate.id, ...)

    return EvalResult(allowed=False, effect=None,
                      matched_policy=None,
                      reason="Nenhuma policy aplicavel encontrada (default deny).")
```

---

## Cache de Decisao

```
Chave:    SHA-256(tenant_id:subject_id:action:resource)
TTL:      60s (default) | configuravel por policy_id via set_policy_ttl()
Eviction: LRU (8192 entradas)
Thread:   thread-safe via threading.Lock

Invalidacao:
  - delete_policy()  -> decision_cache.clear()
  - toggle_policy()  -> decision_cache.clear()
  - reload_from_db() -> decision_cache.clear()
```

---

## Exemplos Praticos

### Deny explicito para usuarios bloqueados (prioridade maxima)

```json
{
  "id": "pol-deny-blocked",
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

### Allow com logica OR (gerente OU aprovador)

```json
{
  "name": "Gerentes e aprovadores — relatorios",
  "effect": "allow",
  "priority": 50,
  "actions": ["relatorio:read", "relatorio:export"],
  "resources": ["relatorio/*"],
  "conditions": [
    {"field": "roles", "op": "contains", "value": "gerente"},
    {"field": "roles", "op": "contains", "value": "aprovador"}
  ],
  "condition_logic": "OR"
}
```

### Glob em resource (admin/*)

```json
{
  "name": "Superadmins — acesso total ao admin",
  "effect": "allow",
  "priority": 5,
  "actions": ["*"],
  "resources": ["admin/*"],
  "conditions": [
    {"field": "is_superuser", "op": "eq", "value": true}
  ]
}
```

### Operador neq (nao bloqueado)

```json
{
  "name": "Usuarios ativos nao bloqueados",
  "effect": "allow",
  "priority": 100,
  "actions": ["*"],
  "resources": ["*"],
  "conditions": [
    {"field": "status", "op": "neq", "value": "blocked"},
    {"field": "is_active", "op": "eq", "value": true}
  ],
  "condition_logic": "AND"
}
```

### Policy com 6 operadores distintos

```json
{
  "name": "Policy multi-operador",
  "effect": "allow",
  "priority": 200,
  "actions": ["cotacao:*"],
  "resources": ["cotacao/*"],
  "conditions": [
    {"field": "roles",       "op": "contains",  "value": "vendedor"},
    {"field": "user_level",  "op": "gte",       "value": 2},
    {"field": "department",  "op": "in",        "value": ["sales", "comercial"]},
    {"field": "email",       "op": "ends_with", "value": "@empresa.com"},
    {"field": "blocked_at",  "op": "not_exists"},
    {"field": "is_active",   "op": "eq",        "value": true}
  ],
  "condition_logic": "AND"
}
```

---

## API — Endpoints APL

| Metodo | Endpoint | Descricao |
|---|---|---|
| POST | `/admin/policies/` | Criar policy (JSON estruturado) |
| POST | `/admin/policies/raw` | Criar policy (JSON/YAML raw string) |
| GET | `/admin/policies/` | Listar policies (filtros: tenant_id, scope) |
| GET | `/admin/policies/{id}` | Obter policy por ID |
| DELETE | `/admin/policies/{id}` | Remover policy |
| PATCH | `/admin/policies/{id}/toggle?enabled=false` | Ativar/desativar |
| POST | `/admin/policies/evaluate` | Avaliar contexto de acesso |
| POST | `/admin/policies/explain` | Rastreamento completo (debug) |
| POST | `/admin/policies/reload` | Recarregar engine do banco |
| GET | `/admin/policies/cache/stats` | Stats do decision cache |
| GET | `/admin/policies/decisions/audit` | Audit trail de decisoes |

---

*Elias Andrade — O2 Data Solutions*

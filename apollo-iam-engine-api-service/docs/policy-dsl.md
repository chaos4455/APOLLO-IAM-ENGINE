# 📜 Apollo Policy Language (APL) v2 — Referência Completa

> *"O Grimório de Jake — versão hardcore do Reino de Ooo!"*
> *"Agora com feitiços dinâmicos, mapas hierárquicos e herança de magias!"*

**Versão:** 2.0  
**Formatos:** JSON, YAML  
**Engine:** `src/domain/policy/policy_dsl.py`  
**Cache:** `src/infrastructure/cache/decision_cache.py`  
**Service:** `src/application/services/policy_service.py`

---

## O que há de novo na v2

| Feature | Descrição |
|---|---|
| ① Variáveis dinâmicas | `{{subject_id}}`, `{{tenant_id}}`, `{{subject.X}}` em `value` |
| ② Hierarquia de recursos | `empresa/*/cotacao/*` bate em `empresa/123/depto/5/cotacao/9` |
| ③ Policy composition | `scope` global → tenant → user com `inherits` e override |
| `/explain` | Rastreamento completo da avaliação (debug/audit) |
| `composition_chain` | Lista de IDs das policies que participaram da decisão |

---

## Estrutura completa de uma Policy v2

### JSON
```json
{
  "id": "pol-vendedor-cotacao",
  "name": "Vendedores podem criar cotações próprias",
  "description": "Acesso ao módulo de cotação — apenas recursos do próprio usuário",
  "version": "2.0",
  "tenant_id": "tenant-empresa-abc",
  "scope": "tenant",
  "subject_id": null,
  "inherits": ["pol-base-global"],
  "effect": "allow",
  "priority": 10,
  "actions": ["cotacao:create", "cotacao:read"],
  "resources": ["empresa/*/cotacao/*"],
  "conditions": [
    {"field": "resource.owner_id", "op": "eq",      "value": "{{subject_id}}"},
    {"field": "user_level",        "op": "gte",      "value": 3},
    {"field": "roles",             "op": "contains", "value": "vendedor"}
  ],
  "condition_logic": "AND",
  "enabled": true
}
```

### YAML
```yaml
id: pol-vendedor-cotacao
name: Vendedores podem criar cotações próprias
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
  - empresa/*/cotacao/*
conditions:
  - field: resource.owner_id
    op: eq
    value: "{{subject_id}}"
  - field: user_level
    op: gte
    value: 3
condition_logic: AND
enabled: true
```

---

## ① Variáveis Dinâmicas (Templating)

Qualquer `value` em uma condição pode conter `{{variável}}`.  
A variável é resolvida em **tempo de avaliação** a partir do contexto.

### Variáveis disponíveis

| Template | Resolve para |
|---|---|
| `{{subject_id}}` | ID do sujeito (`ctx.subject_id`) |
| `{{tenant_id}}` | Tenant do contexto (`ctx.tenant_id`) |
| `{{action}}` | Ação solicitada (`ctx.action`) |
| `{{resource}}` | Recurso alvo (`ctx.resource`) |
| `{{subject.X}}` | Campo `X` do dict `subject` |
| `{{extra.X}}` | Campo `X` do dict `extra` |

### Exemplos

```json
// Usuário só acessa seus próprios recursos
{"field": "resource.owner_id", "op": "eq", "value": "{{subject_id}}"}

// Recurso deve pertencer ao tenant do contexto
{"field": "resource.tenant", "op": "eq", "value": "{{tenant_id}}"}

// Email do subject deve terminar com domínio do tenant
{"field": "email", "op": "ends_with", "value": "{{subject.domain}}"}

// Interpolação parcial em string
{"field": "resource", "op": "starts_with", "value": "empresa/{{subject.company_id}}/"}
```

### Como funciona

```
Condição: {"field": "owner_id", "op": "eq", "value": "{{subject_id}}"}
Contexto: subject_id = "user-abc-123"

→ value resolvido: "user-abc-123"
→ avalia: ctx.get("owner_id") == "user-abc-123"
```

---

## ② Hierarquia de Recursos

Recursos podem ser caminhos hierárquicos com múltiplos níveis.  
O match é feito em **qualquer segmento ancestral** do caminho.

### Formato
```
empresa/{id}/departamento/{id}/cotacao/{id}
```

### Como o match funciona

```
Pattern: "empresa/*/cotacao/*"
Recurso: "empresa/123/departamento/5/cotacao/9"

Segmentos testados:
  "empresa/123"                          → não bate
  "empresa/123/departamento"             → não bate
  "empresa/123/departamento/5"           → não bate
  "empresa/123/departamento/5/cotacao"   → não bate
  "empresa/123/departamento/5/cotacao/9" → não bate (direto)
  tail "empresa/123/cotacao/9"           → BATE ✓ (sufixo)
```

### Exemplos de patterns

| Pattern | Bate em |
|---|---|
| `cotacao/*` | `cotacao/123`, `empresa/abc/cotacao/123` |
| `empresa/*/cotacao/*` | `empresa/123/cotacao/9`, `empresa/abc/cotacao/xyz` |
| `empresa/123/*` | Qualquer recurso dentro de `empresa/123` |
| `*/relatorio/*` | Qualquer relatorio em qualquer empresa |
| `*` | Tudo |

---

## ③ Policy Composition (Herança e Override)

### Scopes

| Scope | Descrição | Prioridade |
|---|---|---|
| `global` | Aplica a todos os tenants | Menor (base) |
| `tenant` | Aplica a um tenant específico | Média |
| `user` | Aplica a um `subject_id` específico | Maior (override) |

### Cascata de avaliação

```
╔══════════════════════════════════════════════════════╗
║  scope=global  (base — vale para todos)              ║
║       ↓ tenant pode sobrescrever                     ║
║  scope=tenant  (regras do tenant)                    ║
║       ↓ user pode sobrescrever                       ║
║  scope=user    (regras individuais — override máximo)║
╚══════════════════════════════════════════════════════╝

Deny explícito em QUALQUER scope → nega imediatamente.
Allow mais específico (user > tenant > global) vence.
```

### Herança de condições (`inherits`)

```json
// Policy base global
{
  "id": "pol-base-global",
  "scope": "global",
  "effect": "allow",
  "actions": ["*"],
  "resources": ["*"],
  "conditions": [
    {"field": "is_active", "op": "eq", "value": true},
    {"field": "blocked",   "op": "not_exists"}
  ]
}

// Policy de tenant herda a base e adiciona condição própria
{
  "id": "pol-tenant-vendedor",
  "scope": "tenant",
  "tenant_id": "tenant-abc",
  "inherits": ["pol-base-global"],
  "effect": "allow",
  "actions": ["cotacao:*"],
  "resources": ["cotacao/*"],
  "conditions": [
    {"field": "roles", "op": "contains", "value": "vendedor"}
    // is_active e blocked herdados do pai
    // se redefinir "is_active" aqui, sobrescreve o pai
  ]
}

// Policy de usuário específico — override máximo
{
  "id": "pol-user-joao",
  "scope": "user",
  "subject_id": "user-joao-123",
  "tenant_id": "tenant-abc",
  "inherits": ["pol-tenant-vendedor"],
  "effect": "allow",
  "actions": ["cotacao:*", "relatorio:read"],
  "resources": ["*"],
  "conditions": []  // sem condições extras — herda tudo do pai
}
```

### Regras de merge de condições

1. Condições do pai são herdadas
2. Se o filho define a mesma `field`, **sobrescreve** a do pai
3. Campos não redefinidos são **mantidos** do pai
4. Ciclos de herança são detectados e ignorados

---

## Campos da Policy v2

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string | UUID gerado automaticamente se omitido |
| `name` | string | Nome descritivo |
| `description` | string | Descrição detalhada |
| `version` | string | Versão (default: "2.0") |
| `tenant_id` | string\|null | Tenant; `null` = global |
| `scope` | enum | `global` \| `tenant` \| `user` |
| `subject_id` | string\|null | Para `scope=user`: ID do sujeito |
| `inherits` | list[string] | IDs de policies pai |
| `effect` | enum | `allow` \| `deny` |
| `priority` | int | Menor = maior prioridade (default: 100) |
| `actions` | list[string] | Ações (glob: `*`, `cotacao:*`) |
| `resources` | list[string] | Recursos (hierárquico + glob) |
| `conditions` | list[Condition] | Condições (suportam `{{template}}`) |
| `condition_logic` | enum | `AND` (default) \| `OR` |
| `enabled` | bool | Ativa/desativa (default: true) |

---

## Os 14 Operadores

| Op | Descrição |
|---|---|
| `eq` | Igual (com coerção de tipo) |
| `neq` | Diferente |
| `gt` | Maior que (numérico) |
| `gte` | Maior ou igual |
| `lt` | Menor que |
| `lte` | Menor ou igual |
| `in` | Está na lista |
| `not_in` | Não está na lista |
| `contains` | Contém (lista ou substring) |
| `not_contains` | Não contém |
| `starts_with` | Começa com |
| `ends_with` | Termina com |
| `regex` | Expressão regular (re.match) |
| `exists` | Campo não é nulo |
| `not_exists` | Campo é nulo |

---

## API

### Criar policy
```bash
POST /admin/policies/
# campos novos: scope, subject_id, inherits
```

### Avaliar (com templating + hierarquia)
```bash
POST /admin/policies/evaluate
{
  "subject": {
    "owner_id": "user-abc",
    "roles": ["vendedor"],
    "user_level": 3
  },
  "action": "cotacao:create",
  "resource": "empresa/123/cotacao/456",
  "tenant_id": "tenant-abc",
  "subject_id": "user-abc",
  "use_cache": true
}
```

**Response:**
```json
{
  "allowed": true,
  "effect": "allow",
  "matched_policy": "pol-vendedor-cotacao",
  "reason": "Permitido pela policy '...' (scope=tenant).",
  "composition_chain": ["pol-base-global", "pol-vendedor-cotacao"]
}
```

### Explain (debug/audit)
```bash
POST /admin/policies/explain
# mesmo payload do evaluate
```

**Response:**
```json
{
  "result": {
    "allowed": true,
    "matched_policy": "pol-vendedor-cotacao",
    "chain": ["pol-base-global", "pol-vendedor-cotacao"]
  },
  "context": {
    "action": "cotacao:create",
    "resource": "empresa/123/cotacao/456",
    "subject_id": "user-abc"
  },
  "steps": [
    {
      "policy": "pol-base-global",
      "scope": "global",
      "action_ok": true,
      "resource_ok": true,
      "cond_ok": true,
      "applicable": true,
      "conditions": [
        {
          "field": "is_active",
          "op": "eq",
          "value": true,
          "resolved": true,
          "actual": true,
          "result": true
        }
      ]
    }
  ]
}
```

### Listar por scope
```bash
GET /admin/policies/?scope=global
GET /admin/policies/?scope=tenant&tenant_id=tenant-abc
GET /admin/policies/?scope=user
```

---

## Cache de Decisão

```
Chave:    SHA-256(tenant_id:subject_id:action:resource)
TTL:      60s (padrão) | configurável por policy_id
Eviction: LRU (8192 entradas)
Thread:   thread-safe via threading.Lock
```

---

*O2 Data Solutions — "O Grimório de Jake tem 3 novos feitiços hardcore!"*

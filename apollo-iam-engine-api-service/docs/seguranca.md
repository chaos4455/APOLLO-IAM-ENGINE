# 🔐 Apollo IAM Engine — Segurança

> *"Marceline guarda os segredos do reino — ninguém passa sem autenticação!"*

**Versão:** 2.0

---

## Modelo de Segurança

### Autenticação
- **JWT HS256** com secret key configurável (32+ chars recomendado)
- Access token: TTL configurável (default 60 min)
- Refresh token: TTL configurável (default 7 dias)
- Token blacklist persistida no banco + cache em memória (TTL 120s)

### Senhas
- **Bcrypt** com salt automático
- Custo computacional intencional (proteção contra brute force)
- Nunca armazenadas em texto plano

### mTLS (Mutual TLS)
```
Habilitado via MTLS_ENABLED=true
Porta: 8443 (API), 8444 (WebApp)
Certificados: certs/ca/, certs/server/, certs/client/
Modos: required | optional | disabled
TLS: 1.2+ | ECDHE+AES-GCM | ECDHE+CHACHA20
Sem: RC4, 3DES, NULL, EXPORT, MD5
```

---

## Rate Limiting

Sliding window por IP:

| Rota | Limite | Janela |
|---|---|---|
| `/auth/token` | 10 req | 60s |
| `/auth/refresh` | 20 req | 60s |
| `/auth/check` | 60 req | 60s |
| `/auth/*` | 30 req | 60s |
| `/admin/*` | 120 req | 60s |
| Global | 200 req | 60s |

IPs na whitelist (`127.0.0.1`, `::1`) nunca são limitados.

---

## Security Headers

Aplicados via `SecurityHeadersMiddleware`:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (quando HTTPS)
- `Content-Security-Policy`

---

## Apollo Policy Language (APL) — Segurança

- **Deny explícito sempre vence** Allow (independente de prioridade)
- **Default deny** — sem policy aplicável = negado
- Apenas superusuários podem criar/remover/toggle policies
- Policies isoladas por `tenant_id` — sem vazamento entre tenants
- Cache de decisão com chave SHA-256 — sem colisão entre tenants/subjects

---

## Audit Log

Todas as ações são registradas no `EventLogger`:
- Auth: login (sucesso/falha), logout, refresh, validate, check
- Policy: criação, remoção, toggle, avaliação, reload, cache hit
- Users: criação, atualização, remoção, toggle status, reset senha
- Roles/Permissions: criação, remoção, assign, revoke
- Groups, RBAC attributes, Custom entities
- Settings: leitura e atualização

Campos: `uid`, `hash` (SHA-256 de integridade), `timestamp`, `event`,  
`actor`, `resource`, `resource_id`, `tenant_id`, `session_id`,  
`status`, `duration_ms`, `tags`, `detail`.

Saídas: JSON (NDJSON), YAML, Markdown, SQLite.

---

## Controle de Acesso

### Superusuário
- Bypass em todas as verificações RBAC/ABAC
- Único que pode gerenciar policies APL
- Criado via seed na inicialização

### Permissões Granulares
Formato: `{resource}:{action}`  
Exemplos: `cotacao:create`, `relatorio:read`, `admin:*`

### Policy DSL (APL)
- Deny explícito sempre vence Allow
- Default deny (sem policy = negado)
- Condições compostas AND/OR com 14 operadores
- Resource-level com glob patterns

---

## Recomendações de Produção

1. Trocar `SECRET_KEY` por valor aleatório de 32+ chars
2. Habilitar mTLS para comunicação entre serviços
3. Migrar para PostgreSQL (SQLite não escala para produção)
4. Usar Redis para cache distribuído em múltiplas instâncias
5. Configurar HTTPS com certificado válido (não auto-assinado)
6. Revisar `RATE_LIMIT_RULES` conforme carga esperada
7. Monitorar audit logs para detecção de anomalias
8. Rotacionar `SECRET_KEY` periodicamente (invalida todos os tokens)
9. Definir policies APL de deny explícito para casos críticos
10. Usar `tenant_id` em todas as policies para isolamento correto

---

*O2 Data Solutions — "Marceline não deixa ninguém passar sem token válido!"*

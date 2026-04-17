# Apollo IAM Engine — Seguranca

**Versao:** 1.0.0  
**Autor:** Elias Andrade — O2 Data Solutions

---

## Modelo de Seguranca

### Autenticacao

**JWT HS256**
- Secret key configuravel via `SECRET_KEY` (minimo 32 chars recomendado)
- Access token: TTL configuravel (default 60 min, ajustavel via `/admin/settings/`)
- Refresh token: TTL configuravel (default 7 dias)
- Payload inclui: `sub`, `user_id`, `is_superuser`, `roles`, `permissions`, `group`, `user_type`, `user_level`, `user_level_rank`, `rbac`, `abac`, `exp`, `iat`, `jti`

**Token Blacklist**
- Revogacao persistida na tabela `token_blacklist` (SQLite)
- Cache L1 em memoria: `blacklist_cache` (TTL 3600s para revogados, 30s para nao-revogados)
- Verificacao: L1 primeiro → L2 (banco) apenas em cache miss
- Indice: `ix_token_blacklist_jti` — lookup O(log n)

**Fluxo de verificacao por request:**
```
Authorization: Bearer <token>
        |
        v
JwtTokenService.decode_token(token)
        |
        +-- token_cache.get(sha256(token)[:32])   [L1, TTL 30s]
        |    HIT  -> retorna TokenPayload (< 0.1ms)
        |    MISS -> continua
        |
        +-- jwt.decode(token, secret_key)
        |
        +-- blacklist_cache.get(jti)              [L1, TTL 120s]
        |    HIT  -> retorna bool
        |    MISS -> SELECT FROM token_blacklist WHERE jti = ?
        |
        +-- token_cache.set(key, payload, ttl)
        |
        v
    TokenPayload
```

---

### Senhas

- **Bcrypt** com salt automatico por entrada
- Custo computacional alto intencional — protecao contra brute force e rainbow tables
- Nunca armazenadas em texto plano
- Reset de senha via `POST /admin/users/{id}/reset-password` (superuser only)

---

### mTLS (Mutual TLS)

```
Habilitado via: MTLS_ENABLED=true
Portas:         8443 (API), 8444 (WebApp)
Certificados:   certs/ca/, certs/server/, certs/client/

Configuracao TLS:
  Versao minima:  TLS 1.2
  Cipher suites:  ECDHE+AES-GCM, ECDHE+CHACHA20
  Desabilitados:  RC4, 3DES, NULL, EXPORT, MD5, SSLv2, SSLv3

Modos:
  required  — cliente DEVE apresentar certificado valido
  optional  — certificado aceito mas nao obrigatorio
  disabled  — TLS sem verificacao de cliente

Certificados incluidos (auto-assinados para desenvolvimento):
  certs/ca/ca.crt          — CA raiz
  certs/server/server.crt  — certificado do servidor
  certs/client/client.crt  — certificado do cliente
  certs/client/client.p12  — bundle PKCS#12 para importacao
```

---

## Rate Limiting

Sliding window por IP. IPs na whitelist (`127.0.0.1`, `::1`) nunca sao limitados.

| Rota | Limite | Janela |
|---|---|---|
| `/auth/token` | 10 req | 60s |
| `/auth/refresh` | 20 req | 60s |
| `/auth/check` | 60 req | 60s |
| `/auth/*` | 30 req | 60s |
| `/admin/*` | 120 req | 60s |
| Global | 200 req | 60s |

**Response 429:**
```json
{"detail": "Rate limit excedido. Tente novamente em 60s."}
```

---

## Security Headers

Aplicados via `SecurityHeadersMiddleware` em todas as respostas:

| Header | Valor |
|---|---|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `X-XSS-Protection` | `1; mode=block` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` (HTTPS) |
| `Content-Security-Policy` | `default-src 'self'` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |

---

## Backpressure

`RequestQueueMiddleware` protege contra sobrecarga:

- Fila de 100 requisicoes simultaneas
- Timeout de 30s por requisicao na fila
- Retorna `503 Service Unavailable` se fila cheia
- Evita que o processo seja derrubado por pico de carga

---

## Apollo Policy Language (APL) — Seguranca

| Regra | Descricao |
|---|---|
| Deny explicito sempre vence | Independente de prioridade — deny e final |
| Default deny | Sem policy aplicavel = acesso negado |
| Superuser only | Apenas superusuarios podem criar/remover/toggle policies |
| Isolamento por tenant | Policies de tenant A nao afetam tenant B |
| Cache isolado | Chave SHA-256 inclui tenant_id — sem vazamento entre tenants |
| Audit trail | Toda decisao e registrada na tabela `decision_audit` |

---

## Controle de Acesso

### Superusuario
- Flag `is_superuser=true` no JWT
- Bypass em todas as verificacoes RBAC/ABAC
- Unico que pode gerenciar policies APL, usuarios, roles, permissoes
- Criado via seed na inicializacao (`ADMIN_USERNAME`, `ADMIN_PASSWORD`)

### Permissoes Granulares
Formato: `{resource}:{action}`

Exemplos:
```
cotacao:create    cotacao:read    cotacao:update    cotacao:delete
relatorio:read    relatorio:export
admin:*           users:*
```

### Dependencies FastAPI

```python
# Exige usuario autenticado
get_current_user

# Exige superuser
require_superuser

# Exige pelo menos uma das roles
require_role("vendedor", "gerente")

# Exige pelo menos uma das permissoes
require_permission("cotacao:create")

# Exige nivel minimo
require_level(min_rank=3)

# Exige atributos ABAC
require_abac(department="sales", region="sul")

# Combinado RBAC + ABAC
require_rbac_and_abac(
    roles=["vendedor"],
    permissions=["cotacao:create"],
    abac_conditions={"department": "sales"},
    min_level=2
)
```

---

## Audit Log

Todas as acoes sao registradas no `EventLogger` com os campos:

| Campo | Descricao |
|---|---|
| `uid` | UUID unico da entrada |
| `hash` | SHA-256 do conteudo (integridade) |
| `seq` | Sequencia autoincrement |
| `timestamp` | ISO 8601 UTC |
| `event` | Tipo do evento (ex: `auth.login_success`) |
| `actor` | Quem executou a acao |
| `resource` | Recurso afetado |
| `resource_id` | ID do recurso |
| `tenant_id` | Tenant (se aplicavel) |
| `session_id` | Sessao (se aplicavel) |
| `status` | `success` \| `failure` |
| `duration_ms` | Duracao da operacao |
| `tags` | Tags adicionais (JSON) |
| `detail` | Detalhes adicionais (JSON) |

### Eventos registrados

| Dominio | Eventos |
|---|---|
| Auth | `auth.login_success`, `auth.login_failure`, `auth.logout`, `auth.refresh`, `auth.validate`, `auth.check` |
| Policy | `policy.created`, `policy.deleted`, `policy.toggled`, `policy.evaluated`, `policy.reloaded`, `policy.cache_hit` |
| Users | `user.created`, `user.updated`, `user.deleted`, `user.toggle_status`, `user.reset_password` |
| Roles | `role.created`, `role.deleted`, `role.assigned`, `role.revoked` |
| Permissions | `permission.created`, `permission.deleted`, `permission.assigned` |
| Groups | `group.created`, `group.deleted`, `group.user_assigned` |
| RBAC | `rbac.attr_created`, `rbac.attr_deleted`, `rbac.attr_assigned` |
| Entities | `entity.type_created`, `entity.value_created`, `entity.assigned`, `entity.unassigned` |
| Settings | `settings.read`, `settings.updated` |
| System | `system.startup`, `system.shutdown` |

---

## Recomendacoes de Producao

1. **SECRET_KEY**: gerar valor aleatorio de 32+ chars (`openssl rand -hex 32`)
2. **mTLS**: habilitar para comunicacao entre microsservicos (`MTLS_ENABLED=true`)
3. **Banco**: migrar para PostgreSQL (SQLite nao escala para producao com alta concorrencia)
4. **Cache**: usar Redis para cache distribuido em multiplas instancias
5. **HTTPS**: certificado valido (nao auto-assinado) para endpoints publicos
6. **Rate limiting**: ajustar `RATE_LIMIT_RULES` conforme carga esperada
7. **Audit logs**: monitorar `event_log` para deteccao de anomalias
8. **SECRET_KEY rotation**: rotacionar periodicamente (invalida todos os tokens ativos)
9. **Policies deny**: definir policies de deny explicito para casos criticos
10. **tenant_id**: usar em todas as policies para garantir isolamento correto
11. **Backup**: fazer backup periodico de `apollo_iam.db` e `apollo_log.db`
12. **Logs**: configurar retencao e rotacao dos arquivos em `logs/`

---

*Elias Andrade — O2 Data Solutions*

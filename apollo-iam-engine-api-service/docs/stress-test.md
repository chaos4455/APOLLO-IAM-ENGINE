# Apollo IAM Engine — Stress Test & Benchmark

**Arquivo:** `benchmark-stress.py`  
**Versao:** 1.0.0  
**Autor:** Elias Andrade — O2 Data Solutions

---

## Objetivo

Identificar os breaking points do sistema sob carga crescente de requisicoes simultaneas nos endpoints mais criticos:

1. **Login** (`/auth/token`) — maior gargalo (bcrypt + DB write)
2. **Validate** (`/auth/validate`) — JWT decode + blacklist check
3. **Check RBAC+ABAC** (`/auth/check`) — validacao completa
4. **APL Evaluate** (`/admin/policies/evaluate`) — engine declarativa (cache miss)
5. **APL Cache Hit** (`/admin/policies/evaluate` com subject_id fixo) — mede ganho do cache
6. **Cenario Misto** — combinacao de todos os endpoints

---

## Como Executar

```bash
# servidor deve estar rodando
python run-init-api-engine.py

# em outro terminal
python benchmark-stress.py
```

Logs salvos em `benchmark-stress-logs/stress_YYYYMMDD_HHMMSS.[json|yaml|md]`

---

## Metodologia

### Rampa de Carga

```
1 -> 5 -> 10 -> 25 -> 50 -> 100 -> 200 -> 500 req simultaneos
```

Para cada nivel:
- Todas as requisicoes disparadas **simultaneamente** (`asyncio.gather`)
- Breaking point: taxa de erro > **50%** -> rampa para
- Metricas coletadas em tempo real

### Setup Automatico

O script cria automaticamente:
- Usuario de teste dedicado
- Policy APL para stress do engine
- Reload do engine antes dos testes

---

## Metricas Coletadas

| Metrica | Descricao |
|---|---|
| `total` | Total de requisicoes disparadas |
| `ok` | Requisicoes com status 200 |
| `errors` | Requisicoes com erro ou timeout |
| `error_rate` | % de erros |
| `avg_ms` | Latencia media em ms |
| `min_ms` | Latencia minima |
| `max_ms` | Latencia maxima |
| `p50_ms` | Percentil 50 (mediana) |
| `p90_ms` | Percentil 90 |
| `p95_ms` | Percentil 95 |
| `p99_ms` | Percentil 99 |
| `rps` | Requisicoes por segundo |
| `status_dist` | Distribuicao de status HTTP |

---

## Cenarios

### 1. Login (`stress_login`)

Rampa completa 1->500 no endpoint `/auth/token`.

Gargalos:
- **Bcrypt**: custo computacional alto intencional (~200ms por hash)
- **SQLite WAL**: lock contention em escritas simultaneas
- **Rate limiter**: 10 req/min por IP (pode limitar antes do breaking point)

### 2. Validate (`stress_validate`)

Rampa completa no `/auth/validate`.

Caracteristicas:
- JWT decode em memoria (< 1ms com cache L1)
- Blacklist check: cache L1 (TTL 120s) — raramente vai ao banco
- Esperado: breaking point alto (200-500+ req)

### 3. Check RBAC+ABAC (`stress_check`)

Rampa completa no `/auth/check`.

Caracteristicas:
- JWT decode + verificacao de roles/permissions/ABAC
- Tudo em memoria (payload no token)
- Esperado: breaking point medio-alto (100-500 req)

### 4. APL Evaluate — Cache Miss (`stress_apl_evaluate`)

Rampa completa com `subject_id` unico por request (forca cache miss).

Caracteristicas:
- PolicyEngine.evaluate() em memoria
- Filtragem por tenant_id, action, resource, conditions
- Sem I/O de banco (engine carregado em memoria)
- Esperado: breaking point alto (100-500 req)

### 5. APL Cache Hit (`stress_apl_cache`)

Rampa completa com `subject_id` **fixo** — forca cache hit.

Caracteristicas:
- DecisionCache.get() — SHA-256 lookup em OrderedDict
- Retorno em < 1ms
- Esperado: breaking point muito alto (500+ req)
- Mede: speedup do cache vs avaliacao completa

### 6. Misto (`stress_mixed`)

Rampa 10->500 com mix de login + validate + check + APL evaluate.

Simula carga real de producao.  
Gargalo dominante: login (bcrypt).

---

## Gargalos Esperados

| Endpoint | Breaking Point Esperado | Causa Principal |
|---|---|---|
| `/auth/token` | 10-50 req | Bcrypt + SQLite write lock |
| `/auth/validate` | 200-500+ req | JWT decode (cache L1) |
| `/auth/check` | 100-500 req | JWT + RBAC em memoria |
| APL evaluate (miss) | 100-500 req | Engine em memoria |
| APL evaluate (hit) | 500+ req | Cache SHA-256 lookup |
| Misto | 25-100 req | Gargalo do login |

---

## Interpretando os Resultados

### Saida saudavel

```
LOGIN x10
Total: 10 | OK: 10 | Erros: 0 | Erro%: 0%
Avg: 245ms | P50: 230ms | P90: 310ms | P99: 380ms | RPS: 8.2
```

### Breaking point

```
LOGIN x50
Total: 50 | OK: 12 | Erros: 38 | Erro%: 76%  <- BREAK
Avg: 8420ms | P50: 9100ms | P90: 15000ms | P99: 28000ms | RPS: 1.1
BREAKING POINT em 50 req simultaneos (erro 76%)
```

### Causas comuns de falha

| Causa | Sintoma | Solucao |
|---|---|---|
| SQLite lock contention | Erros 500, latencia alta em escritas | Migrar para PostgreSQL |
| Rate limiter | Erros 429 | Ajustar `RATE_LIMIT_RULES` em `config/security.yaml` |
| Request queue cheia | Erros 503 | Ajustar `RequestQueueMiddleware` (max_queue, timeout) |
| Bcrypt saturacao | Login lento, timeout | Reduzir rounds ou usar cache de autenticacao |
| Memoria esgotada | Erros 500, OOM | Aumentar RAM ou reduzir tamanho dos caches |
| Timeout de conexao | Erros de rede | Aumentar `timeout` no engine SQLAlchemy |

---

## Comparativo Cache Miss vs Hit

O script gera automaticamente o comparativo:

```
APL EVALUATE — Cache Miss vs Hit
  Miss (subject_id unico):  avg=2.1ms  p99=8.4ms   rps=142
  Hit  (subject_id fixo):   avg=0.3ms  p99=1.2ms   rps=890
  Speedup: 7.0x (miss/hit)
```

---

## Relatorio Consolidado

Ao final, o script gera:
- Tabela de breaking points por cenario
- Comparativo APL cache miss vs hit (speedup)
- Conclusao automatica
- Arquivos: `.json`, `.yaml`, `.md` em `benchmark-stress-logs/`

---

## Configuracao do Ambiente de Teste

Para resultados mais precisos:

```bash
# desabilitar rate limiting para stress test puro
# editar config/security.yaml: rate_limit_enabled: false

# aumentar request queue
# editar RequestQueueMiddleware: max_queue=500, timeout=60

# usar HTTP (sem overhead TLS)
MTLS_ENABLED=false python run-init-api-engine.py
```

---

*Elias Andrade — O2 Data Solutions*

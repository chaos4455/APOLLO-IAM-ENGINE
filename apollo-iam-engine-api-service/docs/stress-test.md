# ⚔️ Apollo IAM Engine — Stress Test & Benchmark

> *"Finn e Jake enfrentam 500 inimigos simultâneos — quem vai quebrar primeiro?"*

**Arquivo:** `benchmark-stress.py`  
**Versão:** 2.0

---

## Objetivo

Identificar os breaking points do sistema sob carga crescente de requisições simultâneas nos endpoints mais críticos:

1. **Login** (`/auth/token`) — maior gargalo (bcrypt + DB write)
2. **Validate** (`/auth/validate`) — JWT decode + blacklist check
3. **Check RBAC+ABAC** (`/auth/check`) — validação completa
4. **APL Evaluate** (`/admin/policies/evaluate`) — engine declarativa
5. **APL Cache Hit** (`/admin/policies/evaluate` com subject_id fixo) — mede ganho do cache
6. **Cenário Misto** — combinação de todos os endpoints

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
1 → 5 → 10 → 25 → 50 → 100 → 200 → 500 req simultâneos
```

Para cada nível:
- Todas as requisições disparadas **simultaneamente** (`asyncio.gather`)
- Breaking point: taxa de erro > **50%** → rampa para
- Métricas coletadas em tempo real

### Setup Automático
O script cria automaticamente:
- Usuário de teste dedicado
- Policy APL para stress do engine
- Reload do engine antes dos testes

---

## Métricas Coletadas

| Métrica | Descrição |
|---|---|
| `total` | Total de requisições disparadas |
| `ok` | Requisições com status 200 |
| `errors` | Requisições com erro ou timeout |
| `error_rate` | % de erros |
| `avg_ms` | Latência média em ms |
| `min_ms` | Latência mínima |
| `max_ms` | Latência máxima |
| `p50_ms` | Percentil 50 (mediana) |
| `p90_ms` | Percentil 90 |
| `p95_ms` | Percentil 95 |
| `p99_ms` | Percentil 99 |
| `rps` | Requisições por segundo |
| `status_dist` | Distribuição de status HTTP |

---

## Cenários

### 1. Login (`stress_login`)
Rampa completa 1→500 no endpoint `/auth/token`.  
Gargalo: bcrypt (intencional) + DB write.

### 2. Validate (`stress_validate`)
Rampa completa no `/auth/validate`.  
Rápido: JWT decode em memória + blacklist cache.

### 3. Check RBAC+ABAC (`stress_check`)
Rampa completa no `/auth/check`.  
Médio: JWT decode + avaliação de roles/permissions/ABAC.

### 4. APL Evaluate (`stress_apl_evaluate`)
Rampa completa no `/admin/policies/evaluate` com `subject_id` único por request.  
Mede: engine APL sem cache (avaliação completa).

### 5. APL Cache Hit (`stress_apl_cache`)
Rampa completa com `subject_id` **fixo** — força cache hit.  
Mede: ganho do `DecisionCache` vs avaliação completa.

### 6. Misto (`stress_mixed`)
Rampa 10→500 com mix de login + validate + check + APL evaluate.  
Simula carga real de produção.

---

## Gargalos Esperados

| Endpoint | Breaking Point Esperado | Causa Principal |
|---|---|---|
| `/auth/token` | 10–50 req | Bcrypt + SQLite lock |
| `/auth/validate` | 100–500 req | JWT decode (rápido) |
| `/auth/check` | 50–200 req | JWT + avaliação RBAC |
| APL evaluate (miss) | 100–500 req | Engine em memória |
| APL evaluate (hit) | 200–500+ req | Cache SHA-256 |
| Misto | 25–100 req | Gargalo do login |

---

## Interpretando os Resultados

### Saída saudável
```
LOGIN x10
Total: 10 | OK: 10 | Erros: 0 | Erro%: 0%
Avg: 245ms | P50: 230ms | P90: 310ms | P99: 380ms | RPS: 8.2
```

### Breaking point
```
LOGIN x50
Total: 50 | OK: 12 | Erros: 38 | Erro%: 76%  ← BREAK
Avg: 8420ms | P50: 9100ms | P90: 15000ms | P99: 28000ms | RPS: 1.1
⚡ BREAKING POINT em 50 req simultâneos (erro 76%)
```

### Causas comuns
| Causa | Sintoma | Solução |
|---|---|---|
| SQLite lock contention | Erros 500, latência alta | Migrar para PostgreSQL |
| Rate limiter | Erros 429 | Ajustar `RATE_LIMIT_RULES` |
| Request queue cheio | Erros 503 | Ajustar `RequestQueueMiddleware` |
| Bcrypt saturação | Login lento, timeout | Reduzir rounds ou usar cache |
| Memória esgotada | Erros 500 | Aumentar RAM ou reduzir cache |

---

## Relatório Consolidado

Ao final, o script gera:
- Tabela de breaking points por cenário
- Comparativo APL cache miss vs hit (speedup)
- Conclusão automática
- Arquivos: `.json`, `.yaml`, `.md` em `benchmark-stress-logs/`

---

*O2 Data Solutions — "500 inimigos simultâneos? Finn não tem medo!"*

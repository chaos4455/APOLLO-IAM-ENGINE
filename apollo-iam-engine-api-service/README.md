# Apollo IAM Engine API Service

Serviço centralizado de IAM + RBAC para múltiplos micro-serviços.
Criado por **O2 Data Solutions**.

## Início rápido

```bash
pip install -r requirements.txt
python -m uvicorn src.interface.api.main:app --reload --port 8000
python -m uvicorn src.interface.webapp.main:app --reload --port 8080
```

- API Docs: http://localhost:8000/docs
- ReDoc:    http://localhost:8000/redoc
- Admin UI: http://localhost:8080/admin  (admin / admin)

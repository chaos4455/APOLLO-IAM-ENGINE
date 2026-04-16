FROM python:3.11-slim

WORKDIR /app

# dependências do sistema para cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# cria pastas necessárias
RUN mkdir -p data logs/json logs/yaml logs/md certs/ca certs/server certs/client

EXPOSE 8443 8444

# entrypoint padrão — API com mTLS
# os certs são gerados automaticamente no primeiro boot via cert_manager.py
CMD ["python", "run-init-api-engine.py"]

from __future__ import annotations
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Apollo IAM Engine"
    app_version: str = "1.0.0"
    secret_key: str = "change-me-super-secret-key-32chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    database_url: str = "sqlite:///./data/apollo_iam.db"
    log_level: str = "INFO"
    admin_username: str = "admin"
    admin_password: str = "admin"
    cors_origins: str = "*"

    # ── mTLS ──────────────────────────────────────────────────
    mtls_enabled: bool = True
    mtls_certs_dir: str = "certs"
    mtls_api_port: int = 8443
    mtls_webapp_port: int = 8444
    # "required" | "optional" | "disabled"
    mtls_client_auth: str = "required"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()

"""
token_blacklist.py
Blacklist de tokens JWT com cache em memória (L1) + SQLite (L2).
- is_revoked: verifica L1 primeiro, só vai ao DB se cache miss
- revoke: escreve no DB e atualiza L1 imediatamente
O2 Data Solutions
"""
from __future__ import annotations
from sqlalchemy.orm import Session
from src.infrastructure.database.models.token_blacklist_model import TokenBlacklistModel
from src.infrastructure.cache.memory_cache import blacklist_cache

_NOT_REVOKED = object()  # sentinel para distinguir "não revogado" de cache miss


class SqliteTokenBlacklist:
    def __init__(self, db: Session):
        self.db = db

    def revoke(self, jti: str) -> None:
        entry = TokenBlacklistModel(jti=jti)
        self.db.merge(entry)
        self.db.commit()
        # atualiza cache imediatamente — TTL longo pois tokens revogados não mudam
        blacklist_cache.set(jti, True, ttl=3600.0)

    def is_revoked(self, jti: str) -> bool:
        # L1: cache em memória
        cached = blacklist_cache.get(jti)
        if cached is True:
            return True
        if cached is False:
            return False

        # L2: banco de dados
        revoked = self.db.query(TokenBlacklistModel).filter_by(jti=jti).first() is not None
        # armazena resultado no cache (False = não revogado, TTL curto)
        blacklist_cache.set(jti, revoked, ttl=120.0 if revoked else 30.0)
        return revoked

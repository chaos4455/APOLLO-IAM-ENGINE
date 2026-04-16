from sqlalchemy.orm import Session
from src.infrastructure.database.models.token_blacklist_model import TokenBlacklistModel


class SqliteTokenBlacklist:
    def __init__(self, db: Session):
        self.db = db

    def revoke(self, jti: str) -> None:
        entry = TokenBlacklistModel(jti=jti)
        self.db.merge(entry)
        self.db.commit()

    def is_revoked(self, jti: str) -> bool:
        return self.db.query(TokenBlacklistModel).filter_by(jti=jti).first() is not None

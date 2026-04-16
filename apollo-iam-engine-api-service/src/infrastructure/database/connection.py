from __future__ import annotations
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.infrastructure.config.settings import get_settings
from src.infrastructure.database.base import Base

settings = get_settings()

# garante que o diretorio data/ existe antes de criar o engine
_db_url = settings.database_url
if _db_url.startswith("sqlite:///"):
    _db_file = _db_url.replace("sqlite:///", "")
    _db_dir = os.path.dirname(os.path.abspath(_db_file))
    os.makedirs(_db_dir, exist_ok=True)

engine = create_engine(
    _db_url,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from src.infrastructure.database.models import (  # noqa: F401
        user_model, role_model, permission_model, group_model,
        user_type_model, user_level_model, rbac_attribute_model,
        settings_model, audit_log_model, token_blacklist_model,
    )
    from src.infrastructure.database.models import custom_entity_model  # noqa: F401
    Base.metadata.create_all(bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

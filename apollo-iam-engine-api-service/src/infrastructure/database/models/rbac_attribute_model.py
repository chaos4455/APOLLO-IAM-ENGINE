from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class RbacAttributeModel(Base):
    __tablename__ = "rbac_attributes"
    id = Column(String, primary_key=True)
    key = Column(String, unique=True, nullable=False, index=True)
    label = Column(String, nullable=False)
    value_type = Column(String, default="string")
    description = Column(String, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

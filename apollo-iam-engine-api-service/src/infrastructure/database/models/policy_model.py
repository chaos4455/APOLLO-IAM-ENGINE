"""
policy_model.py
Modelo SQLAlchemy para persistência de policies Apollo DSL.
O2 Data Solutions
"""
from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base


class PolicyModel(Base):
    __tablename__ = "policies"

    id          = Column(String, primary_key=True)
    name        = Column(String, nullable=False, index=True)
    description = Column(String, default="")
    version     = Column(String, default="2.0")
    tenant_id   = Column(String, nullable=True, index=True)
    effect      = Column(String, nullable=False, default="allow")   # allow | deny
    priority    = Column(Integer, default=100)
    actions     = Column(Text, nullable=False, default="[]")        # JSON list
    resources   = Column(Text, nullable=False, default='["*"]')     # JSON list
    conditions  = Column(Text, nullable=False, default="[]")        # JSON list
    condition_logic = Column(String, default="AND")
    enabled     = Column(Boolean, default=True)
    # v2: composition
    scope       = Column(String, default="tenant")                  # global|tenant|user
    subject_id  = Column(String, nullable=True, index=True)         # scope=user
    inherits    = Column(Text, nullable=False, default="[]")        # JSON list de IDs
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_policy_dict(self) -> dict:
        return {
            "id":              self.id,
            "name":            self.name,
            "description":     self.description,
            "version":         self.version,
            "tenant_id":       self.tenant_id,
            "effect":          self.effect,
            "priority":        self.priority,
            "actions":         json.loads(self.actions),
            "resources":       json.loads(self.resources),
            "conditions":      json.loads(self.conditions),
            "condition_logic": self.condition_logic,
            "enabled":         self.enabled,
            "scope":           self.scope or "tenant",
            "subject_id":      self.subject_id,
            "inherits":        json.loads(self.inherits) if self.inherits else [],
        }

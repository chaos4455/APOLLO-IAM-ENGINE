"""
policy_model.py
Modelo SQLAlchemy para persistência de policies Apollo DSL.
O2 Data Solutions
"""
from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String, Text
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base


class PolicyModel(Base):
    __tablename__ = "policies"
    __table_args__ = (
        Index("ix_policies_tenant_enabled_prio", "tenant_id", "enabled", "priority"),
        Index("ix_policies_scope_enabled", "scope", "enabled"),
    )

    id          = Column(String, primary_key=True)
    name        = Column(String, nullable=False, index=True)
    description = Column(String, default="")
    version     = Column(String, default="2.0")
    tenant_id   = Column(String, nullable=True, index=True)
    effect      = Column(String, nullable=False, default="allow")
    priority    = Column(Integer, default=100)
    actions     = Column(Text, nullable=False, default="[]")
    resources   = Column(Text, nullable=False, default='["*"]')
    conditions  = Column(Text, nullable=False, default="[]")
    condition_logic = Column(String, default="AND")
    enabled     = Column(Boolean, default=True, index=True)
    scope       = Column(String, default="tenant")
    subject_id  = Column(String, nullable=True, index=True)
    inherits    = Column(Text, nullable=False, default="[]")
    # v3: time-based + schema + weight
    valid_from      = Column(String, nullable=True)
    valid_until     = Column(String, nullable=True)
    time_window     = Column(String, nullable=True)
    context_schema  = Column(Text, nullable=True, default="{}")
    weight          = Column(Integer, default=0)
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
            "valid_from":      self.valid_from,
            "valid_until":     self.valid_until,
            "time_window":     self.time_window,
            "context_schema":  json.loads(self.context_schema) if self.context_schema else {},
            "weight":          self.weight or 0,
        }

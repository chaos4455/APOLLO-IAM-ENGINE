"""
custom_entities.py
Sistema genérico de entidades customizadas.

Fluxo:
  1. Crie um tipo:  POST /admin/custom-entities/types   {"slug":"cargo","label":"Cargo"}
  2. Crie valores:  POST /admin/custom-entities/cargo/values  {"name":"Analista"}
  3. Atribua:       POST /admin/custom-entities/assign/{user_id}  {"entity_type_slug":"cargo","entity_value_id":"..."}
  4. Liste:         GET  /admin/custom-entities/types
                    GET  /admin/custom-entities/{slug}/values
                    GET  /admin/custom-entities/user/{user_id}
"""
from __future__ import annotations
import uuid
import json
from typing import Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.models.custom_entity_model import (
    CustomEntityTypeModel, CustomEntityValueModel, UserCustomEntityModel
)
from src.interface.api.dependencies import require_superuser
from src.infrastructure.logging import log_hooks as lh
from src.infrastructure.cache.memory_cache import invalidate_user

router = APIRouter(prefix="/admin/custom-entities", tags=["Admin — Custom Entities"])


# ── schemas ───────────────────────────────────────────────────────────────────

class EntityTypeCreate(BaseModel):
    slug: str           # identificador único, ex: "cargo", "setor", "contrato"
    label: str          # nome legível, ex: "Cargo", "Setor"
    description: str = ""


class EntityTypeUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class EntityTypeResponse(BaseModel):
    id: str
    slug: str
    label: str
    description: str
    is_active: bool
    created_at: str


class EntityValueCreate(BaseModel):
    name: str
    description: str = ""
    metadata: dict[str, Any] = {}   # dados extras livres


class EntityValueUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None


class EntityValueResponse(BaseModel):
    id: str
    entity_type_slug: str
    name: str
    description: str
    metadata: dict
    is_active: bool
    created_at: str


class AssignEntityRequest(BaseModel):
    entity_type_slug: str
    entity_value_id: str


class UserEntityResponse(BaseModel):
    entity_type_slug: str
    entity_value_id: str
    entity_value_name: str
    assigned_at: str


# ── helpers ───────────────────────────────────────────────────────────────────

def _type_out(m: CustomEntityTypeModel) -> dict:
    return {"id": m.id, "slug": m.slug, "label": m.label,
            "description": m.description, "is_active": m.is_active,
            "created_at": str(m.created_at)}


def _val_out(m: CustomEntityValueModel) -> dict:
    try:
        meta = json.loads(m.metadata_json or "{}")
    except Exception:
        meta = {}
    return {"id": m.id, "entity_type_slug": m.entity_type_slug, "name": m.name,
            "description": m.description, "metadata": meta,
            "is_active": m.is_active, "created_at": str(m.created_at)}


def _get_type_or_404(slug: str, db: Session) -> CustomEntityTypeModel:
    m = db.query(CustomEntityTypeModel).filter_by(slug=slug).first()
    if not m:
        raise HTTPException(status_code=404, detail=f"Tipo '{slug}' não encontrado.")
    return m


# ── tipos ─────────────────────────────────────────────────────────────────────

@router.get("/types", response_model=list[EntityTypeResponse])
def list_types(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [_type_out(r) for r in
            db.query(CustomEntityTypeModel).order_by(CustomEntityTypeModel.slug).all()]


@router.post("/types", response_model=EntityTypeResponse, status_code=201)
def create_type(body: EntityTypeCreate, db: Session = Depends(get_db),
                actor=Depends(require_superuser)):
    if db.query(CustomEntityTypeModel).filter_by(slug=body.slug).first():
        raise HTTPException(status_code=409, detail=f"Tipo '{body.slug}' já existe.")
    m = CustomEntityTypeModel(id=str(uuid.uuid4()), slug=body.slug,
                               label=body.label, description=body.description)
    db.add(m)
    db.commit()
    db.refresh(m)
    lh.log_entity_type_created(actor=getattr(actor, "sub", "admin"), entity_id=m.id, slug=m.slug)
    return _type_out(m)


@router.get("/types/{slug}", response_model=EntityTypeResponse)
def get_type(slug: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    return _type_out(_get_type_or_404(slug, db))


@router.put("/types/{slug}", response_model=EntityTypeResponse)
def update_type(slug: str, body: EntityTypeUpdate, db: Session = Depends(get_db),
                actor=Depends(require_superuser)):
    m = _get_type_or_404(slug, db)
    if body.label is not None:
        m.label = body.label
    if body.description is not None:
        m.description = body.description
    if body.is_active is not None:
        m.is_active = body.is_active
    db.commit()
    db.refresh(m)
    lh.log_entity_type_updated(actor=getattr(actor, "sub", "admin"), slug=slug)
    return _type_out(m)


@router.delete("/types/{slug}", status_code=204)
def delete_type(slug: str, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    m = _get_type_or_404(slug, db)
    db.delete(m)
    db.commit()
    lh.log_entity_type_deleted(actor=getattr(actor, "sub", "admin"), slug=slug)


# ── valores ───────────────────────────────────────────────────────────────────

@router.get("/{slug}/values", response_model=list[EntityValueResponse])
def list_values(slug: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    _get_type_or_404(slug, db)
    rows = db.query(CustomEntityValueModel).filter_by(entity_type_slug=slug)\
              .order_by(CustomEntityValueModel.name).all()
    return [_val_out(r) for r in rows]


@router.post("/{slug}/values", response_model=EntityValueResponse, status_code=201)
def create_value(slug: str, body: EntityValueCreate, db: Session = Depends(get_db),
                 actor=Depends(require_superuser)):
    _get_type_or_404(slug, db)
    if db.query(CustomEntityValueModel).filter_by(
            entity_type_slug=slug, name=body.name).first():
        raise HTTPException(status_code=409,
                            detail=f"Valor '{body.name}' já existe em '{slug}'.")
    m = CustomEntityValueModel(
        id=str(uuid.uuid4()), entity_type_slug=slug,
        name=body.name, description=body.description,
        metadata_json=json.dumps(body.metadata, ensure_ascii=False),
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    lh.log_entity_value_created(actor=getattr(actor, "sub", "admin"),
                                  value_id=m.id, slug=slug, name=m.name)
    return _val_out(m)


@router.get("/{slug}/values/{value_id}", response_model=EntityValueResponse)
def get_value(slug: str, value_id: str, db: Session = Depends(get_db),
              _=Depends(require_superuser)):
    m = db.query(CustomEntityValueModel).filter_by(
        id=value_id, entity_type_slug=slug).first()
    if not m:
        raise HTTPException(status_code=404, detail="Valor não encontrado.")
    return _val_out(m)


@router.put("/{slug}/values/{value_id}", response_model=EntityValueResponse)
def update_value(slug: str, value_id: str, body: EntityValueUpdate,
                 db: Session = Depends(get_db), _=Depends(require_superuser)):
    m = db.query(CustomEntityValueModel).filter_by(
        id=value_id, entity_type_slug=slug).first()
    if not m:
        raise HTTPException(status_code=404, detail="Valor não encontrado.")
    if body.name is not None:
        m.name = body.name
    if body.description is not None:
        m.description = body.description
    if body.metadata is not None:
        m.metadata_json = json.dumps(body.metadata, ensure_ascii=False)
    if body.is_active is not None:
        m.is_active = body.is_active
    db.commit()
    db.refresh(m)
    return _val_out(m)


@router.delete("/{slug}/values/{value_id}", status_code=204)
def delete_value(slug: str, value_id: str, db: Session = Depends(get_db),
                 _=Depends(require_superuser)):
    m = db.query(CustomEntityValueModel).filter_by(
        id=value_id, entity_type_slug=slug).first()
    if not m:
        raise HTTPException(status_code=404, detail="Valor não encontrado.")
    db.delete(m)
    db.commit()


# ── atribuição a usuários ─────────────────────────────────────────────────────

@router.post("/assign/{user_id}", status_code=200)
def assign_to_user(user_id: str, body: AssignEntityRequest,
                   db: Session = Depends(get_db), actor=Depends(require_superuser)):
    # valida que o valor existe
    val = db.query(CustomEntityValueModel).filter_by(
        id=body.entity_value_id, entity_type_slug=body.entity_type_slug).first()
    if not val:
        raise HTTPException(status_code=404, detail="Valor de entidade não encontrado.")

    # upsert — um usuário tem no máximo 1 valor por tipo
    existing = db.query(UserCustomEntityModel).filter_by(
        user_id=user_id, entity_type_slug=body.entity_type_slug).first()
    if existing:
        existing.entity_value_id = body.entity_value_id
    else:
        db.add(UserCustomEntityModel(
            id=str(uuid.uuid4()), user_id=user_id,
            entity_type_slug=body.entity_type_slug,
            entity_value_id=body.entity_value_id,
        ))
    db.commit()
    lh.log_entity_assigned_to_user(actor=getattr(actor, "sub", "admin"),
                                    user_id=user_id, slug=body.entity_type_slug,
                                    value_name=val.name)
    invalidate_user(user_id)
    return {"message": f"Entidade '{body.entity_type_slug}' atribuída ao usuário."}


@router.delete("/assign/{user_id}/{slug}", status_code=204)
def unassign_from_user(user_id: str, slug: str, db: Session = Depends(get_db),
                       _=Depends(require_superuser)):
    m = db.query(UserCustomEntityModel).filter_by(
        user_id=user_id, entity_type_slug=slug).first()
    if m:
        db.delete(m)
        db.commit()


@router.get("/user/{user_id}", response_model=list[UserEntityResponse])
def get_user_entities(user_id: str, db: Session = Depends(get_db),
                      _=Depends(require_superuser)):
    rows = db.query(UserCustomEntityModel).filter_by(user_id=user_id).all()
    result = []
    for r in rows:
        val = db.query(CustomEntityValueModel).filter_by(id=r.entity_value_id).first()
        result.append({
            "entity_type_slug": r.entity_type_slug,
            "entity_value_id":  r.entity_value_id,
            "entity_value_name": val.name if val else "—",
            "assigned_at": str(r.assigned_at),
        })
    return result

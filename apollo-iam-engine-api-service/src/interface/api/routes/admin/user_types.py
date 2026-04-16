from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.models.user_type_model import UserTypeModel
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/user-types", tags=["Admin — User Types"])


class UserTypeCreate(BaseModel):
    name: str
    description: str = ""


class UserTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class UserTypeResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: str


def _out(m: UserTypeModel) -> dict:
    return {"id": m.id, "name": m.name, "description": m.description,
            "created_at": str(m.created_at)}


@router.get("/", response_model=list[UserTypeResponse])
def list_user_types(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [_out(r) for r in db.query(UserTypeModel).order_by(UserTypeModel.name).all()]


@router.post("/", response_model=UserTypeResponse, status_code=201)
def create_user_type(body: UserTypeCreate, db: Session = Depends(get_db),
                     _=Depends(require_superuser)):
    if db.query(UserTypeModel).filter_by(name=body.name).first():
        raise HTTPException(status_code=409, detail=f"UserType '{body.name}' já existe.")
    m = UserTypeModel(id=str(uuid.uuid4()), name=body.name, description=body.description)
    db.add(m)
    db.commit()
    db.refresh(m)
    return _out(m)


@router.get("/{type_id}", response_model=UserTypeResponse)
def get_user_type(type_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    m = db.query(UserTypeModel).filter_by(id=type_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="UserType não encontrado.")
    return _out(m)


@router.put("/{type_id}", response_model=UserTypeResponse)
def update_user_type(type_id: str, body: UserTypeUpdate, db: Session = Depends(get_db),
                     _=Depends(require_superuser)):
    m = db.query(UserTypeModel).filter_by(id=type_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="UserType não encontrado.")
    if body.name is not None:
        m.name = body.name
    if body.description is not None:
        m.description = body.description
    db.commit()
    db.refresh(m)
    return _out(m)


@router.delete("/{type_id}", status_code=204)
def delete_user_type(type_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    m = db.query(UserTypeModel).filter_by(id=type_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="UserType não encontrado.")
    db.delete(m)
    db.commit()

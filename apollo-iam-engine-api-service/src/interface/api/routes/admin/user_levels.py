from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.models.user_level_model import UserLevelModel
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/user-levels", tags=["Admin — User Levels"])


class UserLevelCreate(BaseModel):
    name: str
    rank: int = 0
    description: str = ""


class UserLevelUpdate(BaseModel):
    name: Optional[str] = None
    rank: Optional[int] = None
    description: Optional[str] = None


class UserLevelResponse(BaseModel):
    id: str
    name: str
    rank: int
    description: str
    created_at: str


def _out(m: UserLevelModel) -> dict:
    return {"id": m.id, "name": m.name, "rank": m.rank,
            "description": m.description, "created_at": str(m.created_at)}


@router.get("/", response_model=list[UserLevelResponse])
def list_user_levels(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [_out(r) for r in db.query(UserLevelModel).order_by(UserLevelModel.rank).all()]


@router.post("/", response_model=UserLevelResponse, status_code=201)
def create_user_level(body: UserLevelCreate, db: Session = Depends(get_db),
                      _=Depends(require_superuser)):
    if db.query(UserLevelModel).filter_by(name=body.name).first():
        raise HTTPException(status_code=409, detail=f"UserLevel '{body.name}' já existe.")
    m = UserLevelModel(id=str(uuid.uuid4()), name=body.name,
                       rank=body.rank, description=body.description)
    db.add(m)
    db.commit()
    db.refresh(m)
    return _out(m)


@router.get("/{level_id}", response_model=UserLevelResponse)
def get_user_level(level_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    m = db.query(UserLevelModel).filter_by(id=level_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="UserLevel não encontrado.")
    return _out(m)


@router.put("/{level_id}", response_model=UserLevelResponse)
def update_user_level(level_id: str, body: UserLevelUpdate, db: Session = Depends(get_db),
                      _=Depends(require_superuser)):
    m = db.query(UserLevelModel).filter_by(id=level_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="UserLevel não encontrado.")
    if body.name is not None:
        m.name = body.name
    if body.rank is not None:
        m.rank = body.rank
    if body.description is not None:
        m.description = body.description
    db.commit()
    db.refresh(m)
    return _out(m)


@router.delete("/{level_id}", status_code=204)
def delete_user_level(level_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    m = db.query(UserLevelModel).filter_by(id=level_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="UserLevel não encontrado.")
    db.delete(m)
    db.commit()

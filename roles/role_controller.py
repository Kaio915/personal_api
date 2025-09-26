# roles/role_controller.py
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from . import role_service, role_model
from auth.auth_service import require_role

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=role_model.RolePublic, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_role("admin"))])
def create_role(role: role_model.RoleCreate, db: Session = Depends(get_db)):
    """Cria um novo perfil (apenas para administradores)."""
    return role_service.create_new_role(db=db, role=role)

@router.get("/", response_model=List[role_model.RolePublic],
            dependencies=[Depends(require_role("admin"))])
def list_roles(db: Session = Depends(get_db)):
    """Lista todos os perfis (apenas para administradores)."""
    return role_service.get_all(db)
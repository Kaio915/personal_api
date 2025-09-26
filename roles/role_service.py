# roles/role_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import role_repository, role_model

def create_new_role(db: Session, role: role_model.RoleCreate):
    db_role = role_repository.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role name already exists")
    return role_repository.create_role(db=db, role=role)

def get_all(db: Session):
    return role_repository.get_all_roles(db)
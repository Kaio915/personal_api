# roles/role_repository.py
from sqlalchemy.orm import Session
from . import role_model

def get_role_by_name(db: Session, name: str):
    return db.query(role_model.Role).filter(role_model.Role.name == name).first()

# Funções básicas do CRUD para Roles
def get_all_roles(db: Session):
    return db.query(role_model.Role).all()

def create_role(db: Session, role: role_model.RoleCreate):
    db_role = role_model.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role
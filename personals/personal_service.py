# personals/personal_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import personal_repository, personal_models

def create_new_personal(db: Session, personal: personal_models.PersonalCreate):
    db_personal = personal_repository.get_personal_by_email(db, email=personal.email)
    if db_personal:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # A lógica de buscar o role foi removida, pois o ID agora vem do controller
    return personal_repository.create_personal(db=db, personal=personal, role_id=personal.role_id)

def get_all_personals(db: Session):
    return personal_repository.get_personals(db)

def get_personal_by_id(db: Session, personal_id: int):
    db_personal = personal_repository.get_personal(db, personal_id=personal_id)
    if db_personal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal not found")
    return db_personal

def update_existing_personal(db: Session, personal_id: int, personal_in: personal_models.PersonalUpdate):
    db_personal = get_personal_by_id(db, personal_id)
    return personal_repository.update_personal(db=db, db_personal=db_personal, personal_in=personal_in)

def delete_personal_by_id(db: Session, personal_id: int):
    db_personal = get_personal_by_id(db, personal_id)
    return personal_repository.delete_personal(db=db, db_personal=db_personal)
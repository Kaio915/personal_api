# personals/personal_controller.py
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import get_db
from . import personal_service, personal_models

router = APIRouter(prefix="/personal", tags=["Personal"])

@router.post("/", response_model=personal_models.PersonalPublic, status_code=status.HTTP_201_CREATED)
def create_personal(personal: personal_models.PersonalCreate, db: Session = Depends(get_db)):
    """Endpoint para criar um novo personal."""
    return personal_service.create_new_personal(db=db, personal=personal)

@router.get("/", response_model=List[personal_models.PersonalPublic])
def read_personals(db: Session = Depends(get_db)):
    """Endpoint para listar todos os personals."""
    return personal_service.get_all_personals(db)

@router.get("/{personal_id}", response_model=personal_models.PersonalPublic)
def read_personal(personal_id: int, db: Session = Depends(get_db)):
    """Endpoint para buscar um personal pelo ID."""
    return personal_service.get_personal_by_id(db, personal_id=personal_id)

@router.put("/{personal_id}", response_model=personal_models.PersonalPublic)
def update_personal(personal_id: int, personal: personal_models.PersonalUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar um personal."""
    return personal_service.update_existing_personal(db=db, personal_id=personal_id, personal_in=personal)

@router.delete("/{personal_id}", response_model=personal_models.PersonalPublic)
def delete_personal(personal_id: int, db: Session = Depends(get_db)):
    """Endpoint para deletar um personal."""
    return personal_service.delete_personal_by_id(db=db, personal_id=personal_id)
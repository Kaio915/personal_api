# users/user_controller.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import SessionLocal
from . import user_service, user_models

router = APIRouter(prefix="/users", tags=["Users"])

# Esta função é a nossa "Injeção de Dependência".
# O FastAPI vai chamá-la para cada requisição que precisar de uma sessão com o banco.
# A palavra 'yield' entrega a sessão para a rota e, quando a rota termina,
# o código após o 'yield' (db.close()) é executado, garantindo que a conexão seja fechada.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=user_models.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: user_models.UserCreate, db: Session = Depends(get_db)):
    """Endpoint para criar um novo usuário. Recebe os dados validados (user)
    e a sessão do banco (db) através da injeção de dependência."""
    return user_service.create_new_user(db=db, user=user)

@router.get("/", response_model=List[user_models.UserPublic])
def read_users(db: Session = Depends(get_db)):
    """Endpoint para listar todos os usuários."""
    return user_service.get_all_users(db)

@router.get("/{user_id}", response_model=user_models.UserPublic)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Endpoint para buscar um usuário pelo ID."""
    return user_service.get_user_by_id(db, user_id=user_id)

@router.put("/{user_id}", response_model=user_models.UserPublic)
def update_user(user_id: int, user: user_models.UserUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar um usuário."""
    return user_service.update_existing_user(db=db, user_id=user_id, user_in=user)

@router.delete("/{user_id}", response_model=user_models.UserPublic)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Endpoint para deletar um usuário."""
    return user_service.delete_user_by_id(db=db, user_id=user_id)
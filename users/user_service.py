# users/user_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import user_repository, user_models

def create_new_user(db: Session, user: user_models.UserCreate):
    """Serviço para criar um novo usuário com regra de negócio."""
    # REGRA DE NEGÓCIO: Antes de criar, verificar se o e-mail já está em uso.
    db_user = user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        # Se o usuário já existe, lança uma exceção HTTP que o FastAPI retornará ao cliente.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Se a regra passar, chama o repositório para efetivamente criar o usuário.
    return user_repository.create_user(db=db, user=user)

def get_all_users(db: Session):
    """Serviço para listar todos os usuários. Neste caso, apenas repassa a chamada."""
    return user_repository.get_users(db)

def get_user_by_id(db: Session, user_id: int):
    """Serviço para buscar um usuário pelo ID, com tratamento de erro."""
    db_user = user_repository.get_user(db, user_id=user_id)
    # REGRA DE NEGÓCIO: Se o usuário não for encontrado, retornar um erro 404.
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

def update_existing_user(db: Session, user_id: int, user_in: user_models.UserUpdate):
    """Serviço para atualizar um usuário, com tratamento de erro."""
    db_user = get_user_by_id(db, user_id) # Reutiliza a lógica para buscar e checar se o usuário existe.
    return user_repository.update_user(db=db, db_user=db_user, user_in=user_in)

def delete_user_by_id(db: Session, user_id: int):
    """Serviço para deletar um usuário, com tratamento de erro."""
    db_user = get_user_by_id(db, user_id) # Reutiliza a lógica para buscar e checar se o usuário existe.
    return user_repository.delete_user(db=db, db_user=db_user)
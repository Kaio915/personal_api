# users/user_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import personal_repository, personal_models

def create_new_personal(db: Session, personal: personal_models.PersonalCreate):
    """Serviço para criar um novo personal com regra de negócio."""
    # REGRA DE NEGÓCIO: Antes de criar, verificar se o e-mail já está em uso.
    db_personal = personal_repository.get_personal_by_email(db, email=personal.email)
    if db_personal:
        # Se o personal já existe, lança uma exceção HTTP que o FastAPI retornará ao cliente.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Se a regra passar, chama o repositório para efetivamente criar o personal.
    return personal_repository.create_personal(db=db, personal=personal)

def get_all_personals(db: Session):
    """Serviço para listar todos os personals. Neste caso, apenas repassa a chamada."""
    return personal_repository.get_personals(db)

def get_personal_by_id(db: Session, personal_id: int):
    """Serviço para buscar um personal pelo ID, com tratamento de erro."""
    db_personal = personal_repository.get_personal(db, personal_id=personal_id)
    # REGRA DE NEGÓCIO: Se o personal não for encontrado, retornar um erro 404.
    if db_personal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal not found")
    return db_personal

def update_existing_personal(db: Session, personal_id: int, personal_in: personal_models.PersonalUpdate):
    """Serviço para atualizar um personal, com tratamento de erro."""
    db_personal = get_personal_by_id(db, personal_id) # Reutiliza a lógica para buscar e checar se o personal existe.
    return personal_repository.update_personal(db=db, db_personal=db_personal, personal_in=personal_in)

def delete_personal_by_id(db: Session, personal_id: int):
    """Serviço para deletar um personal, com tratamento de erro."""
    db_personal = get_personal_by_id(db, personal_id) # Reutiliza a lógica para buscar e checar se o personal existe.
    return personal_repository.delete_personal(db=db, db_personal=db_personal)
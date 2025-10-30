# connections/connection_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import connection_repository, connection_models

def create_new_connection(db: Session, connection: connection_models.ConnectionCreate):
    """Cria uma nova solicitação de conexão"""
    # Verificar se já existe uma conexão
    existing = connection_repository.get_existing_connection(
        db, 
        student_id=connection.student_id, 
        trainer_id=connection.trainer_id
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conexão já existe entre este aluno e personal trainer"
        )
    
    return connection_repository.create_connection(db=db, connection=connection)

def get_trainer_connections(db: Session, trainer_id: int):
    """Busca todas as conexões de um personal trainer"""
    return connection_repository.get_connections_by_trainer(db, trainer_id=trainer_id)

def get_student_connections(db: Session, student_id: int):
    """Busca todas as conexões de um aluno"""
    return connection_repository.get_connections_by_student(db, student_id=student_id)

def get_trainer_pending_connections(db: Session, trainer_id: int):
    """Busca conexões pendentes de um personal trainer"""
    return connection_repository.get_pending_connections_by_trainer(db, trainer_id=trainer_id)

def update_connection_status(db: Session, connection_id: int, status: connection_models.ConnectionStatus):
    """Atualiza o status de uma conexão (aceitar/rejeitar)"""
    db_connection = connection_repository.get_connection(db, connection_id=connection_id)
    
    if not db_connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conexão não encontrada"
        )
    
    return connection_repository.update_connection_status(
        db=db, 
        db_connection=db_connection, 
        status=status
    )

def delete_connection(db: Session, connection_id: int):
    """Remove uma conexão"""
    db_connection = connection_repository.get_connection(db, connection_id=connection_id)
    
    if not db_connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conexão não encontrada"
        )
    
    return connection_repository.delete_connection(db=db, db_connection=db_connection)

# connections/connection_repository.py
from sqlalchemy.orm import Session
from . import connection_models

# --- FUNÇÕES DE LEITURA (READ) ---
def get_connection(db: Session, connection_id: int):
    return db.query(connection_models.Connection).filter(
        connection_models.Connection.id == connection_id
    ).first()

def get_connections_by_student(db: Session, student_id: int):
    """Busca todas as conexões de um aluno"""
    return db.query(connection_models.Connection).filter(
        connection_models.Connection.student_id == student_id
    ).all()

def get_connections_by_trainer(db: Session, trainer_id: int):
    """Busca todas as conexões de um personal trainer"""
    return db.query(connection_models.Connection).filter(
        connection_models.Connection.trainer_id == trainer_id
    ).all()

def get_pending_connections_by_trainer(db: Session, trainer_id: int):
    """Busca conexões pendentes de um personal trainer"""
    return db.query(connection_models.Connection).filter(
        connection_models.Connection.trainer_id == trainer_id,
        connection_models.Connection.status == connection_models.ConnectionStatus.PENDING
    ).all()

def get_existing_connection(db: Session, student_id: int, trainer_id: int):
    """Verifica se já existe uma conexão entre aluno e trainer"""
    return db.query(connection_models.Connection).filter(
        connection_models.Connection.student_id == student_id,
        connection_models.Connection.trainer_id == trainer_id
    ).first()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---
def create_connection(db: Session, connection: connection_models.ConnectionCreate):
    """Cria uma nova solicitação de conexão"""
    db_connection = connection_models.Connection(
        student_id=connection.student_id,
        trainer_id=connection.trainer_id,
        status=connection_models.ConnectionStatus.PENDING
    )
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---
def update_connection_status(db: Session, db_connection: connection_models.Connection, status: connection_models.ConnectionStatus):
    """Atualiza o status de uma conexão"""
    db_connection.status = status
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---
def delete_connection(db: Session, db_connection: connection_models.Connection):
    db.delete(db_connection)
    db.commit()
    return db_connection

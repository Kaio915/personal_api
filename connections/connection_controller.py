# connections/connection_controller.py
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import get_db
from . import connection_service, connection_models

router = APIRouter(prefix="/connections", tags=["Connections"])

@router.post("/", response_model=connection_models.ConnectionPublic, status_code=status.HTTP_201_CREATED)
def create_connection(connection: connection_models.ConnectionCreate, db: Session = Depends(get_db)):
    """Cria uma nova solicitação de conexão entre aluno e personal trainer"""
    print(f"📨 Recebendo solicitação de conexão: Student {connection.student_id} -> Trainer {connection.trainer_id}")
    result = connection_service.create_new_connection(db=db, connection=connection)
    print(f"✅ Conexão criada com ID: {result.id}, Status: {result.status}")
    return result

@router.get("/trainer/{trainer_id}", response_model=List[connection_models.ConnectionPublic])
def get_trainer_connections(trainer_id: int, db: Session = Depends(get_db)):
    """Lista todas as conexões de um personal trainer"""
    print(f"🔍 Buscando todas as conexões do trainer {trainer_id}")
    connections = connection_service.get_trainer_connections(db, trainer_id=trainer_id)
    print(f"✅ Encontradas {len(connections)} conexões para o trainer {trainer_id}")
    return connections

@router.get("/trainer/{trainer_id}/pending", response_model=List[connection_models.ConnectionPublic])
def get_trainer_pending_connections(trainer_id: int, db: Session = Depends(get_db)):
    """Lista conexões pendentes de um personal trainer"""
    print(f"🔍 Buscando conexões PENDENTES do trainer {trainer_id}")
    connections = connection_service.get_trainer_pending_connections(db, trainer_id=trainer_id)
    print(f"✅ Encontradas {len(connections)} conexões PENDENTES para o trainer {trainer_id}")
    for conn in connections:
        print(f"  - Conexão #{conn.id}: Student {conn.student_id} -> Trainer {conn.trainer_id} ({conn.status})")
    return connections

@router.get("/student/{student_id}", response_model=List[connection_models.ConnectionPublic])
def get_student_connections(student_id: int, db: Session = Depends(get_db)):
    """Lista todas as conexões de um aluno"""
    return connection_service.get_student_connections(db, student_id=student_id)

@router.patch("/{connection_id}", response_model=connection_models.ConnectionPublic)
def update_connection(
    connection_id: int,
    update: connection_models.ConnectionUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza o status de uma conexão (aceitar/rejeitar)"""
    return connection_service.update_connection_status(
        db=db,
        connection_id=connection_id,
        status=update.status
    )

@router.delete("/{connection_id}", response_model=connection_models.ConnectionPublic)
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    """Remove uma conexão"""
    return connection_service.delete_connection(db=db, connection_id=connection_id)

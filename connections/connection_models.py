# connections/connection_models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from database import Base
import enum

# Enum para status da conexão
class ConnectionStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
class Connection(Base):
    __tablename__ = "connections"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(ConnectionStatus), default=ConnectionStatus.PENDING, nullable=False)
    
    # Relacionamentos
    student = relationship("User", foreign_keys=[student_id])
    trainer = relationship("User", foreign_keys=[trainer_id])

# ==================================
# SCHEMAS (Pydantic)
# ==================================
class ConnectionCreate(BaseModel):
    student_id: int
    trainer_id: int

class ConnectionUpdate(BaseModel):
    status: ConnectionStatus

class ConnectionPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    student_id: int
    trainer_id: int
    status: ConnectionStatus

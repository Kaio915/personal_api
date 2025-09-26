# roles/role_model.py
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict
from database import Base

# Modelo da Tabela SQLAlchemy
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# Schema Pydantic para criar/atualizar um Role
class RoleCreate(BaseModel):
    name: str

# Schema Pydantic para dados públicos
class RolePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
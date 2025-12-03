# users/user_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from database import Base
from roles.role_model import RolePublic # Importa o schema público de Role

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, index=True, nullable=True)
    profile_image_url = Column(String, nullable=True)
    approved = Column(Boolean, default=False, nullable=False)  # Novo campo: aprovação do admin
    # Campos adicionais para perfil
    goals = Column(String, nullable=True)  # Objetivos do usuário
    fitness_level = Column(String, nullable=True)  # Nível de condicionamento físico
    registration_date = Column(String, nullable=True)  # Data de cadastro
    # Campos específicos para Personal Trainer
    specialty = Column(String, nullable=True)  # Especialidade do personal
    cref = Column(String, nullable=True)  # Número do CREF
    experience = Column(String, nullable=True)  # Tempo de experiência
    bio = Column(String, nullable=True)  # Biografia
    hourly_rate = Column(String, nullable=True)  # Valor da hora/aula
    city = Column(String, nullable=True)  # Cidade onde atua
    # Chave estrangeira que aponta para a tabela 'roles'
    role_id = Column(Integer, ForeignKey("roles.id"))
    # Cria a relação para que possamos acessar o objeto Role a partir de um User
    role = relationship("Role")

# ==================================
# SCHEMAS (Pydantic)
# ==================================
class UserCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = Field(default=None, min_length=3)
    profile_image_url: str | None = None
    role_id: int = Field(description="ID do role a ser associado ao usuário")
    # Campos de Aluno
    goals: str | None = None
    fitnessLevel: str | None = Field(default=None, alias="fitness_level")
    registration_date: str | None = None
    # Campos de Personal Trainer
    specialty: str | None = None
    cref: str | None = None
    experience: str | None = None
    bio: str | None = None
    hourlyRate: str | None = Field(default=None, alias="hourly_rate")
    city: str | None = None

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=3)
    profile_image_url: str | None = None

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str | None = None
    profile_image_url: str | None = None
    approved: bool = False
    # Campos de Aluno
    goals: str | None = None
    fitness_level: str | None = None
    registration_date: str | None = None
    # Campos de Personal Trainer
    specialty: str | None = None
    cref: str | None = None
    experience: str | None = None
    bio: str | None = None
    hourly_rate: str | None = None
    city: str | None = None
    role: RolePublic # O perfil agora é um objeto aninhado
    # Avaliação média do trainer (preenchida dinamicamente pelo controller)
    average_rating: float | None = None
    rating_count: int | None = None

class UserApproval(BaseModel):
    """Schema para aprovar/desaprovar usuários"""
    approved: bool
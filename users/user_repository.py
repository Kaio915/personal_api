# users/user_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import user_models
from security import get_password_hash
# Import related models so we can remove dependent records before deleting a user
from messages.message_models import Message
from connections.connection_models import Connection

# --- FUNÇÕES DE LEITURA (READ) ---
def get_user(db: Session, user_id: int):
    return db.query(user_models.User).filter(user_models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(user_models.User).filter(user_models.User.email == email).first()

def get_users(db: Session):
    return db.query(user_models.User).all()

def get_users_by_approval_status(db: Session, approved: bool):
    """Busca usuários por status de aprovação"""
    return db.query(user_models.User).filter(user_models.User.approved == approved).all()

def get_approved_trainers(db: Session):
    """Busca personal trainers aprovados (role_id=2 e approved=True)"""
    return db.query(user_models.User).filter(
        user_models.User.role_id == 2,
        user_models.User.approved == True
    ).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---
def create_user(db: Session, user: user_models.UserCreate, role_id: int):
    hashed_password = get_password_hash(user.password)
    # Admin é aprovado automaticamente, outros usuários precisam de aprovação
    is_auto_approved = role_id == 1  # role_id 1 = admin
    db_user = user_models.User(
        email=user.email, 
        hashed_password=hashed_password, 
        full_name=user.full_name,
        profile_image_url=user.profile_image_url,
        role_id=role_id,
        approved=is_auto_approved,
        # Campos de Aluno
        goals=user.goals,
        fitness_level=user.fitnessLevel,  # camelCase do frontend -> snake_case do banco
        registration_date=user.registration_date,
        # Campos de Personal Trainer
        specialty=user.specialty,
        cref=user.cref,
        experience=user.experience,
        bio=user.bio,
        hourly_rate=user.hourlyRate,  # camelCase do frontend -> snake_case do banco
        city=user.city
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---
def update_user(db: Session, db_user: user_models.User, user_in: user_models.UserUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
         if key == "password":
             setattr(db_user, "hashed_password", get_password_hash(value))
         else:
             setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---
def delete_user(db: Session, db_user: user_models.User):
    print(f"📦 REPOSITORY DELETE - Deletando user_id={db_user.id}, email={db_user.email}")
    try:
        # Delete messages where the user is sender or receiver
        deleted_msgs = db.query(Message).filter(
            or_(Message.sender_id == db_user.id, Message.receiver_id == db_user.id)
        ).delete(synchronize_session=False)
        print(f"   🗑️ Mensagens removidas: {deleted_msgs}")

        # Delete connections where the user is student or trainer
        deleted_conns = db.query(Connection).filter(
            or_(Connection.student_id == db_user.id, Connection.trainer_id == db_user.id)
        ).delete(synchronize_session=False)
        print(f"   🗑️ Conexões removidas: {deleted_conns}")

        # Now delete the user
        db.delete(db_user)
        db.commit()
        print(f"   ✅ Commit realizado - usuário deletado permanentemente")
        return db_user
    except Exception as e:
        db.rollback()
        print(f"   ❌ Erro ao deletar usuário: {e}")
        raise

# --- FUNÇÃO DE APROVAÇÃO ---
def update_user_approval(db: Session, db_user: user_models.User, approved: bool):
    """Atualiza o status de aprovação do usuário"""
    db_user.approved = approved
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
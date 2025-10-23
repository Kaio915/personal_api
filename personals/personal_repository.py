# personals/personal_repository.py
from sqlalchemy.orm import Session
from . import personal_models
from security import get_password_hash

# --- FUNÇÕES DE LEITURA (READ) ---
def get_personal(db: Session, personal_id: int):
    return db.query(personal_models.Personal).filter(personal_models.Personal.id == personal_id).first()

def get_personal_by_email(db: Session, email: str):
    return db.query(personal_models.Personal).filter(personal_models.Personal.email == email).first()

def get_personals(db: Session):
    return db.query(personal_models.Personal).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---
def create_personal(db: Session, personal: personal_models.PersonalCreate, role_id: int):
    hashed_password = get_password_hash(personal.password)
    db_personal = personal_models.Personal(
        email=personal.email, 
        hashed_password=hashed_password, 
        full_name=personal.full_name,
        profile_image_url=personal.profile_image_url,
        role_id=role_id
    )
    db.add(db_personal)
    db.commit()
    db.refresh(db_personal)
    return db_personal

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---
def update_personal(db: Session, db_personal: personal_models.Personal, personal_in: personal_models.PersonalUpdate):
    update_data = personal_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
         if key == "password":
             setattr(db_personal, "hashed_password", get_password_hash(value))
         else:
             setattr(db_personal, key, value)
    db.add(db_personal)
    db.commit()
    db.refresh(db_personal)
    return db_personal

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---
def delete_personal(db: Session, db_personal: personal_models.Personal):
    db.delete(db_personal)
    db.commit()
    return db_personal
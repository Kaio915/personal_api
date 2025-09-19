# personals/personal_repository.py

from sqlalchemy.orm import Session
from . import personal_models

# --- FUNÇÕES DE LEITURA (READ) ---
def get_personal(db: Session, personal_id: int):
    """
    Busca um único personal pelo seu ID.
    db.query(personal_models.Personal): Inicia uma consulta na tabela Personal.
    .filter(personal_models.Personal.id == personal_id): Filtra os resultados onde o id seja igual ao fornecido.
    .first(): Retorna o primeiro resultado encontrado ou None se não encontrar.
    """
    return db.query(personal_models.Personal).filter(personal_models.Personal.id == personal_id).first()

def get_personal_by_email(db: Session, email: str):
    """Busca um único personal pelo seu e-mail."""
    return db.query(personal_models.Personal).filter(personal_models.Personal.email == email).first()

def get_personals(db: Session):
    """
    Busca todos os personals cadastrados no banco de dados.
    .all(): Retorna uma lista com todos os resultados da consulta.
    """
    return db.query(personal_models.Personal).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---
def create_personal(db: Session, personal: personal_models.PersonalCreate):
    """
    Cria um novo personal no banco de dados.
    """
    # AVISO: A senha aqui ainda não está segura! Veremos como fazer o hash na próxima aula.
    hashed_password = personal.password

    # Cria uma instância do modelo SQLAlchemy com os dados do schema Pydantic.
    # É aqui que os dados da API são transformados em um objeto que pode ser salvo no banco.
    db_personal = personal_models.Personal(email=personal.email, hashed_password=hashed_password, full_name=personal.full_name)

    db.add(db_personal)      # Adiciona o novo objeto à sessão (área de preparação).
    db.commit()         # Salva (commita) as mudanças no banco de dados.
    db.refresh(db_personal) # Atualiza o objeto db_personal com os dados do banco (como o ID gerado).
    return db_personal

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---
def update_personal(db: Session, db_personal: personal_models.Personal, personal_in: personal_models.PersonalUpdate):
    """Atualiza os dados de um personal existente."""
    update_data = personal_in.model_dump(exclude_unset=True) # Pega só os campos que foram enviados na requisição.
    for key, value in update_data.items():
         # Se o campo for 'password', precisa mapear para 'hashed_password' no modelo SQLAlchemy
        if key == "password":
            setattr(db_personal, "hashed_password", value) # AVISO: A senha ainda não está sendo hasheada!
        else:
            setattr(db_personal, key, value) # Atualiza cada campo no objeto do banco (db_personal).

    db.add(db_personal) # Adiciona o objeto modificado à sessão.
    db.commit()     # Salva as alterações.
    db.refresh(db_personal) # Atualiza o objeto com os dados do banco.
    return db_personal

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---
def delete_personal(db: Session, db_personal: personal_models.Personal):
    """Deleta um personal do banco de dados."""
    db.delete(db_personal) # Marca o objeto para deleção.
    db.commit()        # Efetiva a deleção no banco.
    return db_personal
# main.py
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from personals import personal_controller
from roles import role_controller
from auth import auth_controller
from database import engine, Base, get_db
from users.user_models import User
from roles.role_model import Role
from security import get_password_hash

Base.metadata.create_all(bind=engine)

def seed_admin_user():
    """
    Cria o usuário admin padrão (admin@fitconnect.com / admin123) se não existir.
    """
    db = next(get_db())
    try:
        # Verifica se o usuário admin já existe
        admin_user = db.query(User).filter(User.email == "admin@fitconnect.com").first()
        if admin_user:
            print("✓ Usuário admin já existe no banco.")
            return
        
        # Verifica se o role 'admin' existe, senão cria
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            admin_role = Role(name="admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            print("✓ Role 'admin' criado.")
        
        # Cria o usuário admin com senha hasheada
        hashed_password = get_password_hash("admin123")
        new_admin = User(
            email="admin@fitconnect.com",
            hashed_password=hashed_password,
            full_name="Administrador",
            role_id=admin_role.id
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print("✓ Usuário admin criado com sucesso (admin@fitconnect.com / admin123).")
    except Exception as e:
        print(f"✗ Erro ao criar usuário admin: {e}")
        db.rollback()
    finally:
        db.close()

seed_admin_user()

app = FastAPI(title="API do Meu Projeto", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)
app.include_router(role_controller.router)
app.include_router(auth_controller.router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
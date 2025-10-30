import sys
from database import SessionLocal
from users.user_models import User
from security import get_password_hash

def check_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"=== Usuários no banco ({len(users)} encontrados) ===")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Nome: {user.full_name}, Role: {user.role_id}, Aprovado: {user.approved}")
        return users
    except Exception as e:
        print(f"Erro ao consultar usuários: {e}")
        return []
    finally:
        db.close()

def create_test_user(email, password, full_name, role_id=3):
    db = SessionLocal()
    try:
        # Verifica se já existe
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"❌ Usuário {email} já existe!")
            return None
        
        # Cria novo usuário
        hashed_password = get_password_hash(password)
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role_id=role_id,
            approved=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✅ Usuário {email} criado com sucesso! ID: {new_user.id}")
        return new_user
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar usuário: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("\n🔍 Verificando usuários existentes...")
    users = check_users()
    
    if len(users) == 0:
        print("\n⚠️ Nenhum usuário encontrado! Criando usuários de teste...")
        create_test_user("kaio@gmail.com", "12345678", "Kaio", role_id=3)  # Aluno
        create_test_user("jonas@gmail.com", "12345678", "Jonas", role_id=3)  # Aluno
        create_test_user("personal@gmail.com", "12345678", "Personal Trainer", role_id=2)  # Personal
        print("\n✅ Usuários de teste criados!")
        print("\n🔍 Verificando novamente...")
        check_users()
    else:
        print(f"\n✅ Banco já tem {len(users)} usuário(s)")

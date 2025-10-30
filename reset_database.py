"""
Script para recriar as tabelas do banco de dados.
ATENÇÃO: Este script irá APAGAR TODOS OS DADOS existentes!
"""
from database import engine, Base, get_db
from users.user_models import User
from roles.role_model import Role
from personals.personal_models import Personal
from security import get_password_hash

def reset_database():
    """
    Remove todas as tabelas e recria do zero.
    """
    print("🔄 Iniciando reset do banco de dados...")
    
    # 1. Remove todas as tabelas usando CASCADE para lidar com dependências
    print("🗑️  Removendo tabelas antigas...")
    from sqlalchemy import text
    with engine.begin() as conn:
        # Desabilita temporariamente as checagens de foreign key
        conn.execute(text("SET session_replication_role = 'replica';"))
        
        # Remove todas as tabelas do schema public
        conn.execute(text("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """))
        
        # Reabilita as checagens de foreign key
        conn.execute(text("SET session_replication_role = 'origin';"))
    
    print("✓ Tabelas removidas com sucesso!")
    
    # 2. Recria todas as tabelas
    print("🔨 Criando novas tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tabelas criadas com sucesso!")
    
    # 3. Popula com dados iniciais
    print("📝 Criando dados iniciais...")
    seed_initial_data()
    
    print("✅ Reset do banco de dados concluído com sucesso!")

def seed_initial_data():
    """
    Cria roles e usuário admin padrão.
    """
    db = next(get_db())
    try:
        # Criar roles padrão
        roles_data = [
            {"name": "admin"},
            {"name": "personal"},
            {"name": "aluno"}
        ]
        
        created_roles = {}
        for role_data in roles_data:
            role = Role(**role_data)
            db.add(role)
            db.commit()
            db.refresh(role)
            created_roles[role.name] = role
            print(f"✓ Role '{role.name}' criado com ID {role.id}")
        
        # Criar usuário admin
        hashed_password = get_password_hash("admin123")
        admin_user = User(
            email="admin@fitconnect.com",
            hashed_password=hashed_password,
            full_name="Administrador do Sistema",
            profile_image_url=None,
            role_id=created_roles["admin"].id,
            approved=True  # Admin já é aprovado automaticamente
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"✓ Usuário admin criado com ID {admin_user.id}")
        print(f"  📧 Email: admin@fitconnect.com")
        print(f"  🔑 Senha: admin123")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados iniciais: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*60)
    print("⚠️  ATENÇÃO: Este script irá APAGAR TODOS OS DADOS!")
    print("="*60 + "\n")
    
    resposta = input("Tem certeza que deseja continuar? (sim/não): ")
    
    if resposta.lower() in ['sim', 's', 'yes', 'y']:
        reset_database()
    else:
        print("❌ Operação cancelada.")
        sys.exit(0)

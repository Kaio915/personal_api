"""
Script para adicionar os campos de Personal Trainer na tabela users
"""
from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def add_columns():
    with engine.connect() as connection:
        try:
            # Adicionar coluna specialty
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS specialty TEXT
            """))
            connection.commit()
            print("✅ Coluna 'specialty' adicionada com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar coluna 'specialty': {e}")
        
        try:
            # Adicionar coluna cref
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS cref TEXT
            """))
            connection.commit()
            print("✅ Coluna 'cref' adicionada com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar coluna 'cref': {e}")
        
        try:
            # Adicionar coluna experience
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS experience TEXT
            """))
            connection.commit()
            print("✅ Coluna 'experience' adicionada com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar coluna 'experience': {e}")
        
        try:
            # Adicionar coluna bio
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS bio TEXT
            """))
            connection.commit()
            print("✅ Coluna 'bio' adicionada com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar coluna 'bio': {e}")
        
        try:
            # Adicionar coluna hourly_rate
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS hourly_rate TEXT
            """))
            connection.commit()
            print("✅ Coluna 'hourly_rate' adicionada com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar coluna 'hourly_rate': {e}")
        
        try:
            # Adicionar coluna city
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS city TEXT
            """))
            connection.commit()
            print("✅ Coluna 'city' adicionada com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar coluna 'city': {e}")

if __name__ == "__main__":
    print("🔄 Adicionando colunas de Personal Trainer na tabela users...")
    add_columns()
    print("✅ Migração concluída!")

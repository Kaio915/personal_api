"""
Script para adicionar os campos goals, fitness_level e registration_date na tabela users
"""
from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def add_columns():
    with engine.connect() as connection:
        try:
            # Adicionar coluna goals
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS goals TEXT
            """))
            connection.commit()
            print("✅ Coluna 'goals' adicionada com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar coluna 'goals': {e}")
        
        try:
            # Adicionar coluna fitness_level
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS fitness_level TEXT
            """))
            connection.commit()
            print("✅ Coluna 'fitness_level' adicionada com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar coluna 'fitness_level': {e}")
        
        try:
            # Adicionar coluna registration_date
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS registration_date TEXT
            """))
            connection.commit()
            print("✅ Coluna 'registration_date' adicionada com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar coluna 'registration_date': {e}")

if __name__ == "__main__":
    print("🔄 Adicionando colunas na tabela users...")
    add_columns()
    print("✅ Migração concluída!")

# create_verification_codes_table.py
from sqlalchemy import text
from database import engine

def create_verification_codes_table():
    """Cria a tabela verification_codes no banco de dados"""
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS verification_codes (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        code VARCHAR(6) NOT NULL,
        purpose VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        used INTEGER DEFAULT 0
    );
    
    CREATE INDEX IF NOT EXISTS idx_verification_codes_email ON verification_codes(email);
    CREATE INDEX IF NOT EXISTS idx_verification_codes_code ON verification_codes(code);
    """
    
    try:
        with engine.connect() as conn:
            conn.execute(text(create_table_sql))
            conn.commit()
        print("✅ Tabela verification_codes criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")

if __name__ == "__main__":
    create_verification_codes_table()

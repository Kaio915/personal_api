import psycopg2
from psycopg2.extensions import connection, ISOLATION_LEVEL_AUTOCOMMIT
import sys
import io

# Monkey patch sys.stderr para ignorar erros de Unicode
class SafeStderr:
    def __init__(self, original):
        self.original = original
        
    def write(self, text):
        try:
            self.original.write(text)
        except UnicodeEncodeError:
            pass  # Ignora erros de encoding
            
    def flush(self):
        try:
            self.original.flush()
        except:
            pass

sys.stderr = SafeStderr(sys.stderr)

# Conecta diretamente ao PostgreSQL sem SQLAlchemy
try:
    # Força encoding Latin1 que é compatível com Windows-1252
    conn = psycopg2.connect(
        host='localhost',
        database='personaltrainer',
        user='postgres',
        password='123456',
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_client_encoding('UTF8')  # Muda encoding após conectar
    cursor = conn.cursor()
    
    print("✅ Conectado ao PostgreSQL com sucesso!\n")
    
    # Insere usuários
    cursor.execute("""
        INSERT INTO users (email, hashed_password, full_name, role_id, approved) 
        VALUES ('kaio@gmail.com', '$2b$12$vTE60.99ojIjrMHqE0PNk.Id2zHEPHpaG26tK5P0MWJyam8P8tX0m', 'Kaio', 3, true)
        ON CONFLICT (email) DO NOTHING
    """)
    print("✅ Usuário kaio@gmail.com inserido/atualizado")
    
    cursor.execute("""
        INSERT INTO users (email, hashed_password, full_name, role_id, approved) 
        VALUES ('jonas@gmail.com', '$2b$12$vTE60.99ojIjrMHqE0PNk.Id2zHEPHpaG26tK5P0MWJyam8P8tX0m', 'Jonas', 3, true)
        ON CONFLICT (email) DO NOTHING
    """)
    print("✅ Usuário jonas@gmail.com inserido/atualizado")
    
    # Verifica usuários
    cursor.execute("SELECT id, email, full_name, role_id, approved FROM users")
    users = cursor.fetchall()
    print(f"\n📋 Total de usuários: {len(users)}")
    for user in users:
        print(f"  ID: {user[0]}, Email: {user[1]}, Nome: {user[2]}, Role: {user[3]}, Aprovado: {user[4]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Concluído!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

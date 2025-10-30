# database.py
import os
import warnings
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Força encoding UTF-8 para comunicação com PostgreSQL
os.environ['PGCLIENTENCODING'] = 'UTF8'

# Suprime avisos do psycopg2 sobre collation
warnings.filterwarnings('ignore', category=UserWarning, module='psycopg2')

# Monkey-patch crítico para ignorar erros de Unicode do psycopg2
import sys
if sys.version_info >= (3, 13):
    import psycopg2
    from psycopg2 import extensions
    
    # Salva a função original
    _original_register_type = extensions.register_type
    
    def _patched_register_type(obj, scope=None):
        try:
            return _original_register_type(obj, scope)
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass  # Ignora erros de Unicode
    
    extensions.register_type = _patched_register_type

APP_PROFILE = os.getenv("APP_PROFILE", "DEV")

if APP_PROFILE == "DEV":
    # URL para desenvolvimento local
    # Adiciona parâmetros de conexão para forçar encoding e suprimir avisos
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/personaltrainer?client_encoding=utf8&application_name=fitconnect"
else:
    # URL para produção (Render ou outro provedor)
    # Render fornece a variável DATABASE_URL automaticamente
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/mydb")

# 2. Cria a "engine" do SQLAlchemy, que é o ponto de entrada para o banco de dados.
#    Ela gerencia as conexões com o banco.
# Configuração especial para contornar problemas de encoding do PostgreSQL no Windows
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    pool_recycle=3600,   # Recicla conexões a cada hora
    echo=False,          # Não loga SQL (evita prints com encoding ruim)
    connect_args={
        "options": "-c client_encoding=utf8"
    }
)

# 3. Cria uma fábrica de sessões (SessionLocal). Cada instância de SessionLocal
#    será uma sessão com o banco de dados. Pense nela como uma "conversa" temporária.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Cria uma classe Base. Nossos modelos de tabela do SQLAlchemy herdarão desta
#    classe para que o ORM possa gerenciá-los.
Base = declarative_base()

# 5. [NOVO] Função para obter a sessão do banco (Injeção de Dependência)
#    Esta função garante que a sessão com o banco seja sempre fechada após a requisição.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
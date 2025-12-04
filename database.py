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

APP_PROFILE = os.getenv("APP_PROFILE", "DEV").upper()

# Connection strings
# Local connection string (use this when running locally if no env override provided)
LOCAL_DATABASE_URL = (
    "postgresql://personal:gPrmpnPWEyniyMZwLI8potIHWjjII0zx@"
    "dpg-d4p0pe0gjchc73891jpg-a.oregon-postgres.render.com/personal_bd_or6k"
)

# Choose DB URL based on environment profile.
# - In DEV (local) use the `LOCAL_DATABASE_URL` or the env var `LOCAL_DATABASE_URL` if set.
# - In PROD use the `DATABASE_URL` environment variable (Render/Heroku style),
#   falling back to the same LOCAL_DATABASE_URL only if DATABASE_URL is missing.
if APP_PROFILE == "DEV":
    SQLALCHEMY_DATABASE_URL = os.getenv("LOCAL_DATABASE_URL", LOCAL_DATABASE_URL)
else:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", LOCAL_DATABASE_URL)

print(f"[database] APP_PROFILE={APP_PROFILE}, using DB URL: {SQLALCHEMY_DATABASE_URL.split('@')[-1][:60]}...")

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
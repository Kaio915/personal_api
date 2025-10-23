# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

APP_PROFILE = os.getenv("APP_PROFILE", "DEV")

if APP_PROFILE == "DEV":
    # URL para desenvolvimento local
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@10.5.10.10/personal_db"
else:
    # URL para produção (Render ou outro provedor)
    # Render fornece a variável DATABASE_URL automaticamente
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/mydb")

# 2. Cria a "engine" do SQLAlchemy, que é o ponto de entrada para o banco de dados.
#    Ela gerencia as conexões com o banco.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

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
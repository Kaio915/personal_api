from sqlalchemy import text
from database import engine, Base
# Import all models to ensure they are registered with Base
from users.user_models import User
from roles.role_model import Role
from connections.connection_models import Connection
from messages.message_models import Message

# Drop existing messages table if it exists
with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS messages CASCADE'))
    conn.commit()
    print('✅ Tabela messages removida (se existia)')

# Create all tables
Base.metadata.create_all(bind=engine)
print('✅ Tabela messages criada com sucesso!')

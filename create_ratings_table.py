from sqlalchemy import text
from database import engine, Base
# Import models so they are registered
from users.user_models import User
from roles.role_model import Role
from connections.connection_models import Connection
from messages.message_models import Message
from ratings.rating_models import Rating

with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS ratings CASCADE'))
    conn.commit()
    print('✅ Tabela ratings removida (se existia)')

Base.metadata.create_all(bind=engine)
print('✅ Tabela ratings criada com sucesso!')

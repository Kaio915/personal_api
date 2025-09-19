# main.py
import uvicorn
from fastapi import FastAPI

from personals import personal_controller
from database import engine, Base

# Linha mágica que instrui o SQLAlchemy a criar todas as tabelas
# que herdam da nossa Base (definida em database.py) no banco de dados.
# Isso só deve ser usado em desenvolvimento para facilitar o setup.
Base.metadata.create_all(bind=engine)

# 1. Cria a instância principal da aplicação
app = FastAPI(
    title="API do Meu Projeto",
    version="0.1.0"
)

# 2. Inclui o roteador de personals na aplicação principal
app.include_router(personal_controller.router)

# 4. Código para rodar o servidor
if __name__ == '__main__':
    # Este bloco só executa quando rodamos o script diretamente (python main.py)
    uvicorn.run(app, host="0.0.0.0", port=8000)
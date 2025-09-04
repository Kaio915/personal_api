import uvicorn
from fastapi import FastAPI

# 1. Cria a instância principal da nossa aplicação
app = FastAPI(
    title="API do Meu Projeto",
    version="0.1.0"
)

# 2. Criando o primeiro endpoint
@app.get("/")
def read_root():
    # Quando alguém acessar a raiz ("/") da nossa API via GET...
    # ...retornamos este dicionário. O FastAPI o converte para JSON automaticamente!
    return {"message": "Bem-vindo à API do nosso projeto!"}

# 3. Endpoint com Parâmetro de Rota (Path Parameter)
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    # @app.get: Decorator que define a rota para requisições GET.
    # O que é um Decorator? Pense nele como um "super-poder" que você adiciona
    # a uma função normal. O "@" é a sintaxe do Python para aplicar esse poder.
    # No nosso caso, o decorator @app.get("/") transforma a função simples read_item
    # em um endpoint de API que sabe como responder a requisições web.
    #
    # "/items/{item_id}": O caminho. A parte com chaves {item_id} é dinâmica.
    # item_id: int: O FastAPI pega o valor da URL e o coloca na variável item_id.
    # A dica de tipo ": int" garante que será um número inteiro. Mágica!
    # q: str | None = None: Parâmetro de Consulta (Query Parameter). É opcional.
    # Ex de uso: /items/5?q=teste
    return {"item_id": item_id, "q": q}

# 4. Código para rodar o servidor
if __name__ == '__main__':
    # Este bloco só executa quando rodamos o script diretamente (python main.py)
    uvicorn.run(app, host="0.0.0.0", port=8000)
# app/users/controller.py
from fastapi import APIRouter
from .user_models import UserCreate, UserPublic
from fastapi import APIRouter, HTTPException, status
from .user_models import UserCreate, UserPublic, UserUpdate

# 1. Cria um roteador específico para usuários
router = APIRouter(
    prefix="/users",       # Todas as rotas aqui começarão com /users
    tags=["Users"]         # Agrupa as rotas no Swagger
)

# Lista FAKE para simular um banco de dados
fake_db = []

# 2. Define o endpoint para criar um usuário
@router.post("/save", response_model=UserPublic)
def create_user(user: UserCreate):
    # user aqui é um objeto Pydantic, com dados já validados!
    new_user_data = user.model_dump()
    new_user_data["id"] = len(fake_db) + 1

    new_user = UserPublic(**new_user_data)
    fake_db.append(new_user)

    return new_user # FastAPI converte para JSON

@router.get("/", response_model=list[UserPublic])
def list_users():
    # Converte os dicionários do 'banco de dados' para o modelo público
    return [UserPublic(**user_data) for user_data in fake_db.values()]

@router.put("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user_update: UserUpdate):
    if user_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    stored_user_data = fake_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True) # Apenas campos enviados

    updated_user = stored_user_data.copy()
    updated_user.update(update_data)
    fake_db[user_id] = updated_user

    return UserPublic(**updated_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    del fake_db[user_id]
    # Com status 204, a resposta não deve ter corpo. O FastAPI cuida disso.
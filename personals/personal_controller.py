# app/personals/controller.py
from fastapi import APIRouter
from .personal_models import PersonalCreate, PersonalPublic, PersonalUpdate
from fastapi import APIRouter, HTTPException, status

# 1. Cria um roteador específico para usuários
router = APIRouter(
    prefix="/personals",       # Todas as rotas aqui começarão com /personals
    tags=["Personals"]         # Agrupa as rotas no Swagger
)

# Lista FAKE para simular um banco de dados
fake_db = []

# 2. Define o endpoint para criar um usuário
@router.post("/save", response_model=PersonalPublic)
def create_personal(personal: PersonalCreate):
    # personal aqui é um objeto Pydantic, com dados já validados!
    new_personal_data = personal.model_dump()
    new_personal_data["id"] = len(fake_db) + 1

    new_personal = PersonalPublic(**new_personal_data)
    fake_db.append(new_personal)

    return new_personal # FastAPI converte para JSON

@router.get("/", response_model=list[PersonalPublic])
def list_personals():
    # Converte os dicionários do 'banco de dados' para o modelo público
    return [PersonalPublic(**personal_data) for personal_data in fake_db.values()]

@router.put("/{personal_id}", response_model=PersonalPublic)
def update_personal(personal_id: int, personal_update: PersonalUpdate):
    if personal_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal not found")

    stored_personal_data = fake_db[personal_id]
    update_data = personal_update.model_dump(exclude_unset=True) # Apenas campos enviados

    updated_personal = stored_personal_data.copy()
    updated_personal.update(update_data)
    fake_db[personal_id] = updated_personal

    return PersonalPublic(**updated_personal)

@router.delete("/{personal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_personal(personal_id: int):
    if personal_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal not found")

    del fake_db[personal_id]
    # Com status 204, a resposta não deve ter corpo. O FastAPI cuida disso.
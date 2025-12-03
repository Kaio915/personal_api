from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from . import rating_service, rating_models

router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.post("/", response_model=rating_models.RatingPublic, status_code=status.HTTP_201_CREATED)
def create_rating(payload: rating_models.RatingCreate, db: Session = Depends(get_db)):
    """Cria ou atualiza uma avaliação (1-5) de um aluno para um personal."""
    result = rating_service.rate_trainer(db, payload.trainer_id, payload.student_id, payload.rating)
    return result


@router.get("/trainer/{trainer_id}")
def get_trainer_rating(trainer_id: int, db: Session = Depends(get_db)):
    """Retorna média e contagem de avaliações para um personal."""
    agg = rating_service.get_trainer_rating(db, trainer_id)
    return {"trainer_id": trainer_id, "average": agg.get("avg"), "count": agg.get("count")}

from sqlalchemy.orm import Session
from sqlalchemy import func
from .rating_models import Rating


def create_or_update_rating(db: Session, trainer_id: int, student_id: int, rating_value: int):
    """Cria ou atualiza a avaliação feita por um aluno para um trainer."""
    # Verifica se já existe avaliação deste aluno para este trainer
    existing = db.query(Rating).filter(
        Rating.trainer_id == trainer_id,
        Rating.student_id == student_id,
    ).first()

    if existing:
        existing.rating = rating_value
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    new = Rating(trainer_id=trainer_id, student_id=student_id, rating=rating_value)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


def get_trainer_rating_aggregate(db: Session, trainer_id: int):
    """Retorna média e contagem de avaliações de um trainer."""
    q = db.query(func.count(Rating.id).label("count"), func.avg(Rating.rating).label("avg")).filter(
        Rating.trainer_id == trainer_id
    ).first()

    if q is None:
        return {"count": 0, "avg": None}

    return {"count": int(q.count or 0), "avg": float(q.avg) if q.avg is not None else None}

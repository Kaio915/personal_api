from sqlalchemy.orm import Session
from . import rating_repository


def rate_trainer(db: Session, trainer_id: int, student_id: int, rating_value: int):
    # sanitize rating
    if rating_value < 1:
        rating_value = 1
    if rating_value > 5:
        rating_value = 5
    return rating_repository.create_or_update_rating(db, trainer_id, student_id, rating_value)


def get_trainer_rating(db: Session, trainer_id: int):
    return rating_repository.get_trainer_rating_aggregate(db, trainer_id)

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel, ConfigDict
from database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RatingCreate(BaseModel):
    trainer_id: int
    student_id: int
    rating: int


class RatingPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trainer_id: int
    student_id: int
    rating: int
    created_at: str

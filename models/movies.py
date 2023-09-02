from config.database import Base
from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel, Field
from typing import Optional


class MovieModel(Base):

    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    overview = Column(String(500))
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String(50))


class Movie(BaseModel):

    id: Optional[int]
    title: str = Field(default='The movie title', max_length=50)
    overview: str = Field(default='The movie overview', min_length=5, max_length=500)
    year: int = Field(default=2023, ge=1900, le=2050)
    rating: float = Field(default=0.0, ge=0.0, le=10.0)
    category: str = Field(default='The movie category', max_length=50)
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from ..core import Base

if TYPE_CHECKING:
    from .movie import Movie


class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(250))

    movies: Mapped[List["Movie"]] = relationship("Movie", back_populates="genre", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Genre(name='{self.name}', desc='{self.description}')"
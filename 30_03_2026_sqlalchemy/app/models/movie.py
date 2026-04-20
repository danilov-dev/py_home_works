from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core import Base

if TYPE_CHECKING:
    from .genre import Genre

class Movie(Base):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey('genres.id'))
    genre: Mapped["Genre"] = relationship("Genre", back_populates="movies")

    def __repr__(self):
        g_name = self.genre.name if self.genre else 'N/A'
        return f"Movie(title='{self.title}', genre='{g_name}', year={self.year}, rating={self.rating})"
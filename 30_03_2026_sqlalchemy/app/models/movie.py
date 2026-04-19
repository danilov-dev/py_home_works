from ..core import Base
from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    genre: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"Фильм (Название:'{self.title}', Жанр='{self.genre}', Год={self.year}, Рейтинг={self.rating})"
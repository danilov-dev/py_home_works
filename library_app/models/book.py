from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from library_app.models.base import Base


class Book(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    isbn: Mapped[str] = mapped_column(String(17), unique=True, nullable=True)

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('authors.id'))
    author: Mapped["Author"] = relationship("Author", back_populates="books")

from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from library_app.models.base import Base

class Author(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")
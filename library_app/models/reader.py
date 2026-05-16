from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from library_app.models.base import Base

class Reader(Base):
    __tablename__ = 'readers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(150),unique=True, nullable=False)
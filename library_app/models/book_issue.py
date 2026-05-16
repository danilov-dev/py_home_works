from datetime import date
from sqlalchemy import Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from library_app.models.base import Base


class BookIssue(Base):
    __tablename__ = 'book_issues'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id'), nullable=False)
    reader_id: Mapped[int] = mapped_column(Integer, ForeignKey('readers.id'), nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    book: Mapped["Book"] = relationship("Book")
    reader: Mapped["Reader"] = relationship("Reader")
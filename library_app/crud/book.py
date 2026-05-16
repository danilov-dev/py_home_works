import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from library_app.models import Book


class BookRepository:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    def add_book(self, book: Book):
        self.session.add(book)
        return book

    def get_all_books(self) -> List[Book]:
        return self.session.scalars(select(Book).options(joinedload(Book.author))).all()

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.session.scalars(
            select(Book).options(joinedload(Book.author)).where(Book.id == book_id)
        ).one_or_none()

    def update_book(self, book_id: int, **kwargs) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if not book:
            self.logger.warning("Book not found")
            return None

        for key, value in kwargs.items():
            setattr(book, key, value)
        return book

    def delete_book(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if not book:
            self.logger.warning("Book not found")
            return False
        self.session.delete(book)
        return True

import logging
from typing import List, Optional
from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from library_app.crud.author import AuthorRepository
from library_app.crud.book import BookRepository
from library_app.crud.reader import ReaderRepository
from library_app.models import Base, Author, Book, Reader


class LibraryManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=False)
        self.session_factory = sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )
        self.logger = logging.getLogger(__name__)

    def create_tables(self):
        if self.engine:
            Base.metadata.create_all(bind=self.engine)

    def add_author(self, name: str) -> Optional[Author]:
        with self.session_factory() as session:
            author_repository = AuthorRepository(session)
            new_author = Author(name=name)
            try:
                result = author_repository.add_author(new_author)
                session.commit()
                return result
            except SQLAlchemyError as e:
                session.rollback()
                print(e)
                return None

    def get_all_authors(self) -> Optional[List[Author]]:
        with self.session_factory() as session:
            author_repository = AuthorRepository(session)
            try:
                return author_repository.get_all_authors()
            except SQLAlchemyError as e:
                print(e)
                return None

    def get_author_by_id(self, author_id: int) -> Optional[Author]:
        with self.session_factory() as session:
            author_repository = AuthorRepository(session)
            try:
                return author_repository.get_author_by_id(author_id)
            except SQLAlchemyError as e:
                print(e)
                return None

    def update_author(self, author_id: int, new_name: str) -> Optional[Author]:
        with self.session_factory() as session:
            author_repository = AuthorRepository(session)
            try:
                result = author_repository.update_author(author_id, new_name)
                session.commit()
                return result
            except SQLAlchemyError as e:
                session.rollback()
                print(e)
                return None

    def delete_author(self, author_id: int) -> bool:
        with self.session_factory() as session:
            author_repository = AuthorRepository(session)
            try:
                result = author_repository.delete_author(author_id)
                session.commit()
                return result
            except SQLAlchemyError as e:
                session.rollback()
                print(e)
                return False

    def add_book(self, title, author_id, year, isbn=None) -> Optional[Book]:
        new_book = Book(title=title, author_id=author_id, year=year)
        with self.session_factory() as session:
            book_repository = BookRepository(session)
            author_repository = AuthorRepository(session)
            try:
                author = author_repository.get_author_by_id(author_id)
                if author:
                    new_book.author = author
                book_repository.add_book(new_book)
                session.commit()
                return new_book
            except SQLAlchemyError as e:
                self.logger.error(e)
                session.rollback()
                return None

    def get_all_books(self) -> Optional[List[Book]]:
        with self.session_factory() as session:
            book_repository = BookRepository(session)
            try:
                books = book_repository.get_all_books()
                return books
            except SQLAlchemyError as e:
                self.logger.error(e)
                return None

    def find_book_by_id(self, book_id) -> Optional[Book]:
        with self.session_factory() as session:
            book_repository = BookRepository(session)
            try:
                book = book_repository.get_by_id(book_id)
                return book
            except SQLAlchemyError as e:
                self.logger.error(e)
                return None

    def update_book(self, book_id, new_title=None, new_year=None, new_isbn=None) -> Optional[Book]:
        with self.session_factory() as session:
            book_repository = BookRepository(session)
            try:
                updates_fields = {k: v for k, v in {
                    'title': new_title,
                    'year': new_year,
                    'isbn': new_isbn,
                }.items() if v is not None}

                if not updates_fields:
                    return book_repository.get_by_id(book_id)

                updated_book = book_repository.update_book(book_id, **updates_fields)
                session.commit()
                return updated_book
            except SQLAlchemyError as e:
                self.logger.error(e)
                return None

    def delete_book(self, book_id) -> bool:
        with self.session_factory() as session:
            book_repository = BookRepository(session)
            try:
                success = book_repository.delete_book(book_id)
                session.commit()
                return success
            except SQLAlchemyError as e:
                self.logger.error(e)
                return False

    def add_reader(self, first_name, last_name, email) -> Optional[Reader]:
        with self.session_factory() as session:
            reader_repository = ReaderRepository(session)
            try:
                new_reader = Reader(first_name=first_name, last_name=last_name, email=email)
                reader_repository.add_reader(new_reader)
                session.commit()
                return new_reader
            except SQLAlchemyError as e:
                self.logger.error(e)
                return None

    def get_readers(self) -> Optional[List[Reader]]:
        with self.session_factory() as session:
            reader_repository = ReaderRepository(session)
            try:
                readers = reader_repository.get_all()
                return readers
            except SQLAlchemyError as e:
                self.logger.error(e)
                return None

    def find_reader_by_id(self, reader_id) -> Optional[Reader]:
        with self.session_factory() as session:
            reader_repository = ReaderRepository(session)
            try:
                reader = reader_repository.get_by_id(reader_id)
                return reader
            except SQLAlchemyError as e:
                self.logger.error(e)
                return None
    def update_reader(self, reader_id, new_first_name=None, new_last_name=None, new_email=None):
        with self.session_factory() as session:
            reader_repository = ReaderRepository(session)
            try:
                updates_fields = {k:v for k, v in {
                    'first_name': new_first_name,
                    'last_name': new_last_name,
                    'email': new_email,
                }.items() if v is not None}

                if not updates_fields:
                    return reader_repository.get_by_id(reader_id)
                updated_reader = reader_repository.update_reader(reader_id, **updates_fields)
                session.commit()
                return updated_reader
            except SQLAlchemyError as e:
                self.logger.error(e)
                return None

    def delete_reader(self, reader_id) -> bool:
        with self.session_factory() as session:
            reader_repository = ReaderRepository(session)
            try:
                success = reader_repository.delete_reader(reader_id)
                session.commit()
                return success
            except SQLAlchemyError as e:
                self.logger.error(e)
                return False
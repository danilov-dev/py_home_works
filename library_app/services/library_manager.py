import logging
from datetime import date
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, selectinload
from library_app.models.base import Base
from library_app.models.author import Author
from library_app.models.book import Book
from library_app.models.reader import Reader
from library_app.models.book_issue import BookIssue

logger = logging.getLogger(__name__)


class LibraryManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Создаёт все таблицы, определённые в моделях"""
        Base.metadata.create_all(self.engine)
        logger.info("Таблицы созданы")

    # === АВТОРЫ ===
    def add_author(self, name: str) -> Author:
        with self.Session() as session:
            author = Author(name=name)
            session.add(author)
            session.commit()
            session.refresh(author)
            return author

    def find_author_by_id(self, author_id: int) -> Author | None:
        with self.Session() as session:
            return session.get(Author, author_id)

    def update_author(self, author_id: int, new_name: str) -> Author | None:
        with self.Session() as session:
            author = session.get(Author, author_id)
            if author:
                author.name = new_name
                session.commit()
                session.refresh(author)
            return author

    def delete_author(self, author_id: int) -> bool:
        with self.Session() as session:
            author = session.get(Author, author_id)
            if author:
                session.delete(author)
                session.commit()
                return True
            return False

    # === КНИГИ ===
    def add_book(self, title: str, author_id: int, year: int, isbn: str | None = None) -> Book:
        with self.Session() as session:
            book = Book(title=title, author_id=author_id, year=year, isbn=isbn)
            session.add(book)
            session.commit()
            session.refresh(book)
            # Подгружаем автора сразу
            return session.query(Book).options(selectinload(Book.author)).filter(Book.id == book.id).first()

    def find_book_by_id(self, book_id: int) -> Book | None:
        with self.Session() as session:
            return session.query(Book).options(selectinload(Book.author)).get(book_id)

    def get_all_books(self) -> list[Book]:
        with self.Session() as session:
            return session.query(Book).options(selectinload(Book.author)).all()

    def update_book(self, book_id: int, new_title: str | None = None, new_year: int | None = None) -> Book | None:
        with self.Session() as session:
            book = session.get(Book, book_id)
            if book:
                if new_title:
                    book.title = new_title
                if new_year:
                    book.year = new_year
                session.commit()
                session.refresh(book)
                return session.query(Book).options(selectinload(Book.author)).get(book_id)
            return None

    def delete_book(self, book_id: int) -> bool:
        with self.Session() as session:
            book = session.get(Book, book_id)
            if book:
                session.delete(book)
                session.commit()
                return True
            return False

    # === ЧИТАТЕЛИ ===
    def add_reader(self, first_name: str, last_name: str, email: str) -> Reader:
        with self.Session() as session:
            reader = Reader(first_name=first_name, last_name=last_name, email=email)
            session.add(reader)
            session.commit()
            session.refresh(reader)
            return reader

    def find_reader_by_id(self, reader_id: int) -> Reader | None:
        with self.Session() as session:
            return session.get(Reader, reader_id)

    def update_reader(self, reader_id: int, new_email: str | None = None) -> Reader | None:
        with self.Session() as session:
            reader = session.get(Reader, reader_id)
            if reader and new_email:
                reader.email = new_email
                session.commit()
                session.refresh(reader)
            return reader

    def delete_reader(self, reader_id: int) -> bool:
        with self.Session() as session:
            reader = session.get(Reader, reader_id)
            if reader:
                session.delete(reader)
                session.commit()
                return True
            return False

    # === ВЫДАЧА КНИГ (BookIssue) ===
    def issue_book_to_reader(self, book_id: int, reader_id: int) -> BookIssue:
        """Выдаёт книгу читателю. Проверяет, не выдана ли книга уже."""
        with self.Session() as session:
            # Проверка: есть ли активная выдача этой книги
            active_issue = session.query(BookIssue).filter(
                BookIssue.book_id == book_id,
                BookIssue.return_date.is_(None)
            ).first()

            if active_issue:
                raise ValueError(
                    f"⚠️ Книга с ID {book_id} уже выдана (запись #{active_issue.id}) и не возвращена."
                )

            new_issue = BookIssue(
                book_id=book_id,
                reader_id=reader_id,
                issue_date=date.today()
            )
            session.add(new_issue)
            session.commit()

            # Возвращаем объект с подгруженными связями
            return session.query(BookIssue).options(
                selectinload(BookIssue.book),
                selectinload(BookIssue.reader)
            ).filter(BookIssue.id == new_issue.id).first()

    def return_book_from_reader(self, issue_id: int) -> BookIssue:
        """Возвращает книгу: устанавливает return_date = сегодня."""
        with self.Session() as session:
            issue = session.query(BookIssue).options(
                selectinload(BookIssue.book),
                selectinload(BookIssue.reader)
            ).get(issue_id)

            if not issue:
                raise ValueError(f"Запись выдачи #{issue_id} не найдена.")
            if issue.return_date is not None:
                raise ValueError("Эта книга уже была возвращена ранее.")

            issue.return_date = date.today()
            session.commit()
            session.refresh(issue)
            return issue

    def get_active_issues(self) -> list[BookIssue]:
        """Возвращает все активные (невозвращённые) выдачи."""
        with self.Session() as session:
            return session.query(BookIssue).options(
                selectinload(BookIssue.book),
                selectinload(BookIssue.reader)
            ).filter(BookIssue.return_date.is_(None)).all()
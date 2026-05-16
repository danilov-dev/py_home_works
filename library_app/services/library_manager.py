import logging
from datetime import date
from sqlalchemy import create_engine
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
        Base.metadata.create_all(self.engine)

    def add_author(self, name: str) -> Author:
        with self.Session() as session:
            author = Author(name=name)
            session.add(author)
            session.commit()
            session.refresh(author)
            return author

    def delete_author(self, author_id: int) -> bool:
        with self.Session() as session:
            author = session.get(Author, author_id)
            if not author:
                raise ValueError(f"Автор с ID {author_id} не найден.")

            has_books = session.query(Book).filter(Book.author_id == author_id).first()
            if has_books:
                raise ValueError(f"Невозможно удалить автора '{author.name}': в базе привязаны книги.")

            session.delete(author)
            session.commit()
            return True

    def add_book(self, title: str, author_id: int, year: int, isbn: str | None = None) -> Book:
        with self.Session() as session:
            book = Book(title=title, author_id=author_id, year=year, isbn=isbn)
            session.add(book)
            session.commit()
            session.refresh(book)
            return session.query(Book).options(selectinload(Book.author)).get(book.id)

    def find_books_by_author_name(self, author_name: str) -> list[Book]:
        with self.Session() as session:
            return session.query(Book).join(Author).filter(Author.name == author_name).all()

    def display_all_books_with_authors(self):
        with self.Session() as session:
            results = session.query(Book.title, Book.year, Author.name).join(Author).all()
            if not results:
                print("В библиотеке нет книг.")
                return

            print("\n--- Все книги с авторами ---")
            for title, year, author_name in results:
                print(f"  {title} ({year}) | Автор: {author_name}")
            print("-" * 35)

    def delete_book(self, book_id: int) -> bool:
        with self.Session() as session:
            book = session.get(Book, book_id)
            if not book:
                raise ValueError(f"Книга с ID {book_id} не найдена.")

            active_issue = session.query(BookIssue).filter(
                BookIssue.book_id == book_id,
                BookIssue.return_date.is_(None)
            ).first()
            if active_issue:
                raise ValueError(f"Невозможно удалить книгу '{book.title}': она выдана читателю и не возвращена.")

            session.delete(book)
            session.commit()
            return True

    def add_reader(self, first_name: str, last_name: str, email: str) -> Reader:
        with self.Session() as session:
            reader = Reader(first_name=first_name, last_name=last_name, email=email)
            session.add(reader)
            session.commit()
            session.refresh(reader)
            return reader

    def delete_reader(self, reader_id: int) -> bool:
        with self.Session() as session:
            reader = session.get(Reader, reader_id)
            if not reader:
                raise ValueError(f"Читатель с ID {reader_id} не найден.")

            active_issue = session.query(BookIssue).filter(
                BookIssue.reader_id == reader_id,
                BookIssue.return_date.is_(None)
            ).first()
            if active_issue:
                raise ValueError(f"Невозможно удалить читателя: у него есть активные выдачи книг.")

            session.delete(reader)
            session.commit()
            return True

    def issue_book_to_reader(self, book_id: int, reader_id: int) -> BookIssue:
        with self.Session() as session:
            active_issue = session.query(BookIssue).filter(
                BookIssue.book_id == book_id,
                BookIssue.return_date.is_(None)
            ).first()

            if active_issue:
                raise ValueError(f"Книга с ID {book_id} уже выдана и не возвращена.")

            new_issue = BookIssue(book_id=book_id, reader_id=reader_id, issue_date=date.today())
            session.add(new_issue)
            session.commit()

            return session.query(BookIssue).options(
                selectinload(BookIssue.book),
                selectinload(BookIssue.reader)
            ).filter(BookIssue.id == new_issue.id).first()

    def return_book_from_reader(self, issue_id: int) -> BookIssue:
        with self.Session() as session:
            issue = session.query(BookIssue).options(
                selectinload(BookIssue.book),
                selectinload(BookIssue.reader)
            ).get(issue_id)

            if not issue:
                raise ValueError(f"Запись выдачи #{issue_id} не найдена.")
            if issue.return_date is not None:
                raise ValueError("Эта книга уже возвращена.")

            issue.return_date = date.today()
            session.commit()
            session.refresh(issue)
            return issue

    def get_active_issues(self) -> list[BookIssue]:
        with self.Session() as session:
            return session.query(BookIssue).options(
                selectinload(BookIssue.book),
                selectinload(BookIssue.reader)
            ).filter(BookIssue.return_date.is_(None)).all()
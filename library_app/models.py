from typing import List, Optional

from sqlalchemy import Integer, String, ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    isbn: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('authors.id'))
    author: Mapped["Author"] = relationship("Author", back_populates="books")

class Reader(Base):
    __tablename__ = 'readers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[String] = mapped_column(String(50), nullable=False)
    last_name: Mapped[String] = mapped_column(String(50), nullable=False)
    email: Mapped[String] = mapped_column(String(150),unique=True, nullable=False)

class LibraryManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=False)
        self.session = sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )
    def create_tables(self):
        if self.engine:
            Base.metadata.create_all(bind=self.engine)

    def add_author(self, name):
        author = Author(name=name)
        with self.session() as session:
            session.add(author)
            session.commit()
        return author

    def get_all_authors(self) -> Optional[List[Author]]:
        try:
            with self.session() as session:
                authors = session.scalars(select(Author)).all()
                return list(authors)
        except Exception as e:
            print(e)

    def get_author_by_id(self, id: int) -> Optional[Author]:
        with self.session() as session:
            author = session.scalar(select(Author).where(Author.id == id))
            return author

    def update_author(self, author_id, new_name) -> Optional[Author]:
        with self.session() as session:
            author = session.scalar(select(Author).where(Author.id == author_id))
            if not author:
                print("Author not found")
            author.name = new_name
            session.commit()
            return author

    def delete_author(self, author_id) -> bool:
        with self.session() as session:
            author = session.scalar(select(Author).where(Author.id == author_id))
            if not author:
                print("Author not found")
                return False
            session.delete(author)
            session.commit()
            return True


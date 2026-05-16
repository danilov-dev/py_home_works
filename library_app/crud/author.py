from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from library_app.models import Author


class AuthorRepository:
    def __init__(self, session):
        self.session = session

    def add_author(self, author: Author) -> Author:
        self.session.add(author)
        return author

    def get_all_authors(self) -> List[Author]:
        authors = self.session.scalars(select(Author)).all()
        return list(authors)

    def get_author_by_id(self, author_id: int) -> Optional[Author]:
        author = self.session.scalar(select(Author).where(Author.id == author_id))
        return author

    def update_author(self, author_id: int, new_name: str) -> Optional[Author]:
        author = self.session.scalar(select(Author).where(Author.id == author_id))
        if not author:
            print("Author not found")
            return None
        author.name = new_name
        return author

    def delete_author(self, author_id: int) -> bool:
        author = self.session.scalar(select(Author).where(Author.id == author_id))
        if not author:
            print("Author not found")
            return False
        self.session.delete(author)
        return True
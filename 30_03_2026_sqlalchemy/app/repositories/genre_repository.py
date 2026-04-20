import logging
from typing import Optional, List, Tuple

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, joinedload

from .base import BaseRepository
from ..models import Genre


class GenreRepository(BaseRepository[Genre]):
    def __init__(self, session_factory: sessionmaker):
        super().__init__(Genre, session_factory)
        self.logger = logging.getLogger(__name__)

    def get_by_name(self, name: str) -> Optional[Genre]:
        with self.session_factory() as session:
            return session.scalar(select(Genre).where(Genre.name == name))

    def update_name(self, genre_id: int, new_name: str) -> Optional[Genre]:
        with self.session_factory() as session:
            genre = session.get(Genre, genre_id)
            if genre:
                genre.name = new_name
                session.commit()
                session.refresh(genre)
            return genre

    def update_description(self, genre_id: int, new_desc: str) -> Optional[Genre]:
        with self.session_factory() as session:
            genre = session.get(Genre, genre_id)
            if genre:
                genre.description = new_desc
                session.commit()
                session.refresh(genre)
            return genre

    def get_genres_with_movies_count(self) -> List[Tuple[Genre, int]]:
        with self.session_factory() as session:
            genres = session.scalars(
                select(Genre).options(joinedload(Genre.movies))
            ).unique().all()
            return [(genre, len(genre.movies)) for genre in genres]
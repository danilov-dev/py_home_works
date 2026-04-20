import logging
from typing import List, Optional, Tuple

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from ..models import Genre
from ..repositories import GenreRepository

logger = logging.getLogger(__name__)


class GenreService:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def create_genre(self, name: str, description: str) -> Optional[Genre]:
        """Создать и записать жанр"""
        if not name.strip():
            logger.error("Передано пустое название жанра")
            raise ValueError("Название не может быть пустым")

        new_genre = {'name': name,
                     'description': description
                     }
        repo = GenreRepository(self.session_factory)
        try:
            success = repo.create(new_genre)
            logger.info(f"Жанр '{name}' добавлен")
            return new_genre if success else None
        except SQLAlchemyError as e:
            logger.error(e)

    def get_all_genre(self) -> list[Genre] | None:
        """Получить все жанры"""
        repo = GenreRepository(self.session_factory)
        try:
            return repo.get_all()
        except SQLAlchemyError as e:
            logger.error(e)

    def get_by_id(self, movie_id: int) -> Optional[Genre]:
        """Получить фильм по ID"""
        repo = GenreRepository(self.session_factory)
        try:
            return repo.get_by_id(movie_id)
        except SQLAlchemyError as e:
            logger.error(e)
            raise


    def get_genre_by_name(self, name: str) -> Optional[Genre]:
        """Получить фильм по названию"""
        try:
            repo = GenreRepository(self.session_factory)
            return repo.get_by_name(name)
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def update_name(self, genre_id: int, new_name: str) -> Optional[Genre]:
        """Обновить название жанра"""
        try:
            repo = GenreRepository(self.session_factory)
            movie = repo.update(genre_id, name=new_name)
            if movie is None:
                raise ValueError(f"Жанр с ID: {genre_id} не найден")
            return movie
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def update_description(self, genre_id: int, new_description: str) -> Optional[Genre]:
        """Обновить жанр фильма"""
        try:
            repo = GenreRepository(self.session_factory)
            movie = repo.update(genre_id, description=new_description)
            if movie is None:
                raise ValueError(f"Фильм с ID: {genre_id} не найден")
            return movie
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def delete_by_id(self, genre_id: int) -> None:
        try:
            repo = GenreRepository(self.session_factory)
            success = repo.delete(genre_id)
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def get_genres_with_movies_count(self) ->  List[Tuple[Genre, int]]:
        try:
            repo = GenreRepository(self.session_factory)
            return repo.get_genres_with_movies_count()
        except SQLAlchemyError as e:
            logger.error(e)
            raise

import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from ..models import Movie
from ..repositories import MovieRepository

logger = logging.getLogger(__name__)


class MovieService:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def create_movie(self, title: str, genre: str, year: int, duration: int, rating: float) -> Optional[Movie]:
        """Создать и записать фильм"""
        if not title.strip():
            logger.error("Название не может быть пустым")
            raise ValueError("Название не может быть пустым")

        new_movie = Movie(title=title, genre=genre, year=year, duration=duration, rating=rating)
        repo = MovieRepository(self.session_factory)
        try:
            success = repo.add(new_movie)
            logger.info(f"Фильм '{title}' добавлен")
            return new_movie if success else None
        except SQLAlchemyError as e:
            logger.error(e)

    def get_all_movies(self) -> list[Movie] | None:
        """Получить все фильмы"""
        repo = MovieRepository(self.session_factory)
        try:
            return repo.get_all()
        except SQLAlchemyError as e:
            logger.error(e)

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        """Получить фильм по ID"""
        repo = MovieRepository(self.session_factory)
        try:
            return repo.get_by_id(movie_id)
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def get_movies_by_genre(self, genre: str) -> Optional[List[Movie]]:
        """Получить фильмы по жанру"""
        try:
            repo = MovieRepository(self.session_factory)
            return repo.get_by_genre(genre)
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def get_movie_by_title(self, title: str) -> Optional[Movie]:
        """Получить фильм по названию"""
        try:
            repo = MovieRepository(self.session_factory)
            return repo.get_by_title(title)
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def get_high_rated_movies(self, rating: float) -> Optional[List[Movie]]:
        """Получить фильмы по рейтингу"""
        try:
            repo = MovieRepository(self.session_factory)
            return repo.get_by_rating(rating)
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def get_movies_after_year(self, year: int) -> List[Movie]:
        """Получить фильмы вышедшие после заданного года"""
        try:
            repo = MovieRepository(self.session_factory)
            return repo.get_by_year(year)
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def update_rating(self, movie_id: int, rating: float) -> Optional[Movie]:
        """Обновить рейтинг фильма"""
        try:
            repo = MovieRepository(self.session_factory)
            movie = repo.update(movie_id, rating=rating)
            if movie is None:
                raise ValueError(f"Фильм с ID: {movie_id} не найден")
            return movie
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def update_genre(self, movie_id: int, genre: str) -> Optional[Movie]:
        """Обновить жанр фильма"""
        try:
            repo = MovieRepository(self.session_factory)
            movie = repo.update(movie_id, genre=genre)
            if movie is None:
                raise ValueError(f"Фильм с ID: {movie_id} не найден")
            return movie
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def update_availability(self, movie_id: int, is_available: bool) -> Optional[Movie]:
        """Обновить доступность фильма"""
        try:
            repo = MovieRepository(self.session_factory)
            movie = repo.update(movie_id, is_available=is_available)
            if movie is None:
                raise ValueError(f"Фильм с ID: {movie_id} не найден")
            return movie
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def full_update(self, movie_id: int, **kwargs) -> Optional[Movie]:
        """Полное обновление фильма"""
        try:
            repo = MovieRepository(self.session_factory)
            movie = repo.update(movie_id, **kwargs)
            if movie is None:
                raise ValueError(f"Фильм с ID: {movie_id} не найден")
            return movie
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def delete_by_id(self, movie_id: int) -> None:
        try:
            repo = MovieRepository(self.session_factory)
            success = repo.delete_by_id(movie_id)
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def delete_by_title(self, movie_title: str) -> None:
        try:
            repo = MovieRepository(self.session_factory)
            success = repo.delete_by_title(movie_title)
        except SQLAlchemyError as e:
            logger.error(e)
            raise

    def soft_delete(self, movie_id: int) -> None:
        try:
            repo = MovieRepository(self.session_factory)
            movie = repo.update(movie_id, is_available=False)
            if movie is None:
                raise ValueError(f"Фильм с ID: {movie_id} не найден")
        except SQLAlchemyError as e:
            logger.error(e)
            raise




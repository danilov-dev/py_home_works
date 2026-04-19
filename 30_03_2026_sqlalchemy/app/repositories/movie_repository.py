import logging
from typing import List, Optional

from ..models import Movie
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker


class MovieRepository:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> List[Movie]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос полного списка фильмов")
            return list(session.scalars(select(Movie)).all())

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос фильма по ID - {movie_id}")
            return session.scalar(select(Movie).where(Movie.id == movie_id))

    def get_by_genre(self, genre: str) -> Optional[List[Movie]]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос списка фильмов по жанру - {genre}")
            return list(session.scalars(select(Movie).where(Movie.genre == genre)).all())

    def get_by_rating(self, min_rating: float) -> List[Movie]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос списка фильмов выше {min_rating} рейтинга")
            return list(session.scalars(select(Movie).where(Movie.rating >= min_rating)).all())

    def get_by_year(self, year: int) -> List[Movie]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос списка фильмов с {year} года")
            return list(session.scalars(select(Movie).where(Movie.year > year)).all())

    def add(self, new_movie: Movie) -> bool:
        with self.session_factory() as session:
            try:
                session.add(new_movie)
                session.commit()
                session.refresh(new_movie)
                self.logger.info(f"Фильм {new_movie.id} - {new_movie.title} успешно добавлен")
                return True
            except IntegrityError:
                session.rollback()
                return False

    def get_by_title(self, title: str) -> Optional[Movie]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос фильма по названию - {title}")
            return session.scalar(select(Movie).where(Movie.title == title))

    def update(self, movie_id: int, **kwargs) -> Optional[Movie]:
        with self.session_factory() as session:
            movie = self.get_by_id(movie_id)
            if not movie:
                self.logger.error(f"Фильм с ID '{movie_id}' не найден")
                return None

            for field, value in kwargs.items():
                if hasattr(movie, field):
                    old_value = getattr(movie, field)
                    setattr(movie, field, value)
                    self.logger.info(f"Фильм '{movie_id}' - поле '{field}': '{old_value}' -> '{value}'")

            session.commit()
            self.logger.info(f"Фильм с ID '{movie_id}' обновлен")
            return movie

    def delete_by_title(self, movie_title: str) -> bool:
        with self.session_factory() as session:
            movie = session.scalar(select(Movie).where(Movie.title == movie_title))
            if not movie:
                self.logger.error(f"Фильм - '{movie_title}' не найден")
                return False
            session.delete(movie)
            session.commit()
            self.logger.info(f"Фильм - '{movie_title}' удален")
            return True

    def delete_by_id(self, movie_id: int) -> bool:
        with self.session_factory() as session:
            movie = self.get_by_id(movie_id)
            if not movie:
                self.logger.error(f"Фильм ID: '{movie_id}' не найден")
                return False
            session.delete(movie)
            session.commit()
            self.logger.info(f"Фильм ID: '{movie_id}' удален")
            return True


import logging
from typing import List, Optional

from ..models import Movie, Genre
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, joinedload

from .base import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    def __init__(self, session_factory: sessionmaker):
        super().__init__(Movie, session_factory)
        self.session_factory = session_factory
        self.logger = logging.getLogger(__name__)

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Movie]:
        with self.session_factory() as session:
            stmt = select(Movie).offset(offset).limit(limit).options(joinedload(Movie.genre))
            return list(session.scalars(stmt).all())

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        with self.session_factory() as session:
            stmt = select(Movie).options(joinedload(Movie.genre)).where(Movie.id == movie_id)
            return session.scalar(stmt)

    def get_by_genre(self, genre: str) -> Optional[List[Movie]]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос списка фильмов по жанру - {genre}")
            return list(session.scalars(
            select(Movie)
            .options(joinedload(Movie.genre))
            .where(Movie.genre.has(name=genre))
        ))

    def get_by_rating(self, min_rating: float) -> List[Movie]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос списка фильмов выше {min_rating} рейтинга")
            return list(session.scalars(select(Movie).options(joinedload(Movie.genre)).where(Movie.rating >= min_rating)).all())

    def get_by_year(self, year: int) -> List[Movie]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос списка фильмов с {year} года")
            return list(session.scalars(select(Movie).options(joinedload(Movie.genre)).where(Movie.year > year)).all())

    def get_by_title(self, title: str) -> Optional[Movie]:
        with self.session_factory() as session:
            self.logger.info(f"Запрос фильма по названию - {title}")
            return session.scalar(select(Movie).options(joinedload(Movie.genre)).where(Movie.title == title))

    def create_with_genre_name(self, obj_in: dict) -> Movie:
        with self.session_factory() as session:
            genre_name = obj_in.get("genre")
            if not genre_name:
                raise ValueError("Название жанра не должно быть пустым")

            genre = session.scalar(select(Genre).where(Genre.name == genre_name))
            if not genre:
                raise ValueError(f"Жанр '{obj_in.get("genre")}' не найден в базе")

            movie = Movie(
                title=obj_in["title"],
                year=obj_in["year"],
                duration=obj_in["duration"],
                rating=obj_in["rating"],
                genre=genre
            )
            session.add(movie)
            session.commit()
            session.refresh(movie)
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

    def full_update(self, movie_id: int, **kwargs) -> Optional[Movie]:
        with self.session_factory() as session:
            movie = session.scalar(select(Movie).where(Movie.id == movie_id))
            if not movie:
                raise ValueError("Movie not found")
            kwargs["genre"] = session.scalar(select(Genre).where(Genre.name == kwargs.get("genre")))
            for field, value in kwargs.items():
                setattr(movie, field, value)
            session.commit()
            return movie



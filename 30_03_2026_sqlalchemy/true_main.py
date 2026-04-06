from typing import List, Optional
from sqlalchemy import create_engine, select, String, Integer, Boolean, Float
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    genre: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"Фильм (Название:'{self.title}', Жанр='{self.genre}', Год={self.year}, Рейтинг={self.rating})"


engine = create_engine("sqlite:///cinema.db", echo=False)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)


class MovieRepository:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def get_all(self) -> List[Movie]:
        with self.session_factory() as session:
            return list(session.scalars(select(Movie)).all())

    def get_by_id(self, id: int) -> Optional[Movie]:
        with self.session_factory() as session:
            return session.scalar(select(Movie).where(Movie.id == id))

    def get_by_genre(self, genre: str) -> List[Movie]:
        with self.session_factory() as session:
            return list(session.scalars(select(Movie).where(Movie.genre == genre)).all())

    def get_by_rating(self, min_rating: float) -> List[Movie]:
        with self.session_factory() as session:
            return list(session.scalars(select(Movie).where(Movie.rating >= min_rating)).all())

    def get_by_year(self, year: int) -> List[Movie]:
        with self.session_factory() as session:
            return list(session.scalars(select(Movie).where(Movie.year > year)).all())

    def add(self, new_movie: Movie) -> bool:
        with self.session_factory() as session:
            try:
                session.add(new_movie)
                session.commit()
                session.refresh(new_movie)
                return True
            except IntegrityError:
                session.rollback()
                return False

    def get_by_title(self, title: str) -> Optional[Movie]:
        with self.session_factory() as session:
            return session.scalar(select(Movie).where(Movie.title == title))


class MovieService:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    def create_movie(self, title: str, genre: str, year: int, duration: int, rating: float) -> Optional[Movie]:
        if not title.strip():
            raise ValueError("Название не может быть пустым")
        new_movie = Movie(title=title, genre=genre, year=year, duration=duration, rating=rating)
        success = self.repository.add(new_movie)
        return new_movie if success else None

    def get_all_movies(self) -> List[Movie]: return self.repository.get_all()

    def get_movies_by_genre(self, genre: str) -> List[Movie]: return self.repository.get_by_genre(genre)

    def get_high_rated_movies(self, rating: float) -> List[Movie]: return self.repository.get_by_rating(rating)

    def get_movies_after_year(self, year: int) -> List[Movie]: return self.repository.get_by_year(year)

    def get_movie_by_title(self, title: str) -> Optional[Movie]: return self.repository.get_by_title(title)


def print_movies(movies: List[Movie], header: str) -> None:
    print(f"\n{'=' * 60}\n{header}\n{'=' * 60}")
    if movies:
        for m in movies: print(m)
    else:
        print("Ничего не найдено")
    print('=' * 60)


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    repo = MovieRepository(SessionFactory)
    service = MovieService(repo)

    print("Добавляем фильмы...")
    service.create_movie("Побег из Шоушенка", "Drama", 1994, 142, 9.3)
    service.create_movie("Тёмный рыцарь", "Action", 2008, 152, 9.0)
    service.create_movie("Начало", "Sci-Fi", 2010, 148, 8.8)
    service.create_movie("Криминальное чтиво", "Crime", 1994, 154, 8.9)
    service.create_movie("Матрица", "Sci-Fi", 1999, 136, 8.7)
    print("Готово\n")

    print_movies(service.get_all_movies(), "ВСЕ ФИЛЬМЫ")
    print_movies(service.get_movies_by_genre("Sci-Fi"), "ЖАНР: Sci-Fi")
    print_movies(service.get_high_rated_movies(9.0), "РЕЙТИНГ >= 9.0")
    print_movies(service.get_movies_after_year(2005), "ПОСЛЕ 2005 ГОДА")

    movie = service.get_movie_by_title("Матрица")
    print_movies([movie] if movie else [], "ПО НАЗВАНИЮ: Матрица")
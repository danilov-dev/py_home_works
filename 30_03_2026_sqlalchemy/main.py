from sqlalchemy import create_engine, String, Float, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import List, Optional


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"Movie(id={self.id}, title='{self.title}', genre='{self.genre}', year={self.year}, rating={self.rating})"


engine = create_engine("sqlite:///movies.db", echo=False)


def create_movie(title: str, genre: str, year: int, duration: int, rating: float) -> Movie:
    movie = Movie(
        title=title,
        genre=genre,
        year=year,
        duration=duration,
        rating=rating
    )
    with Session(engine) as session:
        session.add(movie)
        session.commit()
        session.refresh(movie)
    return movie


def get_all_movies() -> List[Movie]:
    with Session(engine) as session:
        return session.query(Movie).all()


def get_movies_by_genre(genre_name: str) -> List[Movie]:
    with Session(engine) as session:
        return session.query(Movie).filter(Movie.genre == genre_name).all()


def get_high_rated_movies(min_rating: float) -> List[Movie]:
    with Session(engine) as session:
        return session.query(Movie).filter(Movie.rating >= min_rating).all()


def get_movies_after_year(year: int) -> List[Movie]:
    with Session(engine) as session:
        return session.query(Movie).filter(Movie.year > year).all()


def get_movie_by_title(title: str) -> Optional[Movie]:
    with Session(engine) as session:
        return session.query(Movie).filter(Movie.title == title).first()


def print_movies(movies: List[Movie], header: str) -> None:
    print(f"\n{'=' * 60}")
    print(header)
    print('=' * 60)
    if movies:
        for movie in movies:
            print(movie)
    else:
        print("No movies found")
    print('=' * 60)


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    print("Adding movies to database...")
    create_movie("The Shawshank Redemption", "Drama", 1994, 142, 9.3)
    create_movie("The Dark Knight", "Action", 2008, 152, 9.0)
    create_movie("Inception", "Sci-Fi", 2010, 148, 8.8)
    create_movie("Pulp Fiction", "Crime", 1994, 154, 8.9)
    create_movie("The Matrix", "Sci-Fi", 1999, 136, 8.7)
    create_movie("Interstellar", "Sci-Fi", 2014, 169, 8.6)
    create_movie("The Godfather", "Crime", 1972, 175, 9.2)

    print("✓ Movies added successfully!\n")


    print_movies(get_all_movies(), "ALL MOVIES")

    print_movies(get_movies_by_genre("Sci-Fi"), "MOVIES BY GENRE: Sci-Fi")

    print_movies(get_high_rated_movies(9.0), "HIGH RATED MOVIES (rating >= 9.0)")

    print_movies(get_movies_after_year(2005), "MOVIES AFTER 2005")

    movie = get_movie_by_title("Inception")
    print(f"\n{'=' * 60}")
    print("MOVIE BY TITLE: Inception")
    print('=' * 60)
    print(movie if movie else "Movie not found")
    print('=' * 60)
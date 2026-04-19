from typing import List, Optional
from ..models import Movie


class MovieViewer:
    def print_header(self, text: str) -> None:
        print(f"\n{'=' * 60}")
        print(f"{text:^60}")
        print(f"{'=' * 60}")

    def print_one(self, movie: Optional[Movie]) -> None:
        if not movie:
            print("Фильм не найден.")
            return
        print(f"ID: {movie.id}")
        print(f"Название: {movie.title}")
        print(f"Жанр: {movie.genre}")
        print(f"Год: {movie.year}")
        print(f"Длительность: {movie.duration} мин.")
        print(f"Рейтинг: {movie.rating}")
        print(f"В прокате: {'Да' if movie.is_available else 'Нет'}")
        print("-" * 30)

    def print_all(self, movies: List[Movie]) -> None:
        if not movies:
            print("Список фильмов пуст.")
            return
        for m in movies:
            status = "В прокате" if m.is_available else "Снят"
            print(f"[{m.id:2}] {m.title:<25} ({m.year}) | {m.genre:<10} | {m.rating} | {status}")
        print(f"\nВсего: {len(movies)} фильм(ов)")
        print("=" * 60)

    def print_statistics(self, movies: List[Movie]) -> None:
        if not movies:
            print("Нет данных для статистики.")
            return

        avg_rating = sum(m.rating for m in movies) / len(movies)
        max_rating = max(m.rating for m in movies)
        min_rating = min(m.rating for m in movies)
        available = sum(1 for m in movies if m.is_available)
        total_duration = sum(m.duration for m in movies)

        print("СТАТИСТИКА БАЗЫ ДАННЫХ")
        print(f"Всего фильмов: {len(movies)}")
        print(f"Доступно: {available} | Снято: {len(movies) - available}")
        print(f"Общий хронометраж: {total_duration} мин.")
        print(f"Средний рейтинг: {avg_rating:.2f}")
        print(f"Макс. рейтинг: {max_rating} | Мин. рейтинг: {min_rating}")
        print("=" * 60)
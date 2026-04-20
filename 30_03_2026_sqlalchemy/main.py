import logging
from app.core import init_db, session_maker
from app.services import MovieService, GenreService
from app.utils.movie_viewer import MovieViewer

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(filename='app.log')],
    )

    init_db()
    movie_service = MovieService(session_maker)
    genre_service = GenreService(session_maker)
    viewer = MovieViewer()

    viewer.print_header("ДОБАВЛЕНИЕ ЖАНРОВ")
    g1 = genre_service.create_genre("Drama", "Серьёзные сюжетные линии")
    g2 = genre_service.create_genre("Sci-Fi", "Научная фантастика и космос")
    g3 = genre_service.create_genre("Action", "Динамичные бои и погони")
    g4 = genre_service.create_genre("Crime", "Лихо закрученный сюжет про преступников")
    print("Жанры созданы.\n")

    viewer.print_header("СОЗДАНИЕ ФИЛЬМОВ")

    m1 = movie_service.create_movie("Побег из Шоушенка", "Drama", 1994, 142, 9.3)
    m2 = movie_service.create_movie("Тёмный рыцарь", "Action", 2008, 152, 9.0)
    m3 = movie_service.create_movie("Начало", "Sci-Fi", 2010, 148, 8.8)
    m4 = movie_service.create_movie("Криминальное чтиво", "Crime", 1994, 154, 8.9)
    m5 = movie_service.create_movie("Матрица", "Sci-Fi", 1999, 136, 8.7)
    print("Фильмы успешно добавлены в базу.\n")


    viewer.print_header("ПРОСМОТР: ВСЕ ФИЛЬМЫ")
    viewer.print_all(movie_service.get_all_movies())

    viewer.print_header("ПРОСМОТР: ЖАНР Sci-Fi")
    viewer.print_all(movie_service.get_movies_by_genre("Sci-Fi"))

    viewer.print_header("ПРОСМОТР: РЕЙТИНГ >= 9.0")
    viewer.print_all(movie_service.get_high_rated_movies(9.0))

    viewer.print_header("ПРОСМОТР: ПОСЛЕ 2005 ГОДА")
    viewer.print_all(movie_service.get_movies_after_year(2005))

    viewer.print_header("ПРОСМОТР: ПО НАЗВАНИЮ")
    viewer.print_one(movie_service.get_movie_by_title("Матрица"))

    viewer.print_header("ОБНОВЛЕНИЕ: РЕЙТИНГ МАТРИЦЫ")
    matrix = movie_service.get_movie_by_title("Матрица")
    if matrix:
        movie_service.update_rating(matrix.id, 8.9)
        viewer.print_one(movie_service.get_by_id(matrix.id))

    viewer.print_header("ОБНОВЛЕНИЕ: ЖАНР ТЁМНОГО РЫЦАРЯ")
    dk = movie_service.get_movie_by_title("Тёмный рыцарь")
    if dk:
        movie_service.update_genre(dk.id, "Action")
        viewer.print_one(movie_service.get_by_id(dk.id))

    viewer.print_header("ОБНОВЛЕНИЕ: СТАТУС ДОСТУПНОСТИ")
    matrix = movie_service.get_movie_by_title("Матрица")
    if matrix:
        movie_service.update_availability(matrix.id, False)
        viewer.print_one(movie_service.get_by_id(matrix.id))

    viewer.print_header("ПОЛНОЕ ОБНОВЛЕНИЕ")
    shawshank = movie_service.get_movie_by_title("Побег из Шоушенка")
    if shawshank:
        movie_service.full_update(shawshank.id, genre="Drama", rating=9.5, duration=145)
        viewer.print_one(movie_service.get_by_id(shawshank.id))

    viewer.print_header("УДАЛЕНИЕ: SOFT DELETE (Матрица)")
    matrix = movie_service.get_movie_by_title("Матрица")
    if matrix:
        movie_service.soft_delete(matrix.id)
        viewer.print_one(movie_service.get_by_id(matrix.id))

    viewer.print_header("УДАЛЕНИЕ: ПО ID (Начало)")
    inception = movie_service.get_movie_by_title("Начало")
    if inception:
        movie_service.delete_by_id(inception.id)
        print("Фильм 'Начало' удалён из базы.\n")

    viewer.print_header("УДАЛЕНИЕ: ПО НАЗВАНИЮ (Тёмный рыцарь)")
    movie_service.delete_by_title("Тёмный рыцарь")
    print("Фильм 'Тёмный рыцарь' удалён по названию.\n")

    viewer.print_header("ИТОГОВАЯ СТАТИСТИКА И СПИСОК")
    all_movies = movie_service.get_all_movies()
    viewer.print_statistics(all_movies)
    viewer.print_all(all_movies)

    viewer.print_genre_with_movie_count(genre_service.get_genres_with_movies_count())


if __name__ == "__main__":
    main()
import logging
from app.core import init_db, session_maker
from app.services import MovieService
from app.utils.movie_viewer import MovieViewer

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(filename='app.log')],
    )

    init_db()
    manager = MovieService(session_maker)
    viewer = MovieViewer()

    viewer.print_header("СОЗДАНИЕ ФИЛЬМОВ")
    m1 = manager.create_movie("Побег из Шоушенка", "Drama", 1994, 142, 9.3)
    m2 = manager.create_movie("Тёмный рыцарь", "Action", 2008, 152, 9.0)
    m3 = manager.create_movie("Начало", "Sci-Fi", 2010, 148, 8.8)
    m4 = manager.create_movie("Криминальное чтиво", "Crime", 1994, 154, 8.9)
    m5 = manager.create_movie("Матрица", "Sci-Fi", 1999, 136, 8.7)
    print("Фильмы успешно добавлены в базу.\n")


    viewer.print_header("ПРОСМОТР: ВСЕ ФИЛЬМЫ")
    viewer.print_all(manager.get_all_movies())

    viewer.print_header("ПРОСМОТР: ЖАНР Sci-Fi")
    viewer.print_all(manager.get_movies_by_genre("Sci-Fi"))

    viewer.print_header("ПРОСМОТР: РЕЙТИНГ >= 9.0")
    viewer.print_all(manager.get_high_rated_movies(9.0))

    viewer.print_header("ПРОСМОТР: ПОСЛЕ 2005 ГОДА")
    viewer.print_all(manager.get_movies_after_year(2005))

    viewer.print_header("ПРОСМОТР: ПО НАЗВАНИЮ")
    viewer.print_one(manager.get_movie_by_title("Матрица"))

    viewer.print_header("ОБНОВЛЕНИЕ: РЕЙТИНГ МАТРИЦЫ")
    matrix = manager.get_movie_by_title("Матрица")
    if matrix:
        manager.update_rating(matrix.id, 8.9)
        viewer.print_one(manager.get_by_id(matrix.id))

    viewer.print_header("ОБНОВЛЕНИЕ: ЖАНР ТЁМНОГО РЫЦАРЯ")
    dk = manager.get_movie_by_title("Тёмный рыцарь")
    if dk:
        manager.update_genre(dk.id, "Action, Crime")
        viewer.print_one(manager.get_by_id(dk.id))

    viewer.print_header("ОБНОВЛЕНИЕ: СТАТУС ДОСТУПНОСТИ")
    matrix = manager.get_movie_by_title("Матрица")
    if matrix:
        manager.update_availability(matrix.id, False)
        viewer.print_one(manager.get_by_id(matrix.id))

    viewer.print_header("ПОЛНОЕ ОБНОВЛЕНИЕ")
    shawshank = manager.get_movie_by_title("Побег из Шоушенка")
    if shawshank:
        manager.full_update(shawshank.id, genre="Drama, Crime", rating=9.5, duration=145)
        viewer.print_one(manager.get_by_id(shawshank.id))

    viewer.print_header("УДАЛЕНИЕ: SOFT DELETE (Матрица)")
    matrix = manager.get_movie_by_title("Матрица")
    if matrix:
        manager.soft_delete(matrix.id)
        viewer.print_one(manager.get_by_id(matrix.id))

    viewer.print_header("УДАЛЕНИЕ: ПО ID (Начало)")
    inception = manager.get_movie_by_title("Начало")
    if inception:
        manager.delete_by_id(inception.id)
        print("Фильм 'Начало' удалён из базы.\n")

    viewer.print_header("УДАЛЕНИЕ: ПО НАЗВАНИЮ (Тёмный рыцарь)")
    manager.delete_by_title("Тёмный рыцарь")
    print("Фильм 'Тёмный рыцарь' удалён по названию.\n")

    viewer.print_header("ИТОГОВАЯ СТАТИСТИКА И СПИСОК")
    all_movies = manager.get_all_movies()
    viewer.print_statistics(all_movies)
    viewer.print_all(all_movies)

if __name__ == "__main__":
    main()
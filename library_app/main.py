import logging
from library_app.services.library_manager import LibraryManager

if __name__ == '__main__':
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    db_url = 'sqlite:///database.db'
    library = LibraryManager(db_url)

    # Создаём таблицы
    library.create_tables()
    print("База данных и таблицы готовы.\n")

    # 1. Создание авторов
    print("1. Создание авторов")
    author1 = library.add_author("Филип Дик")
    author2 = library.add_author("Артур Кларк")
    print(f"   Создан: {author1.name} (ID: {author1.id})")
    print(f"   Создан: {author2.name} (ID: {author2.id})\n")

    # 2. Добавление книг
    print("2. Добавление книг")
    book1 = library.add_book(
        title="Мечтают ли андроиды об электроовцах?",
        author_id=author1.id,
        year=1968,
        isbn="978-0-575-07810-4"
    )
    book2 = library.add_book(
        title="Космическая одиссея 2001 года",
        author_id=author2.id,
        year=1968,
        isbn="978-0-451-45790-3"
    )
    print(f"   Добавлена: {book1.title} (Год: {book1.year}, Автор: {book1.author.name})")
    print(f"   Добавлена: {book2.title} (Год: {book2.year}, Автор: {book2.author.name})\n")

    # 3. Поиск и обновление
    print("3. Поиск и обновление книги")
    found_book = library.find_book_by_id(book1.id)
    print(f"   Найдена: {found_book.title} (Год: {found_book.year})")

    updated = library.update_book(book1.id, new_year=1969)
    print(f"   Обновлён год: '{updated.title}' -> {updated.year}")

    library.update_book(book2.id, new_title="2001: Космическая одиссея", new_year=1969)
    print("   Книга 2 обновлена (название и год).\n")

    # 4. Список всех книг
    print("4. Все книги с авторами")
    all_books = library.get_all_books()
    for b in all_books:
        print(f"   - {b.title} | {b.author.name} ({b.year})")
    print()

    # 5. Читатели
    print("5. Управление читателями")
    reader = library.add_reader("Иван", "Петров", "ivan@test.com")
    print(f"   Читатель создан: {reader.first_name} {reader.last_name} (ID: {reader.id})")

    library.update_reader(reader.id, new_email="ivan.petrov@newmail.com")
    updated_reader = library.find_reader_by_id(reader.id)
    print(f"   Email обновлён: {updated_reader.email}\n")

    # 6. Удаление
    print("6. Удаление записей")
    print(f"   Удаление книги: {book1.title} -> {library.delete_book(book1.id)}")
    print(f"   Удаление автора: {author1.name} -> {library.delete_author(author1.id)}\n")

    # === ТЕСТИРОВАНИЕ BookIssue ===
    print("7. Тест выдачи книг (п. 1.4)")
    try:
        issue1 = library.issue_book_to_reader(book2.id, reader.id)
        print(f"   Выдана: '{issue1.book.title}' -> {issue1.reader.first_name} {issue1.reader.last_name}")
        print(f"      Дата выдачи: {issue1.issue_date}\n")
    except ValueError as e:
        print(f"   Ошибка: {e}\n")

    # Попытка выдать ту же книгу другому читателю
    reader2 = library.add_reader("Мария", "Сидорова", "maria@test.com")
    try:
        library.issue_book_to_reader(book2.id, reader2.id)
        print("   Книга выдана дважды (ошибка валидации!)")
    except ValueError as e:
        print(f"   Валидация сработала: {e}\n")

    # === ТЕСТ ВОЗВРАТА И АКТИВНЫХ ВЫДАЧ ===
    print("8. Тест возврата и активных выдач (п. 2.4)")
    returned = library.return_book_from_reader(issue1.id)
    print(f"   Книга возвращена. Дата возврата: {returned.return_date}\n")

    active = library.get_active_issues()
    print(f"Активные выдачи: {len(active)}")
    if not active:
        print("   (Нет активных выдач — все книги возвращены)")
    else:
        for act in active:
            print(
                f"   - '{act.book.title}' | Выдана: {act.issue_date} | {act.reader.first_name} {act.reader.last_name}")

    print("\nВсе тесты завершены!")
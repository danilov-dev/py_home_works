import sys
from library_app.services.library_manager import LibraryManager

def print_menu():
    print("\n=== Меню библиотеки ===")
    print("1. Добавить автора")
    print("2. Добавить читателя")
    print("3. Добавить книгу")
    print("4. Выдать книгу")
    print("5. Вернуть книгу")
    print("6. Показать активные выдачи")
    print("7. Найти книги по автору")
    print("8. Показать все книги с авторами")
    print("9. Удалить автора")
    print("10. Удалить книгу")
    print("11. Удалить читателя")
    print("0. Выйти")

def main():
    db_url = 'sqlite:///database.db'
    library = LibraryManager(db_url)
    library.create_tables()
    print("База данных и таблицы готовы.")

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == '0':
                print("Завершение работы. До свидания!")
                break

            elif choice == '1':
                name = input("Введите имя автора: ").strip()
                if not name:
                    print("Ошибка: имя не может быть пустым.")
                    continue
                author = library.add_author(name)
                print(f"Автор добавлен: {author.name} (ID: {author.id})")

            elif choice == '2':
                first = input("Имя читателя: ").strip()
                last = input("Фамилия читателя: ").strip()
                email = input("Email: ").strip()
                if not all([first, last, email]):
                    print("Ошибка: заполните все поля.")
                    continue
                reader = library.add_reader(first, last, email)
                print(f"Читатель добавлен: {reader.first_name} {reader.last_name} (ID: {reader.id})")

            elif choice == '3':
                title = input("Название книги: ").strip()
                author_id = int(input("ID автора: "))
                year = int(input("Год издания: "))
                book = library.add_book(title, author_id, year)
                print(f"Книга добавлена: {book.title} (ID: {book.id})")

            elif choice == '4':
                book_id = int(input("ID книги: "))
                reader_id = int(input("ID читателя: "))
                issue = library.issue_book_to_reader(book_id, reader_id)
                print(f"Книга '{issue.book.title}' выдана читателю {issue.reader.first_name} {issue.reader.last_name}")

            elif choice == '5':
                issue_id = int(input("ID записи выдачи: "))
                returned = library.return_book_from_reader(issue_id)
                print(f"Книга '{returned.book.title}' возвращена {returned.return_date}")

            elif choice == '6':
                issues = library.get_active_issues()
                if not issues:
                    print("Нет активных выдач.")
                else:
                    print("\n--- Активные выдачи ---")
                    for iss in issues:
                        print(f"  Запись #{iss.id}: '{iss.book.title}' -> {iss.reader.first_name} {iss.reader.last_name} (выдана: {iss.issue_date})")

            elif choice == '7':
                author_name = input("Введите имя автора для поиска: ").strip()
                books = library.find_books_by_author_name(author_name)
                if not books:
                    print("Книги данного автора не найдены.")
                else:
                    print(f"\nНайдено книг: {len(books)}")
                    for b in books:
                        print(f"  - {b.title} ({b.year})")

            elif choice == '8':
                library.display_all_books_with_authors()

            elif choice == '9':
                author_id = int(input("ID автора для удаления: "))
                library.delete_author(author_id)
                print("Автор удалён.")

            elif choice == '10':
                book_id = int(input("ID книги для удаления: "))
                library.delete_book(book_id)
                print("Книга удалена.")

            elif choice == '11':
                reader_id = int(input("ID читателя для удаления: "))
                library.delete_reader(reader_id)
                print("Читатель удалён.")

            else:
                print("Неверный выбор. Попробуйте снова.")

        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

if __name__ == '__main__':
    main()
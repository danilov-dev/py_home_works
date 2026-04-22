
from library_app.models import LibraryManager

if __name__ == '__main__':
    db_url = 'sqlite:///database.db'
    library_manager = LibraryManager(db_url)
    library_manager.create_tables()

    print("Создаем авторов.")
    author1 = library_manager.add_author('Филип Дик')
    author2 = library_manager.add_author('Артур Кларк')

    print("Загружаем авторов из бд:")
    authors_from_db = library_manager.get_all_authors()
    for author in authors_from_db:
        print(f"Автор: '{author.id}'  |  '{author.name}'")
    print('='*30)

    print("Ищем автора с ID '1':")
    searching_author = library_manager.get_author_by_id(author1.id)
    print(searching_author.name)

    print("Обновляем автора с ID '2':")
    updated_author2 = library_manager.update_author(author2.id, "Станислав Лем")
    print(f"Меняем имя с {author2.name}  на {updated_author2.name}")

    print("Загружаем авторов из бд после обновления:")
    authors_from_db = library_manager.get_all_authors()
    for author in authors_from_db:
        print(f"Автор: {author.id}  |  {author.name}")
    print('='*30)
def _create_default_file() -> str:
    path_file = 'text_file.txt'
    with open(path_file, mode='w', encoding='utf-8') as file:
        file.write('Мама мыла раму')
    return path_file

def get_symbols_count(file_name: str) -> int:
    """
    Считает количество символов в текстовом файле

    :param file_name: Имя файла (полный путь)
    :type file_name: str
    :return: Количество символов в строке
    :rtype: int
    """
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            text = file.read()
            return len(''.join(text.split()))
    except FileNotFoundError:
        print("Ошибка файла не найден")
        return 0
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return 0


def create_text_file(file_path: str, text: str) -> None:
    """
    Создает тесктовый файл и записывает переданный декст

    :param file_path: Путь к файлу
    :type file_path: str

    :param text: текст для записи в файл
    :type text: str
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


def cut_string(text: str) -> list[str] | str:
    """
    Делит строку. Если длина строки меньше 6 - переворачивает

    :param text: Строка для изменений
    :type text: str
    :return: Список [три символа начала строки] [три символа конца] | перевернутую строку
    :rtype: list[Any] | str
    """
    striped_text = text.strip()
    if len(striped_text) < 6:
        return text[::-1]

    res = [striped_text[0:3], striped_text[-3:]]
    return res


path = input("Введите имя файла [default - 'text_file.txt']: \n"
             ">>>")
if path == '':
    path = _create_default_file()

print(get_symbols_count(path))

create_text_file("my_text_file.txt", "Первая строка")

print(cut_string("программирование"))
print(cut_string("мыло"))




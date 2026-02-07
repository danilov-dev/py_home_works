import string

def _create_numeric_file():
    path_file = "numbers_text.txt"
    with open("numbers_text.txt", "w") as f:
        f.write("1 14 5\n"
                "2 7 67\n"
                "4 9 10")
    return path_file

def _create_text_file() -> str:
    file_path = "poem_text.txt"
    with open("poem_text.txt", "w") as f:
        f.write(
            "У лукоморья дуб зелёный;\n"
            "Златая цепь на дубе том:\n"
            "И днём и ночью кот учёный\n"
            "Всё ходит по цепи кругом;\n"
            "\n"
            "Идёт направо — песнь заводит,\n"
            "Налево — сказку говорит.\n"
            "Там чудеса: там леший бродит,\n"
            "Русалка на ветвях сидит;\n"
            "\n"
            "Там на неведомых дорожках\n"
            "Следы невиданных зверей;\n"
            "Избушка там на курьих ножках\n"
            "Стоит без окон, без дверей;\n"
        )
    return file_path

def _delete_punctuation(text: str) -> str:
    translator = str.maketrans('', '', string.punctuation)
    return text.strip().translate(translator)

def get_sum_from_file(path_file: str) -> int:
    """
    Считает сумму всех чисел в файле. С проверкой на тип
    :param path_file: Путь к файлу
    :return: Сумма чисел
    """
    with open(path_file, "r") as f:
        numbers = []
        for line in f.readlines():
            for number in line.split():
                try:
                    numbers.append(float(number))
                except ValueError:
                    continue
    return sum(numbers)


def get_sum_from_file_short(path_file: str) -> int:
    """
    Считает сумму чисел в файле (без проверки)
    :param path_file: Путь к файлу
    :return: Сумма чисел
    """
    with open(path_file, "r") as f:
        numbers = [int(num) for line in f.readlines() for num in line.split()]
    return sum(numbers)

def get_sum_from_lines(path_file: str) -> dict[str, int]:
    """
    Считает сумму целых чисел в файле
    :param path_file: Путь к файлу
    :return: Словарь, где key: Номер строки, value: Сумма чисел в этой строке
    """
    with open(path_file, "r") as f:
        result = {}
        line_counter = 1
        for line in f.readlines():
            result[line_counter] = sum(int(num) if num.isdigit() else 0 for num in line.split())
            line_counter += 1
        return result

def get_sum_from_columns(path_file: str) -> dict[str, int]:
    """
    Считает сумму целых чисел в каждом столбце
    :param path_file: путь к файлу
    :return: Словарь, где key: Номер столбца, value: Сумма чисел в этом столбце
    """
    result = {}
    with open(path_file, "r") as f:
        for index, line in enumerate(f,start=1):
            numbers = [int(num) if num.isdigit() else 0 for num in line.split()]
            for col_index, value in enumerate(numbers, start=1):
                result[col_index] = result.get(col_index, 0) + value
    return result

def get_word_count_in_line(path_file: str) -> dict[str, int]:
    """
    Считает количество слов в каждой строке
    :param path_file: путь к файлу
    :return: Словарь, где key: Номер строки, value: количество слов
    """
    result = {}

    with open(path_file, "r") as f:
        for index, line in enumerate(f.readlines(), 1):
            if line.strip():
                text = _delete_punctuation(line)
                result[index] = len(text.split())

    return result

def get_longer_line(path_file: str) -> str:
    """
    Находит строку с самым большим количеством символов
    :param path_file: путь к файлу
    :return: самую длинную строку
    """
    result_string = ''
    with open(path_file, "r") as f:
        for line in f.readlines():
            if len(line.strip()) >= len(result_string):
                result_string = line.strip()
    return result_string

def get_count_words_longer_then(path_file: str, char_count: int) -> int:
    """
    Считает количество слов больше заданной длины
    :param path_file: путь к файлу
    :param char_count: Минимальная длина
    :return: количество слов
    """
    words_count = 0
    with open(path_file, "r") as f:
        for line in f.readlines():
            text = _delete_punctuation(line)
            for word in text.split():
                if len(word) > char_count:
                    words_count += 1
    return words_count

if __name__ == "__main__":
    numeric_path_file = _create_numeric_file()
    poem_path_file = _create_text_file()
    print(f"{get_sum_from_file(numeric_path_file):,.0f}")
    print(f"{get_sum_from_file_short(numeric_path_file):,.0f}")
    print('-' * 40)
    sum_lines = get_sum_from_lines(numeric_path_file)
    sum_columns = get_sum_from_columns(numeric_path_file)

    for k, v in sum_lines.items():
        print(f"Line: {k} - Sum: {v}")
    print('-' * 40)

    for k, v in sum_columns.items():
        print(f"Column: {k} - Sum: {v}")
    print('-' * 40)

    word_count_in_line = get_word_count_in_line(poem_path_file)
    longer_string = get_longer_line(poem_path_file)
    for k, v in word_count_in_line.items():
        print(f"Line: {k} - words: {v}")
    print('-' * 40)
    print("Самая длинная строка:")
    print(longer_string)
    print('-' * 40)
    print(f"Количество слов больше 2: {get_count_words_longer_then(poem_path_file, 2)}")

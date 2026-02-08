
def write_in_file():
    stop_word = '0'
    is_stopped = False
    with open("text.txt", "w") as file:
        for i in range(3):
            print("Введите строку:")
            word = input(">>> :")
            if word == stop_word:
                print("Программа остановлена")
                is_stopped = True
                break
            file.write(word + "\n")
    if not is_stopped:
        with open("text.txt", "a") as file:
            for i in range(3):
                print("Введите строку:")
                word = input(">>> :")
                if word == stop_word:
                    print("Программа остановлена")
                    break
                file.write(word + "\n")


def delete_lines():
    with open("text.txt", "r") as file:
        text_lines = file.readlines()
    filtered_lines = []
    for i in range(len(text_lines)):
        if i % 2 != 0:
            filtered_lines.append(text_lines[i])

    with open("text.txt", "w") as file:
        file.writelines(filtered_lines)


def delete_lines2():
    with open("text.txt", "r") as file:
        text_lines = file.readlines()
    filtered_lines = text_lines[1::2]
    with open("text.txt", "w") as file:
        file.writelines(filtered_lines)


def delete_lines3():
    with open("text.txt", "r") as file:
        text_lines = file.readlines()
    for i in range(len(text_lines)-1,-1,-1):
        if i % 2 == 0:
            del text_lines[i]
    with open("text.txt", "w") as file:
        file.writelines(text_lines)


def create_numeric_file():
    max_numbers = 10
    separators = "-\\_/!? "

    print(f"Введите {max_numbers} чисел в строку через пробел")
    text = input(">>> ").strip()

    for sep in separators:
        if sep in text:
            text = text.replace(sep, " ")

    numbers = text.split(" ")
    if len(numbers) < max_numbers:
        print("Вы ввели недостаточное количество чисел")
        return
    try:
        even_numbers = [num for num in numbers if float(num)%2 == 0]

        with open("numbers.txt", "w") as file:
            for num in even_numbers:
                file.write(num + "\n")

    except ValueError:
        print("Нужно ввести только числа!")
        return

def create_text_file():
    max_length = 15
    vowels = "аеёиоуыэюяaeiou"
    consonants = "бвгджзйклмнпрстфхцчшщbcdfghjklmnpqrstvwxyz"
    punctuation = ".,!?:;-"
    digits = "0123456789"

    vowels_count = 0
    consonants_count = 0
    punctuation_count = 0
    digits_count = 0
    spaces_count = 0

    print(f"Введите текст длиной в {max_length} символов")
    text = input(">>> ").strip()
    if len(text) < max_length:
        print(f"Строка слишком мала - {len(text)}, нужно - {max_length}")
        return

    for char in text.lower():
        if char in vowels:
            vowels_count += 1
        elif char in consonants:
            consonants_count += 1
        elif char in punctuation:
            punctuation_count += 1
        elif char in digits:
            digits_count += 1
        elif char == " ":
            spaces_count += 1

    result = (f"Количество гласных букв - {vowels_count}\n"
                  f"Количество согласных букв - {consonants_count}\n"
                  f"Количество символов - {len(text)}\n"
                  f"Количество пробелов - {spaces_count}\n"
                  f"Количество цифр - {digits_count}\n"
                  f"Количество знаком препинания - {punctuation_count}\n")

    try:
        with open("result.txt", "w", encoding='utf-8') as file:
            file.write(result)
    except Exception as e:
        print(f"Ошибка {e}")
        return






if __name__ == "__main__":
    # write_in_file()
    # delete_lines2()
    #create_numeric_file()
    create_text_file()
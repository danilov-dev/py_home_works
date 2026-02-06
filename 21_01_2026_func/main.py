# Задача 1
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def sum_even_numbers(numbers: list) -> dict[str, int]:
    """
    Считает сумму всех четных чисел коллекции, если они больше 5
    Считает их среднее арифметическое
    :param numbers: коллекция чисел
    :return: Словарь
    """
    even_numbers = []
    for number in numbers:
        if number > 5 and number % 2 == 0:
            even_numbers.append(number)
    return {
        'sum': sum(even_numbers),
        'mean': sum(even_numbers) / len(even_numbers)
    }


answer_task_1 = sum_even_numbers(numbers)
print(f'Сумма всех четных чисел: {answer_task_1.get('sum', 0)}')
print(f'Среднее арифметическое четных чисел: {answer_task_1.get('mean', 0)}')


# Задача 2:
def get_numbers_greater_than(numbers: list, value: int) -> list[int]:
    """
    Выводит список чисел больше value
    :param numbers: список чисел
    :param value: Число для сравнения
    :return: dict Список
    """
    result = [num for num in numbers if num > value]
    return result


answer_task_2 = get_numbers_greater_than(numbers, 5)
print(answer_task_2)

# Задача 3:

numbers_2 = [1, 43, 3, 55, 5, 6, 12, 8, 99, 10]


def compare_lists(numbers_1: dict, numbers_2: dict):
    recurring = set(numbers_1) & set(numbers_2)
    print("Числа, которые есть в обоих списках:")
    print(recurring if recurring else 'Общих чисел нет')
    print('-' * 40)
    print("Числа, которые есть только в numbers_1:")
    print(set(numbers_1) - set(numbers_2))
    print('-' * 40)
    print(f"Сумма чисел обоих списков:")
    print(sum(numbers_1) + sum(numbers_2))
    print('-' * 40)
    all_numbers = numbers_1 + numbers_2
    print(f"Среднее арифметическое обоих списков:")
    print(sum(all_numbers) / len(all_numbers))
    print('-' * 40)
    max_number = max(all_numbers)
    print(f"Максимальное число из обоих списков:")
    print(max_number)
    print('-' * 40)
    min_number = min(all_numbers)
    print(f"Минимальное число из обоих списков:")
    print(min_number)
    print('-' * 40)
    even_count = sum(1 for num in all_numbers if num % 2 == 0)
    odd_count = len(all_numbers) - even_count

    if even_count > odd_count:
        print(f"Четных больше {even_count}")
    elif odd_count > even_count:
        print(f'Нечетных больше {odd_count}')
    else:
        print('Четных и нечетных поровну')


compare_lists(numbers, numbers_2)

salary_data = {
    "Январь": 50000,
    "Февраль": 52000,
    "Март": 48000,
    "Апрель": 55000,
    "Май": 60000,
    "Июнь": 45000,
    "Июль": 62000,
    "Август": 58000,
    "Сентябрь": 53000,
    "Октябрь": 51000,
    "Ноябрь": 49000,
    "Декабрь": 70000
}


def analyze_salary(salary_data: dict):
    if not salary_data:
        print('Зарплатная ведомость пуста')
        return

    total_salary = sum(salary_data.values())
    max_month = max(salary_data, key=salary_data.get)
    max_salary = salary_data[max_month]
    min_month = min(salary_data, key=salary_data.get)
    min_salary = salary_data[min_month]
    mean_salary = total_salary / len(salary_data)

    print('Ключи ведомости:')
    print(', '.join(salary_data.keys()))
    print('-' * 40)
    for month, salary in salary_data.items():
        print(f"   {month}: {salary:,} руб.")
    print('-' * 40)
    print('Сумма сотрудника за год:')
    print(total_salary)
    print('-' * 40)
    print(f'Максимальная зп сотрудника: {max_month} - {max_salary}')
    print(f'Минимальная зп сотрудника: {min_month} - {min_salary}')
    print('-' * 40)
    print(f'Средняя зарплата за год {mean_salary:,.2f}')


analyze_salary(salary_data)

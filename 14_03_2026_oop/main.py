from datetime import datetime, date


class WashingMachine:
    def __init__(self):
        self.max_load = 6
        self.is_clothes = False
        self.is_powder = False

    def pour_powder(self):
        self.is_powder = True
        print("Порошок засыпан")

    def load_clothes(self, weight: float):
        if weight > self.max_load:
            print("Слишком много белья. Уменьшите вес")
            return
        self.is_clothes = True
        print("Белье загружено")

    def start(self):
        if not self.is_clothes:
            print("Ошибка: Нет белья!")
            return
        if not self.is_powder:
            print("Ошибка: Нет порошка!")
            return
        print("Процесс стирки запущен")


class Dog:
    def __init__(self, name: str, breed: str, age: int):
        self.name = name
        self.breed = breed
        self.age = age
        self._is_at_home = True
        self._is_hungry = True
        self._is_paws_clear = True

    def eat(self):
        if not self._is_hungry:
            print(f"{self.name} не голоден")
            return
        print(f"{self.name} поел")
        self._is_hungry = False

    def make_noise(self):
        if self._is_at_home:
            print("Лаять можно только на улице")
            return
        print(f"{self.name} громко лает!")

    def walk(self):
        if not self._is_at_home:
            print(f"{self.name} уже на прогулке")
            return
        if self._is_hungry:
            print(f"{self.name} должен сначала поесть")
            return
        print(f"{self.name} весело резвится на прогулке")
        self._is_at_home = False
        self._is_hungry = True
        self._is_paws_clear = False

    def wash_paws(self):
        if self._is_at_home:
            print(f"У {self.name} чистые лапы! Он сидит дома")
            return
        print(f"{self.name} не хочет мыть лапы, пытается убежать. Но у тебя получается. Лапы чистые!")
        self._is_paws_clear = True

    def come_home(self):
        if self._is_at_home:
            print(f"{self.name} и так сидит дома!")
            return
        if not self._is_paws_clear:
            print("Сначала нужно вымыть лапы")
            return
        print(f"{self.name} уставший, голодный, но довольный возвращается домой!")


class Employee:
    def __init__(self, first_name: str, last_name: str, position: str, date_of_birth: str, skills: list = None, ):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.date_of_birth = datetime.strptime(date_of_birth, "%d.%m.%Y")
        self.skills = skills if skills else []
        self._salaries: list = []
        self._salary_entered = False

    def get_name_and_position(self):
        print(f"Сотрудник: {self.first_name} {self.last_name}\n"
              f"Должность: {self.position}\n")

    def check_skill(self, skill: str):
        if skill not in self.skills:
            print(f"Навыком {skill} сотрудник не обладает")
            return
        print(f"Навыком {skill} сотрудник обладает")

    def input_salary(self):
        print("введите зарплату за последние 3 месяца")
        for i in range(3):
            while True:
                try:
                    salary = float(input(f"Зарплата {i + 1}: ").strip())
                    if salary < 0:
                        print("Зарплата не может быть отрицательной")
                        continue
                    self._salaries.append(salary)
                    break
                except ValueError:
                    print("Ошибка! Введите число (можно с десятичной частью)")
        self._salary_entered = True
        print("Зарплаты удачно внесены")

    def calculate_average_salary(self):
        if not self._salaries or len(self._salaries) == 0:
            print("Зарплат нет. Внесите зарплаты")
            return 0
        average = sum(self._salaries) / len(self._salaries)
        print(f"Средняя зарплата за 3 месяца составила: {average}")
        return average

    def get_age(self):
        today = datetime.today()
        age = today.year - self.date_of_birth.year
        birthday_this_year = date(today.year, self.date_of_birth.month, self.date_of_birth.day)
        if today < birthday_this_year:
            age -= 1
        print(f"Возраст сотрудника: {age}")
        return age

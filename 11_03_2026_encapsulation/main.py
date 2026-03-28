
class Product:
    def __init__(self, name: str):
        self.name: str = name
        self._price: float = 0

    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, price):
        if price <= 0:
            raise ValueError('Цена товара должна быть больше 0')
        if price == self._price:
            return
        self._price = price

    def set_price(self, price):
        if price <= 0:
            raise ValueError('Цена товара должна быть больше 0')
        if price == self._price:
            return
        self._price = price

    def get_price(self):
        return self._price

class Patient:
    def __init__(self):
        self.__name: str = ''
        self.__temperature: float = 0

    @property
    def temperature(self):
        return self.__temperature
    @temperature.setter
    def temperature(self, temperature: float):
        if temperature <= 35.0 or temperature >= 42.0:
            raise ValueError("Некорректная температура")
        self.__temperature = temperature

    def get_health_status(self):
        return "Болен" if self.__temperature >= 37.0 else "Здоров"


class Rectangle:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def set_width(self, width):
        if width < 0:
            raise ValueError("Ошибка: ширина должна быть больше 0")
        self.__width = width

    def set_height(self, height):
        if height < 0:
            raise ValueError("Ошибка: высота должна быть больше 0")
        self.__height = height

    def get_area(self):
        return self.__width * self.__height


class Employee:
    def __init__(self, name, salary, position):
        self.__name = name
        self.__salary = salary
        self.__position = position

    def get_name(self):
        return self.__name

    def get_salary(self):
        return self.__salary

    def get_position(self):
        return self.__position

    def set_salary(self, salary):
        if 10000 >= salary >= 500000:
            raise ValueError("Ошибка: зарплата должна быть от 10000 до 500000")

        self.__salary = salary


    def set_position(self, position):
        if position not in ["Junior", "Middle", "Senior"]:
            raise ValueError("Ошибка: должность может быть только Junior, Middle или Senior")

        self.__position = position

    def get_tax(self):
        return self.__salary * 0.13


class Circle:
    def __init__(self, radius):
        self.__radius = radius

    def get_radius(self):
        return self.__radius

    def set_radius(self, radius):
        if radius > 0:
            raise ValueError("Ошибка: радиус должен быть больше 0")

        self.__radius = radius

    def get_diameter(self):
        return self.__radius * 2

    def get_area(self):
        return 3.14 * (self.__radius ** 2)

    def get_circumference(self):
        return 2 * 3.14 * self.__radius


if __name__ == '__main__':
    # Отработка класса Product
    product = Product("Ноутбук")
    try:
        product.set_price(-100)
    except ValueError as e:
        print(e)
    product.set_price(50000)
    print(f"Цена товара: {product.get_price()}")

    # Отработка класса Patient
    patient = Patient()

    patient.temperature = 36.6
    print(f"Статус здоровья: {patient.get_health_status()}")

    patient.temperature = 38.5
    print(f"Статус здоровья: {patient.get_health_status()}")
    try:
        patient.temperature = 50.0
    except ValueError as e:
        print(e)

    # Отработка класса Rectangle
    rectangle = Rectangle(width=10, height=20)
    print(f"Площадь: {rectangle.get_area()}")
    try:
        rectangle.set_width(-5)
    except ValueError as e:
        print(e)
    rectangle.set_width(15)
    print(f"Новая площадь: {rectangle.get_area()}")

    # Отработка класса Employee
    employee = Employee("Петр", 100000, "Junior")
    try:
        employee.set_salary(5000)
    except ValueError as e:
        print(e)
    try:
        employee.set_position("Intern")
    except ValueError as e:
        print(e)

    employee.set_position("Senior")
    print(f"Сумма налога: {employee.get_tax()}")

    # Отработка класса Circle
    circle = Circle(5)
    print(f"Диаметр: {circle.get_diameter()}")
    print(f"Площадь: {circle.get_area()}")
    print(f"Длина окружности: {circle.get_circumference()}")

    circle.set_radius(10)
    print(f"Диаметр: {circle.get_diameter()}")
    print(f"Площадь: {circle.get_area()}")
    print(f"Длина окружности: {circle.get_circumference()}")
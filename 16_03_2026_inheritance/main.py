class Shape:
    def __init__(self, color, filled=True):
        self.color = color
        self.filled = filled

    def get_info(self):
        filled_status = "заполнена" if self.filled else "не заполнена"
        return f"Фигура цвета {self.color}, {filled_status}"


class Rectangle(Shape):
    def __init__(self, color, width, height, filled=True):
        super().__init__(color, filled)
        self.width = width
        self.height = height

    def get_info(self):
        base_info = super().get_info()
        return f"{base_info}, размеры: {self.width}×{self.height}"

    def get_area(self):
        return self.width * self.height


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def login(self):
        print(f"Пользователь {self.username} вошёл")

    def get_permissions(self):
        return ["read"]


class Admin(User):
    def __init__(self, username, email):
        super().__init__(username, email)

    def get_permissions(self):
        return ["read", "write", "delete"]

    def ban_user(self, user):
        print(f"Админ забанил {user.username}")


class Device:
    def __init__(self, brand, model, price):
        self.brand = brand
        self.model = model
        self.price = price

    def get_info(self):
        return f"{self.brand} {self.model}, цена: {self.price} руб."

    def turn_on(self):
        print("Устройство включено")


class Phone(Device):
    def __init__(self, brand, model, price, phone_number):
        super().__init__(brand, model, price)
        self.phone_number = phone_number

    def turn_on(self):
        print("Телефон включён")

    def call(self, number):
        print(f"Звонок на {number}")


class Smartphone(Phone):
    def __init__(self, brand, model, price, phone_number, os):
        super().__init__(brand, model, price, phone_number)
        self.os = os

    def turn_on(self):
        print(f"Смартфон включён с {self.os}")

    def install_app(self, app_name):
        print(f"Установлено приложение {app_name}")

if __name__ == "__main__":
    # Отработка класса Shape и его наследников
    shape = Shape("красный")
    print(shape.get_info())

    rectangle = Rectangle("синий", 10, 20)
    print(rectangle.get_info())
    print(f"Площадь прямоугольника: {rectangle.get_area()}")

    # Отработка класса User и его наследников
    user = User("ivan123", "ivan@example.com")
    admin = Admin("admin", "admin@example.com")

    user.login()
    admin.login()

    print(f"Права пользователя: {user.get_permissions()}")
    print(f"Права администратора: {admin.get_permissions()}")

    admin.ban_user(user)

    # Отработка класса Device и его наследников
    device = Device("Samsung", "TV", 50000)
    phone = Phone("Nokia", "3310", 3000, "+7 123 456-78-90")
    smartphone = Smartphone("Apple", "iPhone 15", 80000, "+7 987 654-32-10", "iOS 17")

    # Turn on all devices
    print("Включение устройств:")
    device.turn_on()
    phone.turn_on()
    smartphone.turn_on()

    phone.call("+7 999 888-77-66")

    smartphone.install_app("Instagram")

    print(f"Устройство: {device.get_info()}")
    print(f"Телефон: {phone.get_info()}, номер: {phone.phone_number}")
    print(f"Смартфон: {smartphone.get_info()}, номер: {smartphone.phone_number}, ОС: {smartphone.os}")
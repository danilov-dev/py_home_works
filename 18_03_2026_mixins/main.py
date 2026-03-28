class Wolf:
    def howl(self):
        print("Уууу!")

class Dog:
    def bark(self):
        print("Гав!")

class Werewolf(Wolf, Dog):
    def transform(self):
        print("Превращение!")


class EatMixin:
    def eat(self):
        print("Сотрудник ест")


class SleepMixin:
    def sleep(self):
        print("Сотрудник спит")


class Worker(EatMixin, SleepMixin):
    def __init__(self, name):
        self.name = name

    def work(self):
        print(f"{self.name} работает")

class A:
    def show(self):
        print("Класс A")

class B:
    def show(self):
        print("Класс B")

class C(A, B):
    def test(self):
        self.show()

class PrintMixin:
    def print_document(self, text):
        print(text)

class SaveMixin:
    def save_document(self, text):
        print(f"Сохранено: {text}")

class Document(PrintMixin, SaveMixin):
    def create(self, content):
        print("Создание документа...")
        self.print_document(content)
        self.save_document(content)
        print("Документ создан!")


if __name__ == "__main__":
    werewolf = Werewolf()

    print("Действия оборотня:")
    werewolf.howl()
    werewolf.bark()
    werewolf.transform()

    print("\nПорядок поиска методов (MRO):")
    print(Werewolf.__mro__)

    worker = Worker("Иван")

    print("Режим дня сотрудника:")
    worker.eat()
    worker.work()
    worker.sleep()

    # 1
    obj = C()
    print("Первый вариант (C(A, B)):")
    obj.test()
    print(f"MRO: {C.__mro__}")

    # Answer:
    # Был вызван класс A, потому что Python ищет методы слева направо в порядке наследования.
    # При вызове show() Python сначала ищет метод в классе C, затем в A, затем в B.
    # Так как метод найден в классе A, он и будет выполнен.

    print("\n" + "=" * 50 + "\n")

    # 2
    class C2(B, A):
        def test(self):
            self.show()


    obj2 = C2()
    print("Второй вариант (C2(B, A)):")
    obj2.test()
    print(f"MRO: {C2.__mro__}")

    # Answer:
    # Теперь был вызван класс B, потому что порядок наследования изменился.
    # Python ищет методы сначала в C2, затем в B, затем в A.
    # Метод найден в классе B, поэтому выполняется он.

    doc = Document()
    doc.create("Важный документ")

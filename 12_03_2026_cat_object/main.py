import os
import datetime
import time
import random
from enum import Enum


class Action(Enum):
    FEED = "1"
    PLAY = "2"
    SLEEP = "3"
    HEAL = "4"
    INFO = "5"
    SAY_MEOW = "6"
    SCRATCH = "7"
    EXIT = "0"


class Pet:
    def __init__(self, name: str):
        self.name = name
        self.hungry = 50
        self.health = 100
        self.happiness = 50
        self.energy = 50
        self.age = 0
        self.is_alive = True
        self.last_action = ''

    def say_hello(self, hello_to: str):
        self.last_action = f"Привет {hello_to}! Меня зовут {self.name}, мне {self.age}"

    def feed(self):
        if self.hungry > 20:
            self.hungry -= 20
            self.happiness += 5
            self.last_action = f"{self.name} с удовольствием поел"
        else:
            self.last_action = f"{self.name} не голоден"
        self._normalize_stats()

    def play(self):
        if self.energy > 20:
            self.happiness += 15
            self.energy -= 15
            self.hungry += 15
            self.last_action = f"{self.name} весело играет с тобой"
        else:
            self.last_action = f"{self.name} слишком устал для игр"
        self._normalize_stats()

    def sleep(self):
        if self.energy < 50:
            self.energy += 30
            self.hungry += 15
            self.last_action = f"{self.name} сладко спит Zzz..."
        else:
            self.last_action = f"{self.name} не хочет спать!"
        self._normalize_stats()

    def heal(self):
        if self.health < 90:
            self.health += 20
            self.happiness -= 5
            self.last_action = f"{self.name} полечили"
        else:
            self.last_action = f"{self.name} здоров! Лечение не требуется"
        self._normalize_stats()

    def tick(self):
        self.hungry += random.randint(2, 5)
        self.happiness -= random.randint(1, 3)
        self.energy -= random.randint(1, 3)
        self.age += 1

        if self.hungry > 80 or self.energy < 20 or self.happiness < 30:
            self.health -= random.randint(5, 10)

        self._check_alive()
        self._normalize_stats()

    def _normalize_stats(self):
        self.hungry = max(0, min(100, self.hungry))
        self.health = max(0, min(100, self.health))
        self.energy = max(0, min(100, self.energy))
        self.happiness = max(0, min(100, self.happiness))

    def _check_alive(self):
        if self.health <= 0 or self.hungry >= 100 or self.happiness <= 0 or self.energy <= 0:
            self.is_alive = False

    def get_mood(self):
        if self.happiness > 70:
            return "счастлив!"
        elif self.happiness > 40:
            return "нормальное"
        else:
            return "грустный"


class Dog(Pet):
    def __init__(self, name: str, breed: str, color: str, has_tail: bool = True):
        super().__init__(name)
        self.breed = breed
        self.color = color
        self.has_tail = has_tail

    def get_info(self):
        self.last_action = f"Порода - {self.breed}\nКличка - {self.name}\nХвост - {'есть' if self.has_tail else 'нет'}\nЦвет - {self.color}\n"


class Cat(Pet):
    def __init__(self, name: str, breed: str, color: str, has_tail: bool = True):
        super().__init__(name)
        self.breed = breed
        self.color = color
        self.has_tail = has_tail

    def get_info(self):
        return (f"Порода - {self.breed}\n"
                f"Кличка - {self.name}\n"
                f"Хвост - {'есть' if self.has_tail else 'нет'}\n"
                f"Цвет - {self.color}\n")

    def say_meow(self):
        self.last_action = f"{self.name} говорит Мяу!"
        self.happiness += 5
        self._normalize_stats()

    def scratch(self, object_to_scratch: str):
        self.last_action = f"{self.name} поточила когти о {object_to_scratch}"
        self.energy -= 5
        self.happiness += 10
        self._normalize_stats()


class Game:
    def __init__(self):
        self.pet = None
        self.running = True

    def start(self):
        while True:
            print("Какого питомца ты хочешь завести?")
            print("1. Собаку")
            print("2. Кошку")
            choice = input(">>> ").strip()
            if choice == '1' or choice == '2':
                break
            else:
                print("Не известный питомец! Попробуй еще раз")

        name = input("Введи имя питомца: ").strip()
        if not name:
            name = "Питомец"

        breed = input("Введи породу: ").strip()
        color = input("Введи окрас: ").strip()

        match choice:
            case '1':
                self.pet = Dog(name, breed, color)
            case '2':
                self.pet = Cat(name, breed, color)

        self.game_loop()

    def show_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.pet.last_action)
        print("\n" + "=" * 40)
        print(f"{self.pet.name} | Возраст: {self.pet.age}")
        print(f"Голод: {self.pet.hungry}% | Счастье: {self.pet.happiness}%")
        print(f"Энергия: {self.pet.energy}% | Здоровье: {self.pet.health}%")
        print(f"Настроение: {self.pet.get_mood()}")
        print("=" * 40)
        print("Действия:")
        print(f"{Action.FEED.value}. 🍖 Покормить")
        print(f"{Action.PLAY.value}. 🎾 Поиграть")
        print(f"{Action.SLEEP.value}. 💤 Уложить спать")
        print(f"{Action.HEAL.value}. 💊 Лечить")
        print(f"{Action.INFO.value}. 📓 Информация")
        if isinstance(self.pet, Cat):
            print(f"{Action.SAY_MEOW.value}. Помяукать")
            print(f"{Action.SCRATCH.value}. Поточить когти")
        print(f"{Action.EXIT.value}. Выйти 👋")

    def game_loop(self):
        last_tick = time.time()
        while self.running and self.pet.is_alive:
            self.show_menu()
            choice = input("Введите действие: ").strip()

            match choice:
                case Action.FEED.value:
                    self.pet.feed()
                case Action.PLAY.value:
                    self.pet.play()
                case Action.SLEEP.value:
                    self.pet.sleep()
                case Action.HEAL.value:
                    self.pet.heal()
                case Action.INFO.value:
                    self.pet.get_info()
                case Action.SAY_MEOW.value:
                    if isinstance(self.pet, Cat):
                        self.pet.say_meow()
                    continue
                case Action.SCRATCH.value:
                    if isinstance(self.pet, Cat):
                        objects = ['диван', 'стену', 'кресло', 'твою ногу', ]
                        self.pet.scratch(random.choice(objects))
                    continue
                case Action.EXIT.value:
                    self.running = False
                    break
                case _:
                    print("Неизвестная команда! Попробуй снова")

            current_time = time.time()
            if current_time - last_tick > 5:
                self.pet.tick()
                last_tick = current_time
            if not self.pet.is_alive:
                print(f"\n💔 {self.pet.name} покинул тебя...")
                print("Попробуй еще раз!")
                break


if __name__ == "__main__":
    game = Game()
    game.start()

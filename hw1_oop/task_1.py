import re

#1


class Animal:
    def __repr__(self) -> str:
        """
        Це метод поверне назву тварини, коли об'єкт викликається функцією print
        """
        animal = str(self.__class__)  # <class '__main__.Animal'>
        animal = re.search(r"\.\w+'", animal).group().strip(".").rstrip("'")  # регуляркою вибираємо те шо знаходиться між <.> і <'> обрізаємо лишні символи
        return animal  # Animal

    def sleep(self):
        print(self, "sleeping")  # Animal going

    def eat(self):
        print(self, "eating")


class Dog(Animal):
    def say(self):
        print(self, "barking")


class Cat(Animal):
    def jump(self):
        print(self, "jumping")


class Bird(Animal):
    def fly(self):
        print(self, "flying")


class Horse(Animal):
    def race(self):
        print(self, "is galloping")


class Crocodile(Animal):
    def swim(self):
        print(self, "swims")


#1a

class Human:
    """
    Human class, should have eat, sleep, study, work
    """
    def __repr__(self) -> str:
        return "Human"

    def eat(self):
        print(f"{self} eating")

    def sleep(self):
        print(f"{self} sleeping")

    def study(self):
        print(f"{self} studying")

    def work(self):
        print(f"{self} working")


class Centaur(Animal, Human):  # якщо є однакові методи, буде викликатися метод з того класу який стоїть першим у наслідуванні. Пошук атребутів відбувається зліва направо згідно MRO
    """
    Centaur class should be inherited from Human and Animal
    and has unique method related to it.
    """
    def race(self):
        print(self, "is galloping")


if __name__ == '__main__':
    d = Dog()
    print(d)
    c = Cat()
    b = Bird()
    h = Horse()
    cr = Crocodile()
    d.sleep()
    d.eat()
    d.say()
    c.jump()
    b.fly()
    h.race()
    cr.swim()
#1a
    centaur = Centaur()
    centaur.eat()
    print(centaur)

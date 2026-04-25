class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "..."


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


if __name__ == "__main__":
    animals = [Dog("Rex"), Cat("Murka"), Animal("Unknown")]

    for a in animals:
        print(a.name, "says", a.speak())

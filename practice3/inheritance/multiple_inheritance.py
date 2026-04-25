class Flyable:
    def move(self) -> str:
        return "I can fly"


class Swimmable:
    def move(self) -> str:
        return "I can swim"


class Duck(Flyable, Swimmable):
    pass


if __name__ == "__main__":
    d = Duck()
    print(d.move())

    print("MRO:", [cls.__name__ for cls in Duck.mro()])

class Person:
    def __init__(self, name: str) -> None:
        self.name = name


class Student(Person):
    def __init__(self, name: str, university: str) -> None:
        super().__init__(name)
        self.university = university

    def info(self) -> str:
        return f"{self.name} studies at {self.university}"


if __name__ == "__main__":
    s = Student("Bilan", "KBTU")
    print(s.info())

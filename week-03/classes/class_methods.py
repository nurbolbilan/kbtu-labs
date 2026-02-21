class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        celsius = (fahrenheit - 32) * 5 / 9
        return cls(celsius)

    @staticmethod
    def c_to_f(celsius: float) -> float:
        return celsius * 9 / 5 + 32


if __name__ == "__main__":
    t1 = Temperature(25)
    print("t1 celsius:", t1.celsius, "=> f:", Temperature.c_to_f(t1.celsius))

    t2 = Temperature.from_fahrenheit(77)
    print("t2 from fahrenheit:", t2.celsius)

"""
class_definition.py
Базовое определение класса, атрибуты, методы.
"""


class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def multiply(self, a: float, b: float) -> float:
        return a * b


if __name__ == "__main__":
    calc = Calculator()
    print("add:", calc.add(10, 5))
    print("multiply:", calc.multiply(10, 5))

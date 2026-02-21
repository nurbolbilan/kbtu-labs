def divide(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b


def min_max(numbers: list[int]) -> tuple[int, int]:
    if not numbers:
        raise ValueError("numbers list must not be empty")
    return min(numbers), max(numbers)


def parse_age(text: str) -> int:
    cleaned = text.strip()
    if not cleaned.isdigit():
        raise ValueError("Age must be a positive integer string")
    return int(cleaned)


if __name__ == "__main__":
    print("divide(10, 2) =", divide(10, 2))
    print("divide(10, 0) =", divide(10, 0))

    values = [5, 1, 99, 12]
    smallest, largest = min_max(values)
    print("min =", smallest, "max =", largest)

    print("age =", parse_age(" 18 "))

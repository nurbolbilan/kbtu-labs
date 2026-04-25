def greet_user() -> None:
    print("Hello! Welcome 👋")


def greet_by_name(name: str) -> None:
    print(f"Hello, {name}!")


def add_numbers(a: int, b: int) -> int:
    return a + b


def format_currency(amount: float, symbol: str = "₸") -> str:
    return f"{amount:,.2f} {symbol}"


if __name__ == "__main__":
    greet_user()
    greet_by_name("Bilan")

    result_sum = add_numbers(10, 25)
    print("Sum:", result_sum)

    salary = 190000
    print("Salary:", format_currency(float(salary)))

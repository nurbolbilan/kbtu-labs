def square(x: int) -> int:
    return x * x


if __name__ == "__main__":
    square_lambda = lambda x: x * x  # noqa: E731 (в учебных целях)

    number = 7
    print("square (def):", square(number))
    print("square (lambda):", square_lambda(number))

    full_name = (lambda first, last: f"{last} {first}")("Nurbol", "Bilan")
    print("Full name:", full_name)

def calculate_discount(price: float, discount_percent: float = 10.0) -> float:
    if price < 0:
        raise ValueError("price must be >= 0")
    if not (0 <= discount_percent <= 100):
        raise ValueError("discount_percent must be in [0..100]")

    discount_amount = price * (discount_percent / 100)
    return price - discount_amount


def build_full_name(first_name: str, last_name: str, middle_name: str | None = None) -> str:
    if middle_name:
        return f"{last_name} {first_name} {middle_name}"
    return f"{last_name} {first_name}"


if __name__ == "__main__":
    print(calculate_discount(1000, 15))

    print(calculate_discount(price=2000, discount_percent=5))

    print(calculate_discount(3000))

    print(build_full_name("Nurbol", "Bilan"))
    print(build_full_name("Nurbol", "Bilan", middle_name="A."))

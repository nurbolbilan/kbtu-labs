if __name__ == "__main__":
    prices = [1000, 2500, 3999, 12000]

    increased_prices = list(map(lambda p: round(p * 1.10, 2), prices))

    print("Original:", prices)
    print("Increased:", increased_prices)

    formatted = list(map(lambda p: f"{p:,.0f} ₸", increased_prices))
    print("Formatted:", formatted)

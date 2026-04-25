if __name__ == "__main__":
    numbers = list(range(1, 21))

    even_numbers = list(filter(lambda n: n % 2 == 0, numbers))

    big_numbers = list(filter(lambda n: n > 10, numbers))

    print("Numbers:", numbers)
    print("Even:", even_numbers)
    print("> 10:", big_numbers)

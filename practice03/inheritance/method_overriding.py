class Payment:
    def pay(self, amount: int) -> str:
        return f"Paying {amount} ₸ using generic method"


class CardPayment(Payment):
    def pay(self, amount: int) -> str:
        return f"Paying {amount} ₸ by card"


class CashPayment(Payment):
    def pay(self, amount: int) -> str:
        return f"Paying {amount} ₸ in cash"


if __name__ == "__main__":
    payments: list[Payment] = [Payment(), CardPayment(), CashPayment()]
    for p in payments:
        print(p.pay(5000))

class Account:
    def __init__(self, balance):
        # self.owner = owner
        self.balance = balance
    def withdraw(self, amount):
        if self.balance < amount:
            print("Insufficient Funds")
        else:
            self.balance -= amount
            print(self.balance)
    def deposit(self, amount):
        self.balance += amount

a, b = map(int, input().split())
people = Account(a)
people.withdraw(b)


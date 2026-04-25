class User:
    def __init__(self, username: str, age: int) -> None:
        self.username = username
        self.age = age

    def birthday(self) -> None:
        self.age += 1

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, age={self.age})"


if __name__ == "__main__":
    user = User("Bilan", 18)
    print(user)

    user.birthday()
    print("After birthday:", user)

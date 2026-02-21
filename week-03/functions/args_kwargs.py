def sum_all(*numbers: float) -> float:
    total = 0.0
    for n in numbers:
        total += n
    return total


def print_profile(**info: str) -> None:
    print("Profile info:")
    for key, value in info.items():
        print(f" - {key}: {value}")


def create_message(title: str, *lines: str, **meta: str) -> str:
    message_lines = [f"== {title} =="]
    message_lines.extend(lines)

    if meta:
        message_lines.append("-- meta --")
        for key, value in meta.items():
            message_lines.append(f"{key}={value}")

    return "\n".join(message_lines)


if __name__ == "__main__":
    print("sum_all:", sum_all(1, 2, 3.5, 10))

    print_profile(name="Bilan", city="Almaty", role="Tele2 operator")

    msg = create_message(
        "Daily Report",
        "Did Python practice",
        "Pushed code to GitHub",
        mood="good",
        language="Python",
    )
    print("\n" + msg)

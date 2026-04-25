if __name__ == "__main__":
    students = [
        {"name": "Aruzhan", "score": 88},
        {"name": "Bilan", "score": 91},
        {"name": "Dias", "score": 75},
    ]

    by_score = sorted(students, key=lambda s: s["score"])

    by_name = sorted(students, key=lambda s: s["name"])

    by_score_desc = sorted(students, key=lambda s: s["score"], reverse=True)

    print("By score:", by_score)
    print("By name:", by_name)
    print("By score desc:", by_score_desc)

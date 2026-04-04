n = int(input())
words = input().split()

first = True
for i, word in enumerate(words):
    if first:
        print(f"{i}:{word}", end="")
        first = False
    else:
        print(f" {i}:{word}", end="")

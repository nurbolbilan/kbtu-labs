n = int(input())
unique = set()

for i in range(n):
    name = input()
    if name not in unique:
        unique.add(name)


print(len(unique))
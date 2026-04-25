n = int(input())
numbers = input().split()
l = []

for i in numbers:
    l.append(int(i.strip()))

print(sum(l))
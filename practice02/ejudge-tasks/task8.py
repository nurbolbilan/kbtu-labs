n = int(input())
x = 1
for i in range(n):
    print(x, end=' ')
    x *= 2

    if x > n:
        break
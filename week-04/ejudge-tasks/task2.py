def even(n):
    for i in range(0, n+1):
        if n % 2 == 0:
            yield i

n = int(input())

first = True
for num in even(n):
    if first:
        first = False
        print(num, end='')
    else:
        print(" ", str(num), end='')

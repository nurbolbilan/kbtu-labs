def prime_nums(n):
    for i in range(1, n+1):
        count = 0
        for j in range(1, i):
            if i % j == 0:
                count += 1
        if count == 1:
            yield i

n = int(input())
first = True

for i in prime_nums(n):
    if first:
        first = False
        print(i, end='')
    else:
        print("", i, end='')

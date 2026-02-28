def div_nums(n):
    for i in range(0, n+1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
first = True
for num in div_nums(n):
    if first:
        first = False
        print(num, end='')
    else:
        print(" ", str(num), end='')
def second_degree(n):
    for i in range(0, n+1):
        yield 2 ** i

n = int(input())
first = True

for i in second_degree(n):
    if first:
        first = False
        print(i, end='')
    else:
        print("", i, end='')


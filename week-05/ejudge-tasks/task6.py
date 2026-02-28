def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

n = int(input())
first = True
for i in range(n):
    num = fibonacci(i)
    if first:
        first = False
        print(num, end='')
    else:
        print("," + str(num), end='')
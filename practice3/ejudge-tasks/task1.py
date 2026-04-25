n = int(input())
a = 0
for i in range(1, n):
    if n < 1:
        break
    x = n % 10
    n = n // 10
    if x % 2 == 0:
        continue
    else:
        print("Not valid")
        a = 1
        break
if a == 0:
    print("Valid")
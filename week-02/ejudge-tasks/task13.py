n = int(input())
div = 0

for i in range(1, n):
    if n % i == 0:
        div += 1

if div >= 2:
    print("No")
else:
    print("Yes")
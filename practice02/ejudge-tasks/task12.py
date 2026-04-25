n = int(input())
l = list(map(int, input().split()))

for i in range(n):
    l[i] = l[i] * l[i]

print(*l)
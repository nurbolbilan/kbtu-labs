n = int(input())
l = list(map(int, input().split()))

max_cnt = 0
max_el = 0
for i in range(n):
    if l.count(l[i]) > max_cnt:
        max_cnt = l.count(l[i])
        max_el = l[i]
    elif l.count(l[i]) == max_cnt:
        if max_el > l[i]:
            max_cnt = l.count(l[i])
            max_el = l[i]

print(max_el)
n = int(input())
l = []

for i in range(n):
    phone = input()
    l.append(phone)

cnt = 0
for phone in l:
    if l.count(phone) == 3:
        cnt += 1
        l.remove(phone)

print(cnt)
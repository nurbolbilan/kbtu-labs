n = int(input())
l = input().split()
num_cnt = 0

for i in l:
    if 0 < int(i.strip()):
        num_cnt += 1

print(num_cnt)
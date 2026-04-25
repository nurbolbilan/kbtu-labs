n = int(input())
l = list(map(int, input().split()))
unique = set()

for number in l:
    if number not in unique:
        unique.add(number)
        print("YES")
    else:
        print("NO")
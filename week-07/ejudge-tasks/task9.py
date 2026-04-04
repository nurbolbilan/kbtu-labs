n = int(input())

keys = list(input().split())
values = list(input().split())

result = list(zip(keys, values))
answer = input()

for key, value in result:
    if answer == key:
        print(value)
        break
else: print("Not found")
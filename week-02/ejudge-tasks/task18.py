n = int(input())
arr = [input().strip() for _ in range(n)]

first_index = {}

for i in range(n):
    if arr[i] not in first_index:
        first_index[arr[i]] = i + 1

unique_sorted = sorted(first_index.keys())

for s in unique_sorted:
    print(s, first_index[s])

n = int(input())
nums = list(map(int, input().split()))

result = all(num >= 0 for num in nums)

if result:
    print("Yes")
else:
    print("No")

n = int(input())
nums = set(map(int, input().split()))

nums = sorted(nums)
print(*nums)
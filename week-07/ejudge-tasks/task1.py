n = int(input())
nums = map(int, input().split())

result = map(lambda num: num**2, nums)
print(sum(result))
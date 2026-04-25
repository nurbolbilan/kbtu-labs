n = int(input())
nums = list(map(int, input().split()))

result = list(filter(lambda num: num != 0, nums))
print(len(result))
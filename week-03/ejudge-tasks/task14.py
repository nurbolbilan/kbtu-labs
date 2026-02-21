import math

n = int(input())
nums = list(map(int, input().split()))
n_operations = int(input())

operations = []
for i in range(n_operations):
    operation = list(map(str, input().split()))
    operations.append(operation)

add = lambda x, y: x + y
mul = lambda x, y: x * y

for operation in operations:
    if operation[0] == "add":
        for i in range(n):
            nums[i] = add(nums[i], int(operation[1]))
    if operation[0] == "multiply":
        for i in range(n):
            nums[i] = mul(nums[i], int(operation[1]))
    if operation[0] == "abs":
        for i in range(n):
            nums[i] = abs(nums[i])
    if operation[0] == "power":
        for i in range(n):
            nums[i] = pow(nums[i], int(operation[1]))

print(*nums)
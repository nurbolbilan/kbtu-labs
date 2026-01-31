n, l, r = map(int, input().split())
arr = list(map(int, input().split()))

l -= 1
r -= 1

arr[l:r+1] = reversed(arr[l:r+1])

print(*arr)

n = int(input())
words = list(input().split())

result = max(words, key=len)
print(result)
import re

text = input()
words = re.split("\s", text)

print(len(words))
import re

pattern = re.compile(r"\s")
text = input()

words = re.split(pattern, text)
print(len(words))
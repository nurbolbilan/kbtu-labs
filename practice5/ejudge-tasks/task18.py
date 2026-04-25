import re

text = input()
pattern = input()
pattern = re.escape(pattern)

matches = re.findall(pattern, text)

print(len(matches))
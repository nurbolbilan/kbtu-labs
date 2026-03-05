import re

text = input()
s = input()

answer = re.split(s, text)

print(",".join(answer))
import re

text = input()
s = input()

answer = re.findall(s, text)
if answer:
    print(len(answer))
else:
    print(0)

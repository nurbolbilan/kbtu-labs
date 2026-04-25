import re

text = input()
s = input()

answer = re.search(s, text)
if answer:
    print("Yes")
else:
    print("No")
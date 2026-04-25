import re

text = input()
answer = re.match(r'Hello', text)

if answer:
    print("Yes")
else:
    print("No")
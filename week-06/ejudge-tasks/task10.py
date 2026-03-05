import re

text = input()
result = re.search(r"cat", text) or re.search(r"dog", text)

if result:
    print("Yes")
else:
    print("No")
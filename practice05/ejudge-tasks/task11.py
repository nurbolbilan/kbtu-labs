import re

text = input()
result = re.findall("[A-Z]", text)

if len(result) > 0:
    print(len(result))
else:
    print(0)
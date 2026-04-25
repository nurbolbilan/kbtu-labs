import re

text = input()

result = re.findall(r'^[A–Z]', text) or re.findall(r'^[a–z]', text)
result = re.findall(r'\d+$', text)

if result:
    print("Yes")
else:
    print("No")

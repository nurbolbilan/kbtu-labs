import re

text = input()
a = input()
result = re.search(a, text)
if result:
    b = input()
    answer = re.sub(a, b, text)
    print(answer)
else:
    print(text)
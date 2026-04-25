import re

text = input()
new_text = ""

for i in text:
    if i.isdigit():
        new_text += i*2
    else:
        new_text += i

print(new_text)
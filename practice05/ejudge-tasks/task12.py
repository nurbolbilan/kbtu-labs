import re

text = input()

numbers = re.findall(r"\d+", text)
new_numbers = []

for number in numbers:
    if int(number) // 10 > 0:
        new_numbers.append(str(int(number)))

print(" ".join(new_numbers))
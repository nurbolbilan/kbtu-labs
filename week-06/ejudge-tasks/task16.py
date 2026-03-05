import re

txt = input()
match = re.search(r"Name:\s*(.+),\s*Age:\s*(.+)", txt)

if match:
    name = match.group(1)
    age = match.group(2)
    print(name, age)
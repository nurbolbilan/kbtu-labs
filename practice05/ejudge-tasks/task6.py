import re

text = list(map(str, input().split()))
flags = True
for i in text:
    i = str(i)
    if re.search(r'@', i):
        if i[0] == '@' or i in "no":
            print("No email")
            flags = False
            break

        else:
            print(i)
            flags = False
            break
if flags:
    print("No email")
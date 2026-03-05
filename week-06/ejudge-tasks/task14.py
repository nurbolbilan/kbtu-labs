import re

nums = input()
pattern = re.compile(r'^\d+$')

answer = re.match(pattern, nums)

if answer:
    print("Match")

else:
    print("No match")
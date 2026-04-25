s = input().strip()

to_digit = {
    "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4",
    "FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
}

to_word = {v: k for k, v in to_digit.items()}

for op in "+-*":
    if op in s:
        left, right = s.split(op)
        operator = op
        break
else:
    left, right, operator = s, "", None

def parse_num(t: str) -> int:
    return int("".join(to_digit[t[i:i+3]] for i in range(0, len(t), 3)))

a = parse_num(left)

if operator is None:
    result = a
else:
    b = parse_num(right)
    if operator == "+":
        result = a + b
    elif operator == "-":
        result = a - b
    else:
        result = a * b

if result < 0:
    print("NEG" + "".join(to_word[d] for d in str(-result)))
else:
    print("".join(to_word[d] for d in str(result)))


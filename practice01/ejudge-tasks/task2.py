n = int(input())
l = []
x = input()
for i in range(len(x)):
    if x[i] == '-':
        if x[i + 1].isdigit():
            l.append(int('-' + x[i + 1]))
    if x[i].isdigit():
        l.append(int(x[i]))

print(sum(l))

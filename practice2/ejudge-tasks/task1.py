year = int(input())

if year >= 1 and year <= 30000:
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            print("YES")
    else:
        print("NO")
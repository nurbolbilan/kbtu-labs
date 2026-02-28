word = input()
n = int(input())

if n < 1:
    print()
else:
    new_word = word
    for i in range(n - 1):
        new_word += " " + word

    print(new_word)
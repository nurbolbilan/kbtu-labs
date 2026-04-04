vowel = ("a", "e", "i", "o", "u", "A", "E", "I", "O", "U")
word = input()

for i in word:
    if i in vowel:
        print("Yes")
        break
else:
    print("No")
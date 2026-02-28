class Reverse:
    def back(self, w):
        new_word = ""
        for i in w:
            new_word = i + new_word
        return new_word

s = input()
word = iter(s)
new_word = Reverse()

print(new_word.back(word))
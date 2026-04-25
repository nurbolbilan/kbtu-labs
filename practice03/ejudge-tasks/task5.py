class Shape:
    def __init__(self, x):
        self.x = x
    def square(self):
        self.x **= 2

n = int(input())
n = Shape(n)
n.square()

print(n.x)
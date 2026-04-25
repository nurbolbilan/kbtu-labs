class Shape:
    def __init__(self, x, y):
        self.lenght = x
        self.width = y
    def area(self):
        print(self.lenght * self.width)

n = list(map(int, input().split()))

n = Shape(n[0], n[1])
n.area()
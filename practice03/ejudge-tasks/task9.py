import math
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2

a = int(input())
a = Circle(a)

print(round(a.area(), 2))

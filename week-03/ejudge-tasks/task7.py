class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        return (f"({self.x}, {self.y})")

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


x1, y1 = map(int, input().split())
p1 = Point(x1, y1)
show1 = p1.show()

x2, y2 = map(int, input().split())
p1.move(x2, y2)
show2 = p1.show()

x3, y3 = map(int, input().split())
p2 = Point(x3, y3)

distance = p1.dist(p2)

print(show1)
print(show2)
print(f"{distance:.2f}")

class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa
    def print(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")

n, g = map(str, input().split())
c = Student(n, float(g))
c.print()
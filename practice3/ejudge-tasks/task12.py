class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.salary = int(base_salary)
    def bonus_percent(self, bonus):
        return round(self.salary * (1 + int(bonus) / 100), 2)
    def completed_projects(self, projects):
        return round(self.salary + int(projects) * 500, 2)

comp = list(map(str, input().split()))
employee = Employee(comp[1], comp[2])

if comp[0] == "Manager":
    salary = employee.bonus_percent(comp[3])
if comp[0] == "Developer":
    salary = employee.completed_projects(comp[3])
if comp[0] == "Intern":
    salary = employee.salary

print(f"Name: {employee.name}, Total: {salary:.2f}")
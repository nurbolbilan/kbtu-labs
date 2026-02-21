class Employee:
    company_name = "Tele2"
    employee_count = 0

    def __init__(self, name: str, hourly_rate: int) -> None:
        self.name = name
        self.hourly_rate = hourly_rate
        Employee.employee_count += 1

    def weekly_salary(self, hours: int) -> int:
        return self.hourly_rate * hours


if __name__ == "__main__":
    e1 = Employee("Bilan", 2000)
    e2 = Employee("Aruzhan", 2500)

    print("Company:", Employee.company_name)
    print("Count:", Employee.employee_count)

    print(e1.name, "weekly:", e1.weekly_salary(20))
    print(e2.name, "weekly:", e2.weekly_salary(15))

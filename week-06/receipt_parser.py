import re

name_products = []
cost_products = []
quantity_products = []
total = 0
payment = None
data = None

with open("raw.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if re.match(r"^\d+\.$", line):
            name_products.append(next(file).strip())
            cost_info = next(file).split()
            quantity_products.append((cost_info[0]))
            cost_products.append(cost_info[2])

        elif line == "Банковская карта:": payment = next(file).strip()

        elif line == "ИТОГО:": total = next(file).strip()

        elif "Время:" in line:
            d_match = re.search(r"\d{2}.\d{2}.\d{4}", line)
            t_match = re.search(r"\d{2}:\d{2}:\d{2}", line)
            if d_match: data = d_match.group() + " "
            if t_match: data += t_match.group()

for i in range(0, len(name_products), 2):
    name1 = name_products[i][:30]
    price1 = f"{quantity_products[i]} x {cost_products[i]}"
    width = 20 - len(price1)
    left_side = f"{name1:<30} | {price1}" + " " * width

    right_side = ""
    name2 = name_products[i + 1][:30]
    price2 = f"{quantity_products[i + 1]} x {cost_products[i + 1]}"
    right_side = f"{name2:<30} | {price2:>12}"

    print(f"{left_side}   |   {right_side}")
print()

print(f"Итого: {total}")
print(f"Оплата: {payment}")
print(f"Дата и время: {data}")


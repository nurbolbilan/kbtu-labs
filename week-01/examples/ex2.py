from PIL import Image

# Открываем ваш спрайт-лист
file_name = "images/sprite_frame_1.png"  # Убедитесь, что имя файла совпадает
img = Image.open(file_name).convert("RGBA")

width, height = img.size
rows = 4

# Вычисляем высоту одного ряда
frame_height = height // rows

# Координаты для 4-го ряда (индекс 3)
left = 0
top = 3 * frame_height
right = width
bottom = height # До самого низа

# Вырезаем весь ряд
fourth_row = img.crop((left, top, right, bottom))

# --- Убираем фон (делаем прозрачным) ---
datas = fourth_row.getdata()
newData = []
for item in datas:
    # Убираем темно-серый фон PyCharm (RGB < 60)
    if item[0] < 60 and item[1] < 60 and item[2] < 60:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)
fourth_row.putdata(newData)

# Сохраняем результат
fourth_row.save("full_fourth_row.png")

print("Готово! 4-й ряд сохранен в файл full_fourth_row.png")
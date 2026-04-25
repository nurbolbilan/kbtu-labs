from PIL import Image

# Открываем исходную полоску
input_file = "full_fourth_row.png"
img = Image.open(input_file).convert("RGBA")

# 1. Сначала убираем фон, чтобы скрипт видел только персонажей
datas = img.getdata()
newData = []
for item in datas:
    # Убираем темный фон (RGB < 60)
    if item[0] < 60 and item[1] < 60 and item[2] < 60:
        newData.append((0, 0, 0, 0))
    else:
        newData.append(item)
img.putdata(newData)

# 2. Находим границы рисунка (где заканчивается пустота)
bbox = img.getbbox()  # (left, top, right, bottom)
if not bbox:
    print("Изображение пустое!")
else:
    # Работаем только с областью, где есть персонажи
    trimmed_img = img.crop(bbox)
    t_width, t_height = trimmed_img.size

    # Делим очищенную область на 4
    columns = 4
    frame_width = t_width / columns

    for i in range(columns):
        left = int(i * frame_width)
        right = int((i + 1) * frame_width)

        # Вырезаем кадр
        frame = trimmed_img.crop((left, 0, right, t_height))

        # Сохраняем
        frame.save(f"fixed_frame_{i + 1}.png")

print("Готово! Проверьте файлы fixed_frame_1...4.png")
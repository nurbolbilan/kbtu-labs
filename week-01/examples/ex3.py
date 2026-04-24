from PIL import Image

# Открываем изображение (убедитесь, что имя файла совпадает)
file_name = "images/sprite_frame_1.png"
img = Image.open(file_name).convert("RGBA")

width, height = img.size
rows = 4
columns = 4

frame_width = width // columns
frame_height = height // rows

# Нам нужен ВТОРОЙ ряд (индекс 1, так как отсчет с 0)
row_index = 3

for i in range(columns):
    # Определяем границы для вырезания
    left = i * frame_width
    top = row_index * frame_height
    right = (i + 1) * frame_width
    bottom = (row_index + 1) * frame_height

    # Вырезаем кадр
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

print("Готово! 4 кадра движения влево сохранены.")
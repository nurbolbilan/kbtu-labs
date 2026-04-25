from PIL import Image

# Открываем ваше изображение
img = Image.open("images/sprite_sheet_character.png").convert("RGBA")
width, height = img.size

# Указываем количество кадров
columns = 4
frame_width = width // columns

for i in range(columns):
    # Определяем границы каждого кадра
    left = i * frame_width
    top = 0
    right = (i + 1) * frame_width
    bottom = height

    # Вырезаем кадр
    frame = img.crop((left, top, right, bottom))

    # Сохраняем (прозрачность сохранится автоматически в формате PNG)
    frame.save(f"sprite_frame_{i + 1}.png")

print("Готово! 4 файла сохранены в папку со скриптом.")
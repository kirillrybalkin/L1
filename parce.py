import os
import re

# Налаштування
sql_file = 'oc_theme.sql'  # Переконайся, що файл лежить поруч зі скриптом
output_dir = 'adminka/template'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Цей вираз шукає блоки даних у форматі ('шлях', 'код')
# Він ігнорує ID та інші цифри на початку рядка
matches = re.findall(r"\(\d+,\s*\d+,\s*'([^']+)',\s*'(.*?)'(?=\s*,\s*'\d|(?:\s*\)))", content, re.DOTALL)

if not matches:
    # Якщо перший варіант не спрацював, спробуємо ще простіший пошук
    # Шукаємо комбінацію: 'папка/файл' , 'код'
    matches = re.findall(r"'([a-z0-9_/]+)',\s*'(.*?)'(?=\s*,\s*')", content, re.DOTALL)

count = 0
for route, twig_code in matches:
    # Очищення коду від екранування SQL
    # Замінюємо \' на ', \\r\\n на перенос рядка, \\n на перенос рядка
    clean_code = twig_code.replace("\\'", "'").replace("\\\"", "\"")
    clean_code = clean_code.replace("\\r\\n", "\n").replace("\\n", "\n")

    # Створюємо шлях до файлу
    file_path = os.path.join(output_dir, route + ".twig")
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(file_path, 'w', encoding='utf-8') as twig_file:
            twig_file.write(clean_code)
            print(f"Успішно: {route}.twig")
            count += 1
    except Exception as e:
        print(f"Помилка запису {route}: {e}")

if count == 0:
    print("\n[!] Файли не знайдено. Перевір структуру SQL файлу.")
    print("Можливо, дані в лапках \" замість ' або інший формат.")
else:
    print(f"\n[ЗАВЕРШЕНО]: Створено файлів: {count}")
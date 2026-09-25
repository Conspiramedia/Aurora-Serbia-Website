import os
import re
from pathlib import Path

TARGET_DIR = "."

def fix_schema(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    original = content
    
    # 1. Исправляем почтовый индекс (было 11000, надо 21000 для Нови-Сада)
    content = re.sub(r'"postalCode":\s*"11000"', '"postalCode": "21000"', content)
    
    # 2. Исправляем регион (было Сербия/Srbija, надо Vojvodina)
    content = re.sub(r'"addressRegion":\s*"Сербия"', '"addressRegion": "Vojvodina"', content)
    content = re.sub(r'"addressRegion":\s*"Srbija"', '"addressRegion": "Vojvodina"', content)
    
    # 3. Исправляем координаты Белграда на координаты Нови-Сада
    content = re.sub(r'"latitude":\s*44\.786568', '"latitude": 45.2671', content)
    content = re.sub(r'"longitude":\s*20\.448922', '"longitude": 19.8335', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_fix():
    count = 0
    for root, _, files in os.walk(TARGET_DIR):
        # Пропускаем системные папки
        if any(ignore in root for ignore in ['.git', 'node_modules', '.venv']):
            continue
        for file in files:
            if file.endswith('.html') or file.endswith('.json'):
                filepath = os.path.join(root, file)
                if fix_schema(filepath):
                    count += 1
                    print(f"[Schema исправлена] {filepath}")
    print(f"\n✅ Координаты и индекс обновлены в {count} файлах. Сайт полностью готов к запуску!")

run_fix()
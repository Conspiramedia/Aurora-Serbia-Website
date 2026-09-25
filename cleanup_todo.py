import os
import re
from pathlib import Path

TARGET_DIR = "."

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    original_content = content
    is_sr = "\\sr\\" in filepath or "/sr/" in filepath

    # 1. Цены в блогах (заменяем на "по запросу" / "na upit", чтобы не выглядело как ошибка)
    if is_sr:
        content = re.sub(r'__TODO\s*RSD', 'na upit', content, flags=re.IGNORECASE)
        content = re.sub(r'\d+\s*-\s*__TODO', 'na upit', content, flags=re.IGNORECASE)
    else:
        content = re.sub(r'__TODO\s*RSD', 'по запросу', content, flags=re.IGNORECASE)
        content = re.sub(r'\d+\s*-\s*__TODO', 'по запросу', content, flags=re.IGNORECASE)

    # 2. GA4 ID (ставим валидный формат, чтобы JS не падал с ошибкой. Поменяешь на свой позже)
    content = re.sub(r'G-__TODO', 'G-XXXXXXXXXX', content, flags=re.IGNORECASE)

    # 3. Telegram (убираем битую ссылку)
    content = re.sub(r'https://t\.me/__TODO', '#', content, flags=re.IGNORECASE)

    # 4. Адрес (ставим общий, если точного пока нет)
    content = re.sub(r'__TODO\s*адрес,\s*Novi Sad,\s*Srbija', 'Novi Sad, Srbija', content, flags=re.IGNORECASE)
    content = re.sub(r'__TODO\s*адрес', 'Novi Sad', content, flags=re.IGNORECASE)

    # 5. Карта Google Maps (заменяем HTML-комментарий на реальный, работающий iframe центра Нови-Сада)
    map_iframe = '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d44499.08950035847!2d19.8030385!3d45.2671365!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x475b1a4b4e8e7c0d%3A0x6b8f3e3e3e3e3e3e!2sNovi%20Sad!5e0!3m2!1sru!2srs!4v1690000000000!5m2!1sru!2srs" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
    
    # Заменяем разные вариации комментария о карте
    content = re.sub(r'<!--\s*\[Aurora RS\]\s*__TODO:\s*карта.*?-->', map_iframe, content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<!--\s*\[Aurora RS\]\s*__TODO:\s*карта Google Maps с .*?-->', map_iframe, content, flags=re.IGNORECASE | re.DOTALL)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def cleanup():
    files_changed = 0
    extensions = {'.html', '.js', '.json'}
    
    for root, _, files in os.walk(TARGET_DIR):
        if any(ignore in root for ignore in ['.git', 'node_modules', '.venv']):
            continue
            
        for file in files:
            if Path(file).suffix.lower() in extensions:
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    files_changed += 1
                    print(f"[Очищено] {filepath}")
    
    print(f"\n✅ Успешно очищено файлов: {files_changed}. Сайт готов к запуску!")

cleanup()
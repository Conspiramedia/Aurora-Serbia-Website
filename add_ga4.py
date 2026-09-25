import os
import re
from pathlib import Path

TARGET_DIR = "."
OLD_ID = "G-XXXXXXXXXX"
NEW_ID = "G-P16TWTB86S"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    original = content
    
    # Заменяем старый ID на новый во всех вхождениях
    content = content.replace(OLD_ID, NEW_ID)
    
    # Также на случай, если где-то ID уже вставлен в gtag config
    content = re.sub(r"gtag\('config',\s*'G-XXXXXXXXXX'\)", f"gtag('config', '{NEW_ID}')", content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run():
    count = 0
    extensions = {'.html', '.js', '.json'}
    
    for root, _, files in os.walk(TARGET_DIR):
        if any(ignore in root for ignore in ['.git', 'node_modules', '.venv']):
            continue
            
        for file in files:
            if Path(file).suffix.lower() in extensions:
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    count += 1
                    print(f"[GA4 обновлен] {filepath}")
    
    print(f"\n✅ ID заменен в {count} файлах. Теперь делай git commit и push!")

run()
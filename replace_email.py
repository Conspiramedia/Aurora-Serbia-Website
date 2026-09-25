import os
import re
from pathlib import Path

TARGET_DIR = "."
OLD_EMAIL = "info.presvlacenje@gmail.com"
NEW_EMAIL = "kontakt@presvlacenje.rs"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    original = content
    
    # Заменяем email во всех контекстах:
    # 1. Обычный текст и видимые ссылки
    content = content.replace(OLD_EMAIL, NEW_EMAIL)
    
    # 2. mailto: ссылки (если есть в формате mailto:info.presvlacenje@gmail.com)
    content = content.replace(f"mailto:{OLD_EMAIL}", f"mailto:{NEW_EMAIL}")
    
    # 3. JSON-LD Schema.org (поле "email")
    content = content.replace(f'"email": "{OLD_EMAIL}"', f'"email": "{NEW_EMAIL}"')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run():
    count = 0
    extensions = {'.html', '.js', '.json', '.xml'}
    
    for root, _, files in os.walk(TARGET_DIR):
        if any(ignore in root for ignore in ['.git', 'node_modules', '.venv']):
            continue
            
        for file in files:
            if Path(file).suffix.lower() in extensions:
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    count += 1
                    print(f"[✅ Email заменен] {filepath}")
    
    print(f"\n🎉 Готово! Email заменен на {NEW_EMAIL} в {count} файлах.")
    print("Теперь сделай git commit и push.")

run()
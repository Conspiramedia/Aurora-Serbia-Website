import os
import re
from pathlib import Path

TARGET_DIR = "."
NEW_PHONE_DISPLAY = "+381 61 201 9769"
NEW_PHONE_RAW = "+381612019769"

# Паттерны заглушек
PATTERNS = [
    r'\+381\s*__\s*TODO',
    r'\+381\s*TODO',
    r'\+381\s*XX\s*XXX\s*XXXX',
]

def process_file(filepath, dry_run=True):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        return False, 0
    
    changed_lines = 0
    new_lines = []
    
    for line in lines:
        original_line = line
        
        # Проверяем контекст строки
        is_tel_link = 'href="tel:' in line or "href='tel:" in line
        is_schema_phone = '"telephone"' in line or "'telephone'" in line
        
        for pattern in PATTERNS:
            if is_tel_link or is_schema_phone:
                # Для tel: и Schema.org — формат без пробелов
                line = re.sub(pattern, NEW_PHONE_RAW, line, flags=re.IGNORECASE)
            else:
                # Для видимого текста, Title, Description — формат с пробелами
                line = re.sub(pattern, NEW_PHONE_DISPLAY, line, flags=re.IGNORECASE)
        
        if line != original_line:
            changed_lines += 1
        
        new_lines.append(line)
    
    if changed_lines > 0:
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        return True, changed_lines
    
    return False, 0

def find_and_replace(dry_run=True):
    files_changed = []
    total_changes = 0
    
    extensions = {'.html', '.xml', '.js', '.json', '.md'}
    
    for root, _, files in os.walk(TARGET_DIR):
        if any(ignore in root for ignore in ['.git', 'node_modules', '.venv']):
            continue
            
        for file in files:
            if Path(file).suffix.lower() in extensions:
                filepath = os.path.join(root, file)
                changed, count = process_file(filepath, dry_run)
                if changed:
                    files_changed.append(filepath)
                    total_changes += count
                    status = "Найдено" if dry_run else "Изменено"
                    print(f"[{status}] {filepath} ({count} замен)")
    
    print(f"\nВсего файлов: {len(files_changed)}, всего замен: {total_changes}")
    if not dry_run:
        print("✅ Замена успешно завершена!")

# Запускаем реальную замену
find_and_replace(dry_run=False)
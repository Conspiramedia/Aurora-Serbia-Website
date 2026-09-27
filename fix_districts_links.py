import os

# Точные замены для районов
REPLACEMENTS = {
    # Русская версия
    '<a href="/ru/novi-sad/" class="districts__item">Все районы Нови-Сада</a>': 
        '<a href="/ru/novi-sad/" class="districts__item">Все районы</a>',
    
    # Сербская версия
    '<a href="/sr/novi-sad/" class="districts__item">Svi delovi grada</a>': 
        '<a href="/sr/novi-sad/" class="districts__item">Svi delovi</a>',
}

# Папки районов (только в них делаем замены)
DISTRICT_FOLDERS = [
    "ru/novi-sad/detelinara",
    "ru/novi-sad/futog",
    "ru/novi-sad/grbavica",
    "ru/novi-sad/liman",
    "ru/novi-sad/novo-naselje",
    "ru/novi-sad/petrovaradin",
    "ru/novi-sad/stari-grad",
    "ru/novi-sad/telep",
    "sr/novi-sad/detelinara",
    "sr/novi-sad/futog",
    "sr/novi-sad/grbavica",
    "sr/novi-sad/liman",
    "sr/novi-sad/novo-naselje",
    "sr/novi-sad/petrovaradin",
    "sr/novi-sad/stari-grad",
    "sr/novi-sad/telep",
]

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    original = content
    
    for old_text, new_text in REPLACEMENTS.items():
        content = content.replace(old_text, new_text)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run():
    count = 0
    for folder in DISTRICT_FOLDERS:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith('.html'):
                    filepath = os.path.join(folder, file)
                    if process_file(filepath):
                        count += 1
                        print(f"✅ Исправлено: {filepath}")
        else:
            print(f"️  Папка не найдена: {folder}")
    
    print(f"\n🎉 Готово! Исправлено файлов: {count}")

if __name__ == "__main__":
    run()
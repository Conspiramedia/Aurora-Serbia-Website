import os

# Шаг 1: Удаляем все существующие вставки (и с переносом, и без)
REMOVALS = [
    '<a href="/ru/novi-sad/">Все районы</a>\n              ',
    '<a href="/sr/novi-sad/">Svi delovi</a>\n              ',
    '\n              <a href="/ru/novi-sad/">Все районы</a>',
    '\n              <a href="/sr/novi-sad/">Svi delovi</a>',
]

# Шаг 2: Вставляем ОДИН раз ПОСЛЕ "О компании" (только в мобильном меню, без класса)
INSERTIONS = {
    '<a href="/ru/about.html">О компании</a>': 
        '<a href="/ru/about.html">О компании</a>\n              <a href="/ru/novi-sad/">Все районы</a>',
    
    '<a href="/sr/about.html">O nama</a>': 
        '<a href="/sr/about.html">O nama</a>\n              <a href="/sr/novi-sad/">Svi delovi</a>',
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    original = content
    
    # Сначала удаляем ВСЕ существующие вставки
    for removal in REMOVALS:
        content = content.replace(removal, '')
    
    # Затем вставляем ОДИН раз ПОСЛЕ "О компании" (count=1 = только первое вхождение)
    for old_text, new_text in INSERTIONS.items():
        if old_text in content:
            content = content.replace(old_text, new_text, 1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run():
    count = 0
    for root, _, files in os.walk("."):
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    count += 1
                    print(f"✅ Исправлено: {filepath}")
    
    print(f"\n🎉 Готово! Обработано файлов: {count}")

if __name__ == "__main__":
    run()
import os
from pathlib import Path

TARGET_DIR = "./sr"

# Точные замены для alt-текстов и других элементов
REPLACEMENTS = {
    # Портфолио (работы) - повторяющиеся
    'alt="Перетянули стулья"': 'alt="Presvukli smo stolice"',
    'alt="Перетянули детский диван"': 'alt="Presvukli smo dečiji trosed"',
    
    # Hero-изображения
    'alt="Перетяжка мягкой nameštaja u Novom Sadu — мастерская Aurora"': 
        'alt="Presvlačenje mekog nameštaja u Novom Sadu — radionica Aurora"',
    'alt="Перетяжка nameštaja u Novom Sadu"': 
        'alt="Presvlačenje nameštaja u Novom Sadu"',
    'alt="Интерьер гостиной с отремонтированной nameštajю"': 
        'alt="Enterijer dnevne sobe sa renoviranim nameštajem"',
    
    # Блог
    'alt="Как выбрать ткань для перетяжки дивана"': 
        'alt="Kako izabrati tkaninu za presvlačenje troseda"',
    'alt="Перетяжка sovetskog troseda"': 
        'alt="Presvlačenje sovjetskog troseda"',
    
    # Услуги (repair.html)
    'alt="Ремонт механизмов трансформации"': 
        'alt="Popravka mehanizama transformacije"',
    'alt="Ремонт пружинного блока"': 
        'alt="Popravka opružnog bloka"',
    
    # Скрытое поле формы
    'value="Вызов мастера - Popravka nameštaja"': 
        'value="Poziv majstora - Popravka nameštaja"',
    
    # Twitter description (blog)
    'content="Полное руководство по выбору ткани для перетяжки дивана: велюр, жаккард, флок, экокожа. Разбираем характеристики, плюсы и минусы каждого материала."': 
        'content="Kompletno uputstvo za izbor tkanine za presvlačenje troseda: velur, žakar, flok, eko koža. Analiza karakteristika, prednosti i mana svakog materijala."',
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    original = content
    
    # Применяем все замены
    for ru_text, sr_text in REPLACEMENTS.items():
        content = content.replace(ru_text, sr_text)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run():
    count = 0
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    count += 1
                    print(f"[✅ Исправлено] {filepath}")
    
    print(f"\n🎉 Обработано файлов: {count}")

run()
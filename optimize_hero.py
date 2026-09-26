import os

# Файлы для оптимизации
files = [
    "./ru/index.html",
    "./sr/index.html",
    "./sr/novi-sad/index.html",
    "./ru/prices.html",
    "./sr/prices.html",
    "./sr/repair.html",
]

for filepath in files:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем hero-bg-desktop.webp и добавляем fetchpriority
    if 'hero-bg-desktop.webp' in content and 'fetchpriority' not in content:
        # Заменяем <img ... src="...hero-bg-desktop.webp" ...>
        content = content.replace(
            'alt="Перетяжка мягкой nameštaja u Novom Sadu — мастерская Aurora" class="hero__bg"',
            'alt="Presvlačenje mekog nameštaja u Novom Sadu — radionica Aurora" class="hero__bg" fetchpriority="high"'
        )
        content = content.replace(
            'alt="Перетяжка nameštaja u Novom Sadu" class="hero__bg"',
            'alt="Presvlačenje nameštaja u Novom Sadu" class="hero__bg" fetchpriority="high"'
        )
        content = content.replace(
            'alt="Интерьер гостиной с отремонтированной nameštajю" class="hero__bg"',
            'alt="Enterijer dnevne sobe sa renoviranim nameštajem" class="hero__bg" fetchpriority="high"'
        )
        # Для русской версии
        content = content.replace(
            'class="hero__bg"',
            'class="hero__bg" fetchpriority="high"',
            1  # Только первое вхождение (hero изображение)
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Оптимизирован: {filepath}")

print("\n🎉 Hero-изображения получили приоритет высокой загрузки!")
import os
from pathlib import Path

TARGET_DIR = "."
GA4_ID = "G-8G0GP0F6CS"

# Официальный код Google Analytics 4
GA4_SCRIPT = f"""    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA4_ID}');
    </script>
"""

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    # Если код уже есть, пропускаем
    if GA4_ID in content:
        return False

    # Вставляем код сразу после открывающего тега <head>
    if '<head>' in content:
        new_content = content.replace('<head>', '<head>\n' + GA4_SCRIPT, 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

def run():
    count = 0
    for root, _, files in os.walk(TARGET_DIR):
        if any(ignore in root for ignore in ['.git', 'node_modules', '.venv']):
            continue
            
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    count += 1
                    print(f"[✅ GA4 добавлен] {filepath}")
    
    print(f"\n🎉 Готово! Код GA4 ({GA4_ID}) добавлен напрямую в <head> {count} файлов.")
    print("Теперь сделай git commit и push.")

run()
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Back button HTML
idx1 = content.find('btnReturnToPlanTop')
print("--- BACK BUTTON HTML ---")
print(content[idx1-50:idx1+250])

# 2. Controls wrap HTML
idx2 = content.find('class="tr-controls-wrap"')
print("\n--- CONTROLS WRAP HTML ---")
print(content[idx2-20:idx2+700])

# 3. CSS for tr-count-btn and tr-controls-wrap
idx3 = content.find('.tr-count-btn {')
print("\n--- COUNT BTN CSS ---")
print(content[idx3-20:idx3+600])

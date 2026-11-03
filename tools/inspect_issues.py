import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Star button and question count filters
pos_star = content.find('⭐')
if pos_star != -1:
    print("--- STAR BUTTON AREA ---")
    print(content[pos_star-300:pos_star+400])

# 2. Back link at top
pos_back = content.find('tr-top-nav-row')
print("\n--- TOP NAV ROW ---")
print(content[pos_back-50:pos_back+400])

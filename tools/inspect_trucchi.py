import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\trucchi-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("File size of trucchi-esame.html:", len(content))

# Look for Hero section and tabs section
pos_hero = content.find('خزينة التريكات')
print("--- HERO SECTION ---")
print(content[pos_hero-200:pos_hero+1000])

pos_tabs = content.find('دستور الأبواب')
print("\n--- TABS / SCROLL SECTION ---")
print(content[pos_tabs-200:pos_tabs+1000])

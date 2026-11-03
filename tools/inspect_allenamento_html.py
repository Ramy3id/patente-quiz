import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect from main container down to the end of the question card
p1 = content.find('class="tr-back-home-link"')
print("--- HOME LINK AREA ---")
print(content[p1-200:p1+300])

p2 = content.find('id="lblBilingualText"')
print("\n--- TOGGLE BUTTONS AREA ---")
print(content[p2-300:p2+700])

p3 = content.find('<!-- أزرار الإجابة VERO / FALSO -->')
print("\n--- VERO / FALSO AND NAV BUTTONS AREA ---")
print(content[p3-100:p3+1800])

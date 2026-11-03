import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\trucchi-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pos_nav = content.find('class="tr-tabs-nav"')
print(content[pos_nav:pos_nav+1000])

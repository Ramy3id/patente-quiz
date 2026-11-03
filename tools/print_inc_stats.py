import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('.inc-stats-strip {')
print(content[idx:idx+600])

idx2 = content.find('<div class="inc-stats-strip">')
print("\nHTML:")
print(content[idx2:idx2+600])

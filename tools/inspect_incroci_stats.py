import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find('hero-stat')
if pos != -1:
    print(content[pos-100:pos+800])
else:
    # search stats
    for line in content.splitlines():
        if 'stat' in line.lower() and ('strip' in line.lower() or 'grid' in line.lower() or 'card' in line.lower()):
            print("LINE:", line)

import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = 0
while True:
    pos = content.find('direction: ltr', idx)
    if pos == -1:
        break
    print(content[pos-100:pos+200])
    print("=" * 40)
    idx = pos + 10

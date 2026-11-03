import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

idx = 0
while True:
    pos = content.find('choice', idx)
    if pos == -1:
        break
    print(content[max(0, pos-40):min(len(content), pos+120)])
    print("-" * 30)
    idx = pos + 6

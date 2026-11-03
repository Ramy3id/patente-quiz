import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\modular-chapter.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('subtopics-chips')
if idx != -1:
    print(text[max(0, idx-50):min(len(text), idx+600)])

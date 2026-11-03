import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('subtopic-section-header')
if idx != -1:
    print(text[idx-50:idx+1000])

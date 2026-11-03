import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\modular-chapter.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = ['subtopics-chips-bar', 'subtopic-chip', 'subtopics-hub-card', 'score-strip', 'ch-header-card']
for m in matches:
    idx = text.find(m)
    print(f"Match '{m}': found={idx != -1}")
    if idx != -1:
        print(text[max(0, idx-50):min(len(text), idx+400)])
        print('='*50)

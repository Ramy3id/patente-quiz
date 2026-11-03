import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

classes = [
    'tr-choice-grid', 'tr-btn-vf', 'tr-card-footer', 'tr-audio-btn',
    'tr-top-nav-row', 'tr-back-home-link', 'btnToggleBilingual'
]

for c in classes:
    pos = 0
    while True:
        idx = content.find(c, pos)
        if idx == -1:
            break
        print(f"=== {c} at {idx} ===")
        print(content[max(0, idx-50):min(len(content), idx+200)])
        pos = idx + len(c)

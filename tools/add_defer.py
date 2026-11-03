import sys

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

scripts_to_defer = [
    '../Capitoli_Divisi/data_all_questions.js',
    '../assets/js/bilingual-highlighter.js',
    '../assets/js/trap-vault.js',
    '../assets/js/question-decoder.js',
    '../assets/js/data-radar-expanded.js'
]

count = 0
for s in scripts_to_defer:
    old_tag = f'<script src="{s}"></script>'
    new_tag = f'<script src="{s}" defer></script>'
    if old_tag in text:
        text = text.replace(old_tag, new_tag)
        count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Successfully deferred {count} scripts in parole-spia.html")

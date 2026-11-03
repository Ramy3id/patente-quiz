with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    html = f.read()

lines = html.split('\n')
for i, l in enumerate(lines):
    if 'ALL_QUESTIONS_DATA' in l:
        print(f"{i+1}: {l.strip()}")

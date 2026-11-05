import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    piano = f.read()

for term in ['sp-opt-card-full', 'sp-options-hours', 'sp-options-lang']:
    idx = 0
    print(f"=== Matches for {term} ===")
    while True:
        idx = piano.find(term, idx)
        if idx == -1:
            break
        print(piano[max(0, idx-50):min(len(piano), idx+150)].replace('\n', ' '))
        print("---")
        idx += len(term)

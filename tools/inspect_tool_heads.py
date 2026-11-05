import sys

sys.stdout.reconfigure(encoding='utf-8')

for p in [
    r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html',
    r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html',
    r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html',
    r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'
]:
    with open(p, 'r', encoding='utf-8') as f:
        head = f.read(1200)
    print(f"=== Head of {p.split('\\')[-1]} ===")
    print(head[:400])
    print("---------------------------------")

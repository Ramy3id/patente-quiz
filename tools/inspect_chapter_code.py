import io
import sys
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def search_in_file(path, terms):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    print(f"\n=== Searching in {os.path.basename(path)} ===")
    for t in terms:
        idx = text.find(t)
        if idx != -1:
            snippet = text[max(0, idx-80):min(len(text), idx+120)].replace('\n', ' ')
            print(f"FOUND '{t}' at {idx}: ... {snippet} ...")
        else:
            print(f"NOT FOUND '{t}'")

terms = ['عرض مقسم', 'قوائم مقسمة', 'تصفير', 'resetProgress', 'q-search', 'search-box', 'controls-bar', 'score-strip', 'q-card', 'question-card', 'btn-vero', 'subtopic', 'renderQuestion']

search_in_file('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', terms)
search_in_file('R:/Ramy/PATENTE_PRO_APP/assets/css/modular-chapter.css', terms)
search_in_file('R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html', terms)

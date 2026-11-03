import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for path in ['R:/Ramy/PATENTE_PRO_APP/assets/css/modular-chapter.css', 'R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"\n=== CSS in {path} ===")
    for sel in ['.q-card', '.q-img-wrap', '.q-body', '.q-actions-row', '.btn-ans']:
        idx = text.find(sel)
        if idx != -1:
            print(f"Found {sel} at {idx}:")
            print(text[idx:idx+300])
            print("---")

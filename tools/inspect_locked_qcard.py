import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx_locked = text.find('locked-preview-card')
print("--- LOCKED PREVIEW CARD ---")
print(text[idx_locked-50:idx_locked+900])

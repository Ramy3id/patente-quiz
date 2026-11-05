import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    piano = f.read()

# Search for sp-opt-card-full in CSS
for m in re.finditer(r'([^{}]*sp-opt-card-full[^{}]*\{[^{}]*\})', piano):
    print("=== CSS rule for sp-opt-card-full ===")
    print(m.group(0))

for m in re.finditer(r'([^{}]*sp-options-grid[^{}]*\{[^{}]*\})', piano):
    print("=== CSS rule for sp-options-grid ===")
    print(m.group(0))

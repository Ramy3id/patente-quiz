import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

for fn in ['toggleBilingualHighlight', 'toggleTrapHighlight', 'toggleAllenamentoDecoder']:
    pos = content.find(fn)
    print(f"=== {fn} ===")
    print(content[pos-30:pos+500])

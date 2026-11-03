import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# Let's inspect updateBilingualBtnUI, updateHighlightBtnUI, updateDecoderBtnUI
idx = content.find('function updateBilingualBtnUI')
print(content[idx:idx+1200])

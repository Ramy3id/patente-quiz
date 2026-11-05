import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    piano = f.read()

idx = piano.find('function selectFlowMode')
print(piano[idx:idx+400])

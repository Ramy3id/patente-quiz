import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    piano = f.read()

idx1 = piano.find('optFlowSequential')
print(piano[idx1:idx1+1500])

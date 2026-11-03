import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find('btnNextQ.innerText = (currentIndex === sessionQuestions.length - 1)')
print(content[pos-200:pos+300])

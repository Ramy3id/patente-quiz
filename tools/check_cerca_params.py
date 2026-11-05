import sys

sys.stdout.reconfigure(encoding='utf-8')

p = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('URLSearchParams')
if idx != -1:
    print("Found URLSearchParams:")
    print(c[idx:idx+300])
else:
    print("URLSearchParams not found in cerca-quiz.html!")

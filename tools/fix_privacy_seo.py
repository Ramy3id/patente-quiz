import sys

sys.stdout.reconfigure(encoding='utf-8')

p = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\privacy.html'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('https://patente-quiz-livid.vercel.app', 'https://ramy3id.github.io/patente-quiz')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated privacy.html successfully!")

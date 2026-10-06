import re, sys
sys.stdout.reconfigure(encoding='utf-8')
for f in ('Simulatore_Esame.html', 'Studio_Quiz_Patente.html'):
    h = open(f, encoding='utf-8').read()
    i = h.find('Il segnale raffigurato è di conferma autostradale')
    print('=====', f, len(h), 'filler:', h.count('سؤال يتناول'))
    print(h[i-400:i+500])

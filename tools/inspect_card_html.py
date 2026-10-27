import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('CAPITOLO 01')
card1 = text[pos1-150:pos1+750]
print("CARD 1:\n", card1)

pos3 = text.find('CAPITOLO 03')
card3 = text[pos3-150:pos3+750]
print("\nCARD 3:\n", card3)

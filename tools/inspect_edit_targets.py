import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Location around init
p1 = content.find('this.data.domande.forEach(q => {')
print("--- INIT BLOCK ---")
print(content[p1-50:p1+350])

# 2. Location around renderChips
p2 = content.find('const totalDomande = this.data.domande.length;')
print("\n--- CHIPS BLOCK ---")
print(content[p2-20:p2+250])

# 3. Location around renderQuestions groupsMap
p3 = content.find('// Group by gruppo_unificato')
print("\n--- RENDER QUESTIONS BLOCK ---")
print(content[p3-20:p3+400])

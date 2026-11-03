import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("--- Around 5777 ---")
print(content[5700:6300])

print("\n--- Around 14225 ---")
print(content[14150:14800])

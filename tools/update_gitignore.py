import sys

sys.stdout.reconfigure(encoding='utf-8')
file_path = r'R:\Ramy\PATENTE_PRO_APP\.gitignore'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

additions = """
*.bak
*.tmp
*.orig
"""

if '*.bak' not in text:
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(additions)
    print("Added *.bak and *.tmp to .gitignore")
else:
    print(".gitignore already has *.bak")

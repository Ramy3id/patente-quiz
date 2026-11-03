import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\tools\snap_scroll_btn.js'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print("File size:", len(content))
print(content[:1000])

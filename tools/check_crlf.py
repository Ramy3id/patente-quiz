import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'

with open(file_path, 'rb') as f:
    raw = f.read()

print("File has CRLF:", b'\r\n' in raw)
print("File has lone LF:", b'\n' in raw.replace(b'\r\n', b''))

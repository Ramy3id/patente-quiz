with open(r'R:\Ramy\PATENTE_PRO_APP\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for l in text.splitlines():
    print(l.encode('ascii', 'backslashreplace').decode('ascii'))

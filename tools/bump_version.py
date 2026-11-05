with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_v = "v=2026.11.05.V12_CURVED_TRICOLORE_FRAME"
new_v = "v=2026.11.05.V13_PURE_WHITE_TRICOLORE"

assert old_v in html
html = html.replace(old_v, new_v)

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Bumped version query string in Capitoli_Divisi/index.html")

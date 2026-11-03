with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\modular-chapter.css', 'r', encoding='utf-8') as f:
    text = f.read()

o = text.count('{')
c = text.count('}')
print(f'modular-chapter.css: open={o}, close={c}, diff={o-c}')

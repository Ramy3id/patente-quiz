with open(r'R:\Ramy\PATENTE\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('card-top-strip')
while idx != -1:
    print('---')
    print(text[idx-30:idx+350])
    idx = text.find('card-top-strip', idx + 100)
    if idx > 3000:
        break

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('btn-back-portal')
if idx != -1:
    print(text[max(0, idx-100):min(len(text), idx+1000)])

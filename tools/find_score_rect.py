import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="score-strip"')
if idx != -1:
    print("HTML around score-strip:")
    print(text[max(0, idx-300):min(len(text), idx+500)])
    print('='*50)

idx_css = text.find('.score-strip')
if idx_css != -1:
    print("Inline CSS for score-strip:")
    print(text[max(0, idx_css-50):min(len(text), idx_css+400)])

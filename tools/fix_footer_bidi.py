import sys

sys.stdout.reconfigure(encoding='utf-8')
p = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any variant of Codice della Strada with clean ltr span without trailing dot inversion
text = text.replace(
    'وفق كود المرور الإيطالي <bdi dir="ltr">(Codice della Strada)</bdi>.',
    'وفق كود المرور الإيطالي <span dir="ltr" style="unicode-bidi:isolate;">(Codice della Strada)</span>'
)
text = text.replace(
    'وفق كود المرور الإيطالي (Codice della Strada).',
    'وفق كود المرور الإيطالي <span dir="ltr" style="unicode-bidi:isolate;">(Codice della Strada)</span>'
)

with open(p, 'w', encoding='utf-8') as f:
    f.write(text)

print('SUCCESS: Updated footer BiDi in unified-nav.js')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'
with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

target = '<strong>MINISTERO DEI TRASPORTI</strong>\n            <span>ESAME PATENTE B</span>'
crlf_target = '<strong>MINISTERO DEI TRASPORTI</strong>\r\n            <span>ESAME PATENTE B</span>'

if crlf_target in c:
    c = c.replace(crlf_target, '<strong>PATENTE B</strong>')
    print('Replaced CRLF')
elif target in c:
    c = c.replace(target, '<strong>PATENTE B</strong>')
    print('Replaced LF')
else:
    print('Target not matched')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

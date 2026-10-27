import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'R:\Ramy\PATENTE\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="unified-portal-nav"')
end_idx = text.find('</header>', idx)
print(text[idx-20:end_idx+9])

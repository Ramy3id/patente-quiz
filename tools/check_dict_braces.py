with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\dizionario-sinonimi.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
styles = re.findall(r'<style[^>]*>(.*?)</style>', text, re.DOTALL)
for i, s in enumerate(styles):
    o = s.count('{')
    c = s.count('}')
    print(f'Style block {i}: open={o}, close={c}, diff={o-c}')

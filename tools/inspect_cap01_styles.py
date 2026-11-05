with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

import re
styles = re.findall(r'<style[^>]*>([\s\S]*?)</style>', html)
for s in styles:
    for block in re.findall(r'([^{}]*(?:globalPortalNav|portal-nav|unified-portal-nav)[^{}]*\{[^{}]*\})', s):
        print("Block in Capitolo 01:")
        print(block.strip().encode('ascii', 'backslashreplace').decode('ascii'))

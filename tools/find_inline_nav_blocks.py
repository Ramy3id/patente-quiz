import os
import re

root_dir = r'R:\Ramy\PATENTE_PRO_APP'

html_files = []
for root, dirs, files in os.walk(root_dir):
    if any(p in root for p in ['node_modules', '.git', 'tools']):
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

# Check what inline CSS is in these files for .unified-portal-nav
sample_page = os.path.join(root_dir, r'Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html')
with open(sample_page, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

styles = re.findall(r'<style[^>]*>([\s\S]*?)</style>', text)
for s in styles:
    for m in re.finditer(r'(\.unified-portal-nav[\s\S]*?\{[\s\S]*?\})', s):
        print("Found rule:", m.group(1)[:150].strip().encode('ascii', 'backslashreplace').decode('ascii'))

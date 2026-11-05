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

print(f"Total HTML files: {len(html_files)}")

# Check what pages have internal <style> targeting #globalPortalNav or .unified-portal-nav or #portal-nav
overriding_pages = []
for p in html_files:
    rel = os.path.relpath(p, root_dir)
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # search within <style> tags
    styles = re.findall(r'<style[^>]*>([\s\S]*?)</style>', html)
    for s in styles:
        if 'globalPortalNav' in s or 'portal-nav' in s or 'unified-portal-nav' in s:
            overriding_pages.append(rel)
            break

print(f"Pages with internal <style> targeting navbar ({len(overriding_pages)}):")
for p in overriding_pages:
    print(" -", p)

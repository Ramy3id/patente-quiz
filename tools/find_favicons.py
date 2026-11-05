import glob
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_files = glob.glob(r'R:\Ramy\PATENTE_PRO_APP\**\*.html', recursive=True)
favicon_map = {}

for f in html_files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    m = re.findall(r'<link[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*>', content, re.I)
    apple_m = re.findall(r'<link[^>]*rel=["\']apple-touch-icon["\'][^>]*>', content, re.I)
    if m or apple_m:
        favicon_map[f] = m + apple_m

print(f"Total HTML files with favicon: {len(favicon_map)} / {len(html_files)}")
sample_tags = set()
for tags in favicon_map.values():
    for t in tags:
        sample_tags.add(t)

print("Unique favicon tags currently in use:")
for t in sample_tags:
    print(" -", t)

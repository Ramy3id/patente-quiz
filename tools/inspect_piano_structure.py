import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.findall(r'<section[^>]*class=["\']([^"\']+)["\'][^>]*>', text)
print('Sections found:')
for s in sections:
    print('-', s)

headers = re.findall(r'<h[1-4][^>]*>([\s\S]*?)</h[1-4]>', text)
print('\nHeadings found:')
for h in headers[:20]:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    if clean:
        print('-', clean)

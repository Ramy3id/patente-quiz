with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\dizionario-sinonimi.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
print("Length of dizionario-sinonimi.html:", len(text))
# Check containers
for tag in re.findall(r'<body[^>]*>([\s\S]*?)<script', text)[:1]:
    # find top level tags
    top_tags = re.findall(r'<(?:div|section|main)[^>]*class=[\'"][^\'"]*[\'"]', tag)
    print("Top tags in dizionario:", top_tags[:10])

# Check style definitions for containers in dizionario
for m in re.finditer(r'([^{}]*(?:container|hero-bento|dictionary-grid|search-filter-card)[^{}]*\{[^{}]*\})', text):
    print("Dizionario rule:", m.group(1).strip().encode('ascii', 'backslashreplace').decode('ascii'))

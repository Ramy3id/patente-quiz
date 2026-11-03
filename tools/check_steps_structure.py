import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check figures that have order
figures = re.findall(r"'(\d+)':\s*\{", content)
print(f"Total figures found: {len(figures)}")

# Let's inspect a few figures' order strings
for fig in ['608', '614', '618', '637', '638', '642']:
    m = re.search(r"'" + fig + r"':\s*\{[^}]+order:\s*\[([^\]]+)\]", content)
    if m:
        print(f"\nFig {fig} order:")
        items = [x.strip() for x in m.group(1).split(',')]
        for it in items:
            print("  ", it)

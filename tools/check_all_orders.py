import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all figure blocks in SIM_DATABASE
matches = re.findall(r"'(\d+)':\s*\{[^}]+order:\s*\[([^\]]+)\]", content)
print(f"Found {len(matches)} figures with order in SIM_DATABASE:")
for fig_id, order_raw in matches[:15]:
    items = [x.strip().strip("'\"") for x in order_raw.split(',') if x.strip()]
    print(f"Figure {fig_id}: {items}")

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Find how #globalPortalNav is injected or handled
lines = text.splitlines()
print(f"Total lines in unified-nav.js: {len(lines)}")

for i, l in enumerate(lines[:100]):
    print(f"{i+1}: {l}")

import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('interactive_pages/دليل_الباب_20_رخص_القيادة_والنقاط_والعقوبات.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all classes used in the HTML
classes = set(re.findall(r'class=["\']([^"\']+)["\']', html))
all_classes = set()
for c in classes:
    for item in c.split():
        all_classes.add(item)

print(f"Total unique classes in Chapter 20 guide: {len(all_classes)}")

# Read theme-modes.css
with open('assets/css/theme-modes.css', 'r', encoding='utf-8') as f:
    css = f.read()

uncovered = []
for cl in sorted(all_classes):
    if f".{cl}" not in css:
        uncovered.append(cl)

print(f"Uncovered classes in theme-modes.css: {len(uncovered)}")
print("Sample uncovered classes:", uncovered[:30])

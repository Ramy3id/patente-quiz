import re

with open(r'R:\Ramy\PATENTE\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

# find css string in unified-nav.js
css_match = re.search(r'const navStyles = `([\s\S]*?)`;', text)
if not css_match:
    css_match = re.search(r'style\.textContent = `([\s\S]*?)`;', text)

if css_match:
    css = css_match.group(1)
    print("Found header CSS length:", len(css))
    # Search for button rules
    for line in css.split('\n'):
        if any(cls in line for cls in ['.nav-brand', '.nav-chapters-btn', '.nav-dropdown-tab', '.nav-search-trigger', '.nav-progress-pill', '.nav-auth-pill', '.nav-theme-btn']):
            if '{' in line:
                print(line.strip())

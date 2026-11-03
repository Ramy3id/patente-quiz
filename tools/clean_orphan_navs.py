import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DIR = 'R:/Ramy/PATENTE_PRO_APP/interactive_pages'

for fname in os.listdir(DIR):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(DIR, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check for orphan nav-desktop-actions / orphan nav tags
    pattern = re.compile(r'\s*<div class="nav-desktop-actions">[\s\S]*?</div>\s*</nav>', re.IGNORECASE)
    if pattern.search(content):
        new_content = pattern.sub('', content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"CLEANED orphan nav block in: {fname}")
        
    # Also check single orphan </nav>
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content2 = f.read()
    if '</nav>' in content2 and '<nav' not in content2:
        content2 = content2.replace('</nav>', '')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content2)
        print(f"CLEANED single orphan </nav> in: {fname}")

print("DONE CLEANING ORPHAN NAV TAGS")

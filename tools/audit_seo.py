import os, sys, glob, re

sys.stdout.reconfigure(encoding='utf-8')

repo_dir = r'R:\Ramy\PATENTE_PRO_APP'

print("=== Checking SEO files in root ===")
for fname in ['sitemap.xml', 'robots.txt', 'manifest.json', 'opensearch.xml']:
    p = os.path.join(repo_dir, fname)
    exists = os.path.exists(p)
    print(f"{fname}: {'EXISTS (' + str(os.path.getsize(p)) + ' bytes)' if exists else 'MISSING'}")

# Inspect meta tags across main pages
pages_to_check = [
    os.path.join(repo_dir, 'index.html'),
    os.path.join(repo_dir, 'Capitoli_Divisi', 'index.html'),
    os.path.join(repo_dir, 'interactive_pages', 'scheda-esame.html'),
    os.path.join(repo_dir, 'interactive_pages', 'piano-studio.html'),
    os.path.join(repo_dir, 'Capitoli_Divisi', 'parole-quiz.html')
]

for p in pages_to_check:
    if not os.path.exists(p):
        continue
    rel = os.path.relpath(p, repo_dir)
    print(f"\n==================== {rel} ====================")
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        head = f.read(4000)
    
    title_m = re.search(r'<title>(.*?)</title>', head, re.I | re.S)
    desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', head, re.I)
    canon_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', head, re.I)
    og_title_m = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', head, re.I)
    og_img_m = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', head, re.I)
    jsonld_m = re.search(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', head, re.I | re.S)
    
    print("Title:", title_m.group(1).strip() if title_m else "MISSING")
    print("Description:", desc_m.group(1).strip()[:100] + "..." if desc_m else "MISSING")
    print("Canonical:", canon_m.group(1).strip() if canon_m else "MISSING")
    print("OG:Title:", og_title_m.group(1).strip() if og_title_m else "MISSING")
    print("OG:Image:", og_img_m.group(1).strip() if og_img_m else "MISSING")
    print("Schema.org JSON-LD:", "EXISTS" if jsonld_m else "MISSING")

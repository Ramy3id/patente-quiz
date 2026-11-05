import sys

sys.stdout.reconfigure(encoding='utf-8')

repo_dir = r'R:\Ramy\PATENTE_PRO_APP'

print("=== robots.txt ===")
with open(repo_dir + r'\robots.txt', 'r', encoding='utf-8') as f:
    print(f.read())

print("\n=== sitemap.xml (sample first 1000 chars) ===")
with open(repo_dir + r'\sitemap.xml', 'r', encoding='utf-8') as f:
    print(f.read()[:1000])

print("\n=== manifest.json ===")
with open(repo_dir + r'\manifest.json', 'r', encoding='utf-8') as f:
    print(f.read())

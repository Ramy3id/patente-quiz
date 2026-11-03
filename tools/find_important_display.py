import sys, glob, re
sys.stdout.reconfigure(encoding='utf-8')

for f in glob.glob(r'R:\Ramy\PATENTE_PRO_APP\**\*.*', recursive=True):
    if f.endswith(('.css', '.html')):
        with open(f, 'r', encoding='utf-8') as fp:
            c = fp.read()
            for m in re.finditer(r'[^\n;{}]*chapter-card[^\n;{}]*\{[^}]*display\s*:[^};]+!important', c, re.IGNORECASE):
                print(f"File {f}:")
                print("  ", m.group(0))

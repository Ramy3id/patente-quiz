import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi"
chapters = sorted([d for d in os.listdir(base_dir) if d.startswith("Capitolo_") and os.path.isdir(os.path.join(base_dir, d))])

for chap in chapters:
    html_path = os.path.join(base_dir, chap, "index.html")
    if not os.path.exists(html_path):
        print(f"MISSING {chap}")
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    uses_engine = 'modular-chapter-engine.js' in html
    calls_init = 'ModularChapterEngine.init' in html or 'initModularChapter' in html
    if not uses_engine or not calls_init:
        print(f"{chap}: uses_engine={uses_engine}, calls_init={calls_init}")

print("Check finished.")

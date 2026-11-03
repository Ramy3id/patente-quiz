import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi"
chapters = sorted([d for d in os.listdir(base_dir) if d.startswith("Capitolo_") and os.path.isdir(os.path.join(base_dir, d))])

for chap in chapters:
    json_path = os.path.join(base_dir, chap, "domande.json")
    print(f"{chap}: has domande.json: {os.path.exists(json_path)}")

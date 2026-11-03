import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi"
chapters = sorted([d for d in os.listdir(base_dir) if d.startswith("Capitolo_") and os.path.isdir(os.path.join(base_dir, d))])

for chap in chapters:
    html_path = os.path.join(base_dir, chap, "index.html")
    if not os.path.exists(html_path):
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    m_groups = re.search(r'const\s+UNIFIED_GROUPS\s*=\s*(\{[\s\S]*?\n\s*\});', html)
    if m_groups:
        groups_str = m_groups.group(1)
        entries = re.findall(r'"([^"]+)":\s*\{\s*"num":\s*(\d+)', groups_str)
        nums = [int(num) for k, num in entries]
        if nums != sorted(nums):
            print(f"UNIFIED_GROUPS NOT SORTED in {chap}: {nums}")
        else:
            # check if 1..N continuous
            expected = list(range(1, len(nums) + 1))
            if nums != expected:
                print(f"UNIFIED_GROUPS NOT 1..N in {chap}: {nums}")
            else:
                pass
print("Done checking UNIFIED_GROUPS.")

import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi"
chapters = sorted([d for d in os.listdir(base_dir) if d.startswith("Capitolo_") and os.path.isdir(os.path.join(base_dir, d))])

print(f"Found {len(chapters)} chapter directories.\n")

issues_found = []

for chap in chapters:
    html_path = os.path.join(base_dir, chap, "index.html")
    if not os.path.exists(html_path):
        continue
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find UNIFIED_GROUPS
    m_groups = re.search(r'const\s+UNIFIED_GROUPS\s*=\s*(\{[\s\S]*?\n\s*\});', html)
    if not m_groups:
        print(f"[{chap}] UNIFIED_GROUPS NOT FOUND")
        continue

    groups_str = m_groups.group(1)
    entries = re.findall(r'"([^"]+)":\s*\{\s*"num":\s*(\d+)', groups_str)
    group_num_map = {k: int(num) for k, num in entries}
    groups_order = [int(num) for k, num in entries]
    
    # Check if UNIFIED_GROUPS keys are sorted by num
    expected_order = sorted(groups_order)
    groups_order_ok = (groups_order == expected_order)

    # Find SUBTOPIC_MAP
    m_map = re.search(r'const\s+SUBTOPIC_MAP\s*=\s*(\{[\s\S]*?\n\s*\});', html)
    subtopic_map = {}
    if m_map:
        map_pairs = re.findall(r'"([^"]+)":\s*"([^"]+)"', m_map.group(1))
        subtopic_map = dict(map_pairs)

    # Find DATA
    m_data = re.search(r'const\s+DATA\s*=\s*(\{[\s\S]*?\n\s*\});', html)
    if not m_data:
        print(f"[{chap}] DATA NOT FOUND")
        continue

    data_str = m_data.group(1)
    sottos = re.findall(r'"sotto_argomento":\s*"([^"]+)"', data_str)
    
    seen_groups = []
    for s in sottos:
        g = subtopic_map.get(s, s)
        if g not in seen_groups:
            seen_groups.append(g)

    domande_num_order = [group_num_map.get(g, -1) for g in seen_groups]
    expected_domande_order = sorted(domande_num_order)
    domande_order_ok = (domande_num_order == expected_domande_order)

    status = "OK"
    reasons = []
    if not groups_order_ok:
        reasons.append(f"UNIFIED_GROUPS keys out of order: {groups_order}")
    if not domande_order_ok:
        reasons.append(f"DATA.domande subtopics out of order: {domande_num_order}")

    if reasons:
        print(f"❌ {chap}:")
        for r in reasons:
            print(f"   -> {r}")
        issues_found.append((chap, reasons))
    else:
        print(f"✅ {chap}: {len(entries)} groups in order (1..{max(groups_order) if groups_order else 0})")

print(f"\nTotal chapters with issues: {len(issues_found)}")

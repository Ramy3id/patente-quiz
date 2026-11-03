import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

def analyze_chapter(chap_dir):
    print("=" * 60)
    print("Analyzing:", chap_dir)
    html_path = f"R:\\Ramy\\PATENTE_PRO_APP\\Capitoli_Divisi\\{chap_dir}\\index.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find UNIFIED_GROUPS
    m_groups = re.search(r'const\s+UNIFIED_GROUPS\s*=\s*(\{[\s\S]*?\n\s*\});', html)
    if not m_groups:
        print("UNIFIED_GROUPS not found!")
        return

    groups_str = m_groups.group(1)
    entries = re.findall(r'"([^"]+)":\s*\{\s*"num":\s*(\d+)', groups_str)
    group_num_map = {k: int(num) for k, num in entries}

    # Find SUBTOPIC_MAP
    m_map = re.search(r'const\s+SUBTOPIC_MAP\s*=\s*(\{[\s\S]*?\n\s*\});', html)
    subtopic_map = {}
    if m_map:
        map_pairs = re.findall(r'"([^"]+)":\s*"([^"]+)"', m_map.group(1))
        subtopic_map = dict(map_pairs)

    # Find DATA
    m_data = re.search(r'const\s+DATA\s*=\s*(\{[\s\S]*?\n\s*\});', html)
    if not m_data:
        print("DATA not found!")
        return

    # In DATA, find each sotto_argomento in order
    data_str = m_data.group(1)
    sottos = re.findall(r'"sotto_argomento":\s*"([^"]+)"', data_str)
    
    seen_groups = []
    for s in sottos:
        g = subtopic_map.get(s, s)
        if g not in seen_groups:
            seen_groups.append(g)

    print("\nOrder of first appearance of subtopic groups in DATA.domande:")
    for idx, g in enumerate(seen_groups):
        num = group_num_map.get(g, '?')
        print(f"  Pos {idx+1:2d} -> num: {num:2} | groupKey: {g}")

analyze_chapter("Capitolo_01_definizioni_generali_doveri_strada")
analyze_chapter("Capitolo_02_segnali_pericolo")

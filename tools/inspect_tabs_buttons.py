with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
filters = re.findall(r'<div class=["\']ps-filters-row["\'][^>]*>(.*?)</div>', text, re.DOTALL)
with open(r'R:\Ramy\PATENTE_PRO_APP\tools\tabs_buttons_list.txt', 'w', encoding='utf-8') as out:
    for i, flt in enumerate(filters):
        btns = re.findall(r'<button[^>]*id=["\']([^"\']+)["\'][^>]*>(.*?)</button>', flt, re.DOTALL)
        out.write(f'=== Tab {i+1} Filter Buttons ({len(btns)}) ===\n')
        for b_id, b_text in btns:
            clean = re.sub(r'<[^>]+>', '', b_text).strip()
            out.write(f'  [{b_id}]: {clean}\n')

print('Saved to tools/tabs_buttons_list.txt')

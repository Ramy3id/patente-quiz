with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<button class=["\']dash-tab-btn[^>]*>(.*?)</button>', text, re.DOTALL)
with open(r'R:\Ramy\PATENTE_PRO_APP\tools\dash_tabs_info.txt', 'w', encoding='utf-8') as out:
    out.write(f'Total dash tabs: {len(matches)}\n')
    for i, m in enumerate(matches):
        clean = re.sub(r'<[^>]+>', ' ', m).strip()
        out.write(f'Tab {i+1}: {clean}\n')

    out.write('\n--- CSS for dash-tabs-bar ---\n')
    for m in re.finditer(r'\.dash-tabs-bar\s*\{[^}]*\}', text):
        out.write(m.group(0) + '\n')

    out.write('\n--- CSS for dash-tab-btn ---\n')
    for m in re.finditer(r'\.dash-tab-btn\s*\{[^}]*\}', text):
        out.write(m.group(0) + '\n')

print('Saved to tools/dash_tabs_info.txt')

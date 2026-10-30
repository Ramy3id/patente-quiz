# -*- coding: utf-8 -*-
with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = "updateMarathonDashboardUI();\n    });"
replacement = """updateMarathonDashboardUI();
      if (typeof initSignCounts === 'function') initSignCounts();
      if (typeof initTheoryCounts === 'function') initTheoryCounts();
    });"""

if target in text:
    text = text.replace(target, replacement, 1)
    with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully patched DOMContentLoaded!")
else:
    print("Target not found, checking with CRLF...")
    target_crlf = "updateMarathonDashboardUI();\r\n    });"
    if target_crlf in text:
        text = text.replace(target_crlf, replacement.replace("\n", "\r\n"), 1)
        with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Successfully patched DOMContentLoaded with CRLF!")
    else:
        print("Could not find target.")

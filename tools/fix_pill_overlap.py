with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 1. Update .exam-control-hub margin-bottom
content = re.sub(
    r'\.exam-control-hub\s*\{[^}]*\}',
    '''.exam-control-hub {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 6px 10px;
      margin-bottom: 10px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
    }''',
    content,
    count=1
)

# 2. Update .exam-nav-pills-row and .q-pill
content = re.sub(
    r'\.exam-nav-pills-row\s*\{[^}]*\}',
    '''.exam-nav-pills-row {
      margin-bottom: 10px;
      padding: 2px 0;
    }''',
    content,
    count=1
)

# 3. Update .q-pill.active transform-origin so it never expands upwards into the hub
content = content.replace(
    'transform: scale(1.14) !important;',
    'transform: scale(1.08) !important; transform-origin: center center !important;'
)

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated spacing and transform-origin successfully!")

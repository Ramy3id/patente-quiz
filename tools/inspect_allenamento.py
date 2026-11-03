import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("File size:", len(content))

# Look for the home button
for line in content.splitlines():
    if 'الرئيسية' in line and 'href' in line:
        print("HOME BTN:", line)

# Look for the 3 toggle buttons
for line in content.splitlines():
    if any(k in line for k in ['تظليل المعاني', 'تظليل الفخاخ', 'مفكك ال 3 كتل', 'مفكك الـ 3 كتل']):
        print("TOGGLE BTN:", line)

# Look for VERO / FALSO buttons
for line in content.splitlines():
    if 'VERO' in line or 'FALSO' in line:
        print("VF BTN:", line)

# Look for السابق / التالي
for line in content.splitlines():
    if any(k in line for k in ['السابق', 'التالي', 'nextQuestion', 'prevQuestion']):
        print("NAV BTN:", line)

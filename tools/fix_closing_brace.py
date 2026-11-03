import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'

with open(target_file, 'r', encoding='utf-8') as f:
    c = f.read()

target = """    html.light .cq-dd-menu::-webkit-scrollbar-thumb {
      background: #CBD5E1;

    html.light .cq-dd-menu {"""

replacement = """    html.light .cq-dd-menu::-webkit-scrollbar-thumb {
      background: #CBD5E1;
    }

    html.light .cq-dd-menu {"""

c_norm = c.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')
replacement_norm = replacement.replace('\r\n', '\n')

if target_norm in c_norm:
    c_norm = c_norm.replace(target_norm, replacement_norm, 1)
    if '\r\n' in c:
        final_c = c_norm.replace('\n', '\r\n')
    else:
        final_c = c_norm
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(final_c)
    print("Fixed closing brace successfully!")
else:
    print("Target not found!")
    sys.exit(1)

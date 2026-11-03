with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    html = f.read()

s_start = html.find('<style>')
s_end = html.find('</style>')
css = html[s_start+7:s_end]

lines = css.split('\n')
stack = []
for i, line in enumerate(lines):
    for ch in line:
        if ch == '{':
            stack.append((i+1, line.strip()))
        elif ch == '}':
            if not stack:
                print(f"EXTRA CLOSING BRACE at line {i+1}: {line.strip()}")
            else:
                stack.pop()

print("Remaining open braces:", len(stack))
for l_num, text in stack:
    print(f"Unclosed open brace from line {l_num}: {text[:50]}")

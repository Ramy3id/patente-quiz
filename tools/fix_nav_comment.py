import glob

all_htmls = glob.glob(r'R:\Ramy\PATENTE_PRO_APP\**\*.html', recursive=True)
all_htmls = [h for h in all_htmls if 'node_modules' not in h and '.git' not in h]

fixed_count = 0
for h in all_htmls:
    try:
        with open(h, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        # Check for malformed comment
        if '<!-- Unified Nav will be injected here automatically by unified-nav.js' in content:
            # Let's find lines containing this
            lines = content.splitlines(keepends=True)
            new_lines = []
            for line in lines:
                if '<!-- Unified Nav will be injected here automatically by unified-nav.js' in line and 'unified-header' in line:
                    new_lines.append('<div id="unified-header"></div>\n')
                    modified = True
                else:
                    new_lines.append(line)
            if modified:
                with open(h, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                fixed_count += 1
                print(f"Fixed unclosed nav comment in: {h}")
    except Exception as e:
        print(f"Error checking {h}: {e}")

print(f"Total files fixed: {fixed_count}")

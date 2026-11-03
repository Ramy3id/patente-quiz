import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

root = r'R:\Ramy\PATENTE_PRO_APP'

keywords = ['3 كتل', 'ثلاث كتل', 'كتل', 'كتلة', 'بلوكات', '3 بلوكات', '3 كتل']

for dirpath, dirnames, filenames in os.walk(root):
    if '.git' in dirpath:
        continue
    for f in filenames:
        if f.endswith(('.html', '.js', '.json', '.md')):
            p = os.path.join(dirpath, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    for kw in keywords:
                        if kw in content:
                            print(f"Match '{kw}' in: {os.path.relpath(p, root)}")
                            # print context
                            for m in re.finditer(re.escape(kw), content):
                                st = max(0, m.start() - 60)
                                en = min(len(content), m.end() + 60)
                                print(f"   Context: {content[st:en].replace(chr(10), ' ')}")
                            break
            except Exception:
                pass

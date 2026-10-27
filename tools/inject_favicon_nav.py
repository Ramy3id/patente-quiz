# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

nav_file = 'R:/Ramy/PATENTE/assets/js/unified-nav.js'
with open(nav_file, 'r', encoding='utf-8') as f:
    text = f.read()

old_block = '    injectStyles();\n    const ctx = getPathContext();'
inject_code = '''    injectStyles();
    const ctx = getPathContext();

    // التأكد من وجود أيقونة التبويب (Favicon) تلقائياً في كامل صفحات المنصة
    if (!document.querySelector('link[rel*="icon"]')) {
      const fav = document.createElement('link');
      fav.rel = 'icon';
      fav.type = 'image/x-icon';
      fav.href = ctx.root + 'favicon.ico';
      document.head.appendChild(fav);
    }'''

if old_block in text and 'link[rel*="icon"]' not in text:
    text = text.replace(old_block, inject_code, 1)
    with open(nav_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Favicon auto-injector added to unified-nav.js successfully!')
else:
    print('Already injected or block not found.')

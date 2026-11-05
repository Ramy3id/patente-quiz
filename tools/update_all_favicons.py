import glob
import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

repo = r'R:\Ramy\PATENTE_PRO_APP'

# 1. Update unified-nav.js to dynamically enforce the new favicon
nav_path = os.path.join(repo, 'assets', 'js', 'unified-nav.js')
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

ensure_fn = '''
    // Ensure official browser tab favicon & apple touch icon are active
    try {
      let fav = document.querySelector('link[rel="icon"], link[rel="shortcut icon"]');
      if (!fav) {
        fav = document.createElement('link');
        fav.rel = 'icon';
        document.head.appendChild(fav);
      }
      fav.type = 'image/png';
      fav.href = ctx.root + 'assets/icons/favicon-32x32.png';

      let apple = document.querySelector('link[rel="apple-touch-icon"]');
      if (!apple) {
        apple = document.createElement('link');
        apple.rel = 'apple-touch-icon';
        document.head.appendChild(apple);
      }
      apple.href = ctx.root + 'assets/icons/apple-touch-icon.png';
    } catch(e) {}
'''

# Find init function in unified-nav.js
if 'ensureOfficialFavicon' not in nav:
    # insert before window.initUnifiedPortalNav
    idx_init = nav.find('window.initUnifiedPortalNav = function')
    if idx_init != -1:
        # insert right after context is resolved inside initUnifiedPortalNav
        idx_ctx = nav.find('const ctx = getPortalContext();', idx_init)
        if idx_ctx != -1:
            insert_pos = idx_ctx + len('const ctx = getPortalContext();')
            nav = nav[:insert_pos] + '\n' + ensure_fn + nav[insert_pos:]
            print("Injected dynamic favicon enforcement into unified-nav.js.")
            with open(nav_path, 'w', encoding='utf-8') as f:
                f.write(nav)

# 2. Update all static HTML files
html_files = glob.glob(os.path.join(repo, '**', '*.html'), recursive=True)
updated_count = 0

for hpath in html_files:
    # Compute relative path to root
    rel_dir = os.path.relpath(repo, os.path.dirname(hpath)).replace('\\', '/')
    prefix = '' if rel_dir == '.' else rel_dir + '/'
    
    with open(hpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    new_fav_block = f'''  <!-- Official Patente B Pro Favicons & App Icons -->
  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/icons/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="{prefix}assets/icons/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{prefix}assets/icons/apple-touch-icon.png">
  <link rel="shortcut icon" href="{prefix}favicon.ico">'''

    # Remove old favicon / apple-touch-icon links
    old_content = content
    content = re.sub(r'\s*<link[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*>', '', content, flags=re.I)
    content = re.sub(r'\s*<link[^>]*rel=["\']apple-touch-icon["\'][^>]*>', '', content, flags=re.I)
    
    # Insert new_fav_block right after <head> or after charset/viewport
    if '<head>' in content:
        content = content.replace('<head>', f'<head>\n{new_fav_block}', 1)
    elif '<head ' in content:
        content = re.sub(r'(<head[^>]*>)', f'\\1\n{new_fav_block}', content, count=1)
    
    if content != old_content:
        with open(hpath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1

print(f"Updated favicon tags in {updated_count} HTML files!")

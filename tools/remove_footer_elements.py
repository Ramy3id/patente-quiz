import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove footer-dev-avatar-wrapper
avatar_html = '''              <div class="footer-dev-avatar-wrapper">
                <div class="footer-dev-avatar">👨‍💻</div>
                <span class="footer-dev-status" title="Active Engineer"></span>
              </div>'''

if avatar_html in content:
    content = content.replace(avatar_html, '', 1)
    print("Removed footer-dev-avatar-wrapper successfully.")
else:
    print("WARNING: avatar_html not found exactly, searching with pattern...")
    import re
    content = re.sub(r'<div class="footer-dev-avatar-wrapper">[\s\S]*?</div>\s*</div>', '', content, count=1)
    print("Removed with regex.")

# 2. Remove footer-cache-reset-btn
cache_btn_pattern = r'<button class="footer-cache-reset-btn"[\s\S]*?</button>'
if 'footer-cache-reset-btn' in content:
    import re
    content = re.sub(cache_btn_pattern, '', content, count=1)
    print("Removed footer-cache-reset-btn successfully.")
else:
    print("footer-cache-reset-btn already absent or not found.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated unified-nav.js successfully.")

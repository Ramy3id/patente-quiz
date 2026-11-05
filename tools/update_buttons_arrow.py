import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Current button pattern:
# <a href="..." class="btn-action-study" onclick="soundEngine.click()">
#   <span><svg class="ui-svg" viewBox="0 0 24 24" style="width:13px;height:13px;stroke-width:2.5;margin-left:4px;"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>بدء المذاكرة التفاعلية</span>
# </a>

# Target button pattern:
# Text on the right, arrow on the left pointing left (←)
# In RTL: <span>بدء المذاكرة التفاعلية</span> followed by the arrow SVG!

old_btn_pattern = re.compile(
    r'<a href="([^"]+)" class="btn-action-study" onclick="soundEngine\.click\(\)">\s*'
    r'<span><svg class="ui-svg"[^>]*><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>بدء المذاكرة التفاعلية</span>\s*'
    r'</a>'
)

new_btn_template = (
    r'<a href="\1" class="btn-action-study" onclick="soundEngine.click()">'
    r'<span>بدء المذاكرة التفاعلية</span>'
    r'<svg class="ui-svg btn-arrow-svg" viewBox="0 0 24 24" style="width:15px;height:15px;stroke-width:2.5;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;margin-right:6px;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>'
    r'</a>'
)

new_html, count = old_btn_pattern.subn(new_btn_template, html)
print(f"Replaced {count} buttons in Capitoli_Divisi/index.html")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

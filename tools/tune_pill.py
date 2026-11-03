import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\trucchi-esame.html'

with open(target_file, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace .tr-badge-pill CSS
old_pill_css = """    .tr-badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(168, 85, 247, 0.15);
      color: #C084FC;
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 800;
      margin-bottom: 12px;
      border: 1px solid rgba(168, 85, 247, 0.3);
      max-width: 95%;
      box-sizing: border-box;
      line-height: 1.3;
    }"""

new_pill_css = """    .tr-badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(168, 85, 247, 0.15);
      color: #C084FC;
      padding: 4px 12px;
      border-radius: 999px;
      font-size: clamp(0.7rem, 2.8vw, 0.82rem);
      font-weight: 800;
      margin-bottom: 12px;
      border: 1px solid rgba(168, 85, 247, 0.3);
      max-width: 100%;
      white-space: nowrap;
      box-sizing: border-box;
      line-height: 1.3;
    }"""

if old_pill_css in c:
    c = c.replace(old_pill_css, new_pill_css)
elif old_pill_css.replace('\n', '\r\n') in c:
    c = c.replace(old_pill_css.replace('\n', '\r\n'), new_pill_css.replace('\n', '\r\n'))
else:
    print("Could not find old_pill_css directly, using normalized")
    c_norm = c.replace('\r\n', '\n')
    c_norm = c_norm.replace(old_pill_css, new_pill_css)
    if '\r\n' in c:
        c = c_norm.replace('\n', '\r\n')
    else:
        c = c_norm

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated tr-badge-pill CSS!")

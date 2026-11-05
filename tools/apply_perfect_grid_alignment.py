import glob
import re
import os

root = r'R:\Ramy\PATENTE_PRO_APP'

# 1. Update theme-modes.css
theme_path = os.path.join(root, 'assets', 'css', 'theme-modes.css')
with open(theme_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace or append the master grid rule
universal_rule = '''
/* ==========================================================================
   PLATFORM UNIVERSAL CONTAINER GRID (1200px STANDARD)
   Unifies all page containers across chapters, portal, interactive pages,
   thesaurus, and exam simulator to the exact standard grid width.
   ========================================================================== */
.container,
main.container,
div.container,
.ch-portal-container,
.sp-container,
.inc-container,
.exam-portal-container,
.dict-container,
.interactive-container,
.quiz-container,
.content-wrapper,
.study-plan-container,
.lab-container,
.zero-mistake-container,
.dash-wrapper,
.tr-container,
.ps-container,
.cq-container,
.zm-container,
.privacy-container {
  max-width: 1200px !important;
  width: 100% !important;
  padding-left: 18px !important;
  padding-right: 18px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  box-sizing: border-box !important;
}

/* Master Universal Banner Alignment (1164px Centered Grid) */
.guest-free-sample-banner,
#guestIncrociBanner,
#guestParoleBanner,
#guestTrucchiBanner,
#guestPianoBanner,
[class*="sample-banner"] {
  max-width: 1164px !important;
  width: calc(100% - 36px) !important;
  margin: 16px auto !important;
  box-sizing: border-box !important;
}

#guestDashboardNotice {
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 auto 18px !important;
  box-sizing: border-box !important;
}

@media (max-width: 1240px) {
  .container,
  main.container,
  div.container,
  .ch-portal-container,
  .sp-container,
  .inc-container,
  .exam-portal-container,
  .dict-container,
  .interactive-container,
  .quiz-container,
  .content-wrapper,
  .study-plan-container,
  .lab-container,
  .zero-mistake-container,
  .dash-wrapper,
  .tr-container,
  .ps-container,
  .cq-container,
  .zm-container,
  .privacy-container {
    max-width: 100% !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
  }
  .guest-free-sample-banner,
  #guestIncrociBanner,
  #guestParoleBanner,
  #guestTrucchiBanner,
  #guestPianoBanner,
  [class*="sample-banner"] {
    max-width: calc(100% - 32px) !important;
    width: calc(100% - 32px) !important;
    margin: 14px 16px !important;
  }
}
'''

# Remove old block if present
pattern = r'/\* =+ *\r?\n *PLATFORM UNIVERSAL CONTAINER GRID[\s\S]+?@media \(max-width: 1240px\) \{[\s\S]+?\}\s*\}'
if re.search(pattern, css):
    css = re.sub(pattern, universal_rule.strip(), css)
    print("Replaced existing PLATFORM UNIVERSAL CONTAINER GRID block")
else:
    css += '\n' + universal_rule
    print("Appended PLATFORM UNIVERSAL CONTAINER GRID block")

with open(theme_path, 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update all individual HTML files directly
updates = [
    # Dashboard
    (os.path.join(root, 'interactive_pages', 'dashboard.html'), [
        (r'max-width:\s*1100px;', 'max-width: 1200px;'),
        (r'padding:\s*0\s+16px;', 'padding: 0 18px;')
    ]),
    # Trucchi
    (os.path.join(root, 'interactive_pages', 'trucchi-esame.html'), [
        (r'max-width:\s*1100px;', 'max-width: 1200px;'),
        (r'padding:\s*16px\s+16px\s+40px;', 'padding: 16px 18px 40px;')
    ]),
    # Parole Spia
    (os.path.join(root, 'interactive_pages', 'parole-spia.html'), [
        (r'max-width:\s*1100px;', 'max-width: 1200px;'),
        (r'padding:\s*16px\s+16px\s+40px;', 'padding: 16px 18px 40px;')
    ]),
    # Allenamento
    (os.path.join(root, 'interactive_pages', 'allenamento-capitolo.html'), [
        (r'max-width:\s*900px;', 'max-width: 1200px;')
    ]),
    # Zero Mistake
    (os.path.join(root, 'interactive_pages', 'zero-mistake.html'), [
        (r'max-width:\s*820px;', 'max-width: 1200px;')
    ]),
    # Laboratorio
    (os.path.join(root, 'interactive_pages', 'laboratorio-numeri.html'), [
        (r'max-width:\s*1100px;', 'max-width: 1200px;')
    ]),
    # Privacy
    (os.path.join(root, 'interactive_pages', 'privacy.html'), [
        (r'max-width:\s*900px;', 'max-width: 1200px;')
    ]),
    # Decodificatore
    (os.path.join(root, 'interactive_pages', 'decodificatore-incroci.html'), [
        (r'padding:\s*16px\s+16px\s+40px;', 'padding: 16px 18px 40px;')
    ]),
    # Piano Studio
    (os.path.join(root, 'interactive_pages', 'piano-studio.html'), [
        (r'padding:\s*0\s+16px;', 'padding: 0 18px;')
    ]),
    # Scheda Esame
    (os.path.join(root, 'interactive_pages', 'scheda-esame.html'), [
        (r'padding:\s*0\s+16px;', 'padding: 0 18px;')
    ])
]

for file_path, repls in updates:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            c = f.read()
        for pat, repl in repls:
            c = re.sub(pat, repl, c)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated {os.path.basename(file_path)}")

# Update all 25 chapters padding from 0 16px 50px to 0 18px 50px
chaps = glob.glob(os.path.join(root, 'Capitoli_Divisi', 'Capitolo_*', 'index.html'))
for cp in chaps:
    with open(cp, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'padding: 0 16px 50px;' in c:
        c = c.replace('padding: 0 16px 50px;', 'padding: 0 18px 50px;')
        with open(cp, 'w', encoding='utf-8') as f:
            f.write(c)
print(f"Updated padding in {len(chaps)} chapter files")

# 3. Bump cache version across all HTML files
old_ver = 'v=2026.11.05.V18_UNIFIED_1200_CONTAINER'
new_ver = 'v=2026.11.05.V19_PERFECT_GRID_ALIGNMENT'

all_htmls = glob.glob(os.path.join(root, '**', '*.html'), recursive=True)
all_htmls = [h for h in all_htmls if 'node_modules' not in h and '.git' not in h]

bumped = 0
for h in all_htmls:
    try:
        with open(h, 'r', encoding='utf-8') as f:
            c = f.read()
        if old_ver in c:
            c = c.replace(old_ver, new_ver)
            with open(h, 'w', encoding='utf-8') as f:
                f.write(c)
            bumped += 1
    except Exception as e:
        print(f"Error bumping {h}: {e}")

print(f"Bumped cache version to {new_ver} in {bumped} HTML files")

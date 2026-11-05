import os

root_dir = r'R:\Ramy\PATENTE_PRO_APP'

# Check a sample of files: root index.html, interactive_pages/piano-studio.html, Capitoli_Divisi/index.html, Capitoli_Divisi/Capitolo_01...
sample_files = [
    r'index.html',
    r'Capitoli_Divisi\index.html',
    r'Capitoli_Divisi\parole-quiz.html',
    r'interactive_pages\piano-studio.html',
    r'interactive_pages\scheda-esame.html',
    r'Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html'
]

for sf in sample_files:
    full_path = os.path.join(root_dir, sf)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        has_nav_tag = '<nav' in content
        has_globalPortalNav = 'globalPortalNav' in content
        has_unified_nav = 'unified-nav.js' in content
        has_theme_modes = 'theme-modes.css' in content
        print(f"=== {sf} ===")
        print(f"  <nav: {has_nav_tag}, #globalPortalNav: {has_globalPortalNav}, unified-nav.js: {has_unified_nav}, theme-modes.css: {has_theme_modes}")

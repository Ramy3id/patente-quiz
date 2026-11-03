import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make family pills compact so they wrap beautifully in 2 columns / flex wrap
old_shelf_css = """.families-shelf {
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 8px !important;
    overflow-x: visible !important;
    overflow-y: visible !important;
    overflow: visible !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 12px 0 24px 0 !important;
  }
  .family-pill {
    flex-shrink: 0 !important;
    height: 36px !important;
    min-height: 36px !important;
    padding: 0 14px !important;
    border-radius: 100px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
  }"""

new_shelf_css = """.families-shelf {
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 6px 8px !important;
    overflow-x: visible !important;
    overflow-y: visible !important;
    overflow: visible !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 10px 0 20px 0 !important;
  }
  .family-pill {
    flex: 0 1 auto !important;
    max-width: 100% !important;
    height: 34px !important;
    min-height: 34px !important;
    padding: 0 12px !important;
    border-radius: 100px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
  }"""

if old_shelf_css in content:
    content = content.replace(old_shelf_css, new_shelf_css)
    print("Replaced shelf css with compact flex wrap.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved.")

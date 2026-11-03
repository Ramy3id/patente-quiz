import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Refine preset group responsiveness for desktop sidebar vs mobile full width
old_preset_css = """  /* Block 2: Preset Packs - 2 balanced rows on Mobile, 3 cols on Desktop */
  .preset-btn-group {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
    margin-top: 8px !important;
  }
  .preset-btn-group button:last-child {
    grid-column: span 2 !important;
  }
  @media (min-width: 640px) {
    .preset-btn-group {
      grid-template-columns: repeat(3, 1fr) !important;
    }
    .preset-btn-group button:last-child {
      grid-column: span 1 !important;
    }
  }"""

new_preset_css = """  /* Block 2: Preset Packs - 2 balanced rows on Mobile, neat column in Desktop sidebar */
  .preset-btn-group {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
    margin-top: 8px !important;
  }
  .preset-btn-group button:last-child {
    grid-column: span 2 !important;
  }
  @media (min-width: 900px) {
    .preset-btn-group {
      display: flex !important;
      flex-direction: column !important;
      gap: 8px !important;
    }
    .preset-btn-group button:last-child {
      grid-column: auto !important;
    }
  }"""

if old_preset_css in content:
    content = content.replace(old_preset_css, new_preset_css)
    print("Replaced preset CSS successfully.")
else:
    print("old_preset_css not found directly, checking regex...")
    import re
    content = re.sub(r'/\* Block 2: Preset Packs - 2 balanced rows on Mobile[\s\S]*?\.preset-btn-group button:last-child \{\s*grid-column: span 1 !important;\s*\}', new_preset_css, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved.")

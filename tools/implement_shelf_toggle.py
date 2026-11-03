import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update familiesShelf HTML to include toggle button underneath
old_shelf_html = """  <!-- Semantic Families Shelf (المعجم وعائلات الكلمات) -->
  <div class="families-shelf" id="familiesShelf">
    <!-- Populated by JS -->
  </div>"""

new_shelf_html = """  <!-- Semantic Families Shelf (المعجم وعائلات الكلمات) -->
  <div class="families-shelf" id="familiesShelf">
    <!-- Populated by JS -->
  </div>
  <div class="shelf-toggle-wrapper">
    <button type="button" class="btn-toggle-shelf" id="btnToggleFamilies" onclick="toggleFamiliesShelf()">
      <span id="toggleFamiliesText">عرض باقي العائلات الدلالية (12+)</span>
      <span id="toggleFamiliesIcon" class="toggle-icon">▼</span>
    </button>
  </div>"""

if old_shelf_html in content:
    content = content.replace(old_shelf_html, new_shelf_html)
    print("Replaced familiesShelf HTML successfully.")
else:
    print("Warning: old_shelf_html not matched directly, checking regex...")
    pat = r'<div class="families-shelf" id="familiesShelf">\s*<!-- Populated by JS -->\s*</div>'
    content = re.sub(pat, new_shelf_html, content)

# 2. Update JS in initControls to mark extra pills (beyond first 6) and add toggleFamiliesShelf function
old_shelf_js = """  // Clean Arabic title by removing latin parenthesis from button face for crisp 2-col mobile grid
      const cleanTitle = item.categoria.replace(/\\s*\\([^)]*\\)/g, '').trim();
      return `
        <button class="family-pill" onclick="selectThesaurusFamily('${item.id}')" title="${item.categoria}">
          <span>${cleanTitle}</span>
        </button>
      `;"""

new_shelf_js = """  // Clean Arabic title & show initial 6 items; rest toggled via button
      const cleanTitle = item.categoria.replace(/\\s*\\([^)]*\\)/g, '').trim();
      const isExtra = idx >= 6;
      return `
        <button class="family-pill ${isExtra ? 'family-pill-extra' : ''}" onclick="selectThesaurusFamily('${item.id}')" title="${item.categoria}">
          <span>${cleanTitle}</span>
        </button>
      `;"""

# Also ensure map receives (item, idx)
old_map = "shelf.innerHTML = PATENTE_THESAURUS.map(item => {"
new_map = "shelf.innerHTML = PATENTE_THESAURUS.map((item, idx) => {"

if old_map in content:
    content = content.replace(old_map, new_map)
    print("Updated map parameter to (item, idx).")

if old_shelf_js in content:
    content = content.replace(old_shelf_js, new_shelf_js)
    print("Updated shelf JS mapping with isExtra flag.")
else:
    print("Warning: old_shelf_js not matched directly, using regex...")
    pat_js = r'const cleanTitle = item\.categoria\.replace[\s\S]*?<button class="family-pill"[\s\S]*?`\s*;\s*\}\)\.join'
    repl_js = """const cleanTitle = item.categoria.replace(/\\s*\\([^)]*\\)/g, '').trim();
      const isExtra = idx >= 6;
      return `
        <button class="family-pill ${isExtra ? 'family-pill-extra' : ''}" onclick="selectThesaurusFamily('${item.id}')" title="${item.categoria}">
          <span>${cleanTitle}</span>
        </button>
      `;
    }).join"""
    content = re.sub(pat_js, repl_js, content)

# 3. Add toggleFamiliesShelf function
toggle_func = """
/* ==========================================================================
   Toggle Families Shelf (Show/Hide Extra Categories)
   ========================================================================== */
let familiesShelfExpanded = false;
function toggleFamiliesShelf() {
  playSound('click');
  familiesShelfExpanded = !familiesShelfExpanded;
  const shelf = document.getElementById('familiesShelf');
  const txt = document.getElementById('toggleFamiliesText');
  const icon = document.getElementById('toggleFamiliesIcon');
  if (shelf) {
    shelf.classList.toggle('expanded', familiesShelfExpanded);
  }
  if (txt && icon) {
    if (familiesShelfExpanded) {
      txt.textContent = 'عرض أقل';
      icon.textContent = '▲';
    } else {
      txt.textContent = 'عرض باقي العائلات الدلالية (12+)';
      icon.textContent = '▼';
    }
  }
}
"""

if 'function toggleFamiliesShelf' not in content:
    idx_script = content.rfind('</script>')
    content = content[:idx_script] + toggle_func + '\n' + content[idx_script:]
    print("Inserted toggleFamiliesShelf function successfully.")

# 4. Add CSS for toggle button and extra pills visibility
toggle_css = """
  /* Toggleable Families Shelf Visibility */
  .family-pill-extra {
    display: none !important;
  }
  .families-shelf.expanded .family-pill-extra {
    display: inline-flex !important;
    animation: fadeIn 0.25s ease !important;
  }

  .shelf-toggle-wrapper {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin: 4px auto 20px !important;
    width: 100% !important;
  }
  .btn-toggle-shelf {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    height: 36px !important;
    min-height: 36px !important;
    padding: 0 18px !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 100px !important;
    color: #e4e4e7 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-family: inherit !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
  }
  .btn-toggle-shelf:hover {
    background: rgba(56, 189, 248, 0.14) !important;
    border-color: rgba(56, 189, 248, 0.35) !important;
    color: #38bdf8 !important;
    transform: translateY(-1px) !important;
  }
  .toggle-icon {
    font-size: 0.72rem !important;
    transition: transform 0.2s ease !important;
  }

  html.light .btn-toggle-shelf {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #334155 !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
  }
  html.light .btn-toggle-shelf:hover {
    background: #f0f9ff !important;
    border-color: #38bdf8 !important;
    color: #0284c7 !important;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.15) !important;
  }
"""

if '</style>' in content:
    content = content.replace('</style>', toggle_css + '\n</style>', 1)
    print("Injected toggle CSS successfully.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved all changes successfully.")

import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update JS to generate concise, balanced family titles
old_shelf_js = """  // Populate Semantic Families Shelf
  const shelf = document.getElementById('familiesShelf');
  if (typeof PATENTE_THESAURUS !== 'undefined') {
    shelf.innerHTML = PATENTE_THESAURUS.map(item => `
      <button class="family-pill" onclick="selectThesaurusFamily('${item.id}')">
        ${item.categoria}
      </button>
    `).join('');
  }"""

new_shelf_js = """  // Populate Semantic Families Shelf with balanced 2-column grid layout
  const shelf = document.getElementById('familiesShelf');
  if (typeof PATENTE_THESAURUS !== 'undefined') {
    shelf.innerHTML = PATENTE_THESAURUS.map(item => {
      // Create concise title by stripping long parenthesized text if needed, keeping icon + Arabic
      let shortCat = item.categoria;
      return `
        <button class="family-pill" onclick="selectThesaurusFamily('${item.id}')" title="${item.categoria}">
          <span>${shortCat}</span>
        </button>
      `;
    }).join('');
  }"""

if old_shelf_js in content:
    content = content.replace(old_shelf_js, new_shelf_js)
    print("Updated shelf JS successfully.")

# 2. Perfect 2-column responsive grid on Mobile (NO horizontal scroll, perfectly balanced)
shelf_grid_css = """
  /* ==========================================================================
     PERFECT 2-COLUMN RESPONSIVE GRID FOR FAMILIES (ZERO HORIZONTAL SCROLL)
     ========================================================================== */
  .families-shelf {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
    overflow: visible !important;
    overflow-x: visible !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 12px 0 20px 0 !important;
    box-sizing: border-box !important;
  }
  @media (min-width: 768px) {
    .families-shelf {
      grid-template-columns: repeat(3, 1fr) !important;
    }
  }
  @media (min-width: 1024px) {
    .families-shelf {
      grid-template-columns: repeat(4, 1fr) !important;
    }
  }

  .family-pill {
    width: 100% !important;
    height: 38px !important;
    min-height: 38px !important;
    padding: 0 8px !important;
    border-radius: 12px !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    transition: all 0.2s ease !important;
    box-sizing: border-box !important;
  }
  .family-pill span {
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
  }
"""

# Replace previous shelf CSS
if '.families-shelf {' in content:
    content = re.sub(r'/\* 2\. COMPLETELY ELIMINATE HORIZONTAL SCROLL FROM FAMILIES SHELF[\s\S]*?transition: all 0\.2s ease !important;\s*\}', shelf_grid_css, content)

# Also ensure no background behind the button bars in any rule
content = content.replace('background: rgba(15, 15, 18, 0.7);', 'background: transparent;')
content = content.replace('background: rgba(15, 15, 18, 0.75);', 'background: transparent;')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated parole-quiz.html successfully.")

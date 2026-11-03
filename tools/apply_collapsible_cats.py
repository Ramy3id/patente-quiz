import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\dizionario-sinonimi.html'

with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update JS initDictionary for category chips
old_deck_js = '''  // Categories deck
  const deck = document.getElementById('categoryChipsDeck');
  deck.innerHTML = `
    <button class="cat-chip-btn active" data-cat="all" onclick="selectCategory('all', this)">
      <span>🌟</span> <span>الكل (${PATENTE_THESAURUS.length} عائلة)</span>
    </button>
  ` + PATENTE_THESAURUS.map(t => `
    <button class="cat-chip-btn" data-cat="${t.id}" onclick="selectCategory('${t.id}', this)">${t.categoria}</button>
  `).join('');'''

new_deck_js = '''  // Categories deck (4 visible by default, remainder in collapsible container)
  const deck = document.getElementById('categoryChipsDeck');
  const top4 = PATENTE_THESAURUS.slice(0, 4);
  const remaining = PATENTE_THESAURUS.slice(4);

  deck.innerHTML = `
    <button class="cat-chip-btn active" data-cat="all" onclick="selectCategory('all', this)">
      <span>🌟</span> <span>الكل (${PATENTE_THESAURUS.length} عائلة)</span>
    </button>
    ${top4.map(t => `
      <button class="cat-chip-btn" data-cat="${t.id}" onclick="selectCategory('${t.id}', this)">${t.categoria}</button>
    `).join('')}
    <div id="extraCategoriesGrid" class="extra-categories-container">
      ${remaining.map(t => `
        <button class="cat-chip-btn" data-cat="${t.id}" onclick="selectCategory('${t.id}', this)">${t.categoria}</button>
      `).join('')}
    </div>
    <button type="button" class="cat-toggle-btn" id="btnToggleExtraCats" onclick="toggleExtraCategories()">
      <span id="extraCategoriesToggleText">عرض باقي التصنيفات (${remaining.length} تصنيفاً إضافياً) ▾</span>
    </button>
  `;'''

if old_deck_js in text:
    text = text.replace(old_deck_js, new_deck_js, 1)
    print("Replaced deck JS successfully")
else:
    print("WARNING: old_deck_js not found")

# 2. Add toggleExtraCategories function
toggle_func_js = '''
/* Collapsible Categories Controller */
let extraCategoriesExpanded = false;
function toggleExtraCategories() {
  extraCategoriesExpanded = !extraCategoriesExpanded;
  const extra = document.getElementById('extraCategoriesGrid');
  const txt = document.getElementById('extraCategoriesToggleText');
  if (extra) {
    extra.classList.toggle('is-expanded', extraCategoriesExpanded);
  }
  if (txt) {
    const remainingCount = (typeof PATENTE_THESAURUS !== 'undefined') ? (PATENTE_THESAURUS.length - 4) : 14;
    txt.textContent = extraCategoriesExpanded 
      ? 'إخفاء التصنيفات الإضافية ▴' 
      : `عرض باقي التصنيفات (${remainingCount} تصنيفاً إضافياً) ▾`;
  }
}
'''

if 'function toggleExtraCategories' not in text:
    idx_select = text.find('function selectCategory')
    if idx_select != -1:
        text = text[:idx_select] + toggle_func_js + '\n' + text[idx_select:]
        print("Inserted toggleExtraCategories function successfully")
    else:
        print("WARNING: selectCategory not found")

# 3. Add CSS for .extra-categories-container and .cat-toggle-btn
toggle_css = '''
    /* Collapsible Categories Grid & Toggle Button */
    .extra-categories-container {
      display: none !important;
    }
    .extra-categories-container.is-expanded {
      display: contents !important;
    }
    .cat-toggle-btn {
      grid-column: 1 / -1 !important;
      width: 100% !important;
      height: 42px !important;
      min-height: 42px !important;
      margin-top: 4px !important;
      border-radius: 12px !important;
      border: 1.5px dashed rgba(2, 132, 199, 0.4) !important;
      background: rgba(2, 132, 199, 0.05) !important;
      color: #0284C7 !important;
      font-size: 0.82rem !important;
      font-weight: 700 !important;
      font-family: inherit !important;
      cursor: pointer !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 6px !important;
      box-sizing: border-box !important;
      transition: all 0.2s ease !important;
    }
    html.light .cat-toggle-btn {
      border-color: rgba(2, 132, 199, 0.35) !important;
      background: #F0F9FF !important;
      color: #0284C7 !important;
    }
    html.light .cat-toggle-btn:hover {
      background: #E0F2FE !important;
      border-color: #0284C7 !important;
    }
    html.dark .cat-toggle-btn {
      border-color: rgba(56, 189, 248, 0.35) !important;
      background: rgba(56, 189, 248, 0.08) !important;
      color: #38BDF8 !important;
    }
    html.dark .cat-toggle-btn:hover {
      background: rgba(56, 189, 248, 0.15) !important;
      border-color: #38BDF8 !important;
    }
'''

style_idx = text.find('</style>')
if style_idx != -1:
    text = text[:style_idx] + toggle_css + '\n' + text[style_idx:]
    print("Appended toggle CSS successfully")

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated file successfully")

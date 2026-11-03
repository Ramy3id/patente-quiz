import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# --------------------------------------------------------------------------
# 1. Update Chips Header & Actions HTML (Center alignment, better labels & layout)
# --------------------------------------------------------------------------
old_header_pat = r'<div class="chips-header">[\s\S]*?</div>\s*</div>'
new_header_html = """<div class="chips-header">
      <div class="chips-title">
        <span>🏷️ الكلمات المحفوظة في بنكك:</span>
        <span class="chips-subtitle">(اضغط على أي كلمة للفلترة بها أو إزالتها)</span>
      </div>
      <div class="chips-actions">
        <button class="btn-subtle btn-subtle-primary" onclick="selectAllWords()" title="تحديد كافة الكلمات في البنك">
          <span class="btn-icon">✓</span>
          <span>تحديد الكل</span>
        </button>
        <button class="btn-subtle btn-subtle-neutral" onclick="clearWordSelection()" title="إلغاء تحديد كل الكلمات">
          <span class="btn-icon">✕</span>
          <span>إلغاء</span>
        </button>
        <button class="btn-subtle btn-subtle-danger" onclick="clearAllWords()" title="مسح كافة الكلمات من البنك">
          <span class="btn-icon">🗑️</span>
          <span>تفريغ</span>
        </button>
      </div>
    </div>"""

# Replace chips header
m_header = re.search(r'<div class="chips-header">[\s\S]*?</div>\s*</div>', content)
if m_header:
    content = content[:m_header.start()] + new_header_html + content[m_header.end():]
    print("Updated chips-header HTML successfully.")
else:
    print("WARNING: chips-header regex not matched.")

# --------------------------------------------------------------------------
# 2. Integrate Custom Dropdown for Chapters (so it NEVER overflows the screen)
# --------------------------------------------------------------------------
old_ch_select = """      <!-- Chapter Selector -->
      <div>
        <select id="chapterSelect" class="custom-select" onchange="onSearchChange()">
          <option value="0">📚 كل الأبواب الـ 25 (المنهج كاملاً)</option>
        </select>
      </div>"""

new_ch_dropdown = """      <!-- Chapter Selector (Custom Dropdown bounded within screen) -->
      <div class="pq-dd-container" id="pqChapterDropdown">
        <select id="chapterSelect" style="display:none;" onchange="onSearchChange()">
          <option value="0">📚 كل الأبواب الـ 25 (المنهج كاملاً)</option>
        </select>
        <button type="button" class="pq-dd-btn" id="pqDropdownBtn" onclick="toggleChapterDropdown(event)">
          <span class="pq-dd-label" id="pqDropdownLabel">📚 كل الأبواب الـ 25 (المنهج كاملاً)</span>
          <span class="pq-dd-arrow">▼</span>
        </button>
        <div class="pq-dd-menu" id="pqDropdownMenu">
          <div class="pq-dd-item selected" onclick="selectChapterOption(0, '📚 كل الأبواب الـ 25 (المنهج كاملاً)')">
            <span>📚 كل الأبواب الـ 25 (المنهج كاملاً)</span>
          </div>
          <!-- Other chapters populated dynamically by JS -->
        </div>
      </div>"""

if old_ch_select in content:
    content = content.replace(old_ch_select, new_ch_dropdown)
    print("Replaced chapterSelect with Custom Dropdown successfully.")
else:
    print("WARNING: old_ch_select exact match not found, checking regex...")
    pat_sel = r'<!-- Chapter Selector -->[\s\S]*?<div>\s*<select id="chapterSelect"[\s\S]*?</select>\s*</div>'
    m_sel = re.search(pat_sel, content)
    if m_sel:
        content = content[:m_sel.start()] + new_ch_dropdown + content[m_sel.end():]
        print("Replaced chapterSelect via regex.")

# --------------------------------------------------------------------------
# 3. Update initControls and JS for Custom Dropdown
# --------------------------------------------------------------------------
old_init_controls = """function initControls() {
  // Populate chapters
  const sel = document.getElementById('chapterSelect');
  if (typeof CHAPTERS_META !== 'undefined') {
    CHAPTERS_META.forEach(ch => {
      const opt = document.createElement('option');
      opt.value = ch.num;
      opt.textContent = `الباب ${ch.num}: ${ch.titolo_ar || ch.titolo_it} (${ch.count} سؤال)`;
      sel.appendChild(opt);
    });
  }"""

new_init_controls = """function initControls() {
  // Populate chapters
  const sel = document.getElementById('chapterSelect');
  const ddMenu = document.getElementById('pqDropdownMenu');
  if (typeof CHAPTERS_META !== 'undefined') {
    CHAPTERS_META.forEach(ch => {
      const opt = document.createElement('option');
      opt.value = ch.num;
      const text = `الباب ${ch.num}: ${ch.titolo_ar || ch.titolo_it} (${ch.count} سؤال)`;
      opt.textContent = text;
      sel.appendChild(opt);

      if (ddMenu) {
        const item = document.createElement('div');
        item.className = 'pq-dd-item';
        item.dataset.value = ch.num;
        item.innerHTML = `<span>الباب ${ch.num}: ${ch.titolo_ar || ch.titolo_it} <small style="opacity:0.75; font-family:'JetBrains Mono',monospace;">(${ch.count} سؤال)</small></span>`;
        item.onclick = function() {
          selectChapterOption(ch.num, text);
        };
        ddMenu.appendChild(item);
      }
    });
  }"""

if old_init_controls in content:
    content = content.replace(old_init_controls, new_init_controls)
    print("Updated initControls successfully.")
else:
    print("WARNING: old_init_controls not matched directly.")

# Add dropdown toggle and option selection helper functions
dropdown_helpers = """
/* ==========================================================================
   Custom Chapter Dropdown Helpers
   ========================================================================== */
function toggleChapterDropdown(e) {
  if (e) e.stopPropagation();
  const menu = document.getElementById('pqDropdownMenu');
  const btn = document.getElementById('pqDropdownBtn');
  if (!menu || !btn) return;
  const isOpen = menu.classList.contains('open');
  if (isOpen) {
    menu.classList.remove('open');
    btn.classList.remove('open');
  } else {
    menu.classList.add('open');
    btn.classList.add('open');
  }
}

function selectChapterOption(val, text) {
  const sel = document.getElementById('chapterSelect');
  const label = document.getElementById('pqDropdownLabel');
  const menu = document.getElementById('pqDropdownMenu');
  const btn = document.getElementById('pqDropdownBtn');

  if (sel) {
    sel.value = val;
  }
  if (label) {
    label.textContent = text;
  }
  if (menu) {
    menu.classList.remove('open');
    menu.querySelectorAll('.pq-dd-item').forEach(it => {
      const itemVal = it.dataset.value || 0;
      if (parseInt(itemVal, 10) === parseInt(val, 10)) {
        it.classList.add('selected');
      } else {
        it.classList.remove('selected');
      }
    });
  }
  if (btn) btn.classList.remove('open');
  playSound('click');
  onSearchChange();
}

// Close dropdown on outside click
document.addEventListener('click', (e) => {
  const container = document.getElementById('pqChapterDropdown');
  if (container && !container.contains(e.target)) {
    const menu = document.getElementById('pqDropdownMenu');
    const btn = document.getElementById('pqDropdownBtn');
    if (menu) menu.classList.remove('open');
    if (btn) btn.classList.remove('open');
  }
});
"""

# Insert dropdown helpers before </script>
if dropdown_helpers not in content and '</script>' in content:
    idx_script = content.rfind('</script>')
    content = content[:idx_script] + dropdown_helpers + '\n' + content[idx_script:]
    print("Inserted dropdown helper JS successfully.")

# --------------------------------------------------------------------------
# 4. Master CSS Injection: Centering, Colors, Thesaurus without ugly gray,
#    Families Shelf scrollbar removal, Segmented Control VERO/FALSO centering
# --------------------------------------------------------------------------
master_css = """
  /* ==========================================================================
     ADVANCED ENHANCEMENTS: CHIPS ACTIONS, SHELF, THESAURUS, DROPDOWN, SEGMENTED
     ========================================================================== */

  /* 1. Word Bank Actions Centering & Unified Platform Colors */
  .chips-header {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    gap: 8px !important;
    margin-bottom: 14px !important;
  }
  .chips-title {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    gap: 2px !important;
  }
  .chips-subtitle {
    font-size: 0.78rem !important;
    color: var(--text-muted) !important;
    opacity: 0.85 !important;
  }
  .chips-actions {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 8px !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 4px auto 0 !important;
    width: 100% !important;
  }
  .btn-subtle {
    height: 34px !important;
    min-height: 34px !important;
    padding: 0 14px !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    transition: all 0.2s ease !important;
    font-family: inherit !important;
    box-sizing: border-box !important;
  }
  .btn-subtle .btn-icon {
    font-size: 0.88rem !important;
    line-height: 1 !important;
  }

  /* Subtitle button variants */
  .btn-subtle-primary {
    background: rgba(14, 165, 233, 0.12) !important;
    border: 1px solid rgba(14, 165, 233, 0.3) !important;
    color: #38bdf8 !important;
  }
  .btn-subtle-primary:hover {
    background: rgba(14, 165, 233, 0.24) !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
  }

  .btn-subtle-neutral {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #e4e4e7 !important;
  }
  .btn-subtle-neutral:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
  }

  .btn-subtle-danger {
    background: rgba(244, 63, 94, 0.1) !important;
    border: 1px solid rgba(244, 63, 94, 0.25) !important;
    color: #fb7185 !important;
  }
  .btn-subtle-danger:hover {
    background: rgba(244, 63, 94, 0.22) !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
  }

  /* Light mode palette for word bank actions */
  html.light .btn-subtle-primary {
    background: #e0f2fe !important;
    border: 1px solid #bae6fd !important;
    color: #0284c7 !important;
  }
  html.light .btn-subtle-primary:hover {
    background: #0284c7 !important;
    color: #ffffff !important;
    border-color: #0284c7 !important;
  }
  html.light .btn-subtle-neutral {
    background: #f1f5f9 !important;
    border: 1px solid #cbd5e1 !important;
    color: #334155 !important;
  }
  html.light .btn-subtle-neutral:hover {
    background: #e2e8f0 !important;
    color: #0f172a !important;
  }
  html.light .btn-subtle-danger {
    background: #ffe4e6 !important;
    border: 1px solid #fecdd3 !important;
    color: #e11d48 !important;
  }
  html.light .btn-subtle-danger:hover {
    background: #e11d48 !important;
    color: #ffffff !important;
    border-color: #e11d48 !important;
  }

  /* 2. Semantic Families Shelf (No Scrollbar, Smooth Scroll & Polished Pills) */
  .families-shelf {
    display: flex !important;
    gap: 8px !important;
    overflow-x: auto !important;
    padding: 4px 2px 12px !important;
    margin-bottom: 20px !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .families-shelf::-webkit-scrollbar {
    display: none !important;
  }
  .family-pill {
    flex-shrink: 0 !important;
    height: 38px !important;
    min-height: 38px !important;
    padding: 0 16px !important;
    border-radius: 100px !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #e4e4e7 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    font-family: inherit !important;
  }
  .family-pill:hover {
    background: rgba(56, 189, 248, 0.12) !important;
    border-color: rgba(56, 189, 248, 0.35) !important;
    color: #38bdf8 !important;
  }
  .family-pill.active {
    background: linear-gradient(135deg, #0284c7, #2563eb) !important;
    border-color: #0284c7 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
  }
  html.light .family-pill {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    color: #334155 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
  }
  html.light .family-pill:hover {
    background: #f0f9ff !important;
    border-color: #38bdf8 !important;
    color: #0284c7 !important;
  }
  html.light .family-pill.active {
    background: linear-gradient(135deg, #0284c7, #2563eb) !important;
    border-color: #0284c7 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.28) !important;
  }

  /* 3. Thesaurus Cards: Elimination of Ugly Gray, Pure Clean Surfaces */
  .thesaurus-card {
    border-radius: 20px !important;
    padding: 22px !important;
    transition: all 0.25s ease !important;
  }
  html.light .thesaurus-card {
    background: #ffffff !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.08) !important;
  }
  html.light .thesaurus-title {
    color: #1e1b4b !important;
  }
  html.light .thesaurus-badge {
    background: #eef2ff !important;
    border: 1px solid #c7d2fe !important;
    color: #4f46e5 !important;
  }
  html.light .thesaurus-summary {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-right: 4px solid #6366f1 !important;
    color: #334155 !important;
  }

  /* Thesaurus Subcards (Synonyms & Traps) */
  html.light .thesaurus-subcard.synonyms {
    background: #f0fdf4 !important;
    border: 1px solid #bbf7d0 !important;
  }
  html.light .thesaurus-subcard.synonyms h4 {
    color: #166534 !important;
    font-weight: 800 !important;
  }
  html.light .synonym-chip-btn {
    background: #ffffff !important;
    border: 1px solid #86efac !important;
    color: #15803d !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    font-weight: 700 !important;
  }
  html.light .synonym-chip-btn:hover {
    background: #15803d !important;
    color: #ffffff !important;
    border-color: #15803d !important;
  }

  html.light .thesaurus-subcard.traps {
    background: #fff1f2 !important;
    border: 1px solid #fecdd3 !important;
  }
  html.light .thesaurus-subcard.traps h4 {
    color: #9f1239 !important;
    font-weight: 800 !important;
  }
  html.light .falso-trap-item {
    background: #ffffff !important;
    border: 1px solid #fecdd3 !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02) !important;
    color: #334155 !important;
  }
  html.light .falso-trap-term {
    color: #dc2626 !important;
    font-weight: 800 !important;
  }

  /* Dark mode tweaks for Thesaurus */
  html.dark .thesaurus-card {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.8), rgba(15, 23, 42, 0.9)) !important;
    border: 1px solid rgba(99, 102, 241, 0.35) !important;
  }
  html.dark .thesaurus-subcard.synonyms {
    background: rgba(6, 78, 59, 0.25) !important;
    border: 1px solid rgba(16, 185, 129, 0.25) !important;
  }
  html.dark .thesaurus-subcard.traps {
    background: rgba(136, 19, 55, 0.25) !important;
    border: 1px solid rgba(244, 63, 94, 0.25) !important;
  }

  /* 4. Custom Chapter Dropdown (Prevents OS popover overflow) */
  .pq-dd-container {
    position: relative !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }
  .pq-dd-btn {
    width: 100% !important;
    height: 42px !important;
    min-height: 42px !important;
    padding: 0 14px !important;
    background: rgba(15, 15, 18, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    font-family: inherit !important;
    transition: all 0.2s ease !important;
    box-sizing: border-box !important;
    text-align: right !important;
  }
  .pq-dd-btn.open {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2) !important;
  }
  .pq-dd-arrow {
    font-size: 0.75rem !important;
    transition: transform 0.2s ease !important;
    color: #a1a1aa !important;
    margin-right: 8px !important;
  }
  .pq-dd-btn.open .pq-dd-arrow {
    transform: rotate(180deg) !important;
    color: #38bdf8 !important;
  }
  .pq-dd-label {
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    flex: 1 !important;
  }
  .pq-dd-menu {
    display: none;
    position: absolute !important;
    top: calc(100% + 6px) !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    max-height: 280px !important;
    overflow-y: auto !important;
    background: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 14px !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45) !important;
    z-index: 1000 !important;
    padding: 6px !important;
    box-sizing: border-box !important;
  }
  .pq-dd-menu.open {
    display: block !important;
    animation: fadeIn 0.15s ease !important;
  }
  .pq-dd-item {
    padding: 10px 12px !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #e2e8f0 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    text-align: right !important;
  }
  .pq-dd-item:hover {
    background: rgba(56, 189, 248, 0.15) !important;
    color: #38bdf8 !important;
  }
  .pq-dd-item.selected {
    background: rgba(56, 189, 248, 0.25) !important;
    color: #fff !important;
    font-weight: 700 !important;
  }
  html.light .pq-dd-btn {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #0f172a !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
  }
  html.light .pq-dd-btn.open {
    border-color: #0284c7 !important;
    box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15) !important;
  }
  html.light .pq-dd-menu {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1) !important;
  }
  html.light .pq-dd-item {
    color: #334155 !important;
  }
  html.light .pq-dd-item:hover {
    background: #f0f9ff !important;
    color: #0284c7 !important;
  }
  html.light .pq-dd-item.selected {
    background: #e0f2fe !important;
    color: #0284c7 !important;
    font-weight: 700 !important;
  }

  /* 5. VERO / FALSO Segmented Filter Bar Centering & Polished Interactions */
  .segmented-filter-bar {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 auto !important;
    width: 100% !important;
    max-width: 440px !important;
    height: 42px !important;
    min-height: 42px !important;
    padding: 3px !important;
    gap: 4px !important;
    background: rgba(15, 15, 18, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    box-sizing: border-box !important;
  }
  .segmented-btn {
    flex: 1 !important;
    height: 36px !important;
    min-height: 36px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    border-radius: 9px !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    border: 1px solid transparent !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-family: inherit !important;
    white-space: nowrap !important;
  }
  .segmented-btn.active {
    background: linear-gradient(135deg, #0284c7, #2563eb) !important;
    color: #ffffff !important;
    border-color: #0284c7 !important;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.3) !important;
  }
  .segmented-btn.active-vero {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: #ffffff !important;
    border-color: #10b981 !important;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3) !important;
  }
  .segmented-btn.active-falso {
    background: linear-gradient(135deg, #f43f5e, #e11d48) !important;
    color: #ffffff !important;
    border-color: #f43f5e !important;
    box-shadow: 0 2px 8px rgba(244, 63, 94, 0.3) !important;
  }

  html.light .segmented-filter-bar {
    background: #f1f5f9 !important;
    border: 1px solid #cbd5e1 !important;
  }
  html.light .segmented-btn {
    color: #475569 !important;
  }
  html.light .segmented-btn:hover:not(.active):not(.active-vero):not(.active-falso) {
    background: rgba(15, 23, 42, 0.05) !important;
    color: #0f172a !important;
  }
  html.light .segmented-btn.active {
    background: linear-gradient(135deg, #0284c7, #2563eb) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.28) !important;
  }
  html.light .segmented-btn.active-vero {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.28) !important;
  }
  html.light .segmented-btn.active-falso {
    background: linear-gradient(135deg, #f43f5e, #e11d48) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(244, 63, 94, 0.28) !important;
  }
"""

# Insert or append master_css before </style>
if '</style>' in content:
    content = content.replace('</style>', master_css + '\n</style>', 1)
    print("Injected master CSS successfully.")
else:
    print("ERROR: </style> not found.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved all changes to parole-quiz.html successfully.")

import sys

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# 1. Update search modal header in HTML: change '⎋ Esc' to clean '✕' close button and concise placeholder
old_modal_header = '''          <!-- شريط الإدخال الرئيسي -->
          <div class="search-modal-header">
            <span class="search-modal-icon">🔍</span>
            <input type="text" id="globalSearchInput" class="search-modal-input" placeholder="ابحث عن أي باب، إشارة، مفهوم، أو مصطلح إيطالي... (مثال: precedenza, سرعة, 14, sempre)" autocomplete="off">
            <button class="search-modal-close" id="btnCloseGlobalSearch" aria-label="إغلاق نافذة البحث" title="إغلاق [Esc]">⎋ Esc</button>
          </div>'''

new_modal_header = '''          <!-- شريط الإدخال الرئيسي فائق النقاء -->
          <div class="search-modal-header">
            <span class="search-modal-icon">🔍</span>
            <input type="text" id="globalSearchInput" class="search-modal-input" placeholder="ابحث في الأبواب، الإشارات، والمصطلحات..." autocomplete="off">
            <button class="search-modal-close" id="btnCloseGlobalSearch" aria-label="إغلاق نافذة البحث" title="إغلاق">✕</button>
          </div>'''

if old_modal_header in nav:
    nav = nav.replace(old_modal_header, new_modal_header, 1)
    print("Updated search modal header HTML.")
else:
    print("WARNING: old_modal_header not found")

# 2. Update renderSearchResults HTML in unified-nav.js
old_render_row = '''      searchResults.innerHTML = filtered.map((item, idx) => `
        <a href="${item.href}" class="search-result-row ${idx === 0 ? 'selected' : ''}" data-idx="${idx}">
          <div class="result-badge">${item.badge}</div>
          <div class="result-info">
            <div class="result-title-row">
              <span class="result-title">${window.escapeHtml(item.title)}</span>
              <span class="result-cat-label">${window.escapeHtml(item.categoryLabel)}</span>
            </div>
            <div class="result-subtitle">${window.escapeHtml(item.subtitle)}</div>
          </div>
          <span class="result-jump-icon">↵</span>
        </a>
      `).join('');'''

new_render_row = '''      searchResults.innerHTML = filtered.map((item, idx) => `
        <a href="${item.href}" class="search-result-row ${idx === 0 ? 'selected' : ''}" data-idx="${idx}">
          <div class="result-badge ${item.type === 'chapter' ? 'badge-ch' : 'badge-tool'}">${item.type === 'chapter' ? item.badge.replace('Cap. ', '') : (item.icon || '🔬')}</div>
          <div class="result-info">
            <div class="result-title-row">
              <span class="result-title">${window.escapeHtml(item.title)}</span>
              <span class="result-cat-label">${window.escapeHtml(item.categoryLabel)}</span>
            </div>
            <div class="result-subtitle">${window.escapeHtml(item.subtitle)}</div>
          </div>
          <span class="result-jump-icon">‹</span>
        </a>
      `).join('');'''

if old_render_row in nav:
    nav = nav.replace(old_render_row, new_render_row, 1)
    print("Updated renderSearchResults HTML.")
else:
    print("WARNING: old_render_row not found")

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

# 3. Update theme-modes.css to provide clean, modern, responsive Search Modal styling
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

search_overhaul_css = '''
/* ==========================================================================
   SPOTLIGHT SEARCH PALETTE OVERHAUL (Mobile & Desktop Perfection)
   ========================================================================== */
.global-search-backdrop {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(11, 15, 25, 0.78) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  z-index: 999999 !important;
  display: flex !important;
  align-items: flex-start !important;
  justify-content: center !important;
  padding: 40px 16px 20px !important;
  box-sizing: border-box !important;
  direction: rtl !important;
}

.search-modal-container {
  width: 100% !important;
  max-width: 640px !important;
  max-height: 82vh !important;
  background: #0F172A !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  border-radius: 20px !important;
  box-shadow: 0 25px 65px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255, 255, 255, 0.05) !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
  direction: rtl !important;
}

html.light .search-modal-container {
  background: #FFFFFF !important;
  border-color: rgba(15, 23, 42, 0.12) !important;
  box-shadow: 0 25px 65px rgba(15, 23, 42, 0.18), 0 0 0 1px rgba(15, 23, 42, 0.05) !important;
}

.search-modal-header {
  display: flex !important;
  align-items: center !important;
  padding: 14px 18px !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
  gap: 12px !important;
  direction: rtl !important;
}

html.light .search-modal-header {
  border-bottom-color: rgba(15, 23, 42, 0.08) !important;
}

.search-modal-icon {
  font-size: 1.25rem !important;
  color: #38BDF8 !important;
  flex-shrink: 0 !important;
}

.search-modal-input {
  flex: 1 !important;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  color: #F8FAFC !important;
  font-size: 1.05rem !important;
  font-weight: 700 !important;
  font-family: inherit !important;
  direction: rtl !important;
  text-align: right !important;
  padding: 0 !important;
}

html.light .search-modal-input {
  color: #0F172A !important;
}

.search-modal-close {
  width: 32px !important;
  height: 32px !important;
  min-width: 32px !important;
  min-height: 32px !important;
  border-radius: 8px !important;
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  color: #94A3B8 !important;
  font-size: 1rem !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  transition: all 0.2s ease !important;
  flex-shrink: 0 !important;
}

.search-modal-close:hover {
  background: rgba(239, 68, 68, 0.15) !important;
  color: #EF4444 !important;
  border-color: rgba(239, 68, 68, 0.3) !important;
}

html.light .search-modal-close {
  background: rgba(15, 23, 42, 0.05) !important;
  border-color: rgba(15, 23, 42, 0.1) !important;
  color: #64748B !important;
}

/* Filter Pills Bar */
.search-filter-pills {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 10px 18px !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
  overflow-x: auto !important;
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
  direction: rtl !important;
}

.search-filter-pills::-webkit-scrollbar {
  display: none !important;
}

html.light .search-filter-pills {
  border-bottom-color: rgba(15, 23, 42, 0.06) !important;
}

.search-pill-btn {
  padding: 6px 14px !important;
  border-radius: 20px !important;
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #94A3B8 !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  transition: all 0.2s ease !important;
  flex-shrink: 0 !important;
}

.search-pill-btn.active {
  background: #0284C7 !important;
  border-color: #38BDF8 !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4) !important;
}

html.light .search-pill-btn {
  background: #F1F5F9 !important;
  border-color: rgba(15, 23, 42, 0.08) !important;
  color: #475569 !important;
}

html.light .search-pill-btn.active {
  background: #0284C7 !important;
  border-color: #0284C7 !important;
  color: #FFFFFF !important;
}

/* Search Results List */
.search-results-list {
  max-height: calc(82vh - 140px) !important;
  overflow-y: auto !important;
  padding: 10px 14px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 8px !important;
  direction: rtl !important;
}

.search-result-row {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  padding: 12px 14px !important;
  border-radius: 14px !important;
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.06) !important;
  text-decoration: none !important;
  cursor: pointer !important;
  transition: all 0.18s ease !important;
  direction: rtl !important;
}

html.light .search-result-row {
  background: #F8FAFC !important;
  border-color: rgba(15, 23, 42, 0.06) !important;
}

.search-result-row:hover,
.search-result-row.selected {
  background: rgba(56, 189, 248, 0.12) !important;
  border-color: rgba(56, 189, 248, 0.35) !important;
  transform: translateX(-3px) !important;
}

html.light .search-result-row:hover,
html.light .search-result-row.selected {
  background: #F0F9FF !important;
  border-color: #38BDF8 !important;
  transform: translateX(-3px) !important;
}

/* Badge Icon */
.result-badge {
  width: 38px !important;
  height: 38px !important;
  min-width: 38px !important;
  min-height: 38px !important;
  border-radius: 10px !important;
  background: rgba(56, 189, 248, 0.12) !important;
  border: 1px solid rgba(56, 189, 248, 0.25) !important;
  color: #38BDF8 !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.95rem !important;
  font-weight: 800 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
}

html.light .result-badge {
  background: rgba(2, 132, 199, 0.08) !important;
  border-color: rgba(2, 132, 199, 0.2) !important;
  color: #0284C7 !important;
}

/* Content Area */
.result-info {
  flex: 1 !important;
  min-width: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 3px !important;
}

.result-title-row {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 8px !important;
}

.result-title {
  font-size: 0.92rem !important;
  font-weight: 800 !important;
  color: #F8FAFC !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

html.light .result-title {
  color: #0F172A !important;
}

.result-cat-label {
  font-size: 0.7rem !important;
  font-weight: 700 !important;
  padding: 2px 7px !important;
  border-radius: 6px !important;
  background: rgba(255, 255, 255, 0.08) !important;
  color: #94A3B8 !important;
  white-space: nowrap !important;
  flex-shrink: 0 !important;
}

html.light .result-cat-label {
  background: rgba(15, 23, 42, 0.06) !important;
  color: #64748B !important;
}

.result-subtitle {
  font-size: 0.76rem !important;
  color: #94A3B8 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  font-weight: 500 !important;
}

html.light .result-subtitle {
  color: #64748B !important;
}

.result-jump-icon {
  font-size: 1.15rem !important;
  color: #64748B !important;
  opacity: 0.6 !important;
  flex-shrink: 0 !important;
}

/* Responsive Overrides (Mobile) */
@media (max-width: 768px) {
  .global-search-backdrop {
    padding: 16px 12px 20px !important;
    align-items: flex-start !important;
  }
  .search-modal-container {
    max-height: 88vh !important;
    border-radius: 20px !important;
  }
  .search-modal-footer {
    display: none !important;
  }
  .search-results-list {
    max-height: calc(88vh - 125px) !important;
  }
  .result-cat-label {
    display: none !important;
  }
}
'''

tm += '\n' + search_overhaul_css

with open(tm_path, 'w', encoding='utf-8') as f:
    f.write(tm)

print("Applied Spotlight search overhaul to theme-modes.css.")

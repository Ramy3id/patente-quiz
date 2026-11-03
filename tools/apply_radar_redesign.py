with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. Find and update the HTML for .ps-stats-strip
old_stats_html = '''      <div class="ps-stats-strip">
        <div class="ps-stat-item">
          <span>المصطلحات المفتاحية:</span>
          <strong id="statWordsCount">36</strong>
        </div>
        <div class="ps-stat-item">
          <span>الأسئلة المغطاة بالبنك:</span>
          <strong id="statQuestionsCovered">457 سؤالاً</strong>
        </div>
        <div class="ps-stat-item">
          <span>دقة الحسم المباشر:</span>
          <strong style="color:var(--ps-emerald);">تصل إلى 100%</strong>
        </div>
      </div>'''

new_stats_html = '''      <div class="ps-stats-strip">
        <div class="ps-stat-item">
          <strong id="statWordsCount">154</strong>
          <span>المصطلحات المفتاحية</span>
        </div>
        <div class="ps-stat-item">
          <strong id="statQuestionsCovered">1008</strong>
          <span>الأسئلة المغطاة</span>
        </div>
        <div class="ps-stat-item">
          <strong style="color:var(--ps-emerald) !important;">100%</strong>
          <span>دقة الحسم المباشر</span>
        </div>
      </div>'''

if old_stats_html in text:
    text = text.replace(old_stats_html, new_stats_html, 1)
    print('Updated stats HTML successfully')
else:
    print('old_stats_html not found!')

# 2. Add high-performance CSS for .ps-stats-strip, .ps-stat-item, .ps-filters-row, .ps-filter-btn
css_replacement = '''
    /* =========================================================
       RADAR HERO METRICS DASHBOARD (Unified 3-Column Strip)
       ========================================================= */
    .ps-stats-strip {
      display: grid !important;
      grid-template-columns: repeat(3, 1fr) !important;
      gap: 4px !important;
      margin-top: 16px !important;
      background: rgba(255, 255, 255, 0.04) !important;
      border: 1px solid var(--ps-card-border) !important;
      border-radius: 16px !important;
      padding: 10px 4px !important;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15) !important;
    }
    html.light .ps-stats-strip {
      background: #FFFFFF !important;
      border-color: rgba(15, 23, 42, 0.08) !important;
      box-shadow: 0 2px 12px rgba(15, 23, 42, 0.04) !important;
    }
    .ps-stat-item {
      background: transparent !important;
      border: none !important;
      border-radius: 0 !important;
      padding: 4px 2px !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: center !important;
      text-align: center !important;
      gap: 2px !important;
    }
    .ps-stat-item:not(:last-child) {
      border-left: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    html.light .ps-stat-item:not(:last-child) {
      border-left-color: rgba(15, 23, 42, 0.08) !important;
    }
    .ps-stat-item strong {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 1.15rem !important;
      font-weight: 900 !important;
      color: var(--ps-cyan) !important;
      line-height: 1.15 !important;
      display: block !important;
    }
    html.light .ps-stat-item strong {
      color: #0284C7 !important;
    }
    .ps-stat-item span {
      font-size: 0.68rem !important;
      font-weight: 700 !important;
      color: var(--ps-text-sub) !important;
      line-height: 1.2 !important;
      display: block !important;
      white-space: nowrap !important;
    }
    html.light .ps-stat-item span {
      color: #64748B !important;
    }

    /* =========================================================
       STRUCTURED BALANCED FILTER GRID (2-Column Symmetrical Layout)
       ========================================================= */
    .ps-controls {
      display: flex !important;
      flex-direction: column !important;
      gap: 12px !important;
      margin-bottom: 20px !important;
      background: var(--ps-card-bg) !important;
      padding: 14px !important;
      border-radius: 18px !important;
      border: 1px solid var(--ps-card-border) !important;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
    }
    html.light .ps-controls {
      background: #FFFFFF !important;
      border-color: rgba(15, 23, 42, 0.08) !important;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
    }
    .ps-search-input {
      width: 100% !important;
      padding: 12px 16px !important;
      border-radius: 12px !important;
      border: 1px solid var(--ps-card-border) !important;
      background: rgba(255, 255, 255, 0.04) !important;
      color: var(--ps-text) !important;
      font-family: inherit !important;
      font-size: 0.90rem !important;
      font-weight: 600 !important;
      outline: none !important;
      transition: all 0.2s ease !important;
      box-sizing: border-box !important;
    }
    html.light .ps-search-input {
      background: #F8FAFC !important;
      border-color: #CBD5E1 !important;
      color: #0F172A !important;
    }
    .ps-search-input:focus {
      border-color: var(--ps-cyan) !important;
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15) !important;
    }
    .ps-filters-row {
      display: grid !important;
      grid-template-columns: repeat(2, 1fr) !important;
      gap: 8px !important;
      width: 100% !important;
      margin-top: 2px !important;
      padding: 0 !important;
      box-sizing: border-box !important;
    }
    @media (min-width: 640px) {
      .ps-filters-row {
        grid-template-columns: repeat(3, 1fr) !important;
      }
    }
    @media (min-width: 1024px) {
      .ps-filters-row {
        grid-template-columns: repeat(4, 1fr) !important;
      }
    }
    .ps-filter-btn {
      width: 100% !important;
      height: 40px !important;
      min-height: 40px !important;
      max-height: 40px !important;
      padding: 0 8px !important;
      border-radius: 12px !important;
      border: 1px solid var(--ps-card-border) !important;
      background: rgba(255, 255, 255, 0.03) !important;
      color: var(--ps-text-sub) !important;
      font-family: inherit !important;
      font-size: 0.77rem !important;
      font-weight: 700 !important;
      cursor: pointer !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 5px !important;
      text-align: center !important;
      box-sizing: border-box !important;
      white-space: nowrap !important;
      overflow: hidden !important;
      text-overflow: ellipsis !important;
      transition: all 0.15s ease !important;
    }
    html.light .ps-filter-btn {
      background: #F8FAFC !important;
      border-color: #E2E8F0 !important;
      color: #475569 !important;
    }
    .ps-filter-btn:hover {
      background: rgba(255, 255, 255, 0.08) !important;
      color: var(--ps-text) !important;
    }
    html.light .ps-filter-btn:hover {
      background: #F1F5F9 !important;
      color: #0F172A !important;
    }
    .ps-filter-btn.active {
      background: var(--ps-cyan) !important;
      color: #0B0F19 !important;
      border-color: var(--ps-cyan) !important;
      font-weight: 800 !important;
      box-shadow: 0 2px 8px rgba(56, 189, 248, 0.3) !important;
    }
    html.light .ps-filter-btn.active {
      background: #0284C7 !important;
      color: #FFFFFF !important;
      border-color: #0284C7 !important;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.3) !important;
    }
    .ps-filter-btn.filter-falso.active {
      background: var(--ps-rose) !important;
      color: #FFFFFF !important;
      border-color: var(--ps-rose) !important;
      box-shadow: 0 2px 8px rgba(244, 63, 94, 0.3) !important;
    }
    .ps-filter-btn.filter-vero.active {
      background: var(--ps-emerald) !important;
      color: #FFFFFF !important;
      border-color: var(--ps-emerald) !important;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3) !important;
    }
    .ps-filter-btn.filter-exception.active {
      background: var(--ps-amber) !important;
      color: #0B0F19 !important;
      border-color: var(--ps-amber) !important;
      box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3) !important;
    }
    .ps-filter-btn span {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.72rem !important;
      font-weight: 800 !important;
      opacity: 0.9 !important;
    }
    #btnFilterAll,
    #btnTheoryFilterAll {
      grid-column: 1 / -1 !important;
    }
'''

# Append css before </style>
style_idx = text.find('</style>')
if style_idx != -1:
    text = text[:style_idx] + css_replacement + '\n' + text[style_idx:]
    print('Appended CSS replacement')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated parole-spia.html successfully.')

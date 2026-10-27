import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

# =====================================================================
# 1. Update Capitoli_Divisi/index.html (Card Header & Badges Redesign)
# =====================================================================
index_path = r"R:\Ramy\PATENTE\Capitoli_Divisi\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Pattern for card top strip
pattern = re.compile(
    r'<div class="card-top-strip">\s*'
    r'(<span class="ch-pill-num">.*?</span>)\s*'
    r'(<span class="(?:gate-free-badge|chapter-gated-badge)".*?</span>)?\s*'
    r'<div class="ch-stats-strip">\s*'
    r'<span>📝\s*(\d+)\s*Q</span>\s*'
    r'<span>🖼️\s*(\d+)\s*IMG</span>\s*'
    r'</div>\s*'
    r'</div>\s*'
    r'(<div class="ch-title-it">.*?</div>)\s*'
    r'(<div class="ch-title-ar">.*?</div>)',
    re.DOTALL
)

def format_card(m):
    ch_pill = m.group(1).strip()
    badge = m.group(2) or ''
    q_count = m.group(3)
    img_count = m.group(4)
    title_it = m.group(5)
    title_ar = m.group(6)
    
    clean_badge = ''
    if 'gate-free-badge' in badge:
        clean_badge = '<span class="gate-free-badge">🟢 مفتوح مجاناً</span>'
    elif 'chapter-gated-badge' in badge:
        clean_badge = '<span class="chapter-gated-badge">🔒 عينة 5 أسئلة</span>'
    
    return f'''<div class="card-top-strip">
          {ch_pill}
          {clean_badge}
        </div>
        {title_it}
        {title_ar}
        <div class="card-stats-row">
          <span class="stat-pill"><span class="stat-ico">📝</span> <strong>{q_count}</strong> سؤال</span>
          <span class="stat-pill"><span class="stat-ico">🖼️</span> <strong>{img_count}</strong> إشارة</span>
        </div>'''

new_html, count = pattern.subn(format_card, html)
print(f"Replaced {count} chapter cards with clean two-deck architecture!")

# Add CSS for new card styles
new_card_css = '''
  /* Clean Architecture for Chapter Cards */
  .card-top-strip {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }
  .ch-pill-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    font-weight: 700;
    background: rgba(99, 102, 241, 0.12);
    color: #818cf8;
    border: 1px solid rgba(99, 102, 241, 0.28);
    padding: 3px 10px;
    border-radius: 8px;
    white-space: nowrap;
    letter-spacing: 0.02em;
    flex-shrink: 0;
  }
  html.light .ch-pill-num {
    background: rgba(99, 102, 241, 0.08);
    color: #4f46e5;
    border-color: rgba(99, 102, 241, 0.22);
  }

  .gate-free-badge {
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
    font-size: 0.72rem;
    padding: 3px 8px;
    border-radius: 999px;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
  }
  html.light .gate-free-badge {
    background: rgba(16, 185, 129, 0.1);
    color: #059669;
    border-color: rgba(16, 185, 129, 0.25);
  }

  .chapter-gated-badge {
    background: rgba(245, 158, 11, 0.12);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
    font-size: 0.72rem;
    padding: 3px 8px;
    border-radius: 999px;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
  }
  html.light .chapter-gated-badge {
    background: rgba(217, 119, 6, 0.08);
    color: #b45309;
    border-color: rgba(217, 119, 6, 0.25);
  }

  .card-stats-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }
  .stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', 'Cairo', monospace;
    color: var(--text-muted);
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-subtle);
    padding: 4px 10px;
    border-radius: 8px;
    white-space: nowrap;
  }
  html.light .stat-pill {
    background: #f1f5f9;
    border-color: rgba(15, 23, 42, 0.08);
    color: #475569;
  }
  .stat-pill strong {
    color: var(--text-primary);
    font-weight: 700;
  }
  .stat-ico {
    font-size: 0.82rem;
    line-height: 1;
  }
'''

if '.card-stats-row' not in new_html:
    new_html = new_html.replace('.ch-pill-num {', new_card_css + '\n  /* Old pill styles */\n  .old-ch-pill {')

with open(index_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Capitoli_Divisi/index.html card redesign written successfully!")

# =====================================================================
# 2. Update assets/js/unified-nav.js (Header Harmonization)
# =====================================================================
nav_path = r"R:\Ramy\PATENTE\assets\js\unified-nav.js"
with open(nav_path, "r", encoding="utf-8") as f:
    nav_js = f.read()

# Harmonize header styles
header_override_css = '''
      /* ==================== Harmonized Apple HIG Header System ==================== */
      .unified-portal-nav {
        min-height: 58px;
        padding: 0 20px;
      }
      .nav-brand-group {
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .nav-chapters-btn {
        height: 36px !important;
        border-radius: 10px !important;
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #CBD5E1 !important;
        font-weight: 600 !important;
      }
      html.light .nav-chapters-btn {
        background: rgba(15, 23, 42, 0.04) !important;
        border-color: rgba(15, 23, 42, 0.08) !important;
        color: #334155 !important;
      }
      .nav-chapters-btn:hover, .nav-chapters-btn.active {
        background: rgba(99, 102, 241, 0.12) !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
        color: #818CF8 !important;
      }
      html.light .nav-chapters-btn:hover, html.light .nav-chapters-btn.active {
        background: rgba(99, 102, 241, 0.08) !important;
        border-color: rgba(99, 102, 241, 0.25) !important;
        color: #4F46E5 !important;
      }

      /* Unified Right Toolbar Action Pills */
      .nav-desktop-actions {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .nav-search-trigger,
      .nav-progress-pill,
      .nav-auth-pill,
      .nav-theme-btn {
        height: 36px !important;
        border-radius: 10px !important;
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
      }
      html.light .nav-search-trigger,
      html.light .nav-progress-pill,
      html.light .nav-auth-pill,
      html.light .nav-theme-btn {
        background: rgba(15, 23, 42, 0.04) !important;
        border-color: rgba(15, 23, 42, 0.08) !important;
        color: #334155 !important;
      }

      .nav-search-trigger:hover,
      .nav-progress-pill:hover,
      .nav-auth-pill:hover,
      .nav-theme-btn:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.18) !important;
        transform: translateY(-1px) !important;
      }
      html.light .nav-search-trigger:hover,
      html.light .nav-progress-pill:hover,
      html.light .nav-auth-pill:hover,
      html.light .nav-theme-btn:hover {
        background: rgba(15, 23, 42, 0.07) !important;
        border-color: rgba(15, 23, 42, 0.15) !important;
        color: #0F172A !important;
      }

      .nav-auth-pill {
        color: #38BDF8 !important;
      }
      html.light .nav-auth-pill {
        color: #0284C7 !important;
      }
      .nav-auth-pill.logged-in {
        color: #34D399 !important;
      }
      html.light .nav-auth-pill.logged-in {
        color: #059669 !important;
      }
'''

if 'Harmonized Apple HIG Header System' not in nav_js:
    # Inject before closing of navStyles
    target_insert = '/* 2. هيدر البوابة الموحد (Unified Portal Nav) */'
    nav_js = nav_js.replace(target_insert, header_override_css + '\n      ' + target_insert, 1)
    with open(nav_path, "w", encoding="utf-8") as f:
        f.write(nav_js)
    print("assets/js/unified-nav.js header harmonized successfully!")
else:
    print("Header harmonization already exists in unified-nav.js")

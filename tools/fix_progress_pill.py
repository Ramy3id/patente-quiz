# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'R:/Ramy/PATENTE/assets/js/unified-nav.js'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the HTML structure of globalProgressPill
old_html = '''          <!-- شارة الإنجاز العامة -->
          <a href="${ctx.interactive}dashboard.html" class="nav-progress-pill" id="globalProgressPill" title="إنجازك العام: تم حل ${globalStats.answered} من ${globalStats.total} سؤال (انقر لعرض لوحة التحكم)">
            <span class="prog-pill-icon">🎯</span>
            <div class="prog-pill-meta">
              <span class="prog-pill-label">إنجازك</span>
              <strong class="prog-pill-val" id="globalProgressPctVal">${globalStats.pct}%</strong>
            </div>
            <div class="prog-pill-bar-track">
              <div class="prog-pill-bar-fill" id="globalProgressMiniFill" style="width:${globalStats.pct}%;"></div>
            </div>
          </a>'''

new_html = '''          <!-- شارة الإنجاز العامة الفاخرة (Clean Horizontal Layout) -->
          <a href="${ctx.interactive}dashboard.html" class="nav-progress-pill" id="globalProgressPill" title="إنجازك العام: تم حل ${globalStats.answered} من ${globalStats.total} سؤال (انقر لعرض لوحة التحكم)">
            <span class="prog-pill-icon">🎯</span>
            <span class="prog-pill-label">إنجازك</span>
            <strong class="prog-pill-val" id="globalProgressPctVal">${globalStats.pct}%</strong>
            <div class="prog-pill-bar-track">
              <div class="prog-pill-bar-fill" id="globalProgressMiniFill" style="width:${globalStats.pct}%;"></div>
            </div>
          </a>'''

if old_html in text:
    text = text.replace(old_html, new_html, 1)
    print("globalProgressPill HTML replaced successfully!")
else:
    print("Warning: old_html not found directly!")

# 2. Update CSS rules for .nav-progress-pill
# We will inject a targeted styling block into Harmonized Apple HIG Header System
target_css_marker = '/* Unified Right Toolbar Action Pills */'
custom_pill_css = '''      /* Custom Luxury Styling for .nav-progress-pill */
      .nav-progress-pill {
        height: 36px !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        padding: 0 10px !important;
        border-radius: 10px !important;
        background: rgba(16, 185, 129, 0.08) !important;
        border: 1px solid rgba(16, 185, 129, 0.28) !important;
        text-decoration: none !important;
        white-space: nowrap !important;
        line-height: 1 !important;
        transition: all 0.2s ease !important;
      }
      html.light .nav-progress-pill {
        background: rgba(16, 185, 129, 0.06) !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
      }
      .nav-progress-pill:hover {
        background: rgba(16, 185, 129, 0.16) !important;
        border-color: rgba(16, 185, 129, 0.5) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 10px rgba(16, 185, 129, 0.18) !important;
      }
      .prog-pill-icon {
        font-size: 0.95rem !important;
        line-height: 1 !important;
        flex-shrink: 0 !important;
      }
      .prog-pill-label {
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        line-height: 1 !important;
        white-space: nowrap !important;
        letter-spacing: normal !important;
      }
      html.light .prog-pill-label {
        color: #475569 !important;
      }
      .prog-pill-val {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.84rem !important;
        font-weight: 800 !important;
        color: #10B981 !important;
        line-height: 1 !important;
        white-space: nowrap !important;
      }
      html.light .prog-pill-val {
        color: #059669 !important;
      }
      .prog-pill-bar-track {
        width: 38px !important;
        height: 5px !important;
        background: rgba(255, 255, 255, 0.12) !important;
        border-radius: 99px !important;
        overflow: hidden !important;
        flex-shrink: 0 !important;
        margin-right: 2px !important;
      }
      html.light .prog-pill-bar-track {
        background: rgba(15, 23, 42, 0.1) !important;
      }
      .prog-pill-bar-fill {
        height: 100% !important;
        background: #10B981 !important;
        border-radius: 99px !important;
        transition: width 0.3s ease !important;
      }
      html.light .prog-pill-bar-fill {
        background: #059669 !important;
      }

      '''

if custom_pill_css not in text and target_css_marker in text:
    text = text.replace(target_css_marker, custom_pill_css + target_css_marker, 1)
    print("custom_pill_css injected successfully!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Unified nav updated successfully!")

import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# 1. Update back button arrow to point RIGHT (➡)
old_back_arrow_html = """      <a href="piano-studio.html" class="tr-back-plan-btn" id="btnReturnToPlanTop" title="العودة لجدول الخطة الدراسية">
        <span class="tr-back-arrow">⬅</span>
        <span>العودة إلى جدول الخطة الدراسية</span>
        <span class="tr-back-pill">📅 الخطة</span>
      </a>"""

new_back_arrow_html = """      <a href="piano-studio.html" class="tr-back-plan-btn" id="btnReturnToPlanTop" title="العودة لجدول الخطة الدراسية">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span class="tr-back-arrow">➡</span>
          <span>العودة إلى جدول الخطة الدراسية</span>
        </div>
        <span class="tr-back-pill">📅 الخطة</span>
      </a>"""

# Hover transform for right arrow
old_hover_arrow = """.tr-back-plan-btn:hover .tr-back-arrow {
      transform: translateX(-4px);
    }"""

new_hover_arrow = """.tr-back-plan-btn:hover .tr-back-arrow {
      transform: translateX(4px);
    }"""

# 2. Update controls wrap HTML: remove inline style on الخطة link
old_controls_html = """        <div class="tr-controls-wrap">
          <a href="piano-studio.html" class="tr-count-btn" style="text-decoration: none; display: inline-flex; align-items: center; gap: 4px; border-color: rgba(56, 189, 248, 0.4); color: var(--tr-cyan);" title="العودة لجدول الخطة الدراسية">📅 الخطة</a>
          <span style="font-size: 0.82rem; color: var(--tr-text-sub);">عدد الأسئلة:</span>
          <button class="tr-count-btn" id="btnCount15" onclick="setSessionCount(15)">15 سؤالاً</button>"""

new_controls_html = """        <div class="tr-controls-wrap">
          <a href="piano-studio.html" class="tr-count-btn" title="العودة لجدول الخطة الدراسية">📅 الخطة</a>
          <span style="font-size: 0.82rem; color: var(--tr-text-sub);">عدد الأسئلة:</span>
          <button class="tr-count-btn" id="btnCount15" onclick="setSessionCount(15)">15 سؤالاً</button>"""

# 3. Add unified height and border styles for .tr-controls-wrap .tr-count-btn
controls_css_rule = """
    /* توحيد الارتفاع ولون البوردر الدقيق لزر الخطة و15 سؤالاً وباقي أزرار التحكم */
    .tr-controls-wrap .tr-count-btn {
      height: 38px !important;
      min-height: 38px !important;
      max-height: 38px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 6px !important;
      box-sizing: border-box !important;
      line-height: 1 !important;
      padding: 0 14px !important;
      border-radius: 10px !important;
      font-size: 0.85rem !important;
      font-weight: 700 !important;
      border: 1px solid var(--tr-border) !important;
      text-decoration: none !important;
    }

    html.light .tr-controls-wrap .tr-count-btn {
      background: #FFFFFF !important;
      border: 1px solid #CBD5E1 !important;
      color: #334155 !important;
    }

    html.light .tr-controls-wrap .tr-count-btn:hover {
      background: #F8FAFC !important;
      border-color: #94A3B8 !important;
      color: #0F172A !important;
    }

    html.light .tr-controls-wrap .tr-count-btn.active {
      background: #0284C7 !important;
      border-color: #0284C7 !important;
      color: #FFFFFF !important;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35) !important;
    }
"""

if '\r\n' in content:
    old_back_arrow_html = old_back_arrow_html.replace('\n', '\r\n')
    new_back_arrow_html = new_back_arrow_html.replace('\n', '\r\n')
    old_hover_arrow = old_hover_arrow.replace('\n', '\r\n')
    new_hover_arrow = new_hover_arrow.replace('\n', '\r\n')
    old_controls_html = old_controls_html.replace('\n', '\r\n')
    new_controls_html = new_controls_html.replace('\n', '\r\n')
    controls_css_rule = controls_css_rule.replace('\n', '\r\n')

if old_back_arrow_html in content:
    content = content.replace(old_back_arrow_html, new_back_arrow_html, 1)
    print("1. Replaced back arrow to point RIGHT (➡)")
else:
    print("1. old_back_arrow_html not found!")

if old_hover_arrow in content:
    content = content.replace(old_hover_arrow, new_hover_arrow, 1)
    print("2. Replaced hover arrow transform")

if old_controls_html in content:
    content = content.replace(old_controls_html, new_controls_html, 1)
    print("3. Removed inline style on الخطة link")
else:
    print("3. old_controls_html not found!")

# Add controls_css_rule before </style>
target_style = "</style>"
content = content.replace(target_style, controls_css_rule + "\r\n  " + target_style if '\r\n' in content else controls_css_rule + "\n  " + target_style, 1)
print("4. Added unified height and border CSS rule")

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("Saved file successfully!")

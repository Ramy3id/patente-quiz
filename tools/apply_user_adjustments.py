import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# 1. Update .tr-header-top and .tr-controls-wrap and .tr-back-plan-btn in CSS
old_header_css = """.tr-header-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }"""

new_header_css = """.tr-header-top {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 14px;
      width: 100%;
      text-align: center;
    }"""

old_controls_css = """.tr-controls-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }"""

new_controls_css = """.tr-controls-wrap {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      flex-wrap: wrap;
      width: 100%;
      margin: 0 auto;
    }"""

old_back_plan_css = """.tr-back-plan-btn {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: var(--tr-cyan);
      padding: 10px 18px;
      border-radius: 12px;
      font-weight: 800;
      font-size: 0.95rem;
      text-decoration: none;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    }"""

new_back_plan_css = """.tr-back-plan-btn {
      display: flex;
      width: 100%;
      justify-content: space-between;
      align-items: center;
      box-sizing: border-box;
      gap: 10px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: var(--tr-cyan);
      padding: 12px 20px;
      border-radius: var(--tr-radius);
      font-weight: 800;
      font-size: 0.95rem;
      text-decoration: none;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    }"""

# 2. Fix the active star button text color in Light Mode
active_btn_fix_css = """
    /* إصلاح تباين الزر النشط في الوضع النهاري ليصبح بارزاً ومقروءاً */
    html.light .tr-count-btn.active {
      background: #0284C7 !important;
      color: #FFFFFF !important;
      border-color: #0284C7 !important;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35) !important;
    }
"""

if '\r\n' in content:
    old_header_css = old_header_css.replace('\n', '\r\n')
    new_header_css = new_header_css.replace('\n', '\r\n')
    old_controls_css = old_controls_css.replace('\n', '\r\n')
    new_controls_css = new_controls_css.replace('\n', '\r\n')
    old_back_plan_css = old_back_plan_css.replace('\n', '\r\n')
    new_back_plan_css = new_back_plan_css.replace('\n', '\r\n')
    active_btn_fix_css = active_btn_fix_css.replace('\n', '\r\n')

if old_header_css in content:
    content = content.replace(old_header_css, new_header_css, 1)
    print("1. Replaced header css")

if old_controls_css in content:
    content = content.replace(old_controls_css, new_controls_css, 1)
    print("2. Replaced controls css")

if old_back_plan_css in content:
    content = content.replace(old_back_plan_css, new_back_plan_css, 1)
    print("3. Replaced back plan css to full width")

# Add active_btn_fix_css before </style>
target_style = "</style>"
content = content.replace(target_style, active_btn_fix_css + "\r\n  " + target_style if '\r\n' in content else active_btn_fix_css + "\n  " + target_style, 1)
print("4. Added active button light mode fix")

# 3. Update the 3 tool buttons labels in HTML to: المعاني، الأفخاخ، الـ 3 كتل
old_smart_tools_html = """        <button class="tr-smart-tool-btn" id="btnToggleBilingual" onclick="toggleBilingualHighlight()" title="تظليل متزامن للمصطلحات بين الإيطالية والعربية">
          <span id="lblBilingualIcon">🎨</span>
          <span id="lblBilingualText">تظليل المعاني</span>
        </button>
        <button class="tr-smart-tool-btn" id="btnToggleHighlight" onclick="toggleTrapHighlight()" title="تفعيل/تعطيل كشف وتظليل الفخاخ الوزارية">
          <span id="lblHighlightIcon">👁️</span>
          <span id="lblHighlightText">تظليل الأفخاخ</span>
        </button>
        <button class="tr-smart-tool-btn active" id="btnToggleDecoder" onclick="toggleAllenamentoDecoder()" title="تفكيك السؤال لـ 3 كتل منطقية والمعادلة القانونية">
          <span id="lblDecoderIcon">🧩</span>
          <span id="lblDecoderText">مفكك الـ 3 كتل</span>
        </button>"""

new_smart_tools_html = """        <button class="tr-smart-tool-btn" id="btnToggleBilingual" onclick="toggleBilingualHighlight()" title="تظليل متزامن للمصطلحات بين الإيطالية والعربية">
          <span id="lblBilingualIcon">🎨</span>
          <span id="lblBilingualText">المعاني</span>
        </button>
        <button class="tr-smart-tool-btn" id="btnToggleHighlight" onclick="toggleTrapHighlight()" title="تفعيل/تعطيل كشف وتظليل الفخاخ الوزارية">
          <span id="lblHighlightIcon">👁️</span>
          <span id="lblHighlightText">الأفخاخ</span>
        </button>
        <button class="tr-smart-tool-btn active" id="btnToggleDecoder" onclick="toggleAllenamentoDecoder()" title="تفكيك السؤال لـ 3 كتل منطقية والمعادلة القانونية">
          <span id="lblDecoderIcon">🧩</span>
          <span id="lblDecoderText">الـ 3 كتل</span>
        </button>"""

if '\r\n' in content:
    old_smart_tools_html = old_smart_tools_html.replace('\n', '\r\n')
    new_smart_tools_html = new_smart_tools_html.replace('\n', '\r\n')

if old_smart_tools_html in content:
    content = content.replace(old_smart_tools_html, new_smart_tools_html, 1)
    print("5. Replaced smart tool labels in HTML to المعاني، الأفخاخ، الـ 3 كتل")

# 4. Update JS label updates in updateBilingualBtnUI, updateHighlightBtnUI, updateDecoderBtnUI
# Also update the navigation buttons HTML and JS to: السابق and التالي
old_nav_html = """          <!-- السابق (السهم لليمين خارجياً قبل الكلمة) -->
          <button class="tr-nav-btn tr-nav-prev" id="btnPrevQ" onclick="goToPrevQuestion()">
            <span class="nav-arrow">▶</span>
            <span>السؤال السابق</span>
          </button>

          <!-- زر العودة للخطة في المنتصف -->
          <a href="piano-studio.html" class="tr-nav-plan-link" title="الرجوع لجدول الخطة الدراسية">
            <span>📅 الخطة</span>
          </a>

          <!-- التالي (السهم لليسار خارجياً بعد الكلمة) -->
          <button class="tr-nav-btn tr-nav-next" id="btnNextQ" onclick="goToNextQuestion()">
            <span>السؤال التالي</span>
            <span class="nav-arrow">◀</span>
          </button>"""

new_nav_html = """          <!-- السابق (السهم لليمين خارجياً قبل الكلمة) -->
          <button class="tr-nav-btn tr-nav-prev" id="btnPrevQ" onclick="goToPrevQuestion()">
            <span class="nav-arrow">▶</span>
            <span>السابق</span>
          </button>

          <!-- زر العودة للخطة في المنتصف -->
          <a href="piano-studio.html" class="tr-nav-plan-link" title="الرجوع لجدول الخطة الدراسية">
            <span>📅 الخطة</span>
          </a>

          <!-- التالي (السهم لليسار خارجياً بعد الكلمة) -->
          <button class="tr-nav-btn tr-nav-next" id="btnNextQ" onclick="goToNextQuestion()">
            <span>التالي</span>
            <span class="nav-arrow">◀</span>
          </button>"""

if '\r\n' in content:
    old_nav_html = old_nav_html.replace('\n', '\r\n')
    new_nav_html = new_nav_html.replace('\n', '\r\n')

if old_nav_html in content:
    content = content.replace(old_nav_html, new_nav_html, 1)
    print("6. Replaced nav HTML to السابق and التالي")

# In JS renderCurrentQuestion:
old_render_nav_js = """      // حالة أزرار التالي والسابق بتوجيه أسهم للخارج دائماً
      const btnPrevEl = document.getElementById("btnPrevQ");
      if (btnPrevEl) {
        btnPrevEl.disabled = (currentIndex === 0);
        btnPrevEl.innerHTML = '<span class="nav-arrow">▶</span> <span>السؤال السابق</span>';
      }
      if (btnNextQ) {
        btnNextQ.innerHTML = (currentIndex === sessionQuestions.length - 1)
          ? '<span>إنهاء التدريب 🏁</span>'
          : '<span>السؤال التالي</span> <span class="nav-arrow">◀</span>';
      }"""

new_render_nav_js = """      // حالة أزرار التالي والسابق بتوجيه أسهم للخارج دائماً
      const btnPrevEl = document.getElementById("btnPrevQ");
      if (btnPrevEl) {
        btnPrevEl.disabled = (currentIndex === 0);
        btnPrevEl.innerHTML = '<span class="nav-arrow">▶</span> <span>السابق</span>';
      }
      if (btnNextQ) {
        btnNextQ.innerHTML = (currentIndex === sessionQuestions.length - 1)
          ? '<span>إنهاء التدريب 🏁</span>'
          : '<span>التالي</span> <span class="nav-arrow">◀</span>';
      }"""

if '\r\n' in content:
    old_render_nav_js = old_render_nav_js.replace('\n', '\r\n')
    new_render_nav_js = new_render_nav_js.replace('\n', '\r\n')

if old_render_nav_js in content:
    content = content.replace(old_render_nav_js, new_render_nav_js, 1)
    print("7. Replaced JS render nav to السابق and التالي")

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("All updates written successfully!")

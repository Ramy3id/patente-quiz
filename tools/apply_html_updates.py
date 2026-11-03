import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# 1. Remove the home button from top nav row
# Search for tr-back-home-link
target_home = """      <a href="../index.html" class="tr-back-home-link" title="الصفحة الرئيسية للبرنامج">
        <span>🏠 الرئيسية</span>
      </a>"""

if '\r\n' in content:
    target_home = target_home.replace('\n', '\r\n')

if target_home in content:
    content = content.replace(target_home, "")
    print("1. Removed home button successfully.")
else:
    print("1. target_home not found!")

# 2. Extract the 3 buttons into a dedicated toolbar card above question card
target_q_meta = """      <div class="tr-q-meta-row">
        <div>
          <span class="tr-subtopic-tag" id="lblSubtopic">المحور: المفاهيم العامة</span>
          <span style="font-size: 0.85rem; color: var(--tr-text-sub); margin-right: 8px;" id="lblProgress">سؤال 1 من 20</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
          <button class="tr-audio-btn" id="btnToggleBilingual" onclick="toggleBilingualHighlight()" title="تظليل متزامن للكلمات والمصطلحات بين الإيطالية والعربية">
            <span id="lblBilingualIcon">🎨</span> <span id="lblBilingualText">تظليل المعاني</span>
          </button>
          <button class="tr-audio-btn" id="btnToggleHighlight" onclick="toggleTrapHighlight()" title="تفعيل/تعطيل تظليل كلمات الفخاخ الوزارية">
            <span id="lblHighlightIcon">👁️</span> <span id="lblHighlightText">تظليل الأفخاخ</span>
          </button>
          <button class="tr-audio-btn" id="btnToggleDecoder" onclick="toggleAllenamentoDecoder()" title="تفكيك السؤال لـ 3 كتل منطقية والمعادلة القانونية">
            <span id="lblDecoderIcon">🧩</span> <span id="lblDecoderText">مفكك الـ 3 كتل</span>
          </button>
          <button class="tr-audio-btn" id="btnHandsFree" onclick="toggleHandsFreeMode()" title="تشغيل وضع الاستماع التلقائي بدون لمس الشاشة">
            <span>🎧 استماع تلقائي (Podcast)</span>
          </button>
          <button class="tr-audio-btn" onclick="playQuestionSpeech()" title="استمع لنطق السؤال">
            <span>🔊 استمع</span>
          </button>
        </div>
      </div>"""

replacement_tools_and_card = """    <!-- شريط الأدوات المساعدة الذكية في بلوك منفصل ومستقل -->
    <div class="tr-smart-tools-card">
      <div class="tr-smart-tools-grid">
        <button class="tr-smart-tool-btn" id="btnToggleBilingual" onclick="toggleBilingualHighlight()" title="تظليل متزامن للمصطلحات بين الإيطالية والعربية">
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
        </button>
      </div>
    </div>

    <!-- بطاقة السؤال التفاعلية -->
    <main class="tr-question-card" id="qCardSection">
      <div class="tr-q-meta-row">
        <div>
          <span class="tr-subtopic-tag" id="lblSubtopic">المحور: المفاهيم العامة</span>
          <span style="font-size: 0.85rem; color: var(--tr-text-sub); margin-right: 8px;" id="lblProgress">سؤال 1 من 20</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
          <button class="tr-audio-btn" id="btnHandsFree" onclick="toggleHandsFreeMode()" title="تشغيل وضع الاستماع التلقائي بدون لمس الشاشة">
            <span>🎧 استماع تلقائي</span>
          </button>
          <button class="tr-audio-btn" onclick="playQuestionSpeech()" title="استمع لنطق السؤال">
            <span>🔊 استمع</span>
          </button>
        </div>
      </div>"""

target_card_start = """    <!-- بطاقة السؤال التفاعلية -->
    <main class="tr-question-card" id="qCardSection">
""" + target_q_meta

if '\r\n' in content:
    target_card_start = target_card_start.replace('\n', '\r\n')
    replacement_tools_and_card = replacement_tools_and_card.replace('\n', '\r\n')

if target_card_start in content:
    content = content.replace(target_card_start, replacement_tools_and_card)
    print("2. Moved 3 buttons to dedicated toolbar card successfully.")
else:
    print("2. target_card_start not found!")

# 3. Update VERO / FALSO and Footer Navigation in HTML
target_footer = """      <!-- أسفل البطاقة -->
      <div class="tr-card-footer">
        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
          <button class="tr-count-btn" id="btnPrevQ" onclick="goToPrevQuestion()">➡ السؤال السابق</button>
          <a href="piano-studio.html" class="tr-count-btn" style="text-decoration: none; display: inline-flex; align-items: center; gap: 6px; border-color: rgba(56, 189, 248, 0.4); color: var(--tr-cyan);" title="الرجوع للخطة الدراسية">
            <span>📅</span>
            <span>العودة للخطة</span>
          </a>
        </div>
        <span style="font-size: 0.82rem; color: var(--tr-text-sub);">
          💡 يتم تسجيل الأسئلة غير الصحيحة تلقائياً في سجل الذاكرة والتكرار (SRS).
        </span>
        <button class="tr-count-btn" id="btnNextQ" onclick="goToNextQuestion()">السؤال التالي ⬅</button>
      </div>"""

replacement_footer = """      <!-- أسفل البطاقة: شريط التنقل المتناسق -->
      <div class="tr-card-footer">
        <div class="tr-nav-row">
          <!-- السابق (السهم لليمين خارجياً قبل الكلمة) -->
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
          </button>
        </div>

        <div class="tr-srs-tip">
          <span>💡 يتم تسجيل الأسئلة غير الصحيحة تلقائياً في سجل الذاكرة والتكرار (SRS).</span>
        </div>
      </div>"""

if '\r\n' in content:
    target_footer = target_footer.replace('\n', '\r\n')
    replacement_footer = replacement_footer.replace('\n', '\r\n')

if target_footer in content:
    content = content.replace(target_footer, replacement_footer)
    print("3. Updated footer navigation successfully.")
else:
    print("3. target_footer not found!")

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("HTML updates applied.")

import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

target_card = """    <!-- منطقة السؤال التفاعلية -->
    <main class="tr-question-card" id="qCardSection">
      <div class="tr-q-meta-row">
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

replacement_card = """    <!-- شريط الأدوات المساعدة الذكية في بلوك منفصل ومستقل تماماً -->
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

if '\r\n' in content:
    target_card = target_card.replace('\n', '\r\n')
    replacement_card = replacement_card.replace('\n', '\r\n')

assert target_card in content, "target_card not found in content"
content = content.replace(target_card, replacement_card, 1)

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("Step 2 applied successfully!")

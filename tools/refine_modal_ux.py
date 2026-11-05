import sys
sys.stdout.reconfigure(encoding='utf-8')

target_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace Question 2, 3, 4 HTML in #planSetupModal
old_questions_marker = """      <!-- السؤال 2: ساعات المذاكرة اليومية -->"""
end_marker = """      <!-- أزرار حفظ وإغلاق المودال -->"""

if old_questions_marker in content and end_marker in content:
    start_idx = content.find(old_questions_marker)
    end_idx = content.find(end_marker)
    
    new_questions_html = """      <!-- السؤال 2: ساعات المذاكرة اليومية -->
      <div class="sp-question-block">
        <div class="sp-q-label">
          <span>2. كم ساعة تستطيع تخصيصها للدراسة يومياً؟</span>
          <span class="sp-q-helper" onclick="selectDailyHours(2)">لست متأكداً؟ (ساعتان)</span>
        </div>
        <div class="sp-options-grid sp-options-hours">
          <div class="sp-opt-card" id="optHours1" onclick="selectDailyHours(1)">
            <div class="sp-opt-title">ساعة واحدة ⏱️</div>
            <div class="sp-opt-note">يناسب وقت المواصلات</div>
          </div>
          <div class="sp-opt-card selected" id="optHours2" onclick="selectDailyHours(2)">
            <div class="sp-opt-title">ساعتان يومياً ⭐</div>
            <div class="sp-opt-note">المعدل المثالي للباتنت</div>
          </div>
          <div class="sp-opt-card sp-opt-card-full" id="optHours3" onclick="selectDailyHours(3)">
            <div class="sp-opt-title">🚀 3 ساعات فأكثر (إنجاز فائق ومكثف)</div>
            <div class="sp-opt-note">خيار ممتاز للراغبين في إنهاء المنهج سريعاً وحجز كويز الامتحان بأسرع وقت</div>
          </div>
        </div>
      </div>

      <!-- السؤال 3: مستوى اللغة الإيطالية والكلمات -->
      <div class="sp-question-block">
        <div class="sp-q-label">
          <span>3. مستواك في اللغة الإيطالية ومصطلحات المرور:</span>
          <span class="sp-q-helper">يحدد وقت محطة الكلمات</span>
        </div>
        <div class="sp-options-grid sp-options-lang">
          <div class="sp-opt-card selected sp-opt-card-full" id="optLangBeginner" onclick="selectLangLevel('beginner')">
            <div class="sp-opt-title">⭐ مبتدئ / أركز على الكلمات ومصطلحات المرور</div>
            <div class="sp-opt-note">تخصيص وقت أكبر لمحطة القاموس والمترادفات الوزارية وفك شفرات الأسئلة</div>
          </div>
          <div class="sp-opt-card" id="optLangIntermediate" onclick="selectLangLevel('intermediate')">
            <div class="sp-opt-title">متوسط 📘</div>
            <div class="sp-opt-note">أفهم الأساسيات وأحتاج تثبيت القواعد</div>
          </div>
          <div class="sp-opt-card" id="optLangFluent" onclick="selectLangLevel('fluent')">
            <div class="sp-opt-title">جيد جداً ⚡</div>
            <div class="sp-opt-note">لغتي جيدة وتركيزي الأساسي على الحل السريع</div>
          </div>
        </div>
      </div>

      <!-- السؤال 4: مسار وتدفق ترتيب الأبواب -->
      <div class="sp-question-block">
        <div class="sp-q-label">
          <span>4. منهجية ترتيب تدفق الأبواب:</span>
          <span class="sp-q-helper">طريقة تسلسل الدروس</span>
        </div>
        <div class="sp-flow-grid">
          <!-- المسار العنقودي الذكي -->
          <div class="sp-opt-card sp-flow-item selected" id="optFlowCluster" onclick="selectFlowMode('cluster')">
            <div class="sp-flow-item-head">
              <div class="sp-flow-item-title">
                <span class="sp-flow-item-badge badge-recommended">⭐ الموصى به رسمياً</span>
                <h4>المسار العنقودي الذكي</h4>
              </div>
              <div class="sp-flow-radio-circle"></div>
            </div>
            <p class="sp-flow-item-desc">
              توزيع ذكي يكسر حاجز الخوف والملل، يبدأ بالأبواب الأكثر وضوحاً وأعلى درجات في الامتحان:
            </p>
            <div class="sp-flow-roadmap">
              <span class="sp-flow-chip">1️⃣ باب 01 (التأسيس)</span>
              <span class="sp-flow-arrow">←</span>
              <span class="sp-flow-chip">2️⃣ أبواب 21-25 (السلامة)</span>
              <span class="sp-flow-arrow">←</span>
              <span class="sp-flow-chip">3️⃣ أبواب 11-20 (الأوتوستراد والسرعة)</span>
              <span class="sp-flow-arrow">←</span>
              <span class="sp-flow-chip">4️⃣ أبواب 2-10 (كتلة الإشارات)</span>
            </div>
          </div>

          <!-- المسار التسلسلي الكلاسيكي -->
          <div class="sp-opt-card sp-flow-item" id="optFlowSequential" onclick="selectFlowMode('sequential')">
            <div class="sp-flow-item-head">
              <div class="sp-flow-item-title">
                <span class="sp-flow-item-badge badge-classic">ترتيب تقليدي</span>
                <h4>المسار التسلسلي الكلاسيكي</h4>
              </div>
              <div class="sp-flow-radio-circle"></div>
            </div>
            <p class="sp-flow-item-desc">
              دراسة الأبواب بالتتابع الرقمي المباشر من الباب 01 وحتى الباب 25 وفق الترتيب المعتاد لكتاب المدرسة.
            </p>
            <div class="sp-flow-roadmap">
              <span class="sp-flow-chip">باب 01</span>
              <span class="sp-flow-arrow">←</span>
              <span class="sp-flow-chip">باب 02</span>
              <span class="sp-flow-arrow">←</span>
              <span class="sp-flow-chip">باب 03</span>
              <span class="sp-flow-arrow">...</span>
              <span class="sp-flow-chip">باب 25</span>
            </div>
          </div>
        </div>
      </div>\n\n"""
    
    content = content[:start_idx] + new_questions_html + content[end_idx:]
    print("Successfully replaced questions 2, 3, 4 with refined modular layout.")
else:
    print("Error: markers not found.")

# 2. Add CSS refinements for backdrop, modal header spacing, Question 2, 3, 4
refinement_css = """
  /* ==========================================================================
     MODAL REFINEMENTS: SOFT BACKDROP, SAFE TOP GAP, HARMONIC BUTTONS
     ========================================================================== */
  .sp-modal-backdrop {
    position: fixed !important;
    inset: 0 !important;
    z-index: 2000 !important;
    display: none;
    align-items: flex-start !important;
    justify-content: center !important;
    overflow-y: auto !important;
    padding: 78px 14px 34px 14px !important;
    -webkit-overflow-scrolling: touch;
  }
  .sp-modal-backdrop.open {
    display: flex !important;
  }
  html.light .sp-modal-backdrop {
    background: rgba(15, 23, 42, 0.42) !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
  }
  html.dark .sp-modal-backdrop {
    background: rgba(0, 0, 0, 0.65) !important;
    backdrop-filter: blur(8px) !important;
  }

  .sp-modal-box {
    margin: 0 auto !important;
    width: 100% !important;
    max-width: 680px !important;
    border-radius: 22px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.2) !important;
  }
  @media (max-width: 640px) {
    .sp-modal-backdrop {
      padding: 74px 12px 28px 12px !important;
    }
    .sp-modal-box {
      padding: 22px 16px !important;
      border-radius: 20px !important;
    }
  }

  /* Question 2 & 3: Harmonic Layouts */
  .sp-options-hours,
  .sp-options-lang {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 10px !important;
  }
  .sp-opt-card-full {
    grid-column: 1 / -1 !important;
    text-align: right !important;
  }

  /* Question 4: Flow Methodology Bento */
  .sp-flow-grid {
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
  }
  .sp-flow-item {
    padding: 16px 18px !important;
    border-radius: 16px !important;
    border: 1.5px solid #E2E8F0 !important;
    background: #F8FAFC !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    text-align: right !important;
  }
  html.light .sp-flow-item.selected {
    background: rgba(2, 132, 199, 0.04) !important;
    border-color: #0284C7 !important;
    box-shadow: 0 4px 16px rgba(2, 132, 199, 0.1) !important;
  }
  html.dark .sp-flow-item {
    background: rgba(255, 255, 255, 0.04) !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
  }
  html.dark .sp-flow-item.selected {
    background: rgba(56, 189, 248, 0.08) !important;
    border-color: #38BDF8 !important;
  }
  .sp-flow-item-head {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-bottom: 8px !important;
  }
  .sp-flow-item-title {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
  }
  .sp-flow-item-title h4 {
    margin: 0 !important;
    font-size: 0.98rem !important;
    font-weight: 800 !important;
    color: var(--sp-text) !important;
  }
  .sp-flow-item-badge {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    padding: 3px 8px !important;
    border-radius: 999px !important;
  }
  .badge-recommended {
    background: rgba(2, 132, 199, 0.12) !important;
    color: #0284C7 !important;
    border: 1px solid rgba(2, 132, 199, 0.25) !important;
  }
  .badge-classic {
    background: rgba(100, 116, 139, 0.12) !important;
    color: #64748B !important;
    border: 1px solid rgba(100, 116, 139, 0.2) !important;
  }
  .sp-flow-radio-circle {
    width: 20px !important;
    height: 20px !important;
    border-radius: 50% !important;
    border: 2px solid #CBD5E1 !important;
    background: #FFFFFF !important;
    position: relative !important;
    flex-shrink: 0 !important;
    transition: all 0.2s ease !important;
  }
  html.dark .sp-flow-radio-circle {
    background: #1E293B !important;
    border-color: #475569 !important;
  }
  .sp-flow-item.selected .sp-flow-radio-circle {
    border-color: #0284C7 !important;
    background: #0284C7 !important;
    box-shadow: inset 0 0 0 3px #FFFFFF !important;
  }
  html.dark .sp-flow-item.selected .sp-flow-radio-circle {
    box-shadow: inset 0 0 0 3px #1E293B !important;
  }
  .sp-flow-item-desc {
    margin: 0 0 10px 0 !important;
    font-size: 0.84rem !important;
    line-height: 1.5 !important;
    color: var(--sp-text-sub) !important;
  }
  .sp-flow-roadmap {
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    flex-wrap: wrap !important;
  }
  .sp-flow-chip {
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    padding: 4px 9px !important;
    border-radius: 8px !important;
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    color: #334155 !important;
  }
  html.dark .sp-flow-chip {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.12) !important;
    color: #E2E8F0 !important;
  }
  .sp-flow-arrow {
    color: #94A3B8 !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
  }
"""

content = content.replace('</style>', refinement_css + '\n  </style>')

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated piano-studio.html with modal refinements successfully.")

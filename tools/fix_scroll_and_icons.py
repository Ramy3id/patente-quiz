import sys
sys.stdout.reconfigure(encoding='utf-8')

target_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Question 4 HTML with clean expressive icon cards
old_q4_start = """      <!-- السؤال 4: مسار وتدفق ترتيب الأبواب -->
      <div class="sp-question-block">
        <div class="sp-q-label">
          <span>4. منهجية ترتيب تدفق الأبواب:</span>
          <span class="sp-q-helper">طريقة تسلسل الدروس</span>
        </div>"""

old_q4_end = """      <!-- شريط الإجراءات النهائي: حفظ وإلغاء الخطة -->"""

new_q4_html = """      <!-- السؤال 4: منهجية تدفق وترتيب الأبواب (تصميم مدمج بالأيقونات) -->
      <div class="sp-question-block">
        <div class="sp-q-label">
          <span>4. منهجية تدفق وترتيب الأبواب:</span>
          <span class="sp-q-helper">اختر نمط دراسة المنهج</span>
        </div>
        <div class="sp-flow-clean-grid">
          <!-- المسار العنقودي الذكي -->
          <div class="sp-opt-card sp-flow-icon-card selected" id="optFlowCluster" onclick="selectFlowMode('cluster')">
            <div class="sp-flow-ico-box">🧠</div>
            <div class="sp-flow-info-col">
              <div class="sp-flow-title-row">
                <span class="sp-flow-name">المسار العنقودي الذكي</span>
                <span class="sp-flow-micro-tag" title="الأعلى فاعلية">⚡ موصى به</span>
              </div>
              <div class="sp-flow-sub-row">
                يبدأ بالأبواب الأسهل وأعلى درجات لكسر الملل وسرعة الإنجاز وتثبيت القواعد مبكراً.
              </div>
            </div>
            <div class="sp-flow-radio-circle"></div>
          </div>

          <!-- المسار التسلسلي التقليدي -->
          <div class="sp-opt-card sp-flow-icon-card" id="optFlowSequential" onclick="selectFlowMode('sequential')">
            <div class="sp-flow-ico-box">📖</div>
            <div class="sp-flow-info-col">
              <div class="sp-flow-title-row">
                <span class="sp-flow-name">المسار التسلسلي التقليدي</span>
                <span class="sp-flow-micro-tag-classic">🔢 ترتيب 1 - 25</span>
              </div>
              <div class="sp-flow-sub-row">
                دراسة الأبواب بالتتابع الرقمي من الباب 01 حتى الباب 25 بالتسلسل المعتاد لكتاب المدرسة.
              </div>
            </div>
            <div class="sp-flow-radio-circle"></div>
          </div>
        </div>
      </div>\n\n"""

if old_q4_start in content and old_q4_end in content:
    start_pos = content.find(old_q4_start)
    end_pos = content.find(old_q4_end)
    content = content[:start_pos] + new_q4_html + content[end_pos:]
    print("Replaced Question 4 with sleek expressive icon cards.")
else:
    print("Error: Q4 markers not found.")

# 2. Update JavaScript modal functions to lock body scroll
old_modal_js = """    function openPlanSetupModal() {
      document.getElementById("planSetupModal").classList.add("open");
    }
    function closePlanSetupModal() {
      document.getElementById("planSetupModal").classList.remove("open");
    }

    function openRebalanceModal() {
      document.getElementById("rebalanceModal").classList.add("open");
    }
    function closeRebalanceModal() {
      document.getElementById("rebalanceModal").classList.remove("open");
    }"""

new_modal_js = """    function openPlanSetupModal() {
      const m = document.getElementById("planSetupModal");
      if (m) m.classList.add("open");
      document.documentElement.classList.add("sp-modal-locked");
      document.body.classList.add("sp-modal-locked");
    }
    function closePlanSetupModal() {
      const m = document.getElementById("planSetupModal");
      if (m) m.classList.remove("open");
      document.documentElement.classList.remove("sp-modal-locked");
      document.body.classList.remove("sp-modal-locked");
    }

    function openRebalanceModal() {
      const m = document.getElementById("rebalanceModal");
      if (m) m.classList.add("open");
      document.documentElement.classList.add("sp-modal-locked");
      document.body.classList.add("sp-modal-locked");
    }
    function closeRebalanceModal() {
      const m = document.getElementById("rebalanceModal");
      if (m) m.classList.remove("open");
      document.documentElement.classList.remove("sp-modal-locked");
      document.body.classList.remove("sp-modal-locked");
    }"""

if old_modal_js in content:
    content = content.replace(old_modal_js, new_modal_js)
    print("Updated open/close modal JS with scroll locking.")
else:
    print("Warning: old_modal_js not found verbatim.")

# 3. Add CSS for overscroll contain, body scroll lock, and Question 4 icon cards
new_fixes_css = """
  /* ==========================================================================
     BODY SCROLL LOCK & QUESTION 4 COMPACT ICON CARDS
     ========================================================================== */
  
  /* Prevent scroll chaining & lock background page completely */
  .sp-modal-backdrop {
    overscroll-behavior: contain !important;
  }
  html.sp-modal-locked,
  body.sp-modal-locked {
    overflow: hidden !important;
    height: 100vh !important;
    max-height: 100vh !important;
  }
  body.sp-modal-locked #patenteScrollTopBtn {
    display: none !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }

  /* Question 4: Expressive Icon Cards */
  .sp-flow-clean-grid {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
  }
  .sp-flow-icon-card {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 14px 16px !important;
    border-radius: 16px !important;
    border: 1.5px solid #E2E8F0 !important;
    background: #F8FAFC !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
  }
  html.light .sp-flow-icon-card.selected {
    background: rgba(2, 132, 199, 0.05) !important;
    border-color: #0284C7 !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.12) !important;
  }
  html.dark .sp-flow-icon-card {
    background: rgba(255, 255, 255, 0.04) !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
  }
  html.dark .sp-flow-icon-card.selected {
    background: rgba(56, 189, 248, 0.08) !important;
    border-color: #38BDF8 !important;
  }
  .sp-flow-ico-box {
    width: 44px !important;
    height: 44px !important;
    border-radius: 12px !important;
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    font-size: 1.4rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
  }
  html.dark .sp-flow-ico-box {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.1) !important;
  }
  .sp-flow-info-col {
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
    min-width: 0 !important;
    text-align: right !important;
  }
  .sp-flow-title-row {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
  }
  .sp-flow-name {
    font-size: 0.96rem !important;
    font-weight: 800 !important;
    color: var(--sp-text) !important;
  }
  .sp-flow-micro-tag {
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    padding: 2px 8px !important;
    border-radius: 999px !important;
    background: rgba(2, 132, 199, 0.12) !important;
    color: #0284C7 !important;
  }
  .sp-flow-micro-tag-classic {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    padding: 2px 8px !important;
    border-radius: 999px !important;
    background: rgba(100, 116, 139, 0.12) !important;
    color: #64748B !important;
  }
  .sp-flow-sub-row {
    font-size: 0.78rem !important;
    line-height: 1.4 !important;
    color: var(--sp-text-sub) !important;
  }
"""

content = content.replace('</style>', new_fixes_css + '\n  </style>')

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated piano-studio.html successfully with scroll lock and icon cards.")

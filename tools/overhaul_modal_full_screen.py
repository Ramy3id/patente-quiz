import sys
sys.stdout.reconfigure(encoding='utf-8')

target_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the top section of planSetupModal
old_top_target = """  <!-- النافذة المنبثقة: استبيان إعداد وتخصيص الخطة -->
  <div class="sp-modal-backdrop" id="planSetupModal">
    <div class="sp-modal-box">
      <div class="sp-modal-title">
        <span>⚙️</span>
        <span>تخصيص خطتك الدراسية الذكية</span>
      </div>
      <p class="sp-modal-desc">
        حدد وقتك وظروفك لنقوم بضبط المعادلة وتوزيع الأبواب الـ 25 كاملة والامتحانات الوزارية بطريقة علمية متوازنة.
      </p>

      <!-- زر التخطي الفوري القياسي -->
      <div class="sp-quickstart-banner">
        <div style="font-size: 0.95rem; font-weight: 800; color: var(--sp-emerald); margin-bottom: 6px;">
          🚀 لست متأكداً أو تريد البدء فوراً؟
        </div>
        <div style="font-size: 0.82rem; color: var(--sp-text-sub); margin-bottom: 12px;">
          ابدأ بالمسار العنقودي الذكي الموصى به (30 يوماً - ساعتان) بنقرة واحدة دون ملء أي خانات.
        </div>
        <button class="sp-btn sp-btn-emerald" style="width: 100%; justify-content: center;" onclick="applyStandardPlanAndStart()">
          <span>⚡ ابدأ بالخطة الموصى بها فوراً</span>
        </button>
      </div>"""

new_top_replacement = """  <!-- النافذة المنبثقة: استبيان إعداد وتخصيص الخطة (شاشة كاملة عصرية) -->
  <div class="sp-modal-backdrop" id="planSetupModal">
    <div class="sp-modal-box">
      <!-- الهيدر الاحترافي الفاخر لإعداد الخطة -->
      <div class="sp-setup-hero-card">
        <div class="sp-setup-hero-badge">
          <span>🎯 التخصيص العلمي الذكي</span>
          <span class="sp-setup-dot"></span>
          <span>منهج 2026 المعتمد</span>
        </div>
        <h2 class="sp-setup-hero-title">تخصيص خطتك الدراسية للامتحان</h2>
        <p class="sp-setup-hero-desc">
          أجب عن الأسئلة البسيطة التالية لنقوم بضبط المعادلة وتوزيع الأبواب الـ 25 كاملة ومحطات الكلمات والامتحانات الوزارية وفق وتيرتك.
        </p>

        <!-- كارت الانطلاق السريع الموصى به -->
        <div class="sp-setup-fasttrack">
          <div class="sp-fasttrack-info">
            <div class="sp-fasttrack-icon">⚡</div>
            <div>
              <div class="sp-fasttrack-heading">تريد البدء الفوري الموصى به؟</div>
              <div class="sp-fasttrack-sub">المسار العنقودي القياسي (30 يوماً • ساعتان يومياً) بنقرة واحدة.</div>
            </div>
          </div>
          <button class="sp-fasttrack-btn" onclick="applyStandardPlanAndStart()">
            <span>انطلق بالخطة الموصى بها</span>
            <span>←</span>
          </button>
        </div>
      </div>"""

if old_top_target in content:
    content = content.replace(old_top_target, new_top_replacement)
    print("Replaced top hero banner with ultra-professional bento card.")
else:
    print("Warning: old_top_target not found verbatim.")

# 2. Replace the bottom buttons of planSetupModal
old_bottom_target = """      <!-- أزرار حفظ وإغلاق المودال -->
      <div style="display: flex; gap: 12px; margin-top: 22px;">
        <button class="sp-btn sp-btn-primary" style="flex: 1; justify-content: center;" onclick="saveCustomPlan()">
          <span>💾 حفظ وتوليد الخطة</span>
        </button>
        <button class="sp-btn sp-btn-outline" onclick="closePlanSetupModal()">إلغاء</button>
      </div>"""

new_bottom_replacement = """      <!-- شريط الإجراءات النهائي: حفظ وإلغاء الخطة -->
      <div class="sp-modal-actions-bar">
        <button class="sp-btn sp-btn-primary sp-btn-save-plan" onclick="saveCustomPlan()">
          <span>💾 حفظ وتوليد الخطة الذكية</span>
        </button>
        <button class="sp-btn sp-btn-outline sp-btn-cancel-plan" onclick="closePlanSetupModal()">
          <span>إلغاء</span>
        </button>
      </div>"""

if old_bottom_target in content:
    content = content.replace(old_bottom_target, new_bottom_replacement)
    print("Replaced bottom buttons with floating elevated action bar.")
else:
    print("Warning: old_bottom_target not found verbatim.")

# 3. Add full-width styling, pinned header, and safe bottom dock clearance
full_screen_css = """
  /* ==========================================================================
     FULL-SCREEN MOBILE SETUP & PINNED HEADER (NO GAPS / NO SIDE BACKDROP)
     ========================================================================== */
  
  /* Ensure Global Portal Nav stays pinned at top permanently */
  #globalPortalNav {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    z-index: 10000 !important;
  }

  /* Full-width edge-to-edge modal on mobile */
  @media (max-width: 768px) {
    .sp-modal-backdrop#planSetupModal {
      position: fixed !important;
      inset: 0 !important;
      width: 100% !important;
      max-width: 100% !important;
      height: 100% !important;
      min-height: 100% !important;
      padding: 0 !important;
      margin: 0 !important;
      background: #F8FAFC !important;
      z-index: 5000 !important;
      overflow-y: auto !important;
      -webkit-overflow-scrolling: touch !important;
      scrollbar-width: none !important;
      -ms-overflow-style: none !important;
    }
    html.light .sp-modal-backdrop#planSetupModal {
      background: #F8FAFC !important;
    }
    html.dark .sp-modal-backdrop#planSetupModal {
      background: #0B0F19 !important;
    }
    .sp-modal-backdrop#planSetupModal::-webkit-scrollbar {
      display: none !important;
      width: 0 !important;
      height: 0 !important;
    }
    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      width: 100% !important;
      max-width: 100% !important;
      min-height: 100% !important;
      margin: 0 !important;
      padding: 72px 14px 150px 14px !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      background: transparent !important;
      overflow: visible !important;
    }
  }

  /* Setup Hero Card Refinements */
  .sp-setup-hero-card {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 18px !important;
    padding: 18px !important;
    margin-bottom: 18px !important;
    box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.04) !important;
  }
  html.dark .sp-setup-hero-card {
    background: rgba(255, 255, 255, 0.04) !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
  }
  .sp-setup-hero-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 4px 12px !important;
    border-radius: 999px !important;
    background: rgba(2, 132, 199, 0.08) !important;
    color: #0284C7 !important;
    font-size: 0.76rem !important;
    font-weight: 800 !important;
    margin-bottom: 10px !important;
  }
  .sp-setup-dot {
    width: 4px !important;
    height: 4px !important;
    border-radius: 50% !important;
    background: #0284C7 !important;
  }
  .sp-setup-hero-title {
    font-size: 1.35rem !important;
    font-weight: 900 !important;
    color: var(--sp-text) !important;
    margin: 0 0 6px 0 !important;
    line-height: 1.3 !important;
  }
  .sp-setup-hero-desc {
    font-size: 0.85rem !important;
    line-height: 1.55 !important;
    color: var(--sp-text-sub) !important;
    margin: 0 0 14px 0 !important;
  }
  .sp-setup-fasttrack {
    background: rgba(5, 150, 105, 0.06) !important;
    border: 1px solid rgba(5, 150, 105, 0.22) !important;
    border-radius: 14px !important;
    padding: 12px 14px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
  }
  @media (min-width: 641px) {
    .sp-setup-fasttrack {
      flex-direction: row !important;
      align-items: center !important;
      justify-content: space-between !important;
    }
  }
  .sp-fasttrack-info {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
  }
  .sp-fasttrack-icon {
    font-size: 1.3rem !important;
    width: 36px !important;
    height: 36px !important;
    border-radius: 10px !important;
    background: rgba(5, 150, 105, 0.15) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
  }
  .sp-fasttrack-heading {
    font-size: 0.86rem !important;
    font-weight: 800 !important;
    color: #059669 !important;
    margin-bottom: 2px !important;
  }
  .sp-fasttrack-sub {
    font-size: 0.75rem !important;
    color: var(--sp-text-sub) !important;
  }
  .sp-fasttrack-btn {
    min-height: 42px !important;
    padding: 8px 16px !important;
    border-radius: 10px !important;
    background: #059669 !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 0.84rem !important;
    border: none !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    transition: all 0.15s ease !important;
  }
  .sp-fasttrack-btn:hover {
    background: #047857 !important;
  }

  /* Bottom Actions Bar on Mobile (Floating Above Bottom Navigation Dock) */
  .sp-modal-actions-bar {
    display: flex !important;
    gap: 10px !important;
    margin-top: 24px !important;
  }
  @media (max-width: 768px) {
    .sp-modal-actions-bar {
      position: fixed !important;
      bottom: 56px !important; /* right above the 56px native bottom dock */
      left: 0 !important;
      right: 0 !important;
      width: 100% !important;
      background: rgba(255, 255, 255, 0.96) !important;
      backdrop-filter: blur(16px) !important;
      -webkit-backdrop-filter: blur(16px) !important;
      border-top: 1px solid #E2E8F0 !important;
      padding: 10px 14px !important;
      z-index: 6000 !important;
      box-shadow: 0 -4px 20px rgba(15, 23, 42, 0.08) !important;
      margin: 0 !important;
    }
    html.dark .sp-modal-actions-bar {
      background: rgba(11, 15, 25, 0.96) !important;
      border-top-color: rgba(255, 255, 255, 0.1) !important;
      box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.4) !important;
    }
  }
  .sp-btn-save-plan {
    flex: 2 !important;
    min-height: 48px !important;
    font-size: 0.92rem !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    justify-content: center !important;
    background: linear-gradient(135deg, #0284C7, #0369A1) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25) !important;
    border: none !important;
  }
  .sp-btn-cancel-plan {
    flex: 1 !important;
    min-height: 48px !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    justify-content: center !important;
  }
"""

content = content.replace('</style>', full_screen_css + '\n  </style>')

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated piano-studio.html with full-width screen overhaul.")

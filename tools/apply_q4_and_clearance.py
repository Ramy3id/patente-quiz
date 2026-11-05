import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace Q4 HTML
old_q4_start = '<!-- السؤال 4: منهجية تدفق وترتيب الأبواب (تصميم مدمج بالأيقونات) -->'
old_q4_end = '<!-- شريط الإجراءات النهائي: حفظ وإلغاء الخطة -->'

new_q4_html = '''<!-- السؤال 4: منهجية تدفق وترتيب الأبواب (تصميم أنيق ومريح) -->
      <div class="sp-question-block">
        <div class="sp-q-label">
          <span>4. منهجية تدفق وترتيب الأبواب:</span>
          <span class="sp-q-helper">اختر نمط دراسة المنهج</span>
        </div>
        <div class="sp-options-flow">
          <!-- المسار العنقودي الذكي -->
          <div class="sp-opt-card selected" id="optFlowCluster" onclick="selectFlowMode('cluster')">
            <div class="sp-opt-title" style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
              <span style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 0.96rem;">🧠 المسار العنقودي الذكي ⭐</span>
              <span class="sp-flow-tag" style="font-size: 0.76rem; font-weight: 700; color: #0284c7; background: rgba(2, 132, 199, 0.12); padding: 4px 10px; border-radius: 6px; white-space: nowrap;">⚡ موصى به</span>
            </div>
            <div class="sp-opt-note" style="margin-top: 6px; font-size: 0.84rem; line-height: 1.5; color: var(--sp-text-muted);">
              يبدأ بالأبواب الأسهل وأعلى درجات لكسر الملل وسرعة الإنجاز وتثبيت القواعد مبكراً.
            </div>
          </div>

          <!-- المسار التسلسلي التقليدي -->
          <div class="sp-opt-card" id="optFlowSequential" onclick="selectFlowMode('sequential')">
            <div class="sp-opt-title" style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
              <span style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 0.96rem;">📖 المسار التسلسلي التقليدي</span>
              <span class="sp-flow-tag" style="font-size: 0.76rem; font-weight: 700; color: #64748b; background: rgba(100, 116, 139, 0.12); padding: 4px 10px; border-radius: 6px; white-space: nowrap;">🔢 ترتيب 1 - 25</span>
            </div>
            <div class="sp-opt-note" style="margin-top: 6px; font-size: 0.84rem; line-height: 1.5; color: var(--sp-text-muted);">
              دراسة الأبواب بالتتابع الرقمي من الباب 01 حتى الباب 25 بالتسلسل المعتاد لكتاب المدرسة.
            </div>
          </div>
        </div>
      </div>

      '''

idx_start = content.find(old_q4_start)
idx_end = content.find(old_q4_end)
if idx_start != -1 and idx_end != -1:
    content = content[:idx_start] + new_q4_html + content[idx_end:]
    print("Replaced Q4 HTML successfully.")
else:
    print("ERROR: could not find Q4 boundaries in content!")
    sys.exit(1)

# 2. Update CSS for .sp-options-flow and reduce bottom clearance
# Find the media query for mobile
old_padding_snippet = '''@media (max-width: 768px) {
    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding: 72px 14px 180px 14px !important;
    }
    .sp-modal-actions-bar {
      margin-top: 30px !important;
      margin-bottom: 120px !important;
    }
  }'''

new_padding_snippet = '''@media (max-width: 768px) {
    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding: 68px 14px 24px 14px !important;
    }
    .sp-modal-actions-bar {
      margin-top: 20px !important;
      margin-bottom: 24px !important;
    }
  }
  .sp-options-flow {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    width: 100% !important;
  }
  .sp-options-flow .sp-opt-card {
    width: 100% !important;
    box-sizing: border-box !important;
    text-align: right !important;
    padding: 14px 16px !important;
    border-radius: 14px !important;
    cursor: pointer !important;
  }'''

if old_padding_snippet in content:
    content = content.replace(old_padding_snippet, new_padding_snippet, 1)
    print("Updated bottom clearance and added .sp-options-flow CSS.")
else:
    print("WARNING: old_padding_snippet not found, searching with regex/variation")
    # Let's inspect where 180px is
    idx_p = content.find('180px')
    if idx_p != -1:
        print("Found 180px at:", content[idx_p-50:idx_p+100])

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated piano-studio.html successfully.")

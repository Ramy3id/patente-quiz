import re

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Replace the entire Motorizzazione CSS block
start_marker = "/* ========================================================="
start_sub = "2. شاشة كمبيوتر المرور الإيطالي الرسمي"
end_marker = "/* Mobile-Optimized 1-Line Question Pill Scroll"

start_idx = c.find(start_sub)
if start_idx != -1:
    # backtrack to find start of comment
    comment_start = c.rfind("/*", 0, start_idx)
    end_idx = c.find(end_marker, start_idx)
    if comment_start != -1 and end_idx != -1:
        new_moto_css = '''/* =========================================================
       2. شاشة كمبيوتر المرور الإيطالي الرسمي (Motorizzazione Touch Screen Skin)
       ========================================================= */
    .motorizzazione-screen-wrap {
      display: none;
      background: #1C2430;
      border: 3px solid #334155;
      border-radius: 16px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
      overflow: hidden;
      direction: ltr;
    }
    .skin-moto .motorizzazione-screen-wrap { display: block; }
    .skin-moto .modern-screen-wrap { display: none; }

    .moto-top-header {
      background: #0F172A;
      border-bottom: 2px solid #38BDF8;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #FFFFFF;
    }
    .moto-flag-brand {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .moto-flag-tricolore {
      width: 28px;
      height: 18px;
      display: flex;
      border-radius: 3px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .flag-green { width: 33.33%; background: #009246; }
    .flag-white { width: 33.33%; background: #FFFFFF; }
    .flag-red { width: 33.33%; background: #CE2B37; }
    .moto-titles-text strong {
      display: block;
      font-size: 0.8rem;
      letter-spacing: 0.02em;
    }
    .moto-titles-text span {
      font-size: 0.68rem;
      color: #94A3B8;
    }
    .moto-header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .btn-moto-switch-modern {
      background: linear-gradient(135deg, #0284C7, #0369A1);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #FFFFFF;
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-family: inherit;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35);
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    .btn-moto-switch-modern:hover {
      transform: translateY(-1px);
    }
    .btn-moto-switch-modern:active {
      transform: scale(0.96);
    }
    .moto-timer-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.05rem;
      font-weight: 900;
      color: #38BDF8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 4px 10px;
      border-radius: 6px;
      white-space: nowrap;
    }
    .moto-timer-badge.warning {
      color: #EF4444;
      background: rgba(239, 68, 68, 0.15);
      border-color: #EF4444;
    }

    .moto-main-terminal {
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      background: #18202C;
    }
    .moto-sign-panel {
      background: #FFFFFF;
      border: 2px solid #475569;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 4px;
      height: 90px;
      min-height: 90px;
      max-height: 90px;
      box-sizing: border-box;
    }
    .moto-sign-img {
      max-width: 100%;
      max-height: 80px;
      object-fit: contain;
    }
    .moto-no-sign-official {
      color: #64748B;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.76rem;
      font-weight: 700;
      text-align: center;
      background: #F8FAFC;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      letter-spacing: 0.03em;
    }
    .moto-question-panel {
      display: flex;
      flex-direction: column;
    }
    .moto-q-meta-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .moto-q-num-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.84rem;
      font-weight: 900;
      color: #F8FAFC;
      background: #334155;
      padding: 3px 8px;
      border-radius: 6px;
    }
    .btn-moto-flag {
      padding: 3px 10px;
      border-radius: 6px;
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid #F59E0B;
      color: #FBBF24;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.76rem;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }
    .btn-moto-flag.active {
      background: #F59E0B;
      color: #0F172A;
      box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
    }
    .moto-text-italian {
      height: 85px;
      min-height: 85px;
      max-height: 85px;
      overflow-y: auto;
      font-size: 1.05rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.35;
      margin-bottom: 8px;
      direction: ltr;
      text-align: left;
      scrollbar-width: thin;
      padding: 2px 4px;
      box-sizing: border-box;
    }
    .moto-arabic-helper {
      display: none !important; /* امتحان رسمي إيطالي 100% بدون أي مساعدة ترجمة */
    }

    /* زري اللمس الوزاريين العملاقين */
    .moto-touch-buttons-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 4px;
    }
    .btn-moto-touch {
      height: 52px;
      min-height: 52px;
      max-height: 52px;
      border-radius: 10px;
      border: 2px solid transparent;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      font-family: 'JetBrains Mono', sans-serif;
      font-size: 1.35rem;
      font-weight: 900;
      transition: all 0.12s ease;
      color: #FFFFFF;
    }
    .btn-moto-touch.v {
      background: #0284C7;
      border-color: #38BDF8;
    }
    .btn-moto-touch.v:hover, .btn-moto-touch.v.selected {
      background: #0369A1;
      border-color: #FFFFFF;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.6);
      transform: scale(0.98);
    }
    .btn-moto-touch.f {
      background: #DC2626;
      border-color: #F87171;
    }
    .btn-moto-touch.f:hover, .btn-moto-touch.f.selected {
      background: #B91C1C;
      border-color: #FFFFFF;
      box-shadow: 0 0 16px rgba(239, 68, 68, 0.6);
      transform: scale(0.98);
    }

    /* لوحة التحكم السفلية وشبكة الـ 30 سؤالاً في الموتوريزاسيون */
    .moto-bottom-controls {
      background: #0F172A;
      border-top: 2px solid #334155;
      padding: 8px 12px;
    }
    .moto-nav-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .btn-moto-step {
      padding: 6px 14px;
      height: 36px;
      border-radius: 6px;
      background: #334155;
      border: 1px solid #475569;
      color: #FFFFFF;
      font-weight: 800;
      font-size: 0.78rem;
      cursor: pointer;
      font-family: 'JetBrains Mono', monospace;
      transition: all 0.15s ease;
    }
    .btn-moto-step:hover:not(:disabled) {
      background: #475569;
      border-color: #38BDF8;
    }
    .btn-moto-step:disabled { opacity: 0.35; cursor: not-allowed; }

    .moto-matrix-grid {
      display: grid;
      grid-template-columns: repeat(10, 1fr);
      gap: 3px;
      margin-bottom: 6px;
    }
    .moto-cell {
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      background: #1E293B;
      border: 1px solid #334155;
      color: #94A3B8;
      font-size: 0.72rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      cursor: pointer;
      transition: all 0.1s ease;
    }
    .moto-cell.active {
      border-color: #38BDF8;
      background: #0F172A;
      color: #38BDF8;
      box-shadow: 0 0 6px rgba(56, 189, 248, 0.5);
    }
    .moto-cell.v { background: #0284C7; color: #FFFFFF; border-color: #38BDF8; }
    .moto-cell.f { background: #DC2626; color: #FFFFFF; border-color: #F87171; }
    .moto-cell.flagged { border: 1.5px solid #F59E0B; }

    .btn-moto-conclude {
      height: 38px;
      width: 100%;
      border-radius: 8px;
      background: linear-gradient(135deg, #DC2626, #B91C1C);
      border: none;
      color: #FFFFFF;
      font-size: 0.8rem;
      font-weight: 900;
      font-family: 'JetBrains Mono', monospace;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
      transition: all 0.15s ease;
    }
    .btn-moto-conclude:active { transform: scale(0.97); }

    '''
        c = c[:comment_start] + new_moto_css + c[end_idx:]
        print('Motorizzazione CSS replaced cleanly.')

# 2. Add showArabicTr variable and update renderActiveQuestion
old_render_part = '''            <!-- حاوية نصوص السؤال ذات الارتفاع المتناسق -->
            <div class="exam-text-container">
              <div class="exam-text-it">${q.domanda}</div>
              <div class="exam-text-tr">${q.traduzione || 'سؤال وزاري مباشر.'}</div>
            </div>'''

new_render_part = '''            <!-- حاوية نصوص السؤال ذات الارتفاع المتناسق -->
            <div class="exam-text-container">
              <div class="exam-text-it">${q.domanda}</div>
              <div class="exam-tr-wrapper">
                <button type="button" class="btn-toggle-tr ${showArabicTr ? 'active' : ''}" id="btnToggleTr">
                  <span>${showArabicTr ? '✕ إخفاء الترجمة' : '🌐 الترجمة العربية'}</span>
                </button>
                <div class="exam-text-tr" id="examArabicText" style="display:${showArabicTr ? 'block' : 'none'};">
                  ${q.traduzione || 'سؤال وزاري مباشر.'}
                </div>
              </div>
            </div>'''

if old_render_part in c:
    c = c.replace(old_render_part, new_render_part)
    print('Render part for Arabic translation toggle replaced.')
else:
    print('old_render_part not found.')

# 3. Add event listener for btnToggleTr and declare showArabicTr
if 'let showArabicTr = false;' not in c:
    c = c.replace("const flaggedQuestions = new Set();", "const flaggedQuestions = new Set();\n      let showArabicTr = false;")
    print('Declared showArabicTr variable.')

old_listeners = '''          document.getElementById("btnModernFlag").addEventListener("click", () => toggleFlag(q.id));
        }'''

new_listeners = '''          document.getElementById("btnModernFlag").addEventListener("click", () => toggleFlag(q.id));
          document.getElementById("btnToggleTr")?.addEventListener("click", () => {
            showArabicTr = !showArabicTr;
            const trBox = document.getElementById("examArabicText");
            const trBtn = document.getElementById("btnToggleTr");
            if (trBox && trBtn) {
              trBox.style.display = showArabicTr ? "block" : "none";
              trBtn.classList.toggle("active", showArabicTr);
              trBtn.innerHTML = `<span>${showArabicTr ? "✕ إخفاء الترجمة" : "🌐 الترجمة العربية"}</span>`;
            }
          });
        }'''

if old_listeners in c:
    c = c.replace(old_listeners, new_listeners)
    print('btnToggleTr listener added.')
else:
    print('old_listeners not found.')

# 4. Update Motorizzazione update in renderActiveQuestion
old_moto_update = '''        // 2. تحديث واجهة كمبيوتر الموتوريزاسيون
        const motoBox = document.getElementById("motoSignBox");
        const motoImg = document.getElementById("motoSignImg");
        const motoText = document.getElementById("motoQuestionText");
        const motoTr = document.getElementById("motoQuestionTr");
        const motoBadge = document.getElementById("motoQuestionBadge");
        const motoFlagBtn = document.getElementById("btnMotoFlag");
        const motoV = document.getElementById("btnMotoVero");
        const motoF = document.getElementById("btnMotoFalso");

        if (motoBadge) motoBadge.textContent = `DOMANDA N. ${exam.currentIndex + 1} DI 30`;
        if (motoText) motoText.textContent = q.domanda;
        if (motoTr) motoTr.textContent = q.traduzione || '';

        if (motoBox && motoImg) {
          if (imgPath) {
            motoImg.src = imgPath;
            motoBox.style.display = 'flex';
          } else {
            motoBox.style.display = 'none';
          }
        }'''

new_moto_update = '''        // 2. تحديث واجهة كمبيوتر الموتوريزاسيون (Official Motorizzazione)
        const motoBox = document.getElementById("motoSignBox");
        const motoImg = document.getElementById("motoSignImg");
        const motoNoSign = document.getElementById("motoNoSignPlaceholder");
        const motoText = document.getElementById("motoQuestionText");
        const motoBadge = document.getElementById("motoQuestionBadge");
        const motoFlagBtn = document.getElementById("btnMotoFlag");
        const motoV = document.getElementById("btnMotoVero");
        const motoF = document.getElementById("btnMotoFalso");

        if (motoBadge) motoBadge.textContent = `DOMANDA N. ${exam.currentIndex + 1} DI 30`;
        if (motoText) motoText.textContent = q.domanda;

        if (motoImg && motoNoSign) {
          if (imgPath) {
            motoImg.src = imgPath;
            motoImg.style.display = 'block';
            motoNoSign.style.display = 'none';
          } else {
            motoImg.src = '';
            motoImg.style.display = 'none';
            motoNoSign.style.display = 'flex';
          }
        }'''

if old_moto_update in c:
    c = c.replace(old_moto_update, new_moto_update)
    print('Motorizzazione update logic replaced.')
else:
    print('old_moto_update not found.')

# 5. Add btnMotoReturnModern listener
if "document.getElementById('btnMotoReturnModern')" not in c:
    c = c.replace("document.getElementById('btnSkinMoto').addEventListener('click', () => setSkin('motorizzazione'));",
                  "document.getElementById('btnSkinMoto').addEventListener('click', () => setSkin('motorizzazione'));\n      document.getElementById('btnMotoReturnModern')?.addEventListener('click', () => setSkin('modern'));")
    print('Added btnMotoReturnModern click handler.')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

print('All improvements applied successfully.')

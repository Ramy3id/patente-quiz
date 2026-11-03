file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. NEW CSS FOR COMPACT HUB, FIXED SLOTS & AUTO-ADVANCE
new_css = """
    /* =========================================================
       COMPACT EXAM CONTROL HUB (Single-Card Header Strip)
       ========================================================= */
    .exam-control-hub {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 8px 12px;
      margin-bottom: 12px;
      box-shadow: 0 6px 24px rgba(0, 0, 0, 0.35);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
    }
    html.light .exam-control-hub {
      background: #FFFFFF;
      border-color: rgba(15, 23, 42, 0.1);
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    }
    .hub-primary-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 8px;
    }
    .exam-skin-switcher-mini {
      display: inline-flex;
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 999px;
      padding: 2px;
    }
    html.light .exam-skin-switcher-mini {
      background: #F1F5F9;
      border-color: #E2E8F0;
    }
    .skin-btn-mini {
      border: none;
      background: transparent;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--text-secondary);
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    .skin-btn-mini.active {
      background: #0284C7;
      color: #FFFFFF;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35);
    }
    html.light .skin-btn-mini.active {
      background: #0284C7;
      color: #FFFFFF;
    }
    .hub-progress-badge {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--text-secondary);
      white-space: nowrap;
    }
    .hub-progress-badge strong {
      color: #38BDF8;
      font-size: 0.95rem;
      font-family: 'JetBrains Mono', monospace;
    }
    html.light .hub-progress-badge strong {
      color: #0284C7;
    }
    .exam-timer-box-mini {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.92rem;
      font-weight: 800;
      color: #F8FAFC;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 3px 8px;
      border-radius: 8px;
      white-space: nowrap;
    }
    html.light .exam-timer-box-mini {
      background: #E0F2FE;
      color: #0369A1;
      border-color: #BAE6FD;
    }
    .btn-quick-submit {
      border: none;
      background: linear-gradient(135deg, #10B981, #059669);
      color: #FFFFFF;
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 0.76rem;
      font-weight: 800;
      cursor: pointer;
      font-family: inherit;
      white-space: nowrap;
      transition: transform 0.15s ease;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    .btn-quick-submit:active { transform: scale(0.95); }

    /* =========================================================
       FIXED-SLOT QUESTION CARD (Zero Layout Shift)
       ========================================================= */
    .exam-question-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 16px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 384px;
      box-sizing: border-box;
      margin-bottom: 12px;
    }
    html.light .exam-question-card {
      background: #FFFFFF;
      border-color: rgba(15, 23, 42, 0.1);
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }
    .exam-q-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      padding-bottom: 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      height: 28px;
    }
    html.light .exam-q-header { border-bottom-color: rgba(15, 23, 42, 0.08); }
    .exam-q-badge {
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-cyan);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 2px 10px;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 800;
    }
    .btn-flag-review {
      background: transparent;
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: #FBBF24;
      padding: 3px 10px;
      border-radius: 8px;
      font-size: 0.76rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-family: inherit;
      transition: all 0.15s ease;
    }
    .btn-flag-review.active {
      background: rgba(245, 158, 11, 0.25);
      border-color: #F59E0B;
      color: #F59E0B;
    }

    /* Fixed Media Slot (120px) to prevent vertical bouncing */
    .exam-media-slot {
      height: 120px;
      max-height: 120px;
      min-height: 120px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 4px 0;
      overflow: hidden;
    }
    .exam-sign-frame {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      width: 100%;
    }
    .exam-sign-frame img {
      max-height: 112px;
      max-width: 140px;
      object-fit: contain;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: #FFFFFF;
      padding: 3px;
    }
    .exam-no-img-placeholder {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px dashed rgba(255, 255, 255, 0.14);
      color: #94A3B8;
      font-size: 0.8rem;
      font-weight: 600;
    }
    html.light .exam-no-img-placeholder {
      background: #F8FAFC;
      border-color: #E2E8F0;
      color: #64748B;
    }
    .no-img-icon {
      font-size: 1.15rem;
    }

    /* Fixed Height Question Text Zone */
    .exam-text-container {
      min-height: 84px;
      max-height: 98px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin: 4px 0 8px;
      text-align: center;
    }
    .exam-text-it {
      font-size: 1.12rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.45;
      margin: 0 0 4px;
      direction: ltr;
      text-align: center;
    }
    html.light .exam-text-it { color: #0F172A; }
    .exam-text-tr {
      font-size: 0.92rem;
      font-weight: 600;
      color: #CBD5E1;
      line-height: 1.45;
      direction: rtl;
      text-align: center;
      margin: 0;
    }
    html.light .exam-text-tr { color: #334155; }

    /* Choice Buttons: Fixed Thumb-Zone Height (52px) */
    .exam-choice-buttons {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin: 6px 0;
    }
    .choice-btn {
      height: 52px !important;
      min-height: 52px !important;
      max-height: 52px !important;
      padding: 0 12px !important;
      font-size: 1.1rem !important;
      font-weight: 800 !important;
      border-radius: 14px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 6px !important;
      cursor: pointer !important;
      transition: all 0.15s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    .choice-btn.selected {
      transform: scale(0.98);
      filter: brightness(1.15);
    }

    /* Navigation Steps Bar */
    .exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
      height: 38px;
    }
    .btn-nav-step {
      height: 38px !important;
      min-height: 38px !important;
      max-height: 38px !important;
      font-size: 0.85rem !important;
      padding: 0 12px !important;
      border-radius: 10px !important;
      background: rgba(255, 255, 255, 0.06) !important;
      border: 1px solid rgba(255, 255, 255, 0.1) !important;
      color: var(--text-secondary) !important;
      cursor: pointer !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    html.light .btn-nav-step {
      background: #F1F5F9 !important;
      border-color: #E2E8F0 !important;
      color: #334155 !important;
    }
    .btn-nav-step:disabled {
      opacity: 0.35 !important;
      cursor: not-allowed !important;
    }
    .btn-submit-pill {
      height: 38px !important;
      padding: 0 14px !important;
      border-radius: 10px !important;
      background: linear-gradient(135deg, #10B981, #059669) !important;
      border: none !important;
      color: #FFFFFF !important;
      font-weight: 800 !important;
      font-size: 0.84rem !important;
      cursor: pointer !important;
      white-space: nowrap !important;
      box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3) !important;
      font-family: inherit !important;
    }
    .btn-submit-pill:active { transform: scale(0.95); }

    /* Auto-Advance Flash Animation */
    @keyframes autoAdvancePulse {
      0% { transform: scale(1); }
      50% { transform: scale(0.96); }
      100% { transform: scale(1); }
    }
    .btn-just-answered {
      animation: autoAdvancePulse 0.22s ease-out !important;
    }

    @media (max-width: 640px) {
      .exam-portal-container {
        padding: 4px 10px 8px !important;
        margin: 4px auto 10px !important;
      }
      .exam-nav-pills {
        display: flex !important;
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        padding: 4px 2px !important;
        gap: 5px !important;
        scrollbar-width: none !important;
        -webkit-overflow-scrolling: touch !important;
        margin-bottom: 0 !important;
      }
      .exam-nav-pills::-webkit-scrollbar { display: none !important; }
      .q-pill {
        min-width: 32px !important;
        width: 32px !important;
        height: 32px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
      }
      .btn-submit-exam {
        display: none !important; /* Replaced by the integrated submit buttons */
      }
    }
"""

# Insert new CSS before </style>
text = text.replace('</style>', new_css + '\n</style>')

# 2. REPLACE HTML MARKUP OF TOP CARDS WITH UNIFIED CONTROL HUB
old_html_strip = """    <!-- شريط التبديل بين الوضع العصري ومحاكاة شاشة كمبيوتر المرور -->
    <div class="exam-skin-switcher">
      <button class="skin-btn active" id="btnSkinModern">
        <span>🌟 الوضع العصري الفاخر</span>
      </button>
      <button class="skin-btn" id="btnSkinMoto">
        <span>🖥️ شاشة كمبيوتر المرور الرسمية (Motorizzazione)</span>
      </button>
    </div>

    <!-- =========================================================
         1. واجهة الوضع العصري (Modern Skin)
         ========================================================= -->
    <div class="modern-screen-wrap" id="modernScreenWrap">
      <div class="exam-top-bar">
        <div class="exam-timer-box" id="examTimerDisplay">⏱️ 20:00</div>
        <div style="font-weight:800; color:var(--text-secondary);">
          تمت الإجابة: <span id="answeredCounter" style="color:var(--accent-cyan);">0</span> / 30
        </div>
      </div>

      <!-- شبكة أرقام الأسئلة -->
      <div class="exam-nav-pills" id="examPillsGrid"></div>

      <!-- بطاقة السؤال النشط -->
      <div class="exam-question-card" id="questionCardStage">
        <div style="text-align:center; padding:40px; color:#94A3B8;">جاري إعداد بطاقة الامتحان الوزاري المعتمد...</div>
      </div>

      <!-- زر تسليم الامتحان النهائي -->
      <button type="button" class="btn-submit-exam" id="btnSubmitFinalExam">
        <span>📋 تسليم الامتحان النهائي وتصحيح النتيجة</span>
      </button>
    </div>"""

new_html_strip = """    <!-- =========================================================
         1. واجهة الوضع العصري (Modern Skin)
         ========================================================= -->
    <div class="modern-screen-wrap" id="modernScreenWrap">
      
      <!-- شريط التحكم العلوي المدمج (Unified Compact Control Hub) -->
      <div class="exam-control-hub">
        <div class="hub-primary-row">
          <!-- تبديل الوضع (Pill Switcher) -->
          <div class="exam-skin-switcher-mini">
            <button type="button" class="skin-btn-mini active" id="btnSkinModern" title="الوضع العصري الفاخر">
              <span>🌟 عصري</span>
            </button>
            <button type="button" class="skin-btn-mini" id="btnSkinMoto" title="شاشة كمبيوتر المرور">
              <span>🖥️ رسمي</span>
            </button>
          </div>

          <!-- عداد الإنجاز -->
          <div class="hub-progress-badge">
            <span>تمت:</span>
            <strong id="answeredCounter">0</strong>
            <span>/ 30</span>
          </div>

          <!-- المؤقت التنازلي -->
          <div class="exam-timer-box-mini" id="examTimerDisplay">⏱️ 20:00</div>

          <!-- زر التسليم السريع -->
          <button type="button" class="btn-quick-submit" id="btnQuickSubmit" title="تسليم بطاقة الامتحان وتصحيح النتيجة">
            <span>تسليم 📋</span>
          </button>
        </div>

        <!-- شريط أرقام الأسئلة الـ 30 الفوري -->
        <div class="exam-nav-pills" id="examPillsGrid"></div>
      </div>

      <!-- بطاقة السؤال النشط ذات الارتفاع الثابت (Zero Layout Shift Stage) -->
      <div class="exam-question-card" id="questionCardStage">
        <div style="text-align:center; padding:40px; color:#94A3B8;">جاري إعداد بطاقة الامتحان الوزاري المعتمد...</div>
      </div>

      <!-- زر تسليم احتياطي للشاشات الكبيرة -->
      <button type="button" class="btn-submit-exam" id="btnSubmitFinalExam" style="display:none;">
        <span>📋 تسليم الامتحان النهائي وتصحيح النتيجة</span>
      </button>
    </div>"""

if old_html_strip in text:
    text = text.replace(old_html_strip, new_html_strip)
    print("Replaced Top HTML successfully")
elif old_html_strip.replace('\n', '\r\n') in text:
    text = text.replace(old_html_strip.replace('\n', '\r\n'), new_html_strip.replace('\n', '\r\n'))
    print("Replaced Top HTML (CRLF) successfully")
else:
    print("Top HTML strip not found!")

# 3. UPDATE renderActiveQuestion & answerAndRefresh IN JAVASCRIPT
old_stage_render = """            <div class="exam-q-header">
              <span class="exam-q-badge">سؤال رقم ${exam.currentIndex + 1} من 30</span>
              <button class="btn-flag-review ${isFlag ? 'active' : ''}" id="btnModernFlag">
                <span>${isFlag ? '📌 تم التعليم للمراجعة' : '📌 علّم للمراجعة'}</span>
              </button>
            </div>

            ${imgPath ? `<div class="exam-img-frame"><img src="${imgPath}" alt="Segnale"></div>` : ""}

            <div class="exam-text-it">${q.domanda}</div>
            <div class="exam-text-tr">${q.traduzione || 'سؤال وزاري مباشر.'}</div>

            <div class="exam-choice-buttons">
              <button type="button" class="choice-btn choice-btn-vero ${currentAnswer === true ? 'selected' : ''}" id="btnVero">
                <span>VERO (صح) ✅</span>
              </button>
              <button type="button" class="choice-btn choice-btn-falso ${currentAnswer === false ? 'selected' : ''}" id="btnFalso">
                <span>FALSO (خطأ) ❌</span>
              </button>
            </div>

            <div class="exam-nav-steps">
              <button type="button" class="btn-nav-step" id="btnPrev" ${exam.currentIndex === 0 ? 'disabled' : ''}>السابق ➡</button>
              <span class="exam-nav-hint">التنقل السريع من شريط الأرقام</span>
              <button type="button" class="btn-nav-step" id="btnNext" ${exam.currentIndex === exam.questions.length - 1 ? 'disabled' : ''}>التالي ⬅</button>
            </div>"""

new_stage_render = """            <div class="exam-q-header">
              <span class="exam-q-badge">سؤال ${exam.currentIndex + 1} من 30</span>
              <button type="button" class="btn-flag-review ${isFlag ? 'active' : ''}" id="btnModernFlag">
                <span>${isFlag ? '📌 معلّم للمراجعة' : '📌 علّم للمراجعة'}</span>
              </button>
            </div>

            <!-- حاوية الصورة الثابتة: ارتفاع 120px دائماً لمنع قفز الأزرار -->
            <div class="exam-media-slot">
              ${imgPath ? 
                `<div class="exam-sign-frame"><img src="${imgPath}" alt="Segnale"></div>` : 
                `<div class="exam-no-img-placeholder">
                   <span class="no-img-icon">🚗</span>
                   <span class="no-img-label">سؤال نظري عام • بدون إشارة مصورة</span>
                 </div>`
              }
            </div>

            <!-- حاوية نصوص السؤال ذات الارتفاع المتناسق -->
            <div class="exam-text-container">
              <div class="exam-text-it">${q.domanda}</div>
              <div class="exam-text-tr">${q.traduzione || 'سؤال وزاري مباشر.'}</div>
            </div>

            <!-- أزرار الإجابة الثابتة في منطقة راحة الإبهام -->
            <div class="exam-choice-buttons">
              <button type="button" class="choice-btn choice-btn-vero ${currentAnswer === true ? 'selected' : ''}" id="btnVero">
                <span>VERO (صح) ☑</span>
              </button>
              <button type="button" class="choice-btn choice-btn-falso ${currentAnswer === false ? 'selected' : ''}" id="btnFalso">
                <span>FALSO (خطأ) ✕</span>
              </button>
            </div>

            <!-- أزرار التنقل السفلية -->
            <div class="exam-nav-steps">
              <button type="button" class="btn-nav-step" id="btnPrev" ${exam.currentIndex === 0 ? 'disabled' : ''}>السابق ➡</button>
              <button type="button" class="btn-submit-pill" id="btnModernSubmit">📋 تسليم الامتحان</button>
              <button type="button" class="btn-nav-step" id="btnNext" ${exam.currentIndex === exam.questions.length - 1 ? 'disabled' : ''}>التالي ⬅</button>
            </div>"""

if old_stage_render in text:
    text = text.replace(old_stage_render, new_stage_render)
    print("Replaced stage render template successfully")
elif old_stage_render.replace('\n', '\r\n') in text:
    text = text.replace(old_stage_render.replace('\n', '\r\n'), new_stage_render.replace('\n', '\r\n'))
    print("Replaced stage render template (CRLF) successfully")
else:
    print("old_stage_render not found!")

# 4. UPDATE answerAndRefresh with Auto-Advance logic
old_answer_fn = """      function answerAndRefresh(qid, choice) {
        exam.recordAnswer(qid, choice);
        if (audio) audio.playFeedbackTone("click");
        renderActiveQuestion();
        renderPills();
      }"""

new_answer_fn = """      let _autoAdvanceTimer = null;
      function answerAndRefresh(qid, choice) {
        exam.recordAnswer(qid, choice);
        if (audio && typeof audio.playFeedbackTone === 'function') {
          audio.playFeedbackTone("click");
        }
        renderActiveQuestion();
        renderPills();

        // تفعيل الانتقال التلقائي الفوري للسؤال التالي (Auto-advance 220ms)
        if (_autoAdvanceTimer) clearTimeout(_autoAdvanceTimer);
        if (exam.currentIndex < exam.questions.length - 1) {
          _autoAdvanceTimer = setTimeout(() => {
            exam.nextQuestion();
            renderActiveQuestion();
            renderPills();
          }, 220);
        } else {
          // وميض زر التسليم عند اكتمال السؤال الأخير
          const sBtns = [document.getElementById("btnModernSubmit"), document.getElementById("btnQuickSubmit")];
          sBtns.forEach(b => {
            if (b) {
              b.style.transform = 'scale(1.08)';
              setTimeout(() => { b.style.transform = ''; }, 300);
            }
          });
        }
      }"""

if old_answer_fn in text:
    text = text.replace(old_answer_fn, new_answer_fn)
    print("Replaced answerAndRefresh successfully")
elif old_answer_fn.replace('\n', '\r\n') in text:
    text = text.replace(old_answer_fn.replace('\n', '\r\n'), new_answer_fn.replace('\n', '\r\n'))
    print("Replaced answerAndRefresh (CRLF) successfully")
else:
    print("old_answer_fn not found!")

# 5. Connect submit listeners for quick submit and modern submit
old_submit_hook = """      document.getElementById("btnSubmitFinalExam").addEventListener("click", confirmAndSubmit);
      document.getElementById("btnMotoConclude").addEventListener("click", confirmAndSubmit);"""

new_submit_hook = """      const btnSub = document.getElementById("btnSubmitFinalExam");
      if (btnSub) btnSub.addEventListener("click", confirmAndSubmit);
      const btnQuick = document.getElementById("btnQuickSubmit");
      if (btnQuick) btnQuick.addEventListener("click", confirmAndSubmit);
      const btnMoto = document.getElementById("btnMotoConclude");
      if (btnMoto) btnMoto.addEventListener("click", confirmAndSubmit);
      document.addEventListener("click", (e) => {
        if (e.target && e.target.id === "btnModernSubmit") confirmAndSubmit();
      });"""

if old_submit_hook in text:
    text = text.replace(old_submit_hook, new_submit_hook)
    print("Replaced submit hooks successfully")
elif old_submit_hook.replace('\n', '\r\n') in text:
    text = text.replace(old_submit_hook.replace('\n', '\r\n'), new_submit_hook.replace('\n', '\r\n'))
    print("Replaced submit hooks (CRLF) successfully")
else:
    print("old_submit_hook not found!")

# 6. Ensure active pill auto-scrolls into center in renderPills
old_pills_scroll = """        if (grid) {
          grid.innerHTML = exam.questions.map((q, idx) => {"""

new_pills_scroll = """        if (grid) {
          grid.innerHTML = exam.questions.map((q, idx) => {"""

# Find the end of grid listeners in renderPills to add auto-scroll
old_pills_end = """              renderPills();
            });
          });
        }"""

new_pills_end = """              renderPills();
            });
          });

          // Scroll active pill into center smoothly
          const curPill = grid.querySelector('.q-pill.active');
          if (curPill && curPill.scrollIntoView) {
            curPill.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
          }
        }"""

if old_pills_end in text:
    text = text.replace(old_pills_end, new_pills_end)
    print("Added smooth auto-scroll to active pill")
elif old_pills_end.replace('\n', '\r\n') in text:
    text = text.replace(old_pills_end.replace('\n', '\r\n'), new_pills_end.replace('\n', '\r\n'))
    print("Added smooth auto-scroll to active pill (CRLF)")
else:
    print("old_pills_end not found")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Upgrade of scheda-esame.html finished successfully.")

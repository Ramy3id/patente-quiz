import re

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update text zone CSS (Accordion translation toggle)
old_text_zone = '''    /* Fixed Height Question Text Zone */
    .exam-text-container {
      height: 175px;
      min-height: 175px;
      max-height: 175px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      margin: 6px 0 8px;
      text-align: center;
      padding: 2px 8px;
      scrollbar-width: thin;
    }
    .exam-text-it {
      font-size: 1.05rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.35;
      margin: 0 0 6px;
      direction: ltr;
      text-align: center;
    }
    html.light .exam-text-it { color: #0F172A; }
    .exam-text-tr {
      font-size: 0.88rem;
      font-weight: 600;
      color: #CBD5E1;
      line-height: 1.35;
      direction: rtl;
      text-align: center;
      margin: 0;
    }
    html.light .exam-text-tr { color: #334155; }'''

new_text_zone = '''    /* Fixed Height Question Text Zone (Zero layout shift, no top clipping) */
    .exam-text-container {
      height: 175px;
      min-height: 175px;
      max-height: 175px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      margin: 6px 0 8px;
      text-align: center;
      padding: 4px 8px;
      scrollbar-width: thin;
      box-sizing: border-box;
    }
    .exam-text-it {
      font-size: 1.08rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.4;
      margin: 0 0 8px;
      direction: ltr;
      text-align: center;
    }
    html.light .exam-text-it { color: #0F172A; }
    
    .exam-tr-wrapper {
      margin-top: auto;
      margin-bottom: 2px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      width: 100%;
    }
    .btn-toggle-tr {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 12px;
      border-radius: 999px;
      font-size: 0.76rem;
      font-weight: 700;
      background: rgba(56, 189, 248, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: #0284C7;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: inherit;
    }
    html:not(.light) .btn-toggle-tr {
      background: rgba(56, 189, 248, 0.12);
      border-color: rgba(56, 189, 248, 0.3);
      color: #38BDF8;
    }
    .btn-toggle-tr:hover {
      transform: translateY(-1px);
    }
    .btn-toggle-tr.active {
      background: rgba(148, 163, 184, 0.14) !important;
      border-color: rgba(148, 163, 184, 0.3) !important;
      color: #475569 !important;
    }
    html:not(.light) .btn-toggle-tr.active {
      color: #CBD5E1 !important;
    }
    .exam-text-tr {
      font-size: 0.88rem;
      font-weight: 600;
      color: #CBD5E1;
      line-height: 1.35;
      direction: rtl;
      text-align: center;
      margin: 0;
      width: 100%;
      box-sizing: border-box;
      padding: 6px 10px;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      animation: fadeInTr 0.2s ease-out;
    }
    html.light .exam-text-tr {
      color: #334155;
      background: #F8FAFC;
      border-color: #E2E8F0;
    }
    @keyframes fadeInTr {
      from { opacity: 0; transform: translateY(-4px); }
      to { opacity: 1; transform: translateY(0); }
    }'''

if old_text_zone in c:
    c = c.replace(old_text_zone, new_text_zone)
    print('1. Text zone CSS replaced')
else:
    print('1. old_text_zone not found')

# 2. Update Motorizzazione CSS
moto_css_pattern = re.compile(r'/\* =+ \s* 2\. شاشة كمبيوتر المرور الإيطالي الرسمي.*?(?=\.btn-just-answered|\@media \(max-width: 640px\))', re.DOTALL)

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

if moto_css_pattern.search(c):
    c = moto_css_pattern.sub(new_moto_css, c)
    print('2. Motorizzazione CSS replaced successfully')
else:
    print('2. Pattern not matched for Motorizzazione CSS')

# 3. Update Motorizzazione HTML Markup (return button, placeholder, remove helper)
old_moto_html = '''      <div class="moto-top-header">
        <div class="moto-flag-brand">
          <div class="moto-flag-tricolore">
            <div class="flag-green"></div>
            <div class="flag-white"></div>
            <div class="flag-red"></div>
          </div>
          <div class="moto-titles-text">
            <strong>MINISTERO DELLE INFRASTRUTTURE E DEI TRASPORTI</strong>
            <span>DIPARTIMENTO PER I TRASPORTI TERRESTRI • ESAME PATENTE B</span>
          </div>
        </div>
        <div class="moto-timer-badge" id="motoTimerBadge">TEMPO: 20:00</div>
      </div>

      <div class="moto-main-terminal">
        <!-- لوحة صورة الإشارة إن وجدت -->
        <div class="moto-sign-panel" id="motoSignBox">
          <img id="motoSignImg" class="moto-sign-img" src="" alt="Segnale Stradale">
        </div>

        <!-- لوحة نص السؤال الإيطالي وأزرار اللمس -->
        <div class="moto-question-panel">
          <div>
            <div class="moto-q-meta-row">
              <span class="moto-q-num-badge" id="motoQuestionBadge">DOMANDA N. 1 DI 30</span>
              <button class="btn-moto-flag" id="btnMotoFlag">
                <span>📌</span>
                <span>DA RIVEDERE</span>
              </button>
            </div>
            <div class="moto-text-italian" id="motoQuestionText">Caricamento testo ufficiale...</div>
            <div class="moto-arabic-helper" id="motoQuestionTr">الترجمة السياقية لمساعدتك في الفهم...</div>
          </div>'''

new_moto_html = '''      <div class="moto-top-header">
        <div class="moto-flag-brand">
          <div class="moto-flag-tricolore">
            <div class="flag-green"></div>
            <div class="flag-white"></div>
            <div class="flag-red"></div>
          </div>
          <div class="moto-titles-text">
            <strong>MINISTERO DEI TRASPORTI</strong>
            <span>ESAME PATENTE B</span>
          </div>
        </div>
        <div class="moto-header-actions">
          <button type="button" class="btn-moto-switch-modern" id="btnMotoReturnModern" title="العودة للوضع العصري">
            <span>🌟 الوضع العصري</span>
          </button>
          <div class="moto-timer-badge" id="motoTimerBadge">TEMPO: 20:00</div>
        </div>
      </div>

      <div class="moto-main-terminal">
        <!-- لوحة صورة الإشارة الرسمية الثابتة -->
        <div class="moto-sign-panel" id="motoSignBox">
          <img id="motoSignImg" class="moto-sign-img" src="" alt="Segnale Stradale" style="display:none;">
          <div id="motoNoSignPlaceholder" class="moto-no-sign-official">
            🚗 QUESITO TEORICO • SENZA FIGURA
          </div>
        </div>

        <!-- لوحة نص السؤال الإيطالي الرسمي بدون ترجمة وأزرار اللمس -->
        <div class="moto-question-panel">
          <div>
            <div class="moto-q-meta-row">
              <span class="moto-q-num-badge" id="motoQuestionBadge">DOMANDA N. 1 DI 30</span>
              <button class="btn-moto-flag" id="btnMotoFlag">
                <span>📌</span>
                <span>DA RIVEDERE</span>
              </button>
            </div>
            <div class="moto-text-italian" id="motoQuestionText">Caricamento testo ufficiale...</div>
          </div>'''

if old_moto_html in c:
    c = c.replace(old_moto_html, new_moto_html)
    print('3. Motorizzazione HTML Markup replaced')
else:
    print('3. old_moto_html not matched')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)
print('Done script phase 1.')

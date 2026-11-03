import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\dizionario-sinonimi.html'

with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update HTML Markup for Hero section
old_hero_markup = '''    <div class="glass-card hero-main-card">
      <h1>
        <span>📖</span>
        <span>معجم المترادفات وفروق الوزارة الخادعة</span>
      </h1>
      <p>
        المعجم الأكاديمي الشامل للكلمات ذات نفس المعنى القانوني في رخصة القيادة الإيطالية (*Codice della Strada*). مصمم خصيصاً لتفكيك <strong>الفروق الخادعة وفخاخ الوزارة (Falsi Sinonimi)</strong> التي يتعمد واضع الامتحان استخدامها لإرباك الطلاب.
      </p>
      <div class="hero-stats-row">
        <div class="stat-chip">
          <span>📚 العائلات الدلالية:</span>
          <strong id="statTotalFamilies">18 عائلة</strong>
        </div>
        <div class="stat-chip">
          <span>🟢 المترادفات القانونية:</span>
          <strong id="statTotalSyns">85+ مرادفاً</strong>
        </div>
        <div class="stat-chip">
          <span>🔴 الفخاخ المفككة:</span>
          <strong id="statTotalTraps">38 فخاً وزارياً</strong>
        </div>
      </div>
    </div>'''

new_hero_markup = '''    <div class="glass-card hero-main-card">
      <h1>
        <span>📖</span>
        <span>معجم المترادفات وفروق الوزارة الخادعة</span>
      </h1>
      <p>
        المعجم الأكاديمي الشامل للكلمات ذات نفس المعنى القانوني في رخصة القيادة الإيطالية (<span dir="ltr">Codice della Strada</span>). مصمم خصيصاً لتفكيك <strong>الفروق الخادعة وفخاخ الوزارة (<span dir="ltr">Falsi Sinonimi</span>)</strong> التي يتعمد واضع الامتحان استخدامها لإرباك الطلاب.
      </p>
      <div class="hero-stats-strip">
        <div class="hero-stat-card stat-families">
          <div class="stat-num" id="statTotalFamilies">18</div>
          <div class="stat-label">📚 العائلات الدلالية</div>
        </div>
        <div class="hero-stat-card stat-synonyms">
          <div class="stat-num" id="statTotalSyns">85+</div>
          <div class="stat-label">🟢 المترادفات القانونية</div>
        </div>
        <div class="hero-stat-card stat-traps">
          <div class="stat-num" id="statTotalTraps">38</div>
          <div class="stat-label">🔴 الفخاخ المفككة</div>
        </div>
      </div>
    </div>'''

if old_hero_markup in text:
    text = text.replace(old_hero_markup, new_hero_markup, 1)
    print("Replaced Hero markup successfully")
else:
    print("WARNING: old_hero_markup not found!")

# 2. Update Search Placeholder
old_search_markup = '''      <span class="search-icon-span">🔍</span>
      <input type="text" id="dictSearchInput" class="search-input" placeholder="ابحث عن أي كلمة إيطالية، أو مرادف، أو ترجمة عربية (مثلاً: moderare, sosta, aderenza, vietato)..." oninput="renderThesaurusCards()">'''

new_search_markup = '''      <span class="search-icon-span">🔍</span>
      <input type="text" id="dictSearchInput" class="search-input" placeholder="ابحث عن كلمة إيطالية، مرادف، أو ترجمة بالعربية..." oninput="renderThesaurusCards()">'''

if old_search_markup in text:
    text = text.replace(old_search_markup, new_search_markup, 1)
    print("Replaced Search placeholder successfully")
else:
    print("WARNING: old_search_markup not found!")

# 3. Update JavaScript initDictionary() and renderThesaurusCards()
old_js_init = '''  // Stats
  document.getElementById('statTotalFamilies').textContent = `${PATENTE_THESAURUS.length} عائلة`;
  let synCount = 0;
  let trapCount = 0;
  PATENTE_THESAURUS.forEach(t => {
    synCount += (t.sinonimi || []).length;
    trapCount += (t.falsi_sinonimi || []).length;
  });
  document.getElementById('statTotalSyns').textContent = `${synCount} مرادفاً`;
  document.getElementById('statTotalTraps').textContent = `${trapCount} فخاً`;

  // Categories deck
  const deck = document.getElementById('categoryChipsDeck');
  deck.innerHTML = `
    <button class="cat-chip-btn active" data-cat="all" onclick="selectCategory('all', this)">الكل (${PATENTE_THESAURUS.length})</button>
  ` + PATENTE_THESAURUS.map(t => `
    <button class="cat-chip-btn" data-cat="${t.id}" onclick="selectCategory('${t.id}', this)">${t.categoria}</button>
  `).join('');'''

new_js_init = '''  // Stats
  const famEl = document.getElementById('statTotalFamilies');
  if (famEl) famEl.textContent = `${PATENTE_THESAURUS.length}`;
  let synCount = 0;
  let trapCount = 0;
  PATENTE_THESAURUS.forEach(t => {
    synCount += (t.sinonimi || []).length;
    trapCount += (t.falsi_sinonimi || []).length;
  });
  const synEl = document.getElementById('statTotalSyns');
  if (synEl) synEl.textContent = `${synCount}+`;
  const trapEl = document.getElementById('statTotalTraps');
  if (trapEl) trapEl.textContent = `${trapCount}`;

  // Categories deck
  const deck = document.getElementById('categoryChipsDeck');
  deck.innerHTML = `
    <button class="cat-chip-btn active" data-cat="all" onclick="selectCategory('all', this)">
      <span>🌟</span> <span>الكل (${PATENTE_THESAURUS.length} عائلة)</span>
    </button>
  ` + PATENTE_THESAURUS.map(t => `
    <button class="cat-chip-btn" data-cat="${t.id}" onclick="selectCategory('${t.id}', this)">${t.categoria}</button>
  `).join('');'''

if old_js_init in text:
    text = text.replace(old_js_init, new_js_init, 1)
    print("Replaced JS init successfully")
else:
    print("WARNING: old_js_init not found!")

# 4. Fix hardcoded #fecdd3 and bdi in card rendering
old_trap_box = '''    const trapBoxes = (item.falsi_sinonimi || []).map(tr => `
      <div class="trap-subitem">
        <span class="trap-term-title">⚠️ ${tr.termine}</span>
        <span style="color:#fecdd3;">${tr.spiegazione}</span>
      </div>
    `).join('');'''

new_trap_box = '''    const trapBoxes = (item.falsi_sinonimi || []).map(tr => `
      <div class="trap-subitem">
        <span class="trap-term-title">⚠️ ${tr.termine}</span>
        <span class="trap-explanation">${tr.spiegazione}</span>
      </div>
    `).join('');'''

if old_trap_box in text:
    text = text.replace(old_trap_box, new_trap_box, 1)
    print("Replaced trap box inline styles successfully")
else:
    print("WARNING: old_trap_box not found!")

# Fix bdi in headings
old_syn_heading = '<span>المترادفات الحقيقية في قانون السير (Sinonimi):</span>'
new_syn_heading = '<span>المترادفات الحقيقية في قانون السير <bdi>(Sinonimi)</bdi>:</span>'
if old_syn_heading in text:
    text = text.replace(old_syn_heading, new_syn_heading)
    print("Replaced syn heading bdi")

old_trap_heading = '<span>انتبه! مترادفات خادعة وفروق قاتلة (Falsi Sinonimi):</span>'
new_trap_heading = '<span>انتبه! مترادفات خادعة وفروق قاتلة <bdi>(Falsi Sinonimi)</bdi>:</span>'
if old_trap_heading in text:
    text = text.replace(old_trap_heading, new_trap_heading)
    print("Replaced trap heading bdi")

# 5. Add Master Overhaul CSS before </style>
comprehensive_css = '''
    /* =========================================================
       PATENTE PRO DICTIONARY MASTER RESPONSIVE OVERHAUL (ZERO-SCROLL)
       ========================================================= */
    .hero-main-card {
      padding: 22px 20px !important;
    }
    .hero-main-card h1 {
      font-size: 1.45rem !important;
      line-height: 1.35 !important;
      display: flex !important;
      align-items: center !important;
      gap: 10px !important;
      margin-bottom: 12px !important;
      color: #FFFFFF !important;
    }
    html.light .hero-main-card h1 {
      color: #0F172A !important;
    }
    .hero-main-card p {
      font-size: 0.90rem !important;
      line-height: 1.6 !important;
      margin-bottom: 16px !important;
      color: var(--text-secondary) !important;
    }
    html.light .hero-main-card p {
      color: #475569 !important;
    }

    /* Unified 3-Column Metrics Row */
    .hero-stats-strip {
      display: grid !important;
      grid-template-columns: repeat(3, 1fr) !important;
      gap: 8px !important;
      width: 100% !important;
      padding-top: 14px !important;
      border-top: 1px solid var(--border-subtle) !important;
      box-sizing: border-box !important;
    }
    html.light .hero-stats-strip {
      border-top-color: rgba(15, 23, 42, 0.08) !important;
    }
    .hero-stat-card {
      background: rgba(255, 255, 255, 0.04) !important;
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
      border-radius: 14px !important;
      padding: 10px 4px !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: center !important;
      text-align: center !important;
      box-sizing: border-box !important;
    }
    html.light .hero-stat-card {
      background: #F8FAFC !important;
      border-color: rgba(15, 23, 42, 0.08) !important;
      box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03) !important;
    }
    .stat-num {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 1.35rem !important;
      font-weight: 800 !important;
      line-height: 1.15 !important;
      margin-bottom: 4px !important;
    }
    .stat-label {
      font-size: 0.70rem !important;
      font-weight: 700 !important;
      color: var(--text-secondary) !important;
      line-height: 1.2 !important;
      white-space: nowrap !important;
    }
    html.light .stat-label {
      color: #475569 !important;
    }
    .hero-stat-card.stat-families .stat-num {
      color: #38BDF8 !important;
    }
    html.light .hero-stat-card.stat-families .stat-num {
      color: #0284C7 !important;
    }
    .hero-stat-card.stat-synonyms .stat-num {
      color: #34D399 !important;
    }
    html.light .hero-stat-card.stat-synonyms .stat-num {
      color: #059669 !important;
    }
    .hero-stat-card.stat-traps .stat-num {
      color: #FB7185 !important;
    }
    html.light .hero-stat-card.stat-traps .stat-num {
      color: #DC2626 !important;
    }

    /* Hero Side Card */
    .hero-side-card {
      padding: 20px !important;
      border-radius: 20px !important;
    }
    html.light .hero-side-card {
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.05), rgba(99, 102, 241, 0.05)) !important;
      border-color: rgba(2, 132, 199, 0.25) !important;
    }
    html.light .hero-side-card h3 {
      color: #0F172A !important;
    }
    html.light .hero-side-card p {
      color: #475569 !important;
    }

    /* Search Bar & Zero-Scroll Filter Chips */
    .search-filter-card {
      padding: 18px !important;
      border-radius: 20px !important;
    }
    html.light .search-filter-card {
      background: #FFFFFF !important;
      border-color: rgba(15, 23, 42, 0.1) !important;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
    }
    .search-bar-wrap {
      position: relative !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }
    .search-input {
      width: 100% !important;
      height: 48px !important;
      min-height: 48px !important;
      background: rgba(15, 15, 18, 0.8) !important;
      border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
      border-radius: 14px !important;
      padding: 0 46px 0 16px !important;
      color: #FFFFFF !important;
      font-size: 0.92rem !important;
      font-family: inherit !important;
      outline: none !important;
      box-sizing: border-box !important;
      transition: all 0.2s ease !important;
    }
    .search-input:focus {
      border-color: #38BDF8 !important;
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25) !important;
    }
    html.light .search-input {
      background: #FFFFFF !important;
      border-color: rgba(15, 23, 42, 0.18) !important;
      color: #0F172A !important;
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
    }
    html.light .search-input:focus {
      border-color: #0284C7 !important;
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.18) !important;
    }
    .search-icon-span {
      position: absolute !important;
      right: 14px !important;
      top: 50% !important;
      transform: translateY(-50%) !important;
      color: #94A3B8 !important;
      font-size: 1.15rem !important;
      pointer-events: none !important;
      z-index: 2 !important;
    }

    /* Zero-Scroll 2-Column Balanced Chips */
    .category-chips-row {
      display: grid !important;
      grid-template-columns: repeat(2, 1fr) !important;
      gap: 6px !important;
      width: 100% !important;
      max-width: 100% !important;
      margin-top: 14px !important;
      overflow: visible !important;
      padding-bottom: 0 !important;
      box-sizing: border-box !important;
    }
    @media (min-width: 768px) {
      .category-chips-row {
        grid-template-columns: repeat(3, 1fr) !important;
      }
    }
    @media (min-width: 1024px) {
      .category-chips-row {
        grid-template-columns: repeat(4, 1fr) !important;
      }
    }
    .cat-chip-btn {
      width: 100% !important;
      min-height: 40px !important;
      padding: 6px 10px !important;
      border-radius: 12px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      text-align: center !important;
      font-size: 0.78rem !important;
      font-weight: 700 !important;
      white-space: normal !important;
      line-height: 1.3 !important;
      box-sizing: border-box !important;
      cursor: pointer !important;
      font-family: inherit !important;
      transition: all 0.15s ease !important;
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
      background: rgba(255, 255, 255, 0.04) !important;
      color: #E2E8F0 !important;
    }
    .cat-chip-btn[data-cat="all"] {
      grid-column: 1 / -1 !important;
      min-height: 42px !important;
      font-size: 0.86rem !important;
      gap: 6px !important;
    }
    .cat-chip-btn.active {
      background: #0284C7 !important;
      border-color: #38BDF8 !important;
      color: #FFFFFF !important;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.35) !important;
    }
    html.light .cat-chip-btn {
      background: #F8FAFC !important;
      border: 1px solid rgba(15, 23, 42, 0.12) !important;
      color: #334155 !important;
    }
    html.light .cat-chip-btn:hover {
      background: #F1F5F9 !important;
      color: #0F172A !important;
    }
    html.light .cat-chip-btn.active {
      background: #0284C7 !important;
      border-color: #0284C7 !important;
      color: #FFFFFF !important;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25) !important;
    }

    /* Dictionary Cards Polish */
    .dict-card {
      background: var(--bg-surface) !important;
      border: 1px solid var(--border-subtle) !important;
      border-radius: 20px !important;
      padding: 20px !important;
      display: flex !important;
      flex-direction: column !important;
      gap: 16px !important;
      box-sizing: border-box !important;
      transition: all 0.2s ease !important;
    }
    html.light .dict-card {
      background: #FFFFFF !important;
      border: 1px solid rgba(15, 23, 42, 0.1) !important;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
    }
    .dict-word-main {
      font-size: 1.35rem !important;
      font-weight: 800 !important;
      color: #FFFFFF !important;
      font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace !important;
      letter-spacing: -0.01em !important;
      direction: ltr !important;
      text-align: right !important;
    }
    html.light .dict-word-main {
      color: #0F172A !important;
    }
    .dict-word-ar {
      font-size: 1rem !important;
      font-weight: 700 !important;
      color: #38BDF8 !important;
      margin-top: 3px !important;
    }
    html.light .dict-word-ar {
      color: #0284C7 !important;
    }
    .dict-cat-badge {
      font-size: 0.74rem !important;
      font-weight: 700 !important;
      padding: 4px 10px !important;
      border-radius: 8px !important;
      background: rgba(99, 102, 241, 0.15) !important;
      border: 1px solid rgba(99, 102, 241, 0.3) !important;
      color: #A5B4FC !important;
    }
    html.light .dict-cat-badge {
      background: rgba(2, 132, 199, 0.08) !important;
      border-color: rgba(2, 132, 199, 0.25) !important;
      color: #0369A1 !important;
    }
    .dict-definition-box {
      background: rgba(15, 23, 42, 0.6) !important;
      border-right: 3.5px solid #6366F1 !important;
      border-radius: 12px !important;
      padding: 12px 14px !important;
      font-size: 0.92rem !important;
      line-height: 1.6 !important;
      color: #E2E8F0 !important;
    }
    html.light .dict-definition-box {
      background: #F8FAFC !important;
      border: 1px solid rgba(15, 23, 42, 0.08) !important;
      border-right: 3.5px solid #0284C7 !important;
      color: #1E293B !important;
    }

    /* Synonyms Section */
    .synonyms-section {
      background: rgba(16, 185, 129, 0.06) !important;
      border: 1.5px solid rgba(16, 185, 129, 0.25) !important;
      border-radius: 14px !important;
      padding: 14px !important;
    }
    html.light .synonyms-section {
      background: #F0FDF4 !important;
      border-color: #BBF7D0 !important;
    }
    .synonyms-section h4 {
      font-size: 0.88rem !important;
      font-weight: 800 !important;
      color: #34D399 !important;
      margin-bottom: 10px !important;
      display: flex !important;
      align-items: center !important;
      gap: 6px !important;
    }
    html.light .synonyms-section h4 {
      color: #047857 !important;
    }
    .synonyms-deck {
      display: flex !important;
      flex-wrap: wrap !important;
      gap: 6px !important;
    }
    .syn-chip {
      background: rgba(16, 185, 129, 0.12) !important;
      border: 1px solid rgba(16, 185, 129, 0.3) !important;
      padding: 6px 12px !important;
      border-radius: 9px !important;
      display: inline-flex !important;
      align-items: center !important;
      gap: 6px !important;
      flex-wrap: wrap !important;
    }
    html.light .syn-chip {
      background: #FFFFFF !important;
      border-color: #86EFAC !important;
      box-shadow: 0 1px 3px rgba(16, 185, 129, 0.08) !important;
    }
    .syn-chip-it {
      font-family: 'JetBrains Mono', monospace !important;
      font-weight: 800 !important;
      color: #34D399 !important;
      direction: ltr !important;
    }
    html.light .syn-chip-it {
      color: #047857 !important;
    }
    .syn-chip-ar {
      font-size: 0.82rem !important;
      font-weight: 600 !important;
      color: #E2E8F0 !important;
    }
    html.light .syn-chip-ar {
      color: #1E293B !important;
    }

    /* Traps / False Synonyms Section (PALE RED FIXED COMPLETELY) */
    .traps-section {
      background: rgba(225, 29, 72, 0.08) !important;
      border: 1.5px solid rgba(225, 29, 72, 0.3) !important;
      border-radius: 14px !important;
      padding: 14px !important;
      margin-top: 12px !important;
    }
    html.light .traps-section {
      background: #FEF2F2 !important;
      border-color: #FECDD3 !important;
    }
    .traps-section h4 {
      font-size: 0.88rem !important;
      font-weight: 800 !important;
      color: #FB7185 !important;
      margin-bottom: 10px !important;
      display: flex !important;
      align-items: center !important;
      gap: 6px !important;
    }
    html.light .traps-section h4 {
      color: #991B1B !important;
    }
    .trap-subitem {
      background: rgba(15, 23, 42, 0.6) !important;
      border: 1px solid rgba(225, 29, 72, 0.25) !important;
      border-radius: 10px !important;
      padding: 10px 12px !important;
      margin-bottom: 8px !important;
      font-size: 0.88rem !important;
      line-height: 1.55 !important;
    }
    html.light .trap-subitem {
      background: #FFFFFF !important;
      border-color: #FCA5A5 !important;
      box-shadow: 0 1px 4px rgba(239, 68, 68, 0.06) !important;
    }
    .trap-subitem:last-child {
      margin-bottom: 0 !important;
    }
    .trap-term-title {
      font-weight: 800 !important;
      font-family: 'JetBrains Mono', monospace !important;
      color: #FDA4AF !important;
      display: block !important;
      margin-bottom: 4px !important;
      font-size: 0.90rem !important;
    }
    html.light .trap-term-title {
      color: #DC2626 !important;
    }
    .trap-explanation {
      color: #F1F5F9 !important;
      display: block !important;
      font-weight: 500 !important;
    }
    html.light .trap-explanation {
      color: #1E293B !important;
      font-weight: 600 !important;
    }

    /* Card Footer & Action Buttons */
    .dict-card-footer {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 10px !important;
      padding-top: 14px !important;
      border-top: 1px solid var(--border-subtle) !important;
    }
    html.light .dict-card-footer {
      border-top-color: rgba(15, 23, 42, 0.08) !important;
    }
    .btn-explore-quiz {
      flex: 1 !important;
      height: 40px !important;
      min-height: 40px !important;
      background: rgba(56, 189, 248, 0.14) !important;
      border: 1px solid rgba(56, 189, 248, 0.35) !important;
      color: #38BDF8 !important;
      padding: 0 14px !important;
      border-radius: 10px !important;
      font-size: 0.82rem !important;
      font-weight: 700 !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 6px !important;
      text-decoration: none !important;
      transition: all 0.15s ease !important;
      box-sizing: border-box !important;
    }
    html.light .btn-explore-quiz {
      background: #0284C7 !important;
      border-color: #0284C7 !important;
      color: #FFFFFF !important;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25) !important;
    }
    .btn-explore-quiz:hover {
      transform: translateY(-1px) !important;
    }
    .btn-tts-mini {
      width: 40px !important;
      height: 40px !important;
      min-width: 40px !important;
      min-height: 40px !important;
      background: rgba(255, 255, 255, 0.05) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      color: #E2E8F0 !important;
      border-radius: 10px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      cursor: pointer !important;
      font-size: 1.1rem !important;
      box-sizing: border-box !important;
      transition: all 0.15s ease !important;
    }
    html.light .btn-tts-mini {
      background: #F1F5F9 !important;
      border-color: rgba(15, 23, 42, 0.15) !important;
      color: #0F172A !important;
    }
'''

style_idx = text.find('</style>')
if style_idx != -1:
    text = text[:style_idx] + comprehensive_css + '\n' + text[style_idx:]
    print("Appended CSS successfully")

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated dizionario-sinonimi.html successfully.")

import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. New CSS
new_css = """    /* Search Box Wrapper */
    .cq-search-box-wrapper {
      position: sticky;
      top: 60px;
      z-index: 40;
      background: rgba(11, 15, 25, 0.92);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      padding: 12px 0 14px;
      margin-bottom: 18px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      transition: background 0.3s;
    }

    html.light .cq-search-box-wrapper {
      background: rgba(248, 250, 252, 0.92);
      border-bottom-color: rgba(0, 0, 0, 0.08);
    }

    .cq-search-input-group {
      position: relative;
      max-width: 860px;
      margin: 0 auto;
    }

    .cq-search-icon {
      position: absolute;
      right: 18px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1.3rem;
      color: var(--cq-cyan);
      pointer-events: none;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .cq-search-input {
      width: 100%;
      height: 54px;
      padding: 12px 52px 12px 75px;
      font-family: inherit;
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--cq-text);
      background: var(--cq-surface);
      border: 2px solid rgba(56, 189, 248, 0.35);
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
      outline: none;
      transition: all 0.25s ease;
      box-sizing: border-box;
    }

    html.light .cq-search-input {
      background: #FFFFFF;
      border-color: #CBD5E1;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
    }

    .cq-search-input:focus {
      border-color: var(--cq-cyan);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25), 0 8px 24px rgba(0, 0, 0, 0.2);
    }

    html.light .cq-search-input:focus {
      border-color: #0284C7;
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.2), 0 8px 24px rgba(0, 0, 0, 0.08);
    }

    .cq-search-actions {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .cq-clear-btn {
      background: rgba(255, 255, 255, 0.12);
      border: none;
      color: var(--cq-text-sub);
      width: 32px;
      height: 32px;
      border-radius: 8px;
      cursor: pointer;
      display: none;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
      transition: all 0.2s;
    }
    html.light .cq-clear-btn {
      background: #E2E8F0;
      color: #64748B;
    }

    .cq-clear-btn:hover {
      background: var(--cq-rose);
      color: #FFF;
    }

    .cq-shortcut-badge {
      font-family: 'Fira Code', monospace;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.08);
      color: var(--cq-text-sub);
      border: 1px solid rgba(255, 255, 255, 0.1);
      user-select: none;
    }

    /* Popular Searches Section - Dropdown & Quick Badges */
    .cq-popular-container {
      max-width: 860px;
      margin: 10px auto 0;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .cq-popular-row {
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
    }

    .cq-popular-label {
      font-size: 0.84rem;
      font-weight: 800;
      color: var(--cq-text-sub);
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .cq-popular-select-wrap {
      flex: 1;
      position: relative;
    }

    .cq-popular-select {
      width: 100%;
      height: 38px;
      padding: 0 12px;
      border-radius: 10px;
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--cq-text);
      background: var(--cq-surface);
      border: 1px solid var(--cq-card-border);
      outline: none;
      cursor: pointer;
      transition: border-color 0.2s;
    }

    html.light .cq-popular-select {
      background: #FFFFFF;
      border-color: #CBD5E1;
      color: #334155;
    }

    .cq-popular-select:focus {
      border-color: var(--cq-cyan);
    }

    /* Quick Badges */
    .cq-quick-pills-row {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }

    .cq-quick-pill {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--cq-text-sub);
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: 'Fira Code', 'Cairo', monospace;
    }

    html.light .cq-quick-pill {
      background: #F1F5F9;
      border-color: #E2E8F0;
      color: #475569;
    }

    .cq-quick-pill:hover {
      background: var(--cq-cyan);
      color: #0B0F19;
      border-color: var(--cq-cyan);
    }

    html.light .cq-quick-pill:hover {
      background: #0284C7;
      color: #FFFFFF;
      border-color: #0284C7;
    }

    /* Filters Bar - Clean Modular Grid System */
    .cq-filters-panel {
      max-width: 860px;
      margin: 0 auto 20px;
      background: var(--cq-card);
      border: 1px solid var(--cq-card-border);
      border-radius: 18px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: var(--cq-shadow);
    }

    html.light .cq-filters-panel {
      background: #FFFFFF;
      border-color: #E2E8F0;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04);
    }

    .cq-filter-row {
      display: flex;
      flex-direction: column;
      gap: 8px;
      width: 100%;
    }

    .cq-filter-row-header {
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--cq-text-sub);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Segmented Control for VERO / FALSO / ALL */
    .cq-seg-control {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
      background: rgba(255, 255, 255, 0.04);
      padding: 4px;
      border-radius: 12px;
      border: 1px solid var(--cq-card-border);
    }

    html.light .cq-seg-control {
      background: #F8FAFC;
      border-color: #E2E8F0;
    }

    .cq-seg-btn {
      padding: 8px 10px;
      border-radius: 9px;
      font-size: 0.86rem;
      font-weight: 800;
      text-align: center;
      border: none;
      background: transparent;
      color: var(--cq-text-sub);
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      font-family: inherit;
    }

    .cq-seg-btn:hover {
      color: var(--cq-text);
      background: rgba(255, 255, 255, 0.05);
    }

    html.light .cq-seg-btn:hover {
      color: #0F172A;
      background: #E2E8F0;
    }

    .cq-seg-btn.active {
      background: var(--cq-surface);
      color: var(--cq-text);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }

    html.light .cq-seg-btn.active {
      background: #FFFFFF;
      color: #0284C7;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }

    .cq-seg-btn.btn-vero.active {
      background: var(--cq-emerald) !important;
      color: #FFFFFF !important;
    }

    .cq-seg-btn.btn-falso.active {
      background: var(--cq-rose) !important;
      color: #FFFFFF !important;
    }

    /* Chapter Select */
    .cq-chapter-select-wrap {
      width: 100%;
    }

    .cq-select {
      width: 100%;
      height: 42px;
      background: var(--cq-surface);
      color: var(--cq-text);
      border: 1px solid var(--cq-card-border);
      padding: 0 14px;
      border-radius: 12px;
      font-family: inherit;
      font-size: 0.88rem;
      font-weight: 700;
      outline: none;
      cursor: pointer;
      box-sizing: border-box;
      transition: border-color 0.2s;
    }

    html.light .cq-select {
      background: #F8FAFC;
      border-color: #CBD5E1;
      color: #0F172A;
    }

    .cq-select:focus {
      border-color: var(--cq-cyan);
    }

    /* Special 2-column Grid */
    .cq-special-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      width: 100%;
    }

    .cq-toggle-btn {
      height: 42px;
      padding: 0 12px;
      border-radius: 12px;
      font-size: 0.84rem;
      font-weight: 700;
      border: 1px solid var(--cq-card-border);
      background: var(--cq-surface);
      color: var(--cq-text-sub);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s ease;
    }

    html.light .cq-toggle-btn {
      background: #F8FAFC;
      border-color: #E2E8F0;
      color: #475569;
    }

    .cq-toggle-btn:hover {
      border-color: var(--cq-cyan);
      color: var(--cq-text);
    }

    .cq-toggle-btn.active {
      background: rgba(56, 189, 248, 0.15);
      color: var(--cq-cyan);
      border-color: var(--cq-cyan);
      font-weight: 800;
    }

    html.light .cq-toggle-btn.active {
      background: #E0F2FE;
      color: #0284C7;
      border-color: #0284C7;
    }

    @media (max-width: 640px) {
      .cq-search-input {
        padding: 12px 46px 12px 42px;
        font-size: 0.94rem;
        height: 48px;
      }
      .cq-search-icon {
        right: 14px;
        font-size: 1.15rem;
      }
      .cq-shortcut-badge {
        display: none !important;
      }
      .cq-popular-row {
        flex-direction: column;
        align-items: stretch;
        gap: 6px;
      }
      .cq-popular-label {
        font-size: 0.82rem;
      }
      .cq-seg-btn {
        padding: 7px 6px;
        font-size: 0.82rem;
      }
      .cq-toggle-btn {
        font-size: 0.78rem;
        padding: 0 8px;
      }
    }

    """

# 2. New HTML
new_html = """    <!-- Search Box Sticky Wrapper -->
    <div class="cq-search-box-wrapper">
      <div class="cq-search-input-group">
        <span class="cq-search-icon">🔍</span>
        <input 
          type="text" 
          id="cqSearchInput" 
          class="cq-search-input" 
          placeholder="ابحث بكلمة إيطالية، عربية، أو برقم السؤال..."
          autocomplete="off"
          spellcheck="false"
          oninput="handleSearchInput()"
        >
        <div class="cq-search-actions">
          <button class="cq-clear-btn" id="cqClearBtn" onclick="clearSearch()" title="مسح حقل البحث">✕</button>
          <span class="cq-shortcut-badge" title="اضغط / للتركيز في حقل البحث">/</span>
        </div>
      </div>

      <!-- الأكثر بحثاً: قائمة منسدلة ذكية + شارات سريعة -->
      <div class="cq-popular-container">
        <div class="cq-popular-row">
          <label for="cqPopularSelect" class="cq-popular-label">
            <span>🔥</span>
            <span>الأكثر بحثاً:</span>
          </label>
          <div class="cq-popular-select-wrap">
            <select id="cqPopularSelect" class="cq-popular-select" onchange="handlePopularSelect(this)">
              <option value="" disabled selected>⚡ اختر مصطلحاً أو فخاً شائعاً للبحث...</option>
              <optgroup label="🚗 مصطلحات ومفاهيم متكررة">
                <option value="sorpasso in curva">sorpasso in curva (التجاوز في المنعطف)</option>
                <option value="frizione">frizione (الدبرياج)</option>
                <option value="distanza di sicurezza">distanza di sicurezza (مسافة الأمان)</option>
                <option value="quadricicli">quadricicli (السيارات الرباعية)</option>
                <option value="spazio di frenata">spazio di frenata (مسافة الفرملة)</option>
              </optgroup>
              <optgroup label="⚠️ أشهر فخاخ الكلمات المطلقة">
                <option value="sempre">sempre (فخ: دائماً)</option>
                <option value="solo">solo (فخ: فقط)</option>
                <option value="mai">mai (فخ: أبداً)</option>
                <option value="qualsiasi">qualsiasi (فخ: أي / أياً كان)</option>
              </optgroup>
              <optgroup label="⚖️ الرخص والمخالفات والأمان">
                <option value="punti patente">punti patente (نقاط الرخصة)</option>
                <option value="tasso alcolico">tasso alcolico (نسبة الكحول)</option>
                <option value="cintura di sicurezza">cintura di sicurezza (حزام الأمان)</option>
              </optgroup>
              <optgroup label="🚦 اللوحات والتقاطعات">
                <option value="pannelli integrativi">pannelli integrativi (اللوحات الإضافية)</option>
                <option value="figura 604">figura 604 (التقاطعات المعقدة)</option>
              </optgroup>
            </select>
          </div>
        </div>

        <!-- شارات سريعة للأكثر تداولاً (نقرة واحدة) -->
        <div class="cq-quick-pills-row">
          <button class="cq-quick-pill" onclick="setSearchTerm('sorpasso in curva')">sorpasso in curva</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('frizione')">frizione</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('sempre')">sempre</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('distanza di sicurezza')">distanza</button>
        </div>
      </div>
    </div>

    <!-- لوحة الفلاتر المنظمة -->
    <div class="cq-filters-panel">
      <!-- 1. فلتر نوع الإجابة (Segmented Control) -->
      <div class="cq-filter-row">
        <div class="cq-filter-row-header">
          <span>🎯 تصفية حسب الإجابة:</span>
        </div>
        <div class="cq-seg-control">
          <button class="cq-seg-btn active" id="btnAnsAll" onclick="setAnswerFilter('all')">🌟 الكل</button>
          <button class="cq-seg-btn btn-vero" id="btnAnsVero" onclick="setAnswerFilter('vero')">🟢 صح VERO</button>
          <button class="cq-seg-btn btn-falso" id="btnAnsFalso" onclick="setAnswerFilter('falso')">🔴 خطأ FALSO</button>
        </div>
      </div>

      <!-- 2. فلتر الباب الدراسي -->
      <div class="cq-filter-row">
        <div class="cq-filter-row-header">
          <span>📚 تصفية حسب الباب:</span>
        </div>
        <div class="cq-chapter-select-wrap">
          <select class="cq-select" id="cqChapterSelect" onchange="handleFilterChange()">
            <option value="all">📚 جميع الأبواب الـ 25 (بنك الأسئلة بالكامل)</option>
            <option value="1">الباب 1: المفاهيم العامة واستخدام الطريق</option>
            <option value="2">الباب 2: إشارات الخطر (Pericolo)</option>
            <option value="3">الباب 3: إشارات المنع (Divieto)</option>
            <option value="4">الباب 4: إشارات الإلزام (Obbligo)</option>
            <option value="5">الباب 5: إشارات الأسبقية (Precedenza)</option>
            <option value="6">الباب 6: التخطيط الأرضي (Segnaletica Orizzontale)</option>
            <option value="7">الباب 7: الإشارات الضوئية والشرطي</option>
            <option value="8">الباب 8: إشارات الإرشاد (Indicazione)</option>
            <option value="9">الباب 9: اللوحات المتممة والتحذير</option>
            <option value="10">الباب 10: اللوحات الإضافية (Pannelli Integrativi)</option>
            <option value="11">الباب 11: السرعة والمناورات</option>
            <option value="12">الباب 12: مسافة الأمان (Distanza di Sicurezza)</option>
            <option value="13">الباب 13: قواعد السير وحركة المرور</option>
            <option value="14">الباب 14: أسبقية التقاطعات (Incroci)</option>
            <option value="15">الباب 15: التجاوز (Sorpasso)</option>
            <option value="16">الباب 16: الوقوف والانتظار (Sosta e Fermata)</option>
            <option value="17">الباب 17: الحوادث والطوارئ والإسعاف</option>
            <option value="18">الباب 18: أجهزة الرؤية والإضاءة</option>
            <option value="19">الباب 19: أجهزة السلامة والأمان (Casco e Cinture)</option>
            <option value="20">الباب 20: رخص القيادة وسحب النقاط</option>
            <option value="21">الباب 21: المسؤولية المدنية والجنائية والتأمين</option>
            <option value="22">الباب 22: الحالة البدنية والنفسية والكحول</option>
            <option value="23">الباب 23: العوامل المشتتة للقيادة</option>
            <option value="24">الباب 24: حماية البيئة واستهلاك الوقود</option>
            <option value="25">الباب 25: ميكانيكا وصيانة السيارة</option>
          </select>
        </div>
      </div>

      <!-- 3. فلاتر خاصة إضافية (شبكة ثنائية متوازنة) -->
      <div class="cq-filter-row">
        <div class="cq-special-grid">
          <button class="cq-toggle-btn" id="btnOnlyImg" onclick="toggleImgFilter()">
            <span>🖼️</span>
            <span>أسئلة بها صور توضيحية</span>
          </button>
          <button class="cq-toggle-btn" id="btnOnlyTrap" onclick="toggleTrapFilter()">
            <span>⚠️</span>
            <span>الأفخاخ الوزارية فقط</span>
          </button>
        </div>
      </div>
    </div>
    """

# 3. New JS for handlePopularSelect and clearSearch update
old_clear_js = """    function clearSearch() {
      document.getElementById('cqSearchInput').value = '';
      state.query = '';
      document.getElementById('cqClearBtn').style.display = 'none';
      document.getElementById('cqSearchInput').focus();
      executeSearch();
    }"""

new_clear_js = """    function handlePopularSelect(sel) {
      if (!sel || !sel.value) return;
      setSearchTerm(sel.value);
    }

    function clearSearch() {
      document.getElementById('cqSearchInput').value = '';
      state.query = '';
      document.getElementById('cqClearBtn').style.display = 'none';
      const popSelect = document.getElementById('cqPopularSelect');
      if (popSelect) popSelect.selectedIndex = 0;
      document.getElementById('cqSearchInput').focus();
      executeSearch();
    }"""

# Normalize
content_norm = content.replace('\r\n', '\n')

css_start = content_norm.find('/* Search Box Wrapper */')
css_end = content_norm.find('/* Stats strip */')

if css_start == -1 or css_end == -1:
    print("Could not find CSS markers in content_norm")
    sys.exit(1)

content_norm = content_norm[:css_start] + new_css + content_norm[css_end:]

h_start = content_norm.find('<!-- Search Box Sticky Wrapper -->')
h_end = content_norm.find('<!-- شريط الإحصائيات الفوري -->')

if h_start == -1 or h_end == -1:
    print("Could not find HTML markers in content_norm")
    sys.exit(1)

content_norm = content_norm[:h_start] + new_html + content_norm[h_end:]

old_clear_norm = old_clear_js.replace('\r\n', '\n')
new_clear_norm = new_clear_js.replace('\r\n', '\n')

if old_clear_norm in content_norm:
    content_norm = content_norm.replace(old_clear_norm, new_clear_norm, 1)
else:
    print("Warning: old_clear_norm not found, checking...")

if '\r\n' in content:
    final_content = content_norm.replace('\n', '\r\n')
else:
    final_content = content_norm

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Successfully applied cerca-quiz updates!")

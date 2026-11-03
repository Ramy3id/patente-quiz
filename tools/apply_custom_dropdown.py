import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS: Replace .cq-popular-container and .cq-popular-select etc. with custom dropdown styles
old_pop_css = """    /* Popular Searches Section - Dropdown & Quick Badges */
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
    }"""

new_pop_css = """    /* Custom Dropdown for Popular Searches (Inside Container Frame) */
    .cq-popular-wrap {
      max-width: 860px;
      margin: 10px auto 0;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .cq-popular-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .cq-popular-label {
      font-size: 0.84rem;
      font-weight: 800;
      color: var(--cq-text-sub);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .cq-custom-dropdown {
      position: relative;
      width: 100%;
    }

    .cq-dd-trigger {
      width: 100%;
      height: 44px;
      padding: 0 14px;
      border-radius: 12px;
      font-family: inherit;
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--cq-text);
      background: var(--cq-surface);
      border: 1px solid var(--cq-card-border);
      outline: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s ease;
      box-sizing: border-box;
      text-align: right;
    }

    html.light .cq-dd-trigger {
      background: #FFFFFF;
      border-color: #CBD5E1;
      color: #1E293B;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    .cq-dd-trigger:hover,
    .cq-custom-dropdown.is-open .cq-dd-trigger {
      border-color: var(--cq-cyan);
    }

    html.light .cq-dd-trigger:hover,
    html.light .cq-custom-dropdown.is-open .cq-dd-trigger {
      border-color: #0284C7;
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }

    .cq-dd-trigger-content {
      display: flex;
      align-items: center;
      gap: 8px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .cq-dd-icon {
      font-size: 1rem;
      color: var(--cq-cyan);
    }

    .cq-dd-selected {
      font-weight: 700;
      font-size: 0.86rem;
      color: var(--cq-text);
    }

    .cq-dd-selected.is-placeholder {
      color: var(--cq-text-sub);
    }

    .cq-dd-arrow {
      font-size: 0.85rem;
      color: var(--cq-text-sub);
      transition: transform 0.2s ease;
    }

    .cq-custom-dropdown.is-open .cq-dd-arrow {
      transform: rotate(180deg);
      color: var(--cq-cyan);
    }

    /* Dropdown Menu Popup - Bound 100% to Container Width */
    .cq-dd-menu {
      position: absolute;
      top: calc(100% + 6px);
      right: 0;
      left: 0;
      width: 100%;
      max-width: 100%;
      max-height: 290px;
      overflow-y: auto;
      overflow-x: hidden;
      background: var(--cq-surface);
      border: 1px solid var(--cq-card-border);
      border-radius: 14px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
      z-index: 100;
      display: none;
      padding: 6px;
      box-sizing: border-box;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }

    html.light .cq-dd-menu {
      background: #FFFFFF;
      border-color: #E2E8F0;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
    }

    .cq-custom-dropdown.is-open .cq-dd-menu {
      display: block;
      animation: cqFadeDown 0.2s ease;
    }

    @keyframes cqFadeDown {
      from { opacity: 0; transform: translateY(-6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .cq-dd-group-title {
      font-size: 0.76rem;
      font-weight: 800;
      color: var(--cq-cyan);
      padding: 8px 10px 4px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      margin-top: 4px;
      letter-spacing: 0.3px;
    }

    html.light .cq-dd-group-title {
      color: #0284C7;
      border-bottom-color: #F1F5F9;
    }

    .cq-dd-group-title:first-child {
      margin-top: 0;
    }

    .cq-dd-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 9px 12px;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.15s ease;
      font-size: 0.85rem;
      gap: 10px;
    }

    .cq-dd-item:hover {
      background: rgba(56, 189, 248, 0.12);
    }

    html.light .cq-dd-item:hover {
      background: #F0F9FF;
    }

    .cq-dd-it {
      font-family: 'Fira Code', 'Cairo', monospace;
      font-weight: 700;
      color: var(--cq-text);
      font-size: 0.86rem;
      white-space: nowrap;
    }

    html.light .cq-dd-it {
      color: #0F172A;
    }

    .cq-dd-ar {
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--cq-text-sub);
      text-align: left;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }"""

# 2. Update HTML
old_pop_html = """      <!-- الأكثر بحثاً: قائمة منسدلة ذكية + شارات سريعة -->
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
          <button class="cq-quick-pill" onclick="setSearchTerm('frizione')">frizione (الدبرياج)</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('sempre')">sempre (دائماً)</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('sorpasso')">sorpasso (التجاوز)</button>
        </div>
      </div>"""

new_pop_html = """      <!-- الأكثر بحثاً: قائمة منسدلة مخصصة فائقة الأناقة -->
      <div class="cq-popular-wrap">
        <div class="cq-popular-header">
          <span class="cq-popular-label">
            <span>🔥</span>
            <span>الأكثر بحثاً في بنك الوزارة:</span>
          </span>
        </div>

        <div class="cq-custom-dropdown" id="cqPopularDropdown">
          <button type="button" class="cq-dd-trigger" id="cqDropdownTrigger" onclick="togglePopularMenu(event)" aria-expanded="false">
            <span class="cq-dd-trigger-content">
              <span class="cq-dd-icon">⚡</span>
              <span class="cq-dd-selected is-placeholder" id="cqSelectedPopularText">اختر مصطلحاً أو فخاً شائعاً للبحث...</span>
            </span>
            <span class="cq-dd-arrow" id="cqDropdownArrow">▾</span>
          </button>

          <div class="cq-dd-menu" id="cqPopularMenu" role="listbox">
            <!-- قسم 1: المفاهيم المتكررة -->
            <div class="cq-dd-group-title">🚗 مصطلحات ومفاهيم متكررة</div>
            <div class="cq-dd-item" onclick="selectPopularTerm('sorpasso in curva', 'sorpasso in curva (التجاوز في المنعطف)')">
              <span class="cq-dd-it">sorpasso in curva</span>
              <span class="cq-dd-ar">التجاوز في المنعطف</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('frizione', 'frizione (الدبرياج)')">
              <span class="cq-dd-it">frizione</span>
              <span class="cq-dd-ar">الدبرياج / القابض</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('distanza di sicurezza', 'distanza di sicurezza (مسافة الأمان)')">
              <span class="cq-dd-it">distanza di sicurezza</span>
              <span class="cq-dd-ar">مسافة الأمان</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('quadricicli', 'quadricicli (السيارات الرباعية)')">
              <span class="cq-dd-it">quadricicli</span>
              <span class="cq-dd-ar">السيارات الرباعية الخفيفة</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('spazio di frenata', 'spazio di frenata (مسافة الفرملة)')">
              <span class="cq-dd-it">spazio di frenata</span>
              <span class="cq-dd-ar">مسافة الفرملة</span>
            </div>

            <!-- قسم 2: أشهر فخاخ الكلمات -->
            <div class="cq-dd-group-title">⚠️ أشهر فخاخ الكلمات المطلقة</div>
            <div class="cq-dd-item" onclick="selectPopularTerm('sempre', 'sempre (فخ دائماً)')">
              <span class="cq-dd-it" style="color:var(--cq-rose);">sempre</span>
              <span class="cq-dd-ar">فخ دائماً (غالباً FALSO)</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('solo', 'solo (فخ فقط)')">
              <span class="cq-dd-it" style="color:var(--cq-rose);">solo</span>
              <span class="cq-dd-ar">فخ فقط (استثناءات محددة)</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('mai', 'mai (فخ أبداً)')">
              <span class="cq-dd-it" style="color:var(--cq-rose);">mai</span>
              <span class="cq-dd-ar">فخ أبداً</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('qualsiasi', 'qualsiasi (فخ أي مركبة)')">
              <span class="cq-dd-it" style="color:var(--cq-rose);">qualsiasi</span>
              <span class="cq-dd-ar">فخ أي مركبة / أياً كان</span>
            </div>

            <!-- قسم 3: الرخص والمخالفات -->
            <div class="cq-dd-group-title">⚖️ الرخص والمخالفات والأمان</div>
            <div class="cq-dd-item" onclick="selectPopularTerm('punti patente', 'punti patente (نقاط الرخصة)')">
              <span class="cq-dd-it">punti patente</span>
              <span class="cq-dd-ar">نقاط رخصة القيادة</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('tasso alcolico', 'tasso alcolico (نسبة الكحول)')">
              <span class="cq-dd-it">tasso alcolico</span>
              <span class="cq-dd-ar">نسبة الكحول في الدم</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('cintura di sicurezza', 'cintura di sicurezza (حزام الأمان)')">
              <span class="cq-dd-it">cintura di sicurezza</span>
              <span class="cq-dd-ar">حزام الأمان ومقاعد الأطفال</span>
            </div>

            <!-- قسم 4: التقاطعات واللوحات -->
            <div class="cq-dd-group-title">🚦 اللوحات والتقاطعات</div>
            <div class="cq-dd-item" onclick="selectPopularTerm('pannelli integrativi', 'pannelli integrativi (اللوحات الإضافية)')">
              <span class="cq-dd-it">pannelli integrativi</span>
              <span class="cq-dd-ar">اللوحات الإضافية المتممة</span>
            </div>
            <div class="cq-dd-item" onclick="selectPopularTerm('figura 604', 'figura 604 (التقاطعات المعقدة)')">
              <span class="cq-dd-it">figura 604</span>
              <span class="cq-dd-ar">التقاطعات المعقدة</span>
            </div>
          </div>
        </div>

        <!-- أزرار الاختيار السريع المباشر (Quick Tags) -->
        <div class="cq-quick-pills-row">
          <button type="button" class="cq-quick-pill" onclick="selectPopularTerm('frizione', 'frizione (الدبرياج)')">frizione (الدبرياج)</button>
          <button type="button" class="cq-quick-pill" onclick="selectPopularTerm('sempre', 'sempre (دائماً)')">sempre (دائماً)</button>
          <button type="button" class="cq-quick-pill" onclick="selectPopularTerm('sorpasso', 'sorpasso (التجاوز)')">sorpasso (التجاوز)</button>
        </div>
      </div>"""

# 3. Update JS functions
old_js = """    function handlePopularSelect(sel) {
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

new_js = """    function togglePopularMenu(e) {
      if (e) e.stopPropagation();
      const dd = document.getElementById('cqPopularDropdown');
      if (dd) {
        const isOpen = dd.classList.toggle('is-open');
        const trigger = document.getElementById('cqDropdownTrigger');
        if (trigger) trigger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      }
    }

    function closePopularMenu() {
      const dd = document.getElementById('cqPopularDropdown');
      if (dd) {
        dd.classList.remove('is-open');
        const trigger = document.getElementById('cqDropdownTrigger');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
      }
    }

    function selectPopularTerm(term, label) {
      closePopularMenu();
      const selLabel = document.getElementById('cqSelectedPopularText');
      if (selLabel) {
        selLabel.textContent = label || term;
        selLabel.classList.remove('is-placeholder');
      }
      setSearchTerm(term);
    }

    // إغلاق القائمة عند النقر خارجها
    document.addEventListener('click', (e) => {
      const dd = document.getElementById('cqPopularDropdown');
      if (dd && !dd.contains(e.target)) {
        closePopularMenu();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closePopularMenu();
      }
    });

    function clearSearch() {
      document.getElementById('cqSearchInput').value = '';
      state.query = '';
      document.getElementById('cqClearBtn').style.display = 'none';
      const selLabel = document.getElementById('cqSelectedPopularText');
      if (selLabel) {
        selLabel.textContent = 'اختر مصطلحاً أو فخاً شائعاً للبحث...';
        selLabel.classList.add('is-placeholder');
      }
      closePopularMenu();
      document.getElementById('cqSearchInput').focus();
      executeSearch();
    }"""

content_norm = content.replace('\r\n', '\n')
content_norm = content_norm.replace(old_pop_css.replace('\r\n', '\n'), new_pop_css.replace('\r\n', '\n'))
content_norm = content_norm.replace(old_pop_html.replace('\r\n', '\n'), new_pop_html.replace('\r\n', '\n'))
content_norm = content_norm.replace(old_js.replace('\r\n', '\n'), new_js.replace('\r\n', '\n'))

if '\r\n' in content:
    final_content = content_norm.replace('\n', '\r\n')
else:
    final_content = content_norm

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Applied Custom Dropdown component successfully!")

# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject Master Tabs and Section Wrappers in HTML
master_tabs_html = """
    <!-- أزرار التبويب الرئيسية الثلاثة لرادار الامتحان -->
    <div class="ps-master-tabs" role="tablist">
      <button class="ps-master-tab active" id="tabBtnGeneral" onclick="switchMainRadarTab('general')">
        <span class="pmt-icon">🔤</span>
        <div class="pmt-content">
          <span class="pmt-title">الكلمات السحرية العامة</span>
          <span class="pmt-desc">كلمات الحسم وماراثون الإتقان</span>
        </div>
      </button>

      <button class="ps-master-tab" id="tabBtnSigns" onclick="switchMainRadarTab('signs')">
        <span class="pmt-icon">🚦</span>
        <div class="pmt-content">
          <span class="pmt-title">رادار كشف الفخ مع الإشارة</span>
          <span class="pmt-desc">الأبواب 1 - 10 (فخاخ الإشارات)</span>
        </div>
        <span class="pmt-badge">جديد ⚡</span>
      </button>

      <button class="ps-master-tab" id="tabBtnTheory" onclick="switchMainRadarTab('theory')">
        <span class="pmt-icon">⚖️</span>
        <div class="pmt-content">
          <span class="pmt-title">القواعد والمحرمات النظرية</span>
          <span class="pmt-desc">الأبواب 11 - 25 (الإسعافات والتأمين...)</span>
        </div>
        <span class="pmt-badge">جديد ⚡</span>
      </button>
    </div>

    <!-- 1. قسم الكلمات السحرية العامة والماراثون -->
    <div id="radarSectionGeneral" class="radar-tab-section active">
"""

# Close General section and open Tab 2 (Signs) and Tab 3 (Theory)
closing_and_new_sections_html = """
    </div><!-- نهاية radarSectionGeneral -->

    <!-- 2. قسم رادار كشف الفخ مع الإشارة (الأبواب 1 - 10) -->
    <div id="radarSectionSigns" class="radar-tab-section" style="display:none;">
      <div class="radar-intro-strip">
        <span class="radar-intro-icon">🚦</span>
        <div class="radar-intro-body">
          <h3>رادار فخاخ الإشارات واللوحات الرسمية (الأبواب 1 - 10)</h3>
          <p>
            تكتيكات مدارس تعليم القيادة: عند رؤية إشارة محددة مع كلمة إيطالية معينة في نص السؤال، تحسم الإجابة فوراً VERO أو FALSO بنسبة 100%!
            اختر أي قاعدة لاستعراض كافة أسئلتها الوزارية واختبار نفسك فيها.
          </p>
        </div>
      </div>

      <!-- شريط البحث والفلترة للإشارات -->
      <div class="ps-controls">
        <input type="text" id="signSearchInput" class="ps-search-input" placeholder="🔍 ابحث برقم الإشارة أو اسمها أو الكلمة المفتاحية (مثل filobus أو STOP أو sosta)..." oninput="filterSignsCards()">
        <div class="ps-filters-row">
          <button class="ps-filter-btn active" id="btnSignFilterAll" onclick="setSignFilter('all')">🌟 كافة فخاخ الإشارات (<span id="cntSignAll">0</span>)</button>
          <button class="ps-filter-btn filter-falso" id="btnSignFilterFalso" onclick="setSignFilter('falso')">🔴 أفخاخ FALSO القطعية (<span id="cntSignFalso">0</span>)</button>
          <button class="ps-filter-btn filter-vero" id="btnSignFilterVero" onclick="setSignFilter('vero')">🟢 مفاتيح VERO المؤكدة (<span id="cntSignVero">0</span>)</button>
          <button class="ps-filter-btn" id="btnSignFilterPericolo" onclick="setSignFilter('pericolo')">⚠️ إشارات الخطر</button>
          <button class="ps-filter-btn" id="btnSignFilterDivieto" onclick="setSignFilter('divieto')">🚫 إشارات المنع</button>
          <button class="ps-filter-btn" id="btnSignFilterObbligo" onclick="setSignFilter('obbligo')">🔵 إشارات الإلزام</button>
          <button class="ps-filter-btn" id="btnSignFilterPrecedenza" onclick="setSignFilter('precedenza')">🔺 إشارات الأسبقية</button>
          <button class="ps-filter-btn" id="btnSignFilterOrizzontale" onclick="setSignFilter('orizzontale')">➖ الإشارات الأرضية</button>
        </div>
      </div>

      <!-- شبكة بطاقات فخاخ الإشارات -->
      <div class="ps-grid" id="signsGrid">
        <div style="text-align:center; grid-column:1/-1; padding:40px; color:var(--ps-text-sub);">جاري تحميل بطاقات فخاخ الإشارات...</div>
      </div>
    </div><!-- نهاية radarSectionSigns -->

    <!-- 3. قسم القواعد والمحرمات النظرية (الأبواب 11 - 25) -->
    <div id="radarSectionTheory" class="radar-tab-section" style="display:none;">
      <div class="radar-intro-strip">
        <span class="radar-intro-icon">⚖️</span>
        <div class="radar-intro-body">
          <h3>رادار القواعد الذهبية والمحرمات النظرية (الأبواب 11 - 25)</h3>
          <p>
            الثوابت القطعية في الإسعافات الأولية، التأمين الإجباري RCA، أحزمة الأمان والوسائد الهوائية، وحدود السرعة والفرملة.
            هذه القواعد لا تحتمل التأويل وتأتي أسئلتها حاسمة 100% في الامتحان الوزاري.
          </p>
        </div>
      </div>

      <!-- شريط البحث والفلترة للقواعد النظرية -->
      <div class="ps-controls">
        <input type="text" id="theorySearchInput" class="ps-search-input" placeholder="🔍 ابحث في القواعد النظرية (مثل الإسعافات، التأمين، الحزام، السرعة، النقاط)..." oninput="filterTheoryCards()">
        <div class="ps-filters-row">
          <button class="ps-filter-btn active" id="btnTheoryFilterAll" onclick="setTheoryFilter('all')">🌟 كافة القواعد (<span id="cntTheoryAll">0</span>)</button>
          <button class="ps-filter-btn filter-falso" id="btnTheoryFilterFalso" onclick="setTheoryFilter('falso')">🔴 محرمات FALSO القطعية (<span id="cntTheoryFalso">0</span>)</button>
          <button class="ps-filter-btn filter-vero" id="btnTheoryFilterVero" onclick="setTheoryFilter('vero')">🟢 ثوابت VERO المؤكدة (<span id="cntTheoryVero">0</span>)</button>
          <button class="ps-filter-btn" id="btnTheoryFilterSoccorso" onclick="setTheoryFilter('soccorso')">🚑 الإسعافات الأولية</button>
          <button class="ps-filter-btn" id="btnTheoryFilterAssicurazione" onclick="setTheoryFilter('assicurazione')">🛡️ التأمين RCA</button>
          <button class="ps-filter-btn" id="btnTheoryFilterCinture" onclick="setTheoryFilter('cinture')">💺 الحزام والأيرباج</button>
          <button class="ps-filter-btn" id="btnTheoryFilterDistanza" onclick="setTheoryFilter('distanza')">📏 السرعة ومسافة الأمان</button>
          <button class="ps-filter-btn" id="btnTheoryFilterAlcool" onclick="setTheoryFilter('alcool')">🍷 الكحول والمخدرات</button>
          <button class="ps-filter-btn" id="btnTheoryFilterPatente" onclick="setTheoryFilter('patente')">📋 الرخص ونظام النقاط</button>
          <button class="ps-filter-btn" id="btnTheoryFilterSosta" onclick="setTheoryFilter('sosta')">🛑 الوقوف والتوقف</button>
          <button class="ps-filter-btn" id="btnTheoryFilterMeccanica" onclick="setTheoryFilter('meccanica')">🔧 الميكانيكا والإطارات</button>
        </div>
      </div>

      <!-- شبكة بطاقات القواعد النظرية -->
      <div class="ps-grid" id="theoryGrid">
        <div style="text-align:center; grid-column:1/-1; padding:40px; color:var(--ps-text-sub);">جاري تحميل بطاقات القواعد النظرية...</div>
      </div>
    </div><!-- نهاية radarSectionTheory -->
"""

# Check if not already injected
if 'id="radarSectionGeneral"' not in html:
    # 1. Replace after </header>
    header_end = '</header>'
    html = html.replace(header_end, header_end + '\n' + master_tabs_html, 1)

    # 2. Replace after <div class="ps-grid" id="wordsGrid">...</div>
    grid_end = '    <div class="ps-grid" id="wordsGrid">\n      <div style="text-align:center; grid-column:1/-1; padding:40px; color:var(--ps-text-sub);">جاري تحميل الكلمات وبنك الأسئلة...</div>\n    </div>'
    if grid_end in html:
        html = html.replace(grid_end, grid_end + '\n' + closing_and_new_sections_html, 1)
        print("Successfully injected master tabs and section HTML.")
    else:
        # Flexible replacement
        m = re.search(r'(<div class="ps-grid" id="wordsGrid">[\s\S]*?</div>)', html)
        if m:
            html = html.replace(m.group(0), m.group(0) + '\n' + closing_and_new_sections_html, 1)
            print("Successfully injected master tabs and section HTML (flexible).")
else:
    print("HTML sections already present.")

with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'w', encoding='utf-8') as f:
    f.write(html)

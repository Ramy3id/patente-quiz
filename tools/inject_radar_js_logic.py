# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'r', encoding='utf-8') as f:
    html = f.read()

radar_js = """
    // =========================================================================
    // رادار كشف الفخ مع الإشارة والقواعد النظرية (Master Radar Engine)
    // =========================================================================
    let currentMasterTab = 'general';
    let activeSignFilter = 'all';
    let activeTheoryFilter = 'all';
    let signsRendered = false;
    let theoryRendered = false;

    function switchMainRadarTab(tabKey) {
      currentMasterTab = tabKey;

      // تحديث أزرار التبويب
      document.querySelectorAll('.ps-master-tab').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(
        tabKey === 'general' ? 'tabBtnGeneral' :
        tabKey === 'signs' ? 'tabBtnSigns' : 'tabBtnTheory'
      );
      if (activeBtn) activeBtn.classList.add('active');

      // تبديل الأقسام
      const secGen = document.getElementById('radarSectionGeneral');
      const secSigns = document.getElementById('radarSectionSigns');
      const secTheory = document.getElementById('radarSectionTheory');

      if (secGen) secGen.style.display = tabKey === 'general' ? 'block' : 'none';
      if (secSigns) secSigns.style.display = tabKey === 'signs' ? 'block' : 'none';
      if (secTheory) secTheory.style.display = tabKey === 'theory' ? 'block' : 'none';

      // تحديث إحصائيات الهيدر التفاعلية
      const statWordsEl = document.getElementById('statWordsCount');
      const statQsEl = document.getElementById('statQuestionsCovered');

      if (tabKey === 'general') {
        if (statWordsEl) statWordsEl.innerText = '36 كلمة';
        if (statQsEl) statQsEl.innerText = '457 سؤالاً';
      } else if (tabKey === 'signs') {
        const signCount = (typeof RADAR_SIGN_TRAPS !== 'undefined') ? RADAR_SIGN_TRAPS.length : 19;
        const totalSignQs = (typeof RADAR_SIGN_TRAPS !== 'undefined') ? RADAR_SIGN_TRAPS.reduce((acc, r) => acc + (r.count || 0), 0) : 68;
        if (statWordsEl) statWordsEl.innerText = `${signCount} إشارة وفخ`;
        if (statQsEl) statQsEl.innerText = `${totalSignQs} سؤالاً`;
        if (!signsRendered) {
          renderSignsRadar();
          signsRendered = true;
        }
      } else if (tabKey === 'theory') {
        const theoryCount = (typeof RADAR_THEORY_RULES !== 'undefined') ? RADAR_THEORY_RULES.length : 17;
        const totalTheoryQs = (typeof RADAR_THEORY_RULES !== 'undefined') ? RADAR_THEORY_RULES.reduce((acc, r) => acc + (r.count || 0), 0) : 155;
        if (statWordsEl) statWordsEl.innerText = `${theoryCount} قاعدة ومحرّم`;
        if (statQsEl) statQsEl.innerText = `${totalTheoryQs} سؤالاً`;
        if (!theoryRendered) {
          renderTheoryRadar();
          theoryRendered = true;
        }
      }

      // تمرير ناعم لأعلى الحاوية إذا لزم
      const container = document.querySelector('.ps-container');
      if (container && window.scrollY > 300) {
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    // -------------------------------------------------------------------------
    // 1. منطق رادار فخاخ الإشارات (Sign-Trap Radar)
    // -------------------------------------------------------------------------
    function initSignCounts() {
      if (typeof RADAR_SIGN_TRAPS === 'undefined') return;
      const all = RADAR_SIGN_TRAPS.length;
      const falso = RADAR_SIGN_TRAPS.filter(r => r.type === 'falso').length;
      const vero = RADAR_SIGN_TRAPS.filter(r => r.type === 'vero').length;

      const elAll = document.getElementById('cntSignAll');
      const elFalso = document.getElementById('cntSignFalso');
      const elVero = document.getElementById('cntSignVero');

      if (elAll) elAll.innerText = all;
      if (elFalso) elFalso.innerText = falso;
      if (elVero) elVero.innerText = vero;
    }

    function setSignFilter(fKey) {
      activeSignFilter = fKey;
      document.querySelectorAll('#radarSectionSigns .ps-filter-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById(
        fKey === 'all' ? 'btnSignFilterAll' :
        fKey === 'falso' ? 'btnSignFilterFalso' :
        fKey === 'vero' ? 'btnSignFilterVero' :
        fKey === 'pericolo' ? 'btnSignFilterPericolo' :
        fKey === 'divieto' ? 'btnSignFilterDivieto' :
        fKey === 'obbligo' ? 'btnSignFilterObbligo' :
        fKey === 'precedenza' ? 'btnSignFilterPrecedenza' : 'btnSignFilterOrizzontale'
      );
      if (activeBtn) activeBtn.classList.add('active');
      filterSignsCards();
    }

    function filterSignsCards() {
      if (typeof RADAR_SIGN_TRAPS === 'undefined') return;
      const query = (document.getElementById('signSearchInput')?.value || '').trim().toLowerCase();

      const filtered = RADAR_SIGN_TRAPS.filter(r => {
        // فلتر النوع أو التصنيف
        let matchFilter = true;
        if (activeSignFilter === 'falso') matchFilter = (r.type === 'falso');
        else if (activeSignFilter === 'vero') matchFilter = (r.type === 'vero');
        else if (activeSignFilter !== 'all') matchFilter = (r.category === activeSignFilter);

        if (!matchFilter) return false;

        // فلتر البحث
        if (!query) return true;
        const qStr = `${r.title_it} ${r.title_ar} ${r.keyword_it} ${r.trap_ar} ${r.rule_ar} ${r.fig}`.toLowerCase();
        return qStr.includes(query);
      });

      renderSignsGrid(filtered);
    }

    function renderSignsRadar() {
      initSignCounts();
      filterSignsCards();
    }

    function renderSignsGrid(list) {
      const container = document.getElementById('signsGrid');
      if (!container) return;

      if (!list || list.length === 0) {
        container.innerHTML = `
          <div style="text-align:center; grid-column:1/-1; padding:40px; color:var(--ps-text-sub);">
            🔍 لا توجد فخاخ إشارات مطابقة لخيارات البحث.
          </div>
        `;
        return;
      }

      container.innerHTML = list.map(r => {
        const isFalso = r.type === 'falso';
        const rateColor = isFalso ? 'var(--ps-rose)' : 'var(--ps-emerald)';
        const rateBg = isFalso ? 'rgba(244, 63, 94, 0.12)' : 'rgba(16, 185, 129, 0.12)';
        const rateBorder = isFalso ? 'rgba(244, 63, 94, 0.3)' : 'rgba(16, 185, 129, 0.3)';

        const catName =
          r.category === 'pericolo' ? '⚠️ إشارة خطر' :
          r.category === 'divieto' ? '🚫 إشارة منع' :
          r.category === 'obbligo' ? '🔵 إشارة إلزام' :
          r.category === 'precedenza' ? '🔺 إشارة أسبقية' : '➖ إشارة أرضية';

        const fn = r.fig || '';
        const rawImg = r.img || '';

        return `
          <div class="ps-sign-card">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:0.75rem; font-weight:800; color:var(--ps-cyan); background:rgba(56,189,248,0.1); padding:3px 8px; border-radius:6px;">
                  ${catName} | الباب ${r.ch}
                </span>
                <span style="font-size:0.75rem; font-weight:800; color:${rateColor}; background:${rateBg}; border:1px solid ${rateBorder}; padding:3px 8px; border-radius:999px;">
                  ${r.rate}
                </span>
              </div>

              <!-- معاينة الإشارة المرورية -->
              <div class="sign-card-thumb-wrap">
                <img src="../img_sign/${fn}" alt="${r.title_it}" class="sign-card-thumb" loading="lazy"
                  onerror="if(!this.dataset.fallback && '${rawImg}'){this.dataset.fallback='1'; this.src='../Capitoli_Divisi/' + '${rawImg}';}else{this.parentElement.style.display='none';}">
              </div>

              <h4 style="margin:0 0 4px 0; font-size:1.02rem; font-weight:800; color:var(--ps-text);">
                ${r.title_ar}
              </h4>
              <div style="direction:ltr; text-align:left; font-family:'Plus Jakarta Sans', sans-serif; font-size:0.8rem; font-weight:700; color:var(--ps-cyan); margin-bottom:10px;">
                ${r.title_it}
              </div>

              <!-- كبسولة الكلمة المفتاحية أو الفخ -->
              <div class="trap-keyword-box ${isFalso ? '' : 'vero-key'}">
                <span style="font-weight:800; color:${rateColor};">
                  ${isFalso ? '⚠️ الكلمة الفخ (FALSO):' : '🟢 الكلمة الحسم (VERO):'}
                </span>
                <strong style="direction:ltr; font-family:'Plus Jakarta Sans', sans-serif; font-size:0.95rem; color:var(--ps-text);">
                  ${r.keyword_it}
                </strong>
              </div>

              <!-- شرح الفخ وسر الإجابة -->
              <p class="trap-expl-text">
                <strong>💡 سر الفخ:</strong> ${r.trap_ar}
              </p>
            </div>

            <!-- زر فتح الأسئلة والكويز -->
            <button class="rule-action-btn" onclick="openSignRuleModal('${r.id}')">
              <span>⚡ تدريب على أسئلة الفخ (${r.count || (r.questions ? r.questions.length : 0)} أسئلة)</span>
              <span>⬅</span>
            </button>
          </div>
        `;
      }).join('');
    }

    // -------------------------------------------------------------------------
    // 2. منطق رادار القواعد الذهبية والمحرمات النظرية (Theory Radar)
    // -------------------------------------------------------------------------
    function initTheoryCounts() {
      if (typeof RADAR_THEORY_RULES === 'undefined') return;
      const all = RADAR_THEORY_RULES.length;
      const falso = RADAR_THEORY_RULES.filter(r => r.type === 'falso').length;
      const vero = RADAR_THEORY_RULES.filter(r => r.type === 'vero').length;

      const elAll = document.getElementById('cntTheoryAll');
      const elFalso = document.getElementById('cntTheoryFalso');
      const elVero = document.getElementById('cntTheoryVero');

      if (elAll) elAll.innerText = all;
      if (elFalso) elFalso.innerText = falso;
      if (elVero) elVero.innerText = vero;
    }

    function setTheoryFilter(fKey) {
      activeTheoryFilter = fKey;
      document.querySelectorAll('#radarSectionTheory .ps-filter-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById(
        fKey === 'all' ? 'btnTheoryFilterAll' :
        fKey === 'falso' ? 'btnTheoryFilterFalso' :
        fKey === 'vero' ? 'btnTheoryFilterVero' :
        fKey === 'soccorso' ? 'btnTheoryFilterSoccorso' :
        fKey === 'assicurazione' ? 'btnTheoryFilterAssicurazione' :
        fKey === 'cinture' ? 'btnTheoryFilterCinture' :
        fKey === 'distanza' ? 'btnTheoryFilterDistanza' :
        fKey === 'alcool' ? 'btnTheoryFilterAlcool' :
        fKey === 'patente' ? 'btnTheoryFilterPatente' :
        fKey === 'sosta' ? 'btnTheoryFilterSosta' : 'btnTheoryFilterMeccanica'
      );
      if (activeBtn) activeBtn.classList.add('active');
      filterTheoryCards();
    }

    function filterTheoryCards() {
      if (typeof RADAR_THEORY_RULES === 'undefined') return;
      const query = (document.getElementById('theorySearchInput')?.value || '').trim().toLowerCase();

      const filtered = RADAR_THEORY_RULES.filter(r => {
        let matchFilter = true;
        if (activeTheoryFilter === 'falso') matchFilter = (r.type === 'falso');
        else if (activeTheoryFilter === 'vero') matchFilter = (r.type === 'vero');
        else if (activeTheoryFilter !== 'all') matchFilter = (r.category === activeTheoryFilter);

        if (!matchFilter) return false;

        if (!query) return true;
        const qStr = `${r.topic} ${r.title_ar} ${r.title_it} ${r.keywords_it} ${r.golden_rule_ar} ${r.why_trap_ar}`.toLowerCase();
        return qStr.includes(query);
      });

      renderTheoryGrid(filtered);
    }

    function renderTheoryRadar() {
      initTheoryCounts();
      filterTheoryCards();
    }

    function renderTheoryGrid(list) {
      const container = document.getElementById('theoryGrid');
      if (!container) return;

      if (!list || list.length === 0) {
        container.innerHTML = `
          <div style="text-align:center; grid-column:1/-1; padding:40px; color:var(--ps-text-sub);">
            🔍 لا توجد قواعد نظرية مطابقة لخيارات البحث.
          </div>
        `;
        return;
      }

      container.innerHTML = list.map(r => {
        const isFalso = r.type === 'falso';
        const rateColor = isFalso ? 'var(--ps-rose)' : 'var(--ps-emerald)';
        const rateBg = isFalso ? 'rgba(244, 63, 94, 0.12)' : 'rgba(16, 185, 129, 0.12)';
        const rateBorder = isFalso ? 'rgba(244, 63, 94, 0.3)' : 'rgba(16, 185, 129, 0.3)';

        return `
          <div class="ps-theory-card">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:0.75rem; font-weight:800; color:var(--ps-cyan); background:rgba(56,189,248,0.1); padding:3px 8px; border-radius:6px;">
                  ${r.topic} | الباب ${r.ch}
                </span>
                <span style="font-size:0.75rem; font-weight:800; color:${rateColor}; background:${rateBg}; border:1px solid ${rateBorder}; padding:3px 8px; border-radius:999px;">
                  ${r.rate}
                </span>
              </div>

              <h4 style="margin:6px 0 4px 0; font-size:1.05rem; font-weight:800; color:var(--ps-text);">
                ${r.title_ar}
              </h4>
              <div style="direction:ltr; text-align:left; font-family:'Plus Jakarta Sans', sans-serif; font-size:0.8rem; font-weight:700; color:var(--ps-cyan); margin-bottom:10px;">
                ${r.title_it}
              </div>

              <!-- كبسولة الكلمات المفتاحية باللغة الإيطالية -->
              <div class="trap-keyword-box ${isFalso ? '' : 'vero-key'}">
                <span style="font-weight:800; color:${rateColor}; font-size:0.8rem;">
                  ${isFalso ? '⚠️ المحرّمات الإيطالية:' : '🟢 الثوابت الوزارية:'}
                </span>
                <strong style="direction:ltr; font-family:'Plus Jakarta Sans', sans-serif; font-size:0.88rem; color:var(--ps-text);">
                  ${r.keywords_it}
                </strong>
              </div>

              <!-- القاعدة الذهبية وسر الفخ الوزاري -->
              <p class="trap-expl-text">
                <strong>💡 القاعدة القطعية:</strong> ${r.golden_rule_ar}
              </p>
              <p class="trap-expl-text" style="color:var(--ps-amber); font-size:0.82rem; margin-top:-6px;">
                <strong>⚠️ الفخ الوزاري:</strong> ${r.why_trap_ar}
              </p>
            </div>

            <!-- زر فتح الأسئلة والكويز -->
            <button class="rule-action-btn" onclick="openTheoryRuleModal('${r.id}')">
              <span>⚡ تدريب على أسئلة القاعدة (${r.count || (r.questions ? r.questions.length : 0)} أسئلة)</span>
              <span>⬅</span>
            </button>
          </div>
        `;
      }).join('');
    }

    // -------------------------------------------------------------------------
    // 3. فتح نوافذ الاستعراض والكويز لقواعد الإشارات والنظري
    // -------------------------------------------------------------------------
    function openSignRuleModal(ruleId) {
      if (typeof RADAR_SIGN_TRAPS === 'undefined') return;
      const rule = RADAR_SIGN_TRAPS.find(r => r.id === ruleId);
      if (!rule) return;

      activeModalWord = {
        it: rule.keyword_it,
        ar: rule.title_ar,
        type: rule.type,
        rate: rule.rate,
        rule: rule.trap_ar,
        regex: (rule.keyword_it || "").split("/")[0].trim().replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')
      };
      activeModalQuestions = rule.questions || [];

      const icon = rule.type === 'falso' ? '🔴' : '🟢';
      document.getElementById("modalTitle").innerHTML = `
        <span>${icon} فخ إشارة:</span>
        <strong style="color:var(--ps-cyan);">${rule.title_ar}</strong>
      `;
      document.getElementById("modalSummaryText").innerHTML = `
        يتم الآن استعراض <strong>${activeModalQuestions.length} سؤالاً</strong> رسمياً على هذا الفخ (<strong style="color:${rule.type === 'falso' ? 'var(--ps-rose)' : 'var(--ps-emerald)'};">${rule.rate}</strong>)
      `;

      modalMode = 'browse';
      updateModalTabsUI();
      renderModalBody();

      document.getElementById("qModal").classList.add("open");
    }

    function openTheoryRuleModal(ruleId) {
      if (typeof RADAR_THEORY_RULES === 'undefined') return;
      const rule = RADAR_THEORY_RULES.find(r => r.id === ruleId);
      if (!rule) return;

      activeModalWord = {
        it: rule.keywords_it,
        ar: rule.title_ar,
        type: rule.type,
        rate: rule.rate,
        rule: rule.golden_rule_ar,
        regex: (rule.keywords_it || "").split("/")[0].trim().replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')
      };
      activeModalQuestions = rule.questions || [];

      const icon = rule.type === 'falso' ? '🔴' : '🟢';
      document.getElementById("modalTitle").innerHTML = `
        <span>${icon} قاعدة نظرية:</span>
        <strong style="color:var(--ps-cyan);">${rule.title_ar}</strong>
      `;
      document.getElementById("modalSummaryText").innerHTML = `
        يتم الآن استعراض <strong>${activeModalQuestions.length} سؤالاً</strong> رسمياً على هذه القاعدة (<strong style="color:${rule.type === 'falso' ? 'var(--ps-rose)' : 'var(--ps-emerald)'};">${rule.rate}</strong>)
      `;

      modalMode = 'browse';
      updateModalTabsUI();
      renderModalBody();

      document.getElementById("qModal").classList.add("open");
    }
"""

if 'function switchMainRadarTab' not in html:
    # Find the end of the script before </script>
    m = re.search(r'(</script>\s*</body>)', html)
    if m:
        html = html.replace(m.group(0), radar_js + '\n  ' + m.group(0))
        print("Injected Radar JavaScript logic successfully.")
    else:
        # Fallback to last </script>
        last_script_idx = html.rfind('</script>')
        html = html[:last_script_idx] + radar_js + '\n' + html[last_script_idx:]
        print("Injected Radar JavaScript logic before last script tag.")
else:
    print("switchMainRadarTab already exists in file.")

with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'w', encoding='utf-8') as f:
    f.write(html)

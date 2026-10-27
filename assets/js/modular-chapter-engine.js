/**
 * Patente B Pro - Modular Chapter Engine
 * Handles bite-sized chunking, collapsible accordions (collapsed by default),
 * interactive topic chips, and dual-theme study modes across all chapters.
 */

(function(window, document) {
  'use strict';

  const ModularChapterEngine = {
    data: null,
    groups: {},
    subtopicMap: {},
    userStats: { correct: 0, wrong: 0 },
    userAnswers: {}, // id -> { userChoice, isCorrect }
    masteredIds: new Set(), // ids solved correctly in part quiz
    mistakeIds: new Set(), // ids answered wrong in part quiz
    activeQuiz: null, // { gKey, questions: [], currentIndex: 0, results: [], isRetestOnly: false }
    currentFilter: 'all',
    activeGroupFilter: 'all',
    currentViewMode: 'grouped', // 'grouped' | 'flat'
    expandedSections: new Set(),
    isStudyMode: false,

    isUserLoggedIn() {
      if (typeof window !== 'undefined' && window.PatenteAuth && typeof window.PatenteAuth.isLoggedIn === 'function') {
        return window.PatenteAuth.isLoggedIn();
      }
      if (typeof window !== 'undefined' && window.localStorage) {
        return Boolean(window.localStorage.getItem('patente_user_profile'));
      }
      return false;
    },

    isChapterGated() {
      const chNum = (this.data && typeof this.data.numero === 'number') ? this.data.numero : 0;
      // Chapter 1 and 2 are 100% free; chapters 3 to 25 are gated for registered users
      return chNum > 2 && !this.isUserLoggedIn();
    },

    isQuestionLocked(q) {
      if (!this.isChapterGated()) return false;
      // Free sample: first 5 questions of this chapter
      const originalIndex = this.data.domande.findIndex(item => item.id === q.id);
      return originalIndex >= 5;
    },

    init(config) {
      if (!config || !config.data) {
        console.error('ModularChapterEngine: missing config.data');
        return;
      }
      this.data = config.data;
      this.groups = config.groups || {};
      this.subtopicMap = config.subtopicMap || {};

      // Load persisted progress from localStorage
      this.loadProgress();

      // Map each question to its unified group
      this.data.domande.forEach(q => {
        const rawSub = q.sotto_argomento ? q.sotto_argomento.trim() : '';
        q.gruppo_unificato = this.subtopicMap[rawSub] || rawSub || 'altro';
      });

      // Export globally for inline HTML events
      this.injectQuizStyles();
      this.bindGlobals();

      // Initial render
      this.renderHub();
      this.renderChips();
      this.renderQuestions();
      this.updateChapterProgress();
    },

    getStorageKey() {
      const id = (this.data && this.data.numero !== undefined) ? this.data.numero : (this.data && this.data.capitolo_id ? this.data.capitolo_id : 'default');
      return 'patente_progress_cap_' + id;
    },

    loadProgress() {
      try {
        if (typeof window === 'undefined' || !window.localStorage) return;
        const raw = window.localStorage.getItem(this.getStorageKey());
        if (!raw) return;
        const parsed = JSON.parse(raw);
        if (parsed && typeof parsed.userAnswers === 'object') {
          this.userAnswers = parsed.userAnswers || {};
          let c = 0, w = 0;
          Object.keys(this.userAnswers).forEach(qid => {
            const item = this.userAnswers[qid];
            if (item && item.isCorrect) c++;
            else if (item && item.isCorrect === false) w++;
          });
          this.userStats = { correct: c, wrong: w };
        }
        if (parsed && Array.isArray(parsed.masteredIds)) {
          this.masteredIds = new Set(parsed.masteredIds.map(Number));
        } else {
          this.masteredIds = new Set();
        }
        if (parsed && Array.isArray(parsed.mistakeIds)) {
          this.mistakeIds = new Set(parsed.mistakeIds.map(Number));
        } else {
          this.mistakeIds = new Set();
        }
      } catch (e) {
        console.warn('ModularChapterEngine: could not load progress from localStorage', e);
      }
    },

    saveProgress() {
      try {
        if (typeof window === 'undefined' || !window.localStorage) return;
        const payload = {
          userAnswers: this.userAnswers,
          userStats: this.userStats,
          masteredIds: Array.from(this.masteredIds),
          mistakeIds: Array.from(this.mistakeIds),
          updatedAt: Date.now()
        };
        window.localStorage.setItem(this.getStorageKey(), JSON.stringify(payload));
        if (typeof window.updatePortalProgress === 'function') {
          try { window.updatePortalProgress(); } catch (_) {}
        }
      } catch (e) {
        console.warn('ModularChapterEngine: could not save progress to localStorage', e);
      }
    },

    resetChapterProgress() {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      const confirmed = window.confirm('هل أنت متأكد من رغبتك في إعادة تعيين إنجاز هذا الباب لبدء المذاكرة من جديد؟');
      if (!confirmed) return;

      try {
        if (typeof window !== 'undefined' && window.localStorage) {
          window.localStorage.removeItem(this.getStorageKey());
        }
      } catch (e) {}

      this.userAnswers = {};
      this.userStats = { correct: 0, wrong: 0 };
      this.masteredIds.clear();
      this.mistakeIds.clear();

      this.renderHub();
      this.renderChips();
      this.renderQuestions();
      this.updateScoreDisplay();
      this.updateChapterProgress();
      if (typeof window.updatePortalProgress === 'function') {
        try { window.updatePortalProgress(); } catch (_) {}
      }
    },

    getOverallProgress() {
      const totalQuestions = this.data && this.data.domande ? this.data.domande.length : 0;
      let answeredCount = this.masteredIds.size;

      const groupKeys = Object.keys(this.groups);
      const totalGroups = groupKeys.length;
      let completedGroups = 0;

      groupKeys.forEach(gKey => {
        const groupQuestions = this.data.domande.filter(q => q.gruppo_unificato === gKey);
        const gTotal = groupQuestions.length;
        let gMastered = 0;
        groupQuestions.forEach(q => {
          if (this.masteredIds.has(q.id)) gMastered++;
        });
        if (gTotal > 0 && gMastered >= gTotal) completedGroups++;
      });

      const pct = totalQuestions > 0 ? Math.round((answeredCount / totalQuestions) * 100) : 0;

      return {
        totalQuestions,
        answeredCount,
        pct,
        totalGroups,
        completedGroups
      };
    },

    updateChapterProgress() {
      const progress = this.getOverallProgress();
      const fillEl = document.getElementById('chapter-progress-fill');
      const pctBadge = document.getElementById('chapter-progress-pct');
      const qMeta = document.getElementById('chapter-progress-q-meta');
      const gMeta = document.getElementById('chapter-progress-g-meta');

      if (fillEl) fillEl.style.width = `${progress.pct}%`;
      if (pctBadge) pctBadge.innerText = `${progress.pct}%`;
      if (qMeta) qMeta.innerText = `🎯 أُتقن: ${progress.answeredCount} من ${progress.totalQuestions} سؤالاً`;
      if (gMeta) gMeta.innerText = `🏆 أُتقن بالكامل: ${progress.completedGroups} من ${progress.totalGroups} قسماً`;
    },

    bindGlobals() {
      const self = this;
      window.answerQuestion = (id, choice) => self.answerQuestion(id, choice);
      window.toggleDrawer = (id) => self.toggleDrawer(id);
      window.setFilter = (f) => self.setFilter(f);
      window.filterQuestions = () => self.filterQuestions();
      window.toggleStudyMode = () => self.toggleStudyMode();
      window.selectSubtopicFilter = (key) => self.selectSubtopicFilter(key);
      window.setViewMode = (mode) => self.setViewMode(mode);
      window.toggleSubtopicSection = (key) => self.toggleSubtopicSection(key);
      window.expandAllSections = () => self.expandAllSections();
      window.collapseAllSections = () => self.collapseAllSections();
      window.resetChapterProgress = () => self.resetChapterProgress();
      window.renderQuestions = () => self.renderQuestions();
      window.startPartQuiz = (gKey, count) => self.startPartQuiz(gKey, count);
      window.closePartQuiz = () => self.closePartQuiz();
      window.answerPartQuiz = (choice) => self.answerPartQuiz(choice);
      window.retestPartMissed = (gKey) => self.retestPartMissed(gKey);

      window.addEventListener('patente:auth-changed', () => {
        self.renderHub();
        self.renderChips();
        self.renderQuestions();
      });
    },

    renderHub() {
      let hub = document.getElementById('subtopics-hub-card');
      const qList = document.getElementById('questions-list');
      if (!qList) return;

      // Update or create guest chapter sample banner for chapters 3 to 25
      let banner = document.getElementById('guestChapterBanner');
      const isGated = this.isChapterGated();
      if (isGated) {
        const totalQ = (this.data && this.data.domande) ? this.data.domande.length : 500;
        const bannerHtml = `
          <div class="sample-banner-text">
            <span>🎁</span>
            <span><strong>عينة مجانية:</strong> أنت تتصفح عينة مجانية تشمل أول 5 أسئلة مع الشرح وفك الفخاخ. الشرح الكامل لبنك أسئلة هذا الباب (${totalQ} سؤالاً) مخصص للطلاب المسجلين. سجّل حسابك المجاني في 10 ثوانٍ لفتح الباب بالكامل!</span>
          </div>
          <button class="sample-banner-btn" onclick="window.PatenteAuth && window.PatenteAuth.openAuthModal(true)">
            <span>🚀 فتح شرح الباب بالكامل مجاناً</span>
          </button>
        `;
        if (!banner) {
          banner = document.createElement('div');
          banner.id = 'guestChapterBanner';
          banner.className = 'guest-free-sample-banner';
          banner.style.margin = '0 0 18px 0';
          banner.style.borderRadius = '14px';
          banner.innerHTML = bannerHtml;
          const container = document.querySelector('.container') || document.body;
          container.insertBefore(banner, container.firstChild);
        } else {
          banner.innerHTML = bannerHtml;
          banner.style.display = 'flex';
        }
      } else if (banner) {
        banner.style.display = 'none';
      }

      const groupCount = Object.keys(this.groups).length || 1;
      const progress = this.getOverallProgress();

      const hubContent = `
        <div class="subtopics-hub-header">
          <div class="subtopics-hub-title-wrap">
            <span class="subtopics-hub-badge">📑 تقسيم دراسي ذكي</span>
            <span class="subtopics-hub-title">فهرس أجزاء الباب الـ ${groupCount} الموحدة (اختر قسماً للمذاكرة المركزة أو تصفح الكل)</span>
          </div>
          <div class="subtopics-hub-actions">
            <div class="view-mode-toggle-group">
              <button class="view-mode-btn active" id="btn-mode-grouped" onclick="setViewMode('grouped')" title="عرض مقسم لأقسام وبلوكات">
                <span>🗂️ عرض مقسم (${groupCount} قسماً)</span>
              </button>
              <button class="view-mode-btn" id="btn-mode-flat" onclick="setViewMode('flat')" title="عرض تقليدي متتالي">
                <span>📜 قائمة كاملة</span>
              </button>
            </div>
            <button class="subtopics-action-btn" onclick="expandAllSections()" title="توسيع كافة الأقسام">
              <span>➕ توسيع الكل</span>
            </button>
            <button class="subtopics-action-btn" onclick="collapseAllSections()" title="طي كافة الأقسام">
              <span>➖ طي الكل</span>
            </button>
          </div>
        </div>

        <div class="chapter-progress-strip" id="chapter-progress-strip">
          <div class="chapter-progress-top">
            <div class="chapter-progress-title">
              <span>📊 تقدم المذاكرة والإنجاز المحفوظ</span>
              <span class="chapter-progress-pct-badge" id="chapter-progress-pct">${progress.pct}%</span>
            </div>
            <div class="chapter-progress-meta">
              <span id="chapter-progress-q-meta">🎯 أُتقن: ${progress.answeredCount} من ${progress.totalQuestions} سؤالاً</span>
              <span id="chapter-progress-g-meta">🏆 أُتقن بالكامل: ${progress.completedGroups} من ${progress.totalGroups} قسماً</span>
              <button class="chapter-reset-btn" onclick="resetChapterProgress()" title="إعادة تعيين التقدم لهذا الباب">
                <span>🔄 تصفير الإنجاز</span>
              </button>
            </div>
          </div>
          <div class="chapter-progress-bar-track">
            <div class="chapter-progress-bar-fill" id="chapter-progress-fill" style="width: ${progress.pct}%;"></div>
          </div>
        </div>

        <div class="subtopics-chips-scroll" id="subtopics-chips-bar"></div>
      `;

      if (hub) {
        hub.innerHTML = hubContent;
      } else {
        hub = document.createElement('div');
        hub.className = 'subtopics-hub-card';
        hub.id = 'subtopics-hub-card';
        hub.innerHTML = hubContent;
        qList.parentNode.insertBefore(hub, qList);
      }
    },

    renderChips() {
      const bar = document.getElementById('subtopics-chips-bar');
      if (!bar) return;

      const counts = {};
      this.data.domande.forEach(q => {
        const g = q.gruppo_unificato;
        counts[g] = (counts[g] || 0) + 1;
      });

      const totalDomande = this.data.domande.length;
      const groupKeys = Object.keys(this.groups);
      const totalGroups = groupKeys.length;

      let html = `
        <button class="subtopic-chip ${this.activeGroupFilter === 'all' ? 'active' : ''}" onclick="selectSubtopicFilter('all')" title="عرض كل الأجزاء (${totalDomande} سؤالاً)">
          <span>🌐 كل الأجزاء (${totalGroups})</span>
          <span class="chip-count">${totalDomande}</span>
        </button>
      `;

      groupKeys.forEach(gKey => {
        const info = this.groups[gKey] || {};
        const count = counts[gKey] || 0;
        const isActive = (this.activeGroupFilter === gKey);
        const icon = info.icon || '📌';
        const num = info.num ? `${info.num}. ` : '';
        const label = info.short_ar || info.ar || gKey;

        // Check if group is fully mastered
        const groupQuestions = this.data.domande.filter(q => q.gruppo_unificato === gKey);
        let gMastered = 0;
        groupQuestions.forEach(q => {
          if (this.masteredIds.has(q.id)) gMastered++;
        });
        const isCompleted = (count > 0 && gMastered >= count);

        html += `
          <button class="subtopic-chip ${isActive ? 'active' : ''} ${isCompleted ? 'is-completed' : ''}" onclick="selectSubtopicFilter('${gKey}')" title="${info.ar || ''} (${info.it || ''})">
            <span>${isCompleted ? '✅' : icon} ${num}${label}</span>
            <span class="chip-count">${isCompleted ? 'مكتمل' : count}</span>
          </button>
        `;
      });

      bar.innerHTML = html;
    },

    selectSubtopicFilter(key) {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      this.activeGroupFilter = key;
      if (key !== 'all') {
        this.expandedSections.add(key);
      }
      this.renderChips();
      this.renderQuestions();

      if (key !== 'all') {
        const el = document.getElementById('questions-list');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    },

    setViewMode(mode) {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      this.currentViewMode = mode;
      const btnGrouped = document.getElementById('btn-mode-grouped');
      const btnFlat = document.getElementById('btn-mode-flat');
      if (btnGrouped) btnGrouped.classList.toggle('active', mode === 'grouped');
      if (btnFlat) btnFlat.classList.toggle('active', mode === 'flat');
      this.renderQuestions();
    },

    toggleSubtopicSection(gKey) {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      const secBox = document.getElementById(`subtopic-sec-${gKey}`);
      if (!secBox) return;
      if (this.expandedSections.has(gKey)) {
        this.expandedSections.delete(gKey);
        secBox.classList.add('is-collapsed');
      } else {
        this.expandedSections.add(gKey);
        secBox.classList.remove('is-collapsed');
      }
    },

    expandAllSections() {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      Object.keys(this.groups).forEach(k => this.expandedSections.add(k));
      document.querySelectorAll('.subtopic-section-box').forEach(box => {
        box.classList.remove('is-collapsed');
      });
    },

    collapseAllSections() {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      this.expandedSections.clear();
      document.querySelectorAll('.subtopic-section-box').forEach(box => {
        box.classList.add('is-collapsed');
      });
    },

    updateSubtopicProgress(gKey) {
      if (!gKey) return;
      const badge = document.getElementById(`sec-progress-${gKey}`);
      if (!badge) return;

      const groupQuestions = this.data.domande.filter(q => q.gruppo_unificato === gKey);
      const total = groupQuestions.length;
      let mastered = 0;
      groupQuestions.forEach(q => {
        if (this.masteredIds.has(q.id)) mastered++;
      });

      const isDone = (mastered >= total && total > 0);
      badge.className = `subtopic-stat-pill progress-pill ${isDone ? 'done' : ''}`;
      badge.innerText = `${isDone ? '🏆 إتقان كامل ' : '🎯 إتقان '}${mastered}/${total}`;
    },

    buildQuestionCardHtml(q) {
      const gInfo = this.groups[q.gruppo_unificato] || {};
      const subLabel = gInfo.short_ar ? `${gInfo.icon || '📌'} ${gInfo.num ? gInfo.num + '. ' : ''}${gInfo.short_ar}` : (q.sotto_argomento || '');

      if (this.isQuestionLocked(q)) {
        const totalCapQ = (this.data && this.data.domande) ? this.data.domande.length : 500;
        return `
          <div class="q-card locked-preview-card" onclick="window.PatenteAuth && window.PatenteAuth.showGateModal({ title: 'افتح شرح بنك أسئلة الباب بالكامل!', message: 'لقد شاهدت عينة مجانية تشمل أول 5 أسئلة مع الشرح الشامل وفك الفخاخ. أنشئ حسابك المجاني في 10 ثوانٍ لفتح جميع أسئلة هذا الباب (${totalCapQ} سؤالاً) وشروحاتها الحصرية وفك الشفرات بالكامل!' })">
            <div class="locked-preview-overlay">
              <div style="font-size:2.2rem; margin-bottom:8px;">🔒</div>
              <div style="font-weight:800; font-size:1rem; color:#FBBF24; margin-bottom:6px;">الشرح وفك الفخاخ متاح للطلاب المسجلين</div>
              <div style="font-size:0.8rem; color:#94A3B8; max-width:320px; line-height:1.5;">سؤال #${q.id} - ${subLabel}<br>انقر هنا لإنشاء حسابك المجاني ومتابعة الدراسة 🚀</div>
            </div>
            <div style="filter:blur(4px); opacity:0.3; pointer-events:none;">
              <div class="q-card-top">
                <span class="q-id-pill">#${q.id}</span>
                <span class="q-sub-badge">${subLabel}</span>
              </div>
              <div class="q-text-content">${q.domanda}</div>
              <div class="q-actions-row">
                <button class="btn-ans btn-ans-v"><span>VERO</span></button>
                <button class="btn-ans btn-ans-f"><span>FALSO</span></button>
              </div>
            </div>
          </div>
        `;
      }

      let imgHtml = '';
      if (q.immagine && q.immagine.trim() !== '') {
        imgHtml = `
          <div class="q-img-wrap">
            <img src="${q.immagine}" alt="Segnale" onclick="window.open(this.src, '_blank')" onerror="this.onerror=null; this.src='../../img_sign/' + this.src.split('/').pop()">
          </div>
        `;
      }

      const ans = this.userAnswers[q.id];
      let cardClass = 'q-card';
      let statusClass = 'status-tag';
      let statusText = '';
      if (ans) {
        if (ans.isCorrect) {
          cardClass += ' answered-correct';
          statusClass += ' ok';
          statusText = '✅ إجابة صحيحة';
        } else {
          cardClass += ' answered-wrong';
          statusClass += ' err';
          statusText = `❌ خطأ (الصحيح: ${q.risposta ? 'VERO' : 'FALSO'})`;
        }
      }


      return `
        <div class="${cardClass}" id="q-card-${q.id}">
          ${imgHtml}
          <div class="q-body">
            <div class="q-card-top">
              <span class="q-id-pill">#${q.id}</span>
              <span class="q-sub-badge">${subLabel}</span>
            </div>

            <div class="q-text-content">${q.domanda}</div>

            <div class="q-actions-row">
              <button class="btn-ans btn-ans-v ${ans && ans.userChoice === true ? 'selected' : ''}" onclick="answerQuestion(${q.id}, true)">
                <span>VERO</span>
              </button>
              <button class="btn-ans btn-ans-f ${ans && ans.userChoice === false ? 'selected' : ''}" onclick="answerQuestion(${q.id}, false)">
                <span>FALSO</span>
              </button>

              <span class="${statusClass}" id="status-${q.id}">${statusText}</span>
              <span class="study-badge-direct ${this.isStudyMode ? 'show' : ''} ${q.risposta ? 'is-v' : 'is-f'}" id="study-badge-${q.id}">
                ${q.risposta ? 'VERO ✅' : 'FALSO ❌'}
              </span>

              <button class="btn-explain-toggle" onclick="toggleDrawer(${q.id})">
                <span>💡 الترجمة والشرح وكشف الفخ</span>
              </button>
            </div>

            <div class="explain-drawer ${ans && !ans.isCorrect ? 'open' : ''}" id="drawer-${q.id}">
              <div class="ex-item"><strong>📖 الترجمة السياقية:</strong> ${q.traduzione || 'سؤال وزاري مباشر.'}</div>
              <div class="ex-item"><strong>💡 الشرح والقاعدة المرورية:</strong> ${q.spiegazione || 'مطابق لنصوص كود السير.'}</div>
              ${q.trabocchetto ? `<div class="trap-banner">${q.trabocchetto}</div>` : ''}
              ${window.questionDecoder ? window.questionDecoder.renderDecoderCard({ q: q.domanda, tr: q.traduzione, a: q.risposta, sp: q.spiegazione, tb: q.trabocchetto }, { collapsed: false }) : ''}
              ${q.parole_chiave && q.parole_chiave.length > 0 ? `
                <div class="kw-strip">
                  ${q.parole_chiave.map(k => {
                    if (typeof k === 'object' && k !== null) {
                      return `<span class="kw-pill"><strong>${k.it || ''}</strong>: ${k.ar || ''}</span>`;
                    }
                    if (typeof k === 'string') {
                      const m = k.match(/^([^(]+)\s*\(([^)]+)\)$/);
                      if (m) {
                        return `<span class="kw-pill"><strong>${m[1].trim()}</strong>: ${m[2].trim()}</span>`;
                      }
                      return `<span class="kw-pill">${k}</span>`;
                    }
                    return `<span class="kw-pill">${k}</span>`;
                  }).join('')}
                </div>
              ` : ''}
            </div>
          </div>
        </div>
      `;
    },

    renderQuestions() {
      const container = document.getElementById('questions-list');
      if (!container) return;
      container.innerHTML = '';
      const queryInput = document.getElementById('q-search');
      const query = (queryInput && queryInput.value) ? queryInput.value.toLowerCase().trim() : '';

      const filtered = this.data.domande.filter(q => {
        if (this.currentFilter === 'true' && !q.risposta) return false;
        if (this.currentFilter === 'false' && q.risposta) return false;
        if (this.activeGroupFilter !== 'all' && q.gruppo_unificato !== this.activeGroupFilter) return false;

        if (query !== '') {
          const qTextLower = (q.domanda || '').toLowerCase();
          const subLower = (q.sotto_argomento || '').toLowerCase();
          const trLower = (q.traduzione || '').toLowerCase();
          const gInfo = this.groups[q.gruppo_unificato];
          const gArLower = gInfo && gInfo.ar ? gInfo.ar.toLowerCase() : '';
          if (!qTextLower.includes(query) && !subLower.includes(query) && !trLower.includes(query) && !gArLower.includes(query)) {
            return false;
          }
        }
        return true;
      });

      if (this.activeGroupFilter !== 'all') {
        const info = this.groups[this.activeGroupFilter] || {};
        const banner = document.createElement('div');
        banner.className = 'single-subtopic-banner';
        const totalGroups = Object.keys(this.groups).length || 1;
        banner.innerHTML = `
          <div class="single-subtopic-banner-text">
            <span>🎯 أنت الآن في وضع المذاكرة المركزة على: <strong>${info.icon || '📌'} ${info.num ? info.num + '. ' : ''}${info.ar || this.activeGroupFilter}</strong> (${filtered.length} سؤال)</span>
          </div>
          <button class="single-subtopic-reset-btn" onclick="selectSubtopicFilter('all')">
            <span>عرض كافة الأقسام (${totalGroups} قسماً) ↺</span>
          </button>
        `;
        container.appendChild(banner);
      }

      if (filtered.length === 0) {
        container.innerHTML += `
          <div style="text-align:center; padding: 40px 20px; color: var(--text-muted); background: var(--bg-surface); border-radius: 16px; border: 1px solid var(--border-subtle); margin-top: 10px;">
            <div style="font-size:2rem; margin-bottom:8px;">🔍</div>
            <div style="font-size:1.05rem; font-weight:700; color:var(--text-primary, #fff);">لا توجد أسئلة مطابقة للبحث أو الفلتر المحدد</div>
            <div style="font-size:0.85rem; margin-top:6px;">جرّب تعديل كلمات البحث أو اختيار فلتر "الكل".</div>
          </div>
        `;
        this.updateScoreDisplay();
        return;
      }

      if (this.currentViewMode === 'flat') {
        const wrapper = document.createElement('div');
        wrapper.className = 'flat-questions-wrap';
        wrapper.innerHTML = filtered.map(q => this.buildQuestionCardHtml(q)).join('');
        container.appendChild(wrapper);
      } else {
        // Group by gruppo_unificato
        const groupsMap = new Map();
        filtered.forEach(q => {
          const gKey = q.gruppo_unificato || 'altro';
          if (!groupsMap.has(gKey)) groupsMap.set(gKey, []);
          groupsMap.get(gKey).push(q);
        });

        const totalGroupsCount = Object.keys(this.groups).length || 1;

        groupsMap.forEach((questions, gKey) => {
          const info = this.groups[gKey] || {
            num: '•',
            short_ar: gKey,
            ar: gKey,
            it: gKey,
            icon: '📌',
            group: 'القسم'
          };

          const totalInSub = questions.length;
          const vCount = questions.filter(q => q.risposta).length;
          const fCount = totalInSub - vCount;

          let answeredInSub = 0;
          let masteredInSub = 0;
          questions.forEach(q => {
            if (this.userAnswers[q.id]) answeredInSub++;
            if (this.masteredIds.has(q.id)) masteredInSub++;
          });

          const isExpanded = (query !== '') || (this.activeGroupFilter !== 'all') || this.expandedSections.has(gKey);
          const isCollapsed = !isExpanded;
          const isMasteredDone = (masteredInSub >= totalInSub && totalInSub > 0);

          let quizBtnHtml = '';
          if (totalInSub <= 6) {
            quizBtnHtml = `
              <button class="btn-part-quiz-trigger" onclick="startPartQuiz('${gKey}', ${totalInSub})" title="امتحان عشوائي على كافة أسئلة الجزء (${totalInSub} أسئلة)">
                <span>⚡ كويز الجزء (${totalInSub} أسئلة)</span>
              </button>
            `;
          } else {
            quizBtnHtml = `
              <button class="btn-part-quiz-trigger" onclick="startPartQuiz('${gKey}', 5)" title="كويز سريع: 5 أسئلة عشوائية بالأولوية">
                <span>⚡ كويز سريع (5Q)</span>
              </button>
              <button class="btn-part-quiz-trigger full" onclick="startPartQuiz('${gKey}', ${totalInSub})" title="اختبار شامل لكافة أسئلة هذا الجزء">
                <span>🎯 اختبار الجزء</span>
              </button>
            `;
          }

          const secBox = document.createElement('div');
          secBox.className = `subtopic-section-box ${isCollapsed ? 'is-collapsed' : ''}`;
          secBox.id = `subtopic-sec-${gKey}`;

          secBox.innerHTML = `
            <div class="subtopic-section-header" onclick="toggleSubtopicSection('${gKey}')">
              <div class="subtopic-header-main">
                <div class="subtopic-header-icon">${info.icon || '📌'}</div>
                <div class="subtopic-header-text">
                  <div class="subtopic-meta-line">
                    <span class="subtopic-num-pill">الجزء ${info.num || '•'} من ${totalGroupsCount}</span>
                    <span class="subtopic-group-pill">${info.group || 'القسم'}</span>
                  </div>
                  <div class="subtopic-ar-heading">${info.ar || gKey}</div>
                  <div class="subtopic-it-heading">${info.it || ''}</div>
                </div>
              </div>

              <div class="subtopic-header-stats">
                <span class="subtopic-stat-pill">
                  <strong>${totalInSub}</strong> أسئلة
                </span>
                <span class="subtopic-stat-pill vf">
                  <span style="color:#10b981;">${vCount} V</span> • <span style="color:#ef4444;">${fCount} F</span>
                </span>
                <span class="subtopic-stat-pill progress-pill ${isMasteredDone ? 'done' : ''}" id="sec-progress-${gKey}">
                  ${isMasteredDone ? '🏆 إتقان كامل ' : '🎯 إتقان '}${masteredInSub}/${totalInSub}
                </span>
                <div class="part-quiz-actions-wrap" onclick="event.stopPropagation()">
                  ${quizBtnHtml}
                </div>
                ${this.activeGroupFilter === 'all' ? `
                  <button class="subtopic-focus-btn" onclick="event.stopPropagation(); selectSubtopicFilter('${gKey}')">
                    🎯 مذاكرة هذا الجزء
                  </button>
                ` : ''}
                <span class="subtopic-chevron">▼</span>
              </div>
            </div>

            <div class="subtopic-section-body">
              ${questions.map(q => this.buildQuestionCardHtml(q)).join('')}
            </div>
          `;

          container.appendChild(secBox);
        });
      }

      this.updateScoreDisplay();
    },

    answerQuestion(id, userChoice) {
      const q = this.data.domande.find(item => item.id === id);
      if (!q) return;

      if (this.isQuestionLocked(q)) {
        if (window.PatenteAuth && window.PatenteAuth.showGateModal) {
          const totalCapQ = (this.data && this.data.domande) ? this.data.domande.length : 500;
          window.PatenteAuth.showGateModal({
            title: 'افتح شرح بنك أسئلة الباب بالكامل!',
            message: 'لقد شاهدت عينة مجانية تشمل أول 5 أسئلة مع الشرح وفك الفخاخ. أنشئ حسابك المجاني في 10 ثوانٍ لفتح جميع أسئلة هذا الباب (' + totalCapQ + ' سؤالاً) وشروحاتها وتفكيك الفخاخ بالكامل!'
          });
        }
        return;
      }

      const isCorrect = (userChoice === q.risposta);
      const wasAnswered = !!this.userAnswers[id];
      const prevCorrect = wasAnswered ? this.userAnswers[id].isCorrect : null;

      if (!wasAnswered) {
        if (isCorrect) this.userStats.correct++;
        else this.userStats.wrong++;
      } else {
        if (prevCorrect !== isCorrect) {
          if (isCorrect) { this.userStats.correct++; this.userStats.wrong--; }
          else { this.userStats.wrong++; this.userStats.correct--; }
        }
      }

      this.userAnswers[id] = { userChoice, isCorrect };

      const card = document.getElementById(`q-card-${id}`);
      const tag = document.getElementById(`status-${id}`);

      if (card) {
        const btnV = card.querySelector('.btn-ans-v');
        const btnF = card.querySelector('.btn-ans-f');
        if (btnV) btnV.classList.toggle('selected', userChoice === true);
        if (btnF) btnF.classList.toggle('selected', userChoice === false);
      }

      if (isCorrect) {
        if (window.soundEngine && window.soundEngine.correct) window.soundEngine.correct();
        if (tag) {
          tag.className = 'status-tag ok';
          tag.innerText = '✅ إجابة صحيحة';
        }
        if (card) {
          card.classList.remove('answered-wrong');
          card.classList.add('answered-correct');
        }
      } else {
        if (window.soundEngine && window.soundEngine.wrong) window.soundEngine.wrong();
        if (tag) {
          tag.className = 'status-tag err';
          tag.innerText = `❌ خطأ (الصحيح: ${q.risposta ? 'VERO' : 'FALSO'})`;
        }
        if (card) {
          card.classList.remove('answered-correct');
          card.classList.add('answered-wrong');
        }
        const drawer = document.getElementById(`drawer-${id}`);
        if (drawer) drawer.classList.add('open');
      }

      this.saveProgress();
      this.updateSubtopicProgress(q.gruppo_unificato);
      this.updateScoreDisplay();
      this.updateChapterProgress();
      if (typeof window.updatePortalProgress === 'function') {
        try { window.updatePortalProgress(); } catch (_) {}
      }
      this.renderChips();
    },

    toggleDrawer(id) {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      const drawer = document.getElementById(`drawer-${id}`);
      if (drawer) drawer.classList.toggle('open');
    },

    setFilter(f) {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      this.currentFilter = f;
      document.querySelectorAll('.f-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.f === f);
      });
      this.renderQuestions();
    },

    filterQuestions() {
      this.renderQuestions();
    },

    toggleStudyMode() {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      const toggle = document.getElementById('study-mode-toggle');
      this.isStudyMode = toggle ? toggle.checked : false;
      document.querySelectorAll('.study-badge-direct').forEach(b => {
        b.classList.toggle('show', this.isStudyMode);
      });
    },


    // =========================================================
    // Part Quiz Engine (Smart Priority-Based In-Place Mastery)
    // =========================================================
    startPartQuiz(gKey, reqCount) {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      
      let questionsInGroup = this.data.domande.filter(q => q.gruppo_unificato === gKey);
      if (!questionsInGroup.length) return;

      if (this.isChapterGated()) {
        const available = questionsInGroup.filter(q => !this.isQuestionLocked(q));
        if (available.length === 0) {
          if (window.PatenteAuth && window.PatenteAuth.showGateModal) {
            window.PatenteAuth.showGateModal({
              title: 'كويزات الإتقان مخصصة للطلاب المسجلين!',
              message: 'اختبارات الإتقان الذكية وحفظ تقدم الأجزاء متاحة للطلاب المسجلين. سجّل حسابك المجاني في 10 ثوانٍ لفتح جميع كويزات هذا الباب!'
            });
          }
          return;
        }
        questionsInGroup = available;
      }

      // Priority Sampling:
      // Priority 1: Unmastered questions (never answered correctly in quiz)
      const unmastered = questionsInGroup.filter(q => !this.masteredIds.has(q.id));
      // Priority 2: Missed questions (currently in mistakeIds)
      const mistakes = questionsInGroup.filter(q => this.mistakeIds.has(q.id));
      // Priority 3: Mastered questions (for spaced review)
      const mastered = questionsInGroup.filter(q => this.masteredIds.has(q.id));

      // Shuffle helper (Fisher-Yates)
      const shuffle = (arr) => {
        const a = [...arr];
        for (let i = a.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [a[i], a[j]] = [a[j], a[i]];
        }
        return a;
      };

      const shuffledUnmastered = shuffle(unmastered);
      const shuffledMistakes = shuffle(mistakes.filter(q => !unmastered.includes(q)));
      const shuffledMastered = shuffle(mastered);

      // Build ordered priority list
      let pool = [...shuffledUnmastered, ...shuffledMistakes, ...shuffledMastered];

      // De-duplicate
      const seen = new Set();
      pool = pool.filter(q => {
        if (seen.has(q.id)) return false;
        seen.add(q.id);
        return true;
      });

      const count = Math.min(reqCount || pool.length, pool.length);
      const selected = pool.slice(0, count);

      this.activeQuiz = {
        gKey,
        questions: selected,
        currentIndex: 0,
        results: [], // { question, userChoice, isCorrect }
        isRetestOnly: false
      };

      this.injectQuizStyles();
      this.renderQuizModal();
    },

    retestPartMissed(gKey) {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      if (!this.activeQuiz || !this.activeQuiz.results) return;

      const missedQuestions = this.activeQuiz.results
        .filter(r => !r.isCorrect)
        .map(r => r.question);

      if (!missedQuestions.length) return;

      // Shuffle missed questions
      for (let i = missedQuestions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [missedQuestions[i], missedQuestions[j]] = [missedQuestions[j], missedQuestions[i]];
      }

      this.activeQuiz = {
        gKey,
        questions: missedQuestions,
        currentIndex: 0,
        results: [],
        isRetestOnly: true
      };

      this.renderQuizModal();
    },

    closePartQuiz() {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      const modal = document.getElementById('partQuizModal');
      if (modal) {
        modal.classList.remove('open');
        setTimeout(() => modal.remove(), 250);
      }
      this.activeQuiz = null;
      document.body.classList.remove('quiz-modal-open');
    },

    answerPartQuiz(userChoice) {
      if (!this.activeQuiz) return;
      const curIdx = this.activeQuiz.currentIndex;
      const q = this.activeQuiz.questions[curIdx];
      if (!q) return;

      const isCorrect = (userChoice === q.risposta);

      // Play sound
      if (isCorrect) {
        if (window.soundEngine && window.soundEngine.correct) window.soundEngine.correct();
      } else {
        if (window.soundEngine && window.soundEngine.wrong) window.soundEngine.wrong();
      }

      // Record result
      this.activeQuiz.results.push({
        question: q,
        userChoice,
        isCorrect
      });

      // Update Mastery & Mistakes
      if (isCorrect) {
        this.masteredIds.add(q.id);
        this.mistakeIds.delete(q.id);
      } else {
        this.mistakeIds.add(q.id);
      }

      // Record answer in userAnswers for chapter stats
      this.userAnswers[q.id] = { userChoice, isCorrect };

      // Advance
      this.activeQuiz.currentIndex++;

      if (this.activeQuiz.currentIndex >= this.activeQuiz.questions.length) {
        // Quiz Finished!
        this.finishPartQuiz();
      } else {
        // Render next question with micro-animation
        this.renderQuizModal();
      }
    },

    finishPartQuiz() {
      // Save progress to persist new masteredIds and mistakeIds
      this.saveProgress();
      this.renderHub();
      this.renderChips();
      this.renderQuestions();
      this.updateChapterProgress();

      const modal = document.getElementById('partQuizModal');
      if (!modal) return;

      const total = this.activeQuiz.questions.length;
      const correctCount = this.activeQuiz.results.filter(r => r.isCorrect).length;
      const wrongCount = total - correctCount;
      const pct = Math.round((correctCount / total) * 100);
      const isPerfect = (correctCount === total);

      const info = this.groups[this.activeQuiz.gKey] || {};
      const partName = `${info.icon || '📌'} ${info.num ? info.num + '. ' : ''}${info.ar || this.activeQuiz.gKey}`;

      // Calculate part mastery stats
      const questionsInGroup = this.data.domande.filter(q => q.gruppo_unificato === this.activeQuiz.gKey);
      const totalPartQ = questionsInGroup.length;
      let partMastered = 0;
      questionsInGroup.forEach(q => {
        if (this.masteredIds.has(q.id)) partMastered++;
      });
      const partPct = Math.round((partMastered / totalPartQ) * 100);

      const resultsHtml = `
        <div class="quiz-modal-card quiz-results-card">
          <div class="quiz-results-header">
            <div style="font-size:2.8rem; line-height:1; margin-bottom:8px;">${isPerfect ? '🏆' : (pct >= 80 ? '🎉' : (pct >= 50 ? '👍' : '💪'))}</div>
            <div class="quiz-results-title">${isPerfect ? 'إتقان تام ومبهر!' : (pct >= 80 ? 'أداء ممتاز جداً!' : (pct >= 50 ? 'محاولة جيدة، واصل التقدم!' : 'بداية طيبة، كرّر لتثبيت المفاهيم!'))}</div>
            <div class="quiz-results-subtitle">نتيجة كويز: <strong>${partName}</strong></div>
          </div>

          <div class="quiz-score-badge-row">
            <div class="quiz-score-box ${isPerfect ? 'perfect' : (pct >= 80 ? 'high' : 'normal')}">
              <span class="quiz-score-val">${correctCount} / ${total}</span>
              <span class="quiz-score-lbl">الإجابات الصحيحة (${pct}%)</span>
            </div>
            <div class="quiz-score-box part-progress">
              <span class="quiz-score-val" style="color:#10B981;">${partMastered} / ${totalPartQ}</span>
              <span class="quiz-score-lbl">إجمالي إتقان الجزء (${partPct}%)</span>
            </div>
          </div>

          <!-- شريط تقدم الجزء بعد التحديث -->
          <div style="margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:700; margin-bottom:6px;">
              <span>مؤشر إتقان هذا الجزء</span>
              <span style="color:#10B981;">${partPct}%</span>
            </div>
            <div class="quiz-progress-bar-track" style="height:8px; border-radius:99px; background:rgba(255,255,255,0.08); overflow:hidden;">
              <div style="height:100%; width:${partPct}%; background:linear-gradient(90deg, #10B981, #059669); border-radius:99px; transition:width 0.4s ease;"></div>
            </div>
          </div>

          ${wrongCount > 0 ? `
            <div class="quiz-mistakes-container">
              <div class="quiz-mistakes-header">
                <span>⚠️ الأسئلة التي تحتاج لمراجعة (${wrongCount}):</span>
                <span style="font-size:0.75rem; color:#94A3B8;">تم نقلها لبنك أخطائك للتركيز عليها</span>
              </div>
              <div class="quiz-mistakes-list">
                ${this.activeQuiz.results.filter(r => !r.isCorrect).map(r => `
                  <div class="quiz-mistake-item">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                      <span class="q-id-pill">#${r.question.id}</span>
                      <span style="font-size:0.78rem; font-weight:700; color:#EF4444;">إجابتك: ${r.userChoice ? 'VERO' : 'FALSO'} • الصحيح: ${r.question.risposta ? 'VERO' : 'FALSO'}</span>
                    </div>
                    <div style="font-size:0.88rem; font-weight:700; color:var(--text-primary, #FFF); line-height:1.4; margin-bottom:4px;">${r.question.domanda}</div>
                    <div style="font-size:0.8rem; color:#94A3B8; line-height:1.4;">📖 ${r.question.traduzione || ''}</div>
                    ${r.question.trabocchetto ? `<div class="trap-banner" style="margin-top:6px; padding:6px 10px; font-size:0.78rem;">💡 ${r.question.trabocchetto}</div>` : ''}
                  </div>
                `).join('')}
              </div>
            </div>
          ` : `
            <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:12px; padding:14px; text-align:center; color:#34D399; font-weight:700; margin-bottom:18px;">
              ✨ رائع! لم ترتكب أي خطأ في هذا الكويز. لقد ثبّت معلومات هذا الجزء في ذاكرتك بنجاح!
            </div>
          `}

          <div class="quiz-results-actions">
            ${wrongCount > 0 ? `
              <button class="btn-quiz-action retest" onclick="retestPartMissed('${this.activeQuiz.gKey}')">
                <span>🔄 اختبرني في الأخطاء فقط (${wrongCount})</span>
              </button>
            ` : ''}
            <button class="btn-quiz-action repeat" onclick="startPartQuiz('${this.activeQuiz.gKey}', ${total})">
              <span>⚡ إعادة الكويز بأسئلة أخرى</span>
            </button>
            <button class="btn-quiz-action finish" onclick="closePartQuiz()">
              <span>📖 العودة لصفحة الباب</span>
            </button>
          </div>
        </div>
      `;

      modal.innerHTML = resultsHtml;
    },

    renderQuizModal() {
      if (!this.activeQuiz) return;
      const curIdx = this.activeQuiz.currentIndex;
      const total = this.activeQuiz.questions.length;
      const q = this.activeQuiz.questions[curIdx];
      if (!q) return;

      let modal = document.getElementById('partQuizModal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'partQuizModal';
        modal.className = 'part-quiz-modal-backdrop';
        document.body.appendChild(modal);
        requestAnimationFrame(() => modal.classList.add('open'));
      }
      document.body.classList.add('quiz-modal-open');

      const info = this.groups[this.activeQuiz.gKey] || {};
      const partName = `${info.icon || '📌'} ${info.num ? info.num + '. ' : ''}${info.ar || this.activeQuiz.gKey}`;
      const pct = Math.round(((curIdx) / total) * 100);

      let imgHtml = '';
      if (q.immagine && q.immagine.trim() !== '') {
        imgHtml = `
          <div class="quiz-modal-img-wrap">
            <img src="${q.immagine}" alt="Segnale" onerror="this.onerror=null; this.src='../../img_sign/' + this.src.split('/').pop()">
          </div>
        `;
      }

      modal.innerHTML = `
        <div class="quiz-modal-card">
          <!-- Header: Clean Left-to-Right Balanced Layout -->
          <div class="quiz-modal-topbar">
            <div class="quiz-modal-part-info">
              <span class="quiz-modal-part-badge">⚡ كويز الجزء</span>
              <span class="quiz-modal-part-name" title="${escapeHtml(partName)}">${escapeHtml(partName)}</span>
            </div>
            <button class="quiz-modal-close-btn" onclick="closePartQuiz()" aria-label="إغلاق" title="إغلاق الكويز">✕</button>
          </div>

          <!-- Progress Strip: Fixed LTR direction for correct 0% to 100% reading -->
          <div class="quiz-modal-prog-wrap">
            <div class="quiz-modal-prog-text">
              <span class="prog-q-num">السؤال <strong>${curIdx + 1}</strong> من <strong>${total}</strong></span>
              <span class="prog-pct-num">${pct}% مكتمل</span>
            </div>
            <div class="quiz-modal-prog-track">
              <div class="quiz-modal-prog-fill" style="width:${pct}%;"></div>
            </div>
          </div>

          <!-- Question Content -->
          <div class="quiz-modal-q-body">
            ${imgHtml}
            <div class="quiz-modal-q-text">
              ${escapeHtml(q.domanda)}
            </div>
            <div class="quiz-modal-q-tr">
              ${escapeHtml(q.traduzione || '')}
            </div>
          </div>

          <!-- Action Buttons: VERO on Right, FALSO on Left (Standard Natural Driving Exam Ergonomics) -->
          <div class="quiz-modal-actions-row">
            <button class="btn-quiz-choice vero" onclick="answerPartQuiz(true)">
              <span class="choice-icon">✔</span>
              <span class="choice-lbl">VERO</span>
              <span class="choice-sub">صحيح</span>
            </button>
            <button class="btn-quiz-choice falso" onclick="answerPartQuiz(false)">
              <span class="choice-icon">✖</span>
              <span class="choice-lbl">FALSO</span>
              <span class="choice-sub">خطأ</span>
            </button>
          </div>
        </div>
      `;
    },

    injectQuizStyles() {
      if (document.getElementById('part-quiz-injected-styles')) return;
      const s = document.createElement('style');
      s.id = 'part-quiz-injected-styles';
      s.textContent = `
        /* =========================================================
           Part Quiz (Active Mastery) Modal & Mobile-First Styling
           ========================================================= */
        body.quiz-modal-open {
          overflow: hidden !important;
          touch-action: none !important;
        }
        .part-quiz-modal-backdrop {
          position: fixed;
          inset: 0;
          background: rgba(11, 15, 25, 0.88);
          backdrop-filter: blur(20px);
          -webkit-backdrop-filter: blur(20px);
          z-index: 100000;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 16px;
          opacity: 0;
          visibility: hidden;
          transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.22s;
          direction: rtl;
        }
        .part-quiz-modal-backdrop.open {
          opacity: 1;
          visibility: visible;
        }
        .quiz-modal-card {
          width: 100%;
          max-width: 620px;
          background: #111827;
          border: 1px solid rgba(255, 255, 255, 0.14);
          border-radius: 24px;
          box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.85), 0 0 0 1px rgba(255, 255, 255, 0.05);
          padding: 24px 26px 28px;
          max-height: 92vh;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
          color: #F8FAFC;
          font-family: 'Plus Jakarta Sans', 'Cairo', system-ui, -apple-system, sans-serif;
          position: relative;
          transform: translateY(14px) scale(0.97);
          transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        html.light .quiz-modal-card {
          background: #FFFFFF;
          border-color: rgba(15, 23, 42, 0.12);
          box-shadow: 0 25px 60px -12px rgba(15, 23, 42, 0.22), 0 4px 12px rgba(15, 23, 42, 0.06);
          color: #0F172A;
        }
        .part-quiz-modal-backdrop.open .quiz-modal-card {
          transform: translateY(0) scale(1);
        }

        /* Topbar Header */
        .quiz-modal-topbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
          padding-bottom: 14px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          margin-bottom: 16px;
        }
        html.light .quiz-modal-topbar {
          border-bottom-color: rgba(15, 23, 42, 0.08);
        }
        .quiz-modal-part-info {
          display: flex;
          align-items: center;
          gap: 10px;
          min-width: 0;
          flex: 1;
        }
        .quiz-modal-part-badge {
          background: rgba(99, 102, 241, 0.15);
          color: #818CF8;
          border: 1px solid rgba(99, 102, 241, 0.3);
          border-radius: 8px;
          font-size: 0.74rem;
          font-weight: 800;
          padding: 3px 9px;
          white-space: nowrap;
          flex-shrink: 0;
        }
        html.light .quiz-modal-part-badge {
          background: rgba(99, 102, 241, 0.08);
          color: #4F46E5;
          border-color: rgba(99, 102, 241, 0.25);
        }
        .quiz-modal-part-name {
          font-size: 0.92rem;
          font-weight: 800;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          color: inherit;
        }
        .quiz-modal-close-btn {
          width: 34px;
          height: 34px;
          border-radius: 10px;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: #94A3B8;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.95rem;
          font-weight: 700;
          transition: all 0.18s ease;
          flex-shrink: 0;
        }
        html.light .quiz-modal-close-btn {
          background: rgba(15, 23, 42, 0.05);
          border-color: rgba(15, 23, 42, 0.1);
          color: #475569;
        }
        .quiz-modal-close-btn:hover {
          background: rgba(239, 68, 68, 0.15);
          color: #EF4444;
          border-color: rgba(239, 68, 68, 0.3);
          transform: rotate(90deg);
        }

        /* Progress Wrap with Clean LTR/RTL Geometry */
        .quiz-modal-prog-wrap {
          margin-bottom: 22px;
        }
        .quiz-modal-prog-text {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 0.82rem;
          font-weight: 700;
          margin-bottom: 8px;
        }
        .prog-q-num {
          color: var(--text-primary, inherit);
        }
        .prog-pct-num {
          font-family: 'JetBrains Mono', monospace;
          color: #38BDF8;
          font-size: 0.86rem;
          font-weight: 800;
        }
        html.light .prog-pct-num {
          color: #0284C7;
        }
        .quiz-modal-prog-track {
          width: 100%;
          height: 7px;
          background: rgba(255, 255, 255, 0.08);
          border-radius: 99px;
          overflow: hidden;
          direction: ltr; /* Fills smoothly left to right */
        }
        html.light .quiz-modal-prog-track {
          background: rgba(15, 23, 42, 0.08);
        }
        .quiz-modal-prog-fill {
          height: 100%;
          background: linear-gradient(90deg, #6366F1, #10B981);
          border-radius: 99px;
          transition: width 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* Question Body Typography */
        .quiz-modal-q-body {
          margin-bottom: 26px;
        }
        .quiz-modal-img-wrap {
          text-align: center;
          margin-bottom: 18px;
        }
        .quiz-modal-img-wrap img {
          max-height: 150px;
          max-width: 100%;
          border-radius: 14px;
          background: #FFFFFF;
          padding: 8px;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }
        .quiz-modal-q-text {
          font-size: 1.22rem;
          font-weight: 800;
          line-height: 1.55;
          margin-bottom: 12px;
          direction: ltr;
          text-align: left;
          color: #FFFFFF;
          letter-spacing: -0.01em;
        }
        html.light .quiz-modal-q-text {
          color: #0F172A;
        }
        .quiz-modal-q-tr {
          font-size: 0.94rem;
          color: #94A3B8;
          line-height: 1.65;
          direction: rtl;
          text-align: right;
          font-weight: 500;
        }
        html.light .quiz-modal-q-tr {
          color: #475569;
        }

        /* Action Buttons: Ergonomic Grid */
        .quiz-modal-actions-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 14px;
        }
        .btn-quiz-choice {
          height: 64px;
          border-radius: 16px;
          border: 1.5px solid transparent;
          cursor: pointer;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
          font-family: inherit;
          user-select: none;
          -webkit-tap-highlight-color: transparent;
        }
        .btn-quiz-choice:active {
          transform: scale(0.97);
        }
        .btn-quiz-choice.vero {
          background: rgba(16, 185, 129, 0.12);
          border-color: rgba(16, 185, 129, 0.38);
          color: #34D399;
        }
        html.light .btn-quiz-choice.vero {
          background: rgba(16, 185, 129, 0.08);
          border-color: rgba(16, 185, 129, 0.38);
          color: #059669;
        }
        .btn-quiz-choice.vero:hover {
          background: #10B981;
          color: #FFFFFF;
          border-color: #10B981;
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(16, 185, 129, 0.35);
        }
        .btn-quiz-choice.falso {
          background: rgba(239, 68, 68, 0.12);
          border-color: rgba(239, 68, 68, 0.38);
          color: #F87171;
        }
        html.light .btn-quiz-choice.falso {
          background: rgba(239, 68, 68, 0.08);
          border-color: rgba(239, 68, 68, 0.38);
          color: #DC2626;
        }
        .btn-quiz-choice.falso:hover {
          background: #EF4444;
          color: #FFFFFF;
          border-color: #EF4444;
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(239, 68, 68, 0.35);
        }
        .choice-icon {
          font-size: 1.1rem;
          line-height: 1;
          margin-bottom: 2px;
        }
        .choice-lbl {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.2rem;
          font-weight: 900;
          line-height: 1.1;
        }
        .choice-sub {
          font-size: 0.72rem;
          font-weight: 700;
          opacity: 0.85;
        }

        /* Results Card */
        .quiz-results-card {
          text-align: center;
        }
        .quiz-results-header {
          margin-bottom: 20px;
        }
        .quiz-results-title {
          font-size: 1.4rem;
          font-weight: 900;
          color: #F8FAFC;
          margin-bottom: 4px;
        }
        html.light .quiz-results-title {
          color: #0F172A;
        }
        .quiz-results-subtitle {
          font-size: 0.88rem;
          color: #94A3B8;
        }
        html.light .quiz-results-subtitle {
          color: #64748B;
        }

        .quiz-score-badge-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 12px;
          margin-bottom: 20px;
        }
        .quiz-score-box {
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 16px;
          padding: 14px;
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        html.light .quiz-score-box {
          background: rgba(15, 23, 42, 0.03);
          border-color: rgba(15, 23, 42, 0.08);
        }
        .quiz-score-val {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.45rem;
          font-weight: 900;
          color: #38BDF8;
          line-height: 1.2;
        }
        .quiz-score-box.perfect .quiz-score-val {
          color: #10B981;
        }
        .quiz-score-lbl {
          font-size: 0.74rem;
          color: #94A3B8;
          font-weight: 700;
          margin-top: 4px;
        }
        html.light .quiz-score-lbl {
          color: #64748B;
        }

        .quiz-mistakes-container {
          background: rgba(239, 68, 68, 0.05);
          border: 1px solid rgba(239, 68, 68, 0.2);
          border-radius: 14px;
          padding: 14px;
          text-align: right;
          margin-bottom: 20px;
          max-height: 240px;
          overflow-y: auto;
        }
        .quiz-mistakes-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 0.82rem;
          font-weight: 800;
          color: #F87171;
          margin-bottom: 10px;
          padding-bottom: 6px;
          border-bottom: 1px solid rgba(239, 68, 68, 0.15);
        }
        .quiz-mistake-item {
          padding: 10px 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .quiz-mistake-item:last-child {
          border-bottom: none;
        }
        html.light .quiz-mistakes-header {
          color: #DC2626;
          border-bottom-color: rgba(220, 38, 38, 0.2);
        }
        html.light .quiz-mistake-item {
          border-bottom-color: rgba(15, 23, 42, 0.08);
        }

        .quiz-results-actions {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .btn-quiz-action {
          width: 100%;
          height: 46px;
          border-radius: 12px;
          font-weight: 800;
          font-size: 0.9rem;
          cursor: pointer;
          border: none;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          font-family: inherit;
          transition: all 0.2s ease;
        }
        .btn-quiz-action.retest {
          background: #EF4444;
          color: #FFFFFF;
          box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
        }
        .btn-quiz-action.retest:hover {
          background: #DC2626;
          transform: translateY(-1px);
        }
        .btn-quiz-action.repeat {
          background: rgba(56, 189, 248, 0.15);
          border: 1px solid rgba(56, 189, 248, 0.3);
          color: #38BDF8;
        }
        html.light .btn-quiz-action.repeat {
          background: rgba(2, 132, 199, 0.08);
          color: #0284C7;
          border-color: rgba(2, 132, 199, 0.25);
        }
        .btn-quiz-action.finish {
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: #CBD5E1;
        }
        html.light .btn-quiz-action.finish {
          background: rgba(15, 23, 42, 0.05);
          color: #334155;
          border-color: rgba(15, 23, 42, 0.1);
        }
        .btn-quiz-action:hover {
          transform: translateY(-1px);
        }

        /* Buttons in Section Header */
        .part-quiz-actions-wrap {
          display: inline-flex;
          align-items: center;
          gap: 6px;
        }
        .btn-part-quiz-trigger {
          height: 30px;
          display: inline-flex;
          align-items: center;
          gap: 4px;
          padding: 0 11px;
          border-radius: 8px;
          background: rgba(99, 102, 241, 0.15);
          border: 1px solid rgba(99, 102, 241, 0.35);
          color: #818CF8;
          font-size: 0.76rem;
          font-weight: 800;
          cursor: pointer;
          transition: all 0.18s ease;
          font-family: inherit;
          white-space: nowrap;
        }
        html.light .btn-part-quiz-trigger {
          background: rgba(99, 102, 241, 0.08);
          border-color: rgba(99, 102, 241, 0.3);
          color: #4F46E5;
        }
        .btn-part-quiz-trigger:hover {
          background: #6366F1;
          color: #FFFFFF;
          transform: translateY(-1px);
          box-shadow: 0 3px 10px rgba(99, 102, 241, 0.3);
        }
        .btn-part-quiz-trigger.full {
          background: rgba(16, 185, 129, 0.12);
          border-color: rgba(16, 185, 129, 0.3);
          color: #34D399;
        }
        html.light .btn-part-quiz-trigger.full {
          background: rgba(16, 185, 129, 0.08);
          border-color: rgba(16, 185, 129, 0.28);
          color: #059669;
        }
        .btn-part-quiz-trigger.full:hover {
          background: #10B981;
          color: #FFFFFF;
          box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3);
        }

        /* Mobile & Smartphone Bottom-Sheet Ergonomics (< 640px) */
        @media (max-width: 640px) {
          .part-quiz-modal-backdrop {
            padding: 0;
            align-items: flex-end; /* Slides up like native iOS/Android sheet */
          }
          .quiz-modal-card {
            border-radius: 24px 24px 0 0;
            max-height: 88vh;
            padding: 20px 18px env(safe-area-inset-bottom, 24px);
            margin: 0;
            border-bottom: none;
            transform: translateY(100%);
          }
          .part-quiz-modal-backdrop.open .quiz-modal-card {
            transform: translateY(0);
          }
          .quiz-modal-part-name {
            font-size: 0.84rem;
            max-width: 170px;
          }
          .quiz-modal-q-text {
            font-size: 1.05rem;
            line-height: 1.5;
          }
          .quiz-modal-q-tr {
            font-size: 0.86rem;
          }
          .btn-quiz-choice {
            height: 58px;
          }
          .choice-lbl {
            font-size: 1.05rem;
          }
          .choice-sub {
            font-size: 0.68rem;
          }
          .part-quiz-actions-wrap {
            width: 100%;
            margin-top: 8px;
            display: flex;
            gap: 8px;
          }
          .btn-part-quiz-trigger {
            flex: 1;
            height: 36px;
            justify-content: center;
            font-size: 0.82rem;
          }
        }
      `;
      document.head.appendChild(s);
    },
    updateScoreDisplay() {
      const cEl = document.getElementById('stat-correct');
      const wEl = document.getElementById('stat-wrong');
      const rEl = document.getElementById('stat-remaining');
      if (cEl) cEl.innerText = this.userStats.correct;
      if (wEl) wEl.innerText = this.userStats.wrong;
      const remaining = Math.max(0, this.data.domande.length - (this.userStats.correct + this.userStats.wrong));
      if (rEl) rEl.innerText = remaining;
    }
  };

  window.ModularChapterEngine = ModularChapterEngine;

})(window, document);

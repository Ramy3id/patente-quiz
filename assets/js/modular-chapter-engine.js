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
    currentFilter: 'all',
    activeGroupFilter: 'all',
    currentViewMode: 'grouped', // 'grouped' | 'flat'
    expandedSections: new Set(),
    isStudyMode: false,

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
          updatedAt: Date.now()
        };
        window.localStorage.setItem(this.getStorageKey(), JSON.stringify(payload));
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

      this.renderHub();
      this.renderChips();
      this.renderQuestions();
      this.updateScoreDisplay();
      this.updateChapterProgress();
    },

    getOverallProgress() {
      const totalQuestions = this.data && this.data.domande ? this.data.domande.length : 0;
      let answeredCount = 0;
      if (this.data && this.data.domande) {
        this.data.domande.forEach(q => {
          if (this.userAnswers[q.id]) answeredCount++;
        });
      }

      const groupKeys = Object.keys(this.groups);
      const totalGroups = groupKeys.length;
      let completedGroups = 0;

      groupKeys.forEach(gKey => {
        const groupQuestions = this.data.domande.filter(q => q.gruppo_unificato === gKey);
        const gTotal = groupQuestions.length;
        let gAnswered = 0;
        groupQuestions.forEach(q => {
          if (this.userAnswers[q.id]) gAnswered++;
        });
        if (gTotal > 0 && gAnswered === gTotal) completedGroups++;
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
      if (qMeta) qMeta.innerText = `📝 أُجيب: ${progress.answeredCount} من ${progress.totalQuestions} سؤالاً`;
      if (gMeta) gMeta.innerText = `🏆 اكتمل: ${progress.completedGroups} من ${progress.totalGroups} قسماً`;
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
    },

    renderHub() {
      let hub = document.getElementById('subtopics-hub-card');
      const qList = document.getElementById('questions-list');
      if (!qList) return;

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
              <span id="chapter-progress-q-meta">📝 أُجيب: ${progress.answeredCount} من ${progress.totalQuestions} سؤالاً</span>
              <span id="chapter-progress-g-meta">🏆 اكتمل: ${progress.completedGroups} من ${progress.totalGroups} قسماً</span>
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

        // Check if group is fully answered
        const groupQuestions = this.data.domande.filter(q => q.gruppo_unificato === gKey);
        let gAnswered = 0;
        groupQuestions.forEach(q => {
          if (this.userAnswers[q.id]) gAnswered++;
        });
        const isCompleted = (count > 0 && gAnswered === count);

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
      let answered = 0;
      groupQuestions.forEach(q => {
        if (this.userAnswers[q.id]) answered++;
      });

      const isDone = (answered === total && total > 0);
      badge.className = `subtopic-stat-pill progress-pill ${isDone ? 'done' : ''}`;
      badge.innerText = `${isDone ? '🎉 مكتمل ' : '🎯 إنجاز '}${answered}/${total}`;
    },

    buildQuestionCardHtml(q) {
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

      const gInfo = this.groups[q.gruppo_unificato] || {};
      const subLabel = gInfo.short_ar ? `${gInfo.icon || '📌'} ${gInfo.num ? gInfo.num + '. ' : ''}${gInfo.short_ar}` : (q.sotto_argomento || '');

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
          questions.forEach(q => {
            if (this.userAnswers[q.id]) answeredInSub++;
          });

          const isExpanded = (query !== '') || (this.activeGroupFilter !== 'all') || this.expandedSections.has(gKey);
          const isCollapsed = !isExpanded;
          const isDone = (answeredInSub === totalInSub && totalInSub > 0);

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
                <span class="subtopic-stat-pill progress-pill ${isDone ? 'done' : ''}" id="sec-progress-${gKey}">
                  ${isDone ? '🎉 مكتمل ' : '🎯 إنجاز '}${answeredInSub}/${totalInSub}
                </span>
                ${this.activeGroupFilter === 'all' ? `
                  <button class="subtopic-focus-btn" onclick="event.stopPropagation(); selectSubtopicFilter('${gKey}')">
                    🎯 مذاكرة هذا الجزء فقط
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

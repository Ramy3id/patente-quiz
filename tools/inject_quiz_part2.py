# -*- coding: utf-8 -*-
"""
Part 2: Inject Part Quiz Logic, Modal Runner, and CSS into modular-chapter-engine.js
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'R:/Ramy/PATENTE/assets/js/modular-chapter-engine.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update secBox.innerHTML to show Mastery Progress and Quiz Action Buttons
old_sec_stats = """              <div class="subtopic-header-stats">
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
              </div>"""

new_sec_stats = """              <div class="subtopic-header-stats">
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
              </div>"""

# Need to also calculate masteredInSub and quizBtnHtml right before secBox.innerHTML
old_sub_calc = """          let answeredInSub = 0;
          questions.forEach(q => {
            if (this.userAnswers[q.id]) answeredInSub++;
          });

          const isExpanded = (query !== '') || (this.activeGroupFilter !== 'all') || this.expandedSections.has(gKey);
          const isCollapsed = !isExpanded;
          const isDone = (answeredInSub === totalInSub && totalInSub > 0);"""

new_sub_calc = """          let answeredInSub = 0;
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
          }"""

code = code.replace(old_sub_calc, new_sub_calc, 1)
code = code.replace(old_sec_stats, new_sec_stats, 1)

# 2. Update renderChips to use masteredIds
old_chip_calc = """        // Check if group is fully answered
        const groupQuestions = this.data.domande.filter(q => q.gruppo_unificato === gKey);
        let gAnswered = 0;
        groupQuestions.forEach(q => {
          if (this.userAnswers[q.id]) gAnswered++;
        });
        const isCompleted = (count > 0 && gAnswered === count);"""

new_chip_calc = """        // Check if group is fully mastered
        const groupQuestions = this.data.domande.filter(q => q.gruppo_unificato === gKey);
        let gMastered = 0;
        groupQuestions.forEach(q => {
          if (this.masteredIds.has(q.id)) gMastered++;
        });
        const isCompleted = (count > 0 && gMastered >= count);"""

code = code.replace(old_chip_calc, new_chip_calc, 1)

# 3. Add Quiz Runner Methods: startPartQuiz, answerPartQuiz, closePartQuiz, renderQuizRunnerModal, finishPartQuiz, retestPartMissed, injectQuizModalStyles
quiz_methods = """
    // =========================================================
    // Part Quiz Engine (Smart Priority-Based In-Place Mastery)
    // =========================================================
    startPartQuiz(gKey, reqCount) {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      
      const questionsInGroup = this.data.domande.filter(q => q.gruppo_unificato === gKey);
      if (!questionsInGroup.length) return;

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
          <!-- Top Bar -->
          <div class="quiz-modal-topbar">
            <div class="quiz-modal-part-info">
              <span class="quiz-modal-part-badge">⚡ كويز الجزء</span>
              <span class="quiz-modal-part-name">${partName}</span>
            </div>
            <button class="quiz-modal-close-btn" onclick="closePartQuiz()" title="إغلاق والعودة لصفحة الباب">✕</button>
          </div>

          <!-- Progress Strip -->
          <div class="quiz-modal-prog-wrap">
            <div class="quiz-modal-prog-text">
              <span>السؤال <strong>${curIdx + 1}</strong> من <strong>${total}</strong></span>
              <span>${pct}% مكتمل</span>
            </div>
            <div class="quiz-modal-prog-track">
              <div class="quiz-modal-prog-fill" style="width:${pct}%;"></div>
            </div>
          </div>

          <!-- Question Body -->
          <div class="quiz-modal-q-body">
            ${imgHtml}
            <div class="quiz-modal-q-text">
              ${q.domanda}
            </div>
            <div class="quiz-modal-q-tr">
              ${q.traduzione || ''}
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="quiz-modal-actions-row">
            <button class="btn-quiz-choice vero" onclick="answerPartQuiz(true)">
              <span class="choice-icon">✅</span>
              <span class="choice-lbl">VERO</span>
              <span class="choice-sub">صحيح</span>
            </button>
            <button class="btn-quiz-choice falso" onclick="answerPartQuiz(false)">
              <span class="choice-icon">❌</span>
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
           Part Quiz (Active Mastery) Modal & Micro-Runner Styling
           ========================================================= */
        body.quiz-modal-open {
          overflow: hidden !important;
        }
        .part-quiz-modal-backdrop {
          position: fixed;
          inset: 0;
          background: rgba(11, 15, 25, 0.88);
          backdrop-filter: blur(16px);
          -webkit-backdrop-filter: blur(16px);
          z-index: 100000;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 16px;
          opacity: 0;
          visibility: hidden;
          transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.25s;
          direction: rtl;
        }
        .part-quiz-modal-backdrop.open {
          opacity: 1;
          visibility: visible;
        }
        .quiz-modal-card {
          width: 100%;
          max-width: 580px;
          background: #111827;
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 24px;
          box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.1);
          padding: 24px;
          max-height: 90vh;
          overflow-y: auto;
          color: #F8FAFC;
          font-family: 'Plus Jakarta Sans', 'Cairo', system-ui, sans-serif;
          position: relative;
          transform: translateY(12px) scale(0.97);
          transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        html.light .quiz-modal-card {
          background: #FFFFFF;
          border-color: rgba(15, 23, 42, 0.12);
          box-shadow: 0 24px 60px rgba(15, 23, 42, 0.2);
          color: #0F172A;
        }
        .part-quiz-modal-backdrop.open .quiz-modal-card {
          transform: translateY(0) scale(1);
        }

        .quiz-modal-topbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding-bottom: 14px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          margin-bottom: 14px;
        }
        html.light .quiz-modal-topbar {
          border-bottom-color: rgba(15, 23, 42, 0.08);
        }
        .quiz-modal-part-info {
          display: flex;
          align-items: center;
          gap: 8px;
          overflow: hidden;
        }
        .quiz-modal-part-badge {
          background: rgba(99, 102, 241, 0.15);
          color: #818CF8;
          border: 1px solid rgba(99, 102, 241, 0.3);
          border-radius: 6px;
          font-size: 0.72rem;
          font-weight: 800;
          padding: 2px 7px;
          white-space: nowrap;
        }
        html.light .quiz-modal-part-badge {
          background: rgba(99, 102, 241, 0.08);
          color: #4F46E5;
        }
        .quiz-modal-part-name {
          font-size: 0.88rem;
          font-weight: 800;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .quiz-modal-close-btn {
          width: 32px;
          height: 32px;
          border-radius: 8px;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: #94A3B8;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.9rem;
          transition: all 0.2s;
        }
        html.light .quiz-modal-close-btn {
          background: rgba(15, 23, 42, 0.04);
          border-color: rgba(15, 23, 42, 0.1);
          color: #475569;
        }
        .quiz-modal-close-btn:hover {
          background: rgba(239, 68, 68, 0.15);
          color: #EF4444;
          border-color: rgba(239, 68, 68, 0.3);
        }

        .quiz-modal-prog-wrap {
          margin-bottom: 20px;
        }
        .quiz-modal-prog-text {
          display: flex;
          justify-content: space-between;
          font-size: 0.78rem;
          color: #94A3B8;
          font-weight: 700;
          margin-bottom: 6px;
        }
        html.light .quiz-modal-prog-text {
          color: #64748B;
        }
        .quiz-modal-prog-track {
          width: 100%;
          height: 6px;
          background: rgba(255, 255, 255, 0.08);
          border-radius: 99px;
          overflow: hidden;
        }
        html.light .quiz-modal-prog-track {
          background: rgba(15, 23, 42, 0.08);
        }
        .quiz-modal-prog-fill {
          height: 100%;
          background: linear-gradient(90deg, #6366F1, #38BDF8);
          border-radius: 99px;
          transition: width 0.3s ease;
        }

        .quiz-modal-q-body {
          margin-bottom: 24px;
        }
        .quiz-modal-img-wrap {
          text-align: center;
          margin-bottom: 16px;
        }
        .quiz-modal-img-wrap img {
          max-height: 140px;
          max-width: 100%;
          border-radius: 12px;
          background: #FFF;
          padding: 6px;
          box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        }
        .quiz-modal-q-text {
          font-size: 1.15rem;
          font-weight: 800;
          line-height: 1.5;
          margin-bottom: 10px;
          direction: ltr;
          text-align: left;
          color: #FFFFFF;
        }
        html.light .quiz-modal-q-text {
          color: #0F172A;
        }
        .quiz-modal-q-tr {
          font-size: 0.92rem;
          color: #94A3B8;
          line-height: 1.6;
          direction: rtl;
          text-align: right;
        }
        html.light .quiz-modal-q-tr {
          color: #475569;
        }

        .quiz-modal-actions-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 14px;
        }
        .btn-quiz-choice {
          height: 64px;
          border-radius: 16px;
          border: 2px solid transparent;
          cursor: pointer;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
          font-family: inherit;
        }
        .btn-quiz-choice.vero {
          background: rgba(16, 185, 129, 0.12);
          border-color: rgba(16, 185, 129, 0.35);
          color: #34D399;
        }
        html.light .btn-quiz-choice.vero {
          background: rgba(16, 185, 129, 0.08);
          border-color: rgba(16, 185, 129, 0.35);
          color: #059669;
        }
        .btn-quiz-choice.vero:hover {
          background: #10B981;
          color: #FFFFFF;
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(16, 185, 129, 0.35);
        }
        .btn-quiz-choice.falso {
          background: rgba(239, 68, 68, 0.12);
          border-color: rgba(239, 68, 68, 0.35);
          color: #F87171;
        }
        html.light .btn-quiz-choice.falso {
          background: rgba(239, 68, 68, 0.08);
          border-color: rgba(239, 68, 68, 0.35);
          color: #DC2626;
        }
        .btn-quiz-choice.falso:hover {
          background: #EF4444;
          color: #FFFFFF;
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(239, 68, 68, 0.35);
        }
        .choice-lbl {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.15rem;
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
          font-size: 1.35rem;
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

        .quiz-results-actions {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .btn-quiz-action {
          width: 100%;
          height: 44px;
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
          height: 28px;
          display: inline-flex;
          align-items: center;
          gap: 4px;
          padding: 0 10px;
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

        @media (max-width: 640px) {
          .quiz-modal-card {
            padding: 18px 16px;
            border-radius: 20px;
          }
          .quiz-modal-q-text {
            font-size: 1rem;
          }
          .btn-quiz-choice {
            height: 56px;
          }
          .part-quiz-actions-wrap {
            width: 100%;
            margin-top: 6px;
          }
          .btn-part-quiz-trigger {
            flex: 1;
            justify-content: center;
          }
        }
      `;
      document.head.appendChild(s);
    },
"""

# Insert quiz_methods right before closing of ModularChapterEngine
target_engine_end = "    updateScoreDisplay() {"
pos_target = code.find(target_engine_end)
if pos_target != -1:
    code = code[:pos_target] + quiz_methods + '\n    ' + code[pos_target:]
    print("Quiz methods injected successfully!")
else:
    print("Error: target_engine_end not found!")

# Also auto-inject quiz styles in init()
init_target = "this.bindGlobals();"
code = code.replace(init_target, "this.injectQuizStyles();\n      this.bindGlobals();", 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Part 2: Part Quiz Runner, Priority Sampling and Styling applied successfully!")

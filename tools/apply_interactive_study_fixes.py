import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Update modular-chapter-engine.js
engine_file = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'
with open(engine_file, 'r', encoding='utf-8') as f:
    engine_text = f.read()

# Replace renderChips() in engine
old_render_chips = '''    renderChips() {
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
    },'''

new_render_chips = '''    renderChips() {
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

      const renderChipHtml = (gKey) => {
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

        return `
          <button class="subtopic-chip ${isActive ? 'active' : ''} ${isCompleted ? 'is-completed' : ''}" onclick="selectSubtopicFilter('${gKey}')" title="${info.ar || ''} (${info.it || ''})">
            <span>${isCompleted ? '✅' : icon} ${num}${label}</span>
            <span class="chip-count">${isCompleted ? 'مكتمل' : count}</span>
          </button>
        `;
      };

      const topKeys = groupKeys.slice(0, 4);
      const remainingKeys = groupKeys.slice(4);
      const hasCollapsible = remainingKeys.length > 0;

      // Auto-expand if active filter is among remaining
      if (this.activeGroupFilter !== 'all' && remainingKeys.includes(this.activeGroupFilter)) {
        this.extraSubtopicsExpanded = true;
      }

      let html = `
        <button class="subtopic-chip ${this.activeGroupFilter === 'all' ? 'active' : ''}" data-filter="all" onclick="selectSubtopicFilter('all')" title="عرض كل الأجزاء (${totalDomande} سؤالاً)">
          <span>🌐 كل الأجزاء (${totalGroups})</span>
          <span class="chip-count">${totalDomande} سؤالاً</span>
        </button>
        ${topKeys.map(renderChipHtml).join('')}
      `;

      if (hasCollapsible) {
        const isExpanded = !!this.extraSubtopicsExpanded;
        html += `
          <div id="extraSubtopicsContainer" class="extra-subtopics-container ${isExpanded ? 'is-expanded' : ''}">
            ${remainingKeys.map(renderChipHtml).join('')}
          </div>
          <button type="button" class="subtopics-toggle-btn" id="btnToggleExtraSubtopics" onclick="toggleExtraSubtopics()">
            <span id="extraSubtopicsToggleText">${isExpanded ? 'إخفاء الأجزاء الإضافية ▴' : `عرض باقي الأجزاء (${remainingKeys.length} أجزاء إضافية) ▾`}</span>
          </button>
        `;
      }

      bar.innerHTML = html;
    },'''

if old_render_chips in engine_text:
    engine_text = engine_text.replace(old_render_chips, new_render_chips, 1)
    print("Replaced renderChips() in modular-chapter-engine.js successfully")
else:
    print("WARNING: old_render_chips not found in engine")

# Add toggleExtraSubtopics function
toggle_subtopics_js = '''
window.toggleExtraSubtopics = function() {
  if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
  const engine = window.ModularChapterEngine;
  if (!engine) return;
  engine.extraSubtopicsExpanded = !engine.extraSubtopicsExpanded;
  const container = document.getElementById('extraSubtopicsContainer');
  const txt = document.getElementById('extraSubtopicsToggleText');
  if (container) {
    container.classList.toggle('is-expanded', engine.extraSubtopicsExpanded);
  }
  if (txt) {
    const groupKeys = Object.keys(engine.groups || {});
    const remCount = Math.max(0, groupKeys.length - 4);
    txt.textContent = engine.extraSubtopicsExpanded 
      ? 'إخفاء الأجزاء الإضافية ▴' 
      : `عرض باقي الأجزاء (${remCount} أجزاء إضافية) ▾`;
  }
};
'''

if 'window.toggleExtraSubtopics' not in engine_text:
    idx_bind = engine_text.find('bindGlobals() {')
    if idx_bind != -1:
        engine_text = engine_text[:idx_bind] + toggle_subtopics_js + '\n    ' + engine_text[idx_bind:]
        print("Added window.toggleExtraSubtopics successfully")

# Refactor subtopic-section-header in renderQuestions to avoid detached chevron
old_sec_header = '''              <div class="subtopic-header-stats">
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
              </div>'''

new_sec_header = '''              <div class="subtopic-header-stats">
                <span class="subtopic-stat-pill">
                  <strong>${totalInSub}</strong> أسئلة
                </span>
                <span class="subtopic-stat-pill vf">
                  <span style="color:#10b981;">${vCount} V</span> • <span style="color:#ef4444;">${fCount} F</span>
                </span>
                <span class="subtopic-stat-pill progress-pill ${isMasteredDone ? 'done' : ''}" id="sec-progress-${gKey}">
                  ${isMasteredDone ? '🏆 إتقان كامل ' : '🎯 إتقان '}${masteredInSub}/${totalInSub}
                </span>
              </div>

              <div class="subtopic-actions-footer">
                <div class="part-quiz-actions-wrap" onclick="event.stopPropagation()">
                  ${quizBtnHtml}
                </div>
                <div class="subtopic-footer-nav-row">
                  ${this.activeGroupFilter === 'all' ? `
                    <button class="subtopic-focus-btn" onclick="event.stopPropagation(); selectSubtopicFilter('${gKey}')">
                      <span>🎯 مذاكرة هذا الجزء</span>
                    </button>
                  ` : ''}
                  <button class="subtopic-chevron-btn" onclick="event.stopPropagation(); ModularChapterEngine.toggleSubtopicSection('${gKey}')" title="فتح أو طي أسئلة هذا الجزء">
                    <span>الأسئلة</span>
                    <span class="subtopic-chevron">▼</span>
                  </button>
                </div>
              </div>'''

if old_sec_header in engine_text:
    engine_text = engine_text.replace(old_sec_header, new_sec_header, 1)
    print("Replaced section header in modular-chapter-engine.js successfully")
else:
    print("WARNING: old_sec_header not found in engine")

with open(engine_file, 'w', encoding='utf-8') as f:
    f.write(engine_text)
print("Updated modular-chapter-engine.js successfully")

# 2. Update modular-chapter.css
css_file = r'R:\Ramy\PATENTE_PRO_APP\assets\css\modular-chapter.css'
with open(css_file, 'r', encoding='utf-8') as f:
    css_text = f.read()

master_chapter_css = '''
/* ==========================================================================
   2026 MASTER MOBILE OVERHAUL: ZERO-SCROLL CHIPS & HARMONIZED METRICS
   ========================================================================== */

/* Header Card Overrides */
.ch-header-card {
  padding: 20px 18px !important;
  border-radius: 20px !important;
  box-sizing: border-box !important;
}
html.light .ch-header-card {
  background: #FFFFFF !important;
  border: 1px solid rgba(15, 23, 42, 0.1) !important;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
}
.btn-back-portal {
  background: rgba(255, 255, 255, 0.04) !important;
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.1)) !important;
  border-radius: 10px !important;
  height: 38px !important;
  min-height: 38px !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  padding: 0 14px !important;
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  text-decoration: none !important;
  color: var(--text-secondary, #cbd5e1) !important;
  box-sizing: border-box !important;
}
html.light .btn-back-portal {
  background: #F8FAFC !important;
  border-color: rgba(15, 23, 42, 0.12) !important;
  color: #334155 !important;
}
.btn-guide-link {
  height: 38px !important;
  min-height: 38px !important;
  border-radius: 10px !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  padding: 0 14px !important;
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  box-sizing: border-box !important;
}
.ch-main-title {
  font-size: 1.40rem !important;
  font-weight: 800 !important;
  line-height: 1.3 !important;
  color: #FFFFFF !important;
  margin-bottom: 6px !important;
  letter-spacing: -0.01em !important;
}
html.light .ch-main-title {
  color: #0F172A !important;
}
.ch-ar-title {
  font-size: 1.05rem !important;
  font-weight: 700 !important;
  color: #38BDF8 !important;
  margin-bottom: 16px !important;
}
html.light .ch-ar-title {
  color: #0284C7 !important;
}

/* 3-Column Metrics Score Strip */
.score-strip {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
  gap: 8px !important;
  width: 100% !important;
  padding-top: 14px !important;
  border-top: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08)) !important;
  margin-top: 14px !important;
  box-sizing: border-box !important;
  direction: rtl !important;
}
html.light .score-strip {
  border-top-color: rgba(15, 23, 42, 0.08) !important;
}
.score-cell {
  background: rgba(255, 255, 255, 0.04) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 14px !important;
  padding: 8px 4px !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  box-sizing: border-box !important;
  min-width: 0 !important;
}
html.light .score-cell {
  background: #F8FAFC !important;
  border-color: rgba(15, 23, 42, 0.08) !important;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03) !important;
}
.score-cell span {
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  margin-bottom: 3px !important;
  white-space: nowrap !important;
}
.score-cell strong {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.30rem !important;
  font-weight: 800 !important;
  line-height: 1.15 !important;
  color: #FFFFFF !important;
}
html.light .score-cell strong {
  color: #0F172A !important;
}

/* Subtopics Hub Card */
.subtopics-hub-card {
  padding: 18px !important;
  border-radius: 20px !important;
  box-sizing: border-box !important;
}
html.light .subtopics-hub-card {
  background: #FFFFFF !important;
  border-color: rgba(15, 23, 42, 0.1) !important;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
}
.subtopics-hub-title {
  font-size: 0.95rem !important;
  font-weight: 800 !important;
  line-height: 1.4 !important;
}
html.light .subtopics-hub-title {
  color: #0F172A !important;
}

/* Symmetrical Hub Actions Grid */
.subtopics-hub-actions {
  display: grid !important;
  grid-template-columns: repeat(2, 1fr) !important;
  gap: 6px !important;
  width: 100% !important;
  margin-top: 12px !important;
  box-sizing: border-box !important;
}
.view-mode-toggle-group {
  grid-column: 1 / -1 !important;
  display: grid !important;
  grid-template-columns: repeat(2, 1fr) !important;
  gap: 4px !important;
  background: rgba(0, 0, 0, 0.25) !important;
  padding: 4px !important;
  border-radius: 12px !important;
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08)) !important;
}
html.light .view-mode-toggle-group {
  background: #F1F5F9 !important;
  border-color: rgba(15, 23, 42, 0.08) !important;
}
.view-mode-btn {
  height: 38px !important;
  min-height: 38px !important;
  border-radius: 9px !important;
  font-size: 0.80rem !important;
  font-weight: 700 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 6px !important;
  cursor: pointer !important;
  border: none !important;
  transition: all 0.15s ease !important;
}
.subtopics-action-btn {
  width: 100% !important;
  height: 38px !important;
  min-height: 38px !important;
  border-radius: 10px !important;
  font-size: 0.80rem !important;
  font-weight: 700 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 6px !important;
  cursor: pointer !important;
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.1)) !important;
  background: rgba(255, 255, 255, 0.04) !important;
  color: var(--text-secondary, #cbd5e1) !important;
  transition: all 0.15s ease !important;
}
html.light .subtopics-action-btn {
  background: #FFFFFF !important;
  border-color: rgba(15, 23, 42, 0.12) !important;
  color: #334155 !important;
}

/* ZERO-SCROLL BALANCED SUBTOPICS CHIPS GRID */
.subtopics-chips-scroll {
  display: grid !important;
  grid-template-columns: repeat(2, 1fr) !important;
  gap: 6px !important;
  width: 100% !important;
  max-width: 100% !important;
  overflow: visible !important;
  padding: 10px 0 0 0 !important;
  margin-top: 10px !important;
  border-top: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08)) !important;
  box-sizing: border-box !important;
}
html.light .subtopics-chips-scroll {
  border-top-color: rgba(15, 23, 42, 0.08) !important;
}
@media (min-width: 768px) {
  .subtopics-chips-scroll {
    grid-template-columns: repeat(3, 1fr) !important;
  }
}
@media (min-width: 1024px) {
  .subtopics-chips-scroll {
    grid-template-columns: repeat(4, 1fr) !important;
  }
}
.subtopic-chip {
  width: 100% !important;
  min-height: 42px !important;
  padding: 8px 10px !important;
  border-radius: 12px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  text-align: right !important;
  gap: 6px !important;
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  white-space: normal !important;
  line-height: 1.3 !important;
  box-sizing: border-box !important;
  cursor: pointer !important;
  font-family: inherit !important;
  transition: all 0.15s ease !important;
  background: rgba(255, 255, 255, 0.04) !important;
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08)) !important;
  color: #E2E8F0 !important;
}
html.light .subtopic-chip {
  background: #F8FAFC !important;
  border-color: rgba(15, 23, 42, 0.12) !important;
  color: #334155 !important;
}
html.light .subtopic-chip:hover {
  background: #F1F5F9 !important;
  color: #0F172A !important;
}
.subtopic-chip.active {
  background: #0284C7 !important;
  border-color: #38BDF8 !important;
  color: #FFFFFF !important;
  box-shadow: 0 0 12px rgba(56, 189, 248, 0.35) !important;
}
html.light .subtopic-chip.active {
  background: #0284C7 !important;
  border-color: #0284C7 !important;
  color: #FFFFFF !important;
  box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25) !important;
}
.subtopic-chip[data-filter="all"] {
  grid-column: 1 / -1 !important;
  min-height: 44px !important;
  font-size: 0.86rem !important;
  justify-content: center !important;
  gap: 8px !important;
}

/* Collapsible Subtopics Container & Toggle Button */
.extra-subtopics-container {
  display: none !important;
}
.extra-subtopics-container.is-expanded {
  display: contents !important;
}
.subtopics-toggle-btn {
  grid-column: 1 / -1 !important;
  width: 100% !important;
  height: 42px !important;
  min-height: 42px !important;
  margin-top: 4px !important;
  border-radius: 12px !important;
  border: 1.5px dashed rgba(2, 132, 199, 0.4) !important;
  background: rgba(2, 132, 199, 0.05) !important;
  color: #0284C7 !important;
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  font-family: inherit !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 6px !important;
  box-sizing: border-box !important;
  transition: all 0.2s ease !important;
}
html.light .subtopics-toggle-btn {
  border-color: rgba(2, 132, 199, 0.35) !important;
  background: #F0F9FF !important;
  color: #0284C7 !important;
}
html.light .subtopics-toggle-btn:hover {
  background: #E0F2FE !important;
  border-color: #0284C7 !important;
}
html.dark .subtopics-toggle-btn {
  border-color: rgba(56, 189, 248, 0.35) !important;
  background: rgba(56, 189, 248, 0.08) !important;
  color: #38BDF8 !important;
}
html.dark .subtopics-toggle-btn:hover {
  background: rgba(56, 189, 248, 0.15) !important;
  border-color: #38BDF8 !important;
}

/* Subtopic Section Card Actions Polish */
.subtopic-actions-footer {
  width: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 8px !important;
  margin-top: 12px !important;
  padding-top: 12px !important;
  border-top: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08)) !important;
  box-sizing: border-box !important;
}
html.light .subtopic-actions-footer {
  border-top-color: rgba(15, 23, 42, 0.08) !important;
}
.part-quiz-actions-wrap {
  width: 100% !important;
  display: grid !important;
  grid-template-columns: repeat(2, 1fr) !important;
  gap: 6px !important;
}
.part-quiz-btn {
  width: 100% !important;
  height: 40px !important;
  min-height: 40px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 10px !important;
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  text-decoration: none !important;
  box-sizing: border-box !important;
}
.subtopic-footer-nav-row {
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
}
.subtopic-focus-btn {
  flex: 1 !important;
  height: 40px !important;
  min-height: 40px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 10px !important;
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  box-sizing: border-box !important;
  background: rgba(99, 102, 241, 0.15) !important;
  border: 1px solid rgba(99, 102, 241, 0.35) !important;
  color: #C7D2FE !important;
  transition: all 0.15s ease !important;
}
html.light .subtopic-focus-btn {
  background: #0284C7 !important;
  border-color: #0284C7 !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25) !important;
}
.subtopic-chevron-btn {
  height: 40px !important;
  min-height: 40px !important;
  padding: 0 12px !important;
  border-radius: 10px !important;
  background: rgba(255, 255, 255, 0.04) !important;
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.1)) !important;
  color: var(--text-secondary, #cbd5e1) !important;
  font-size: 0.80rem !important;
  font-weight: 700 !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  cursor: pointer !important;
  box-sizing: border-box !important;
}
html.light .subtopic-chevron-btn {
  background: #F1F5F9 !important;
  border-color: rgba(15, 23, 42, 0.12) !important;
  color: #334155 !important;
}
'''

css_text += '\n' + master_chapter_css
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(css_text)
print("Updated modular-chapter.css successfully")

# 3. Update Capitolo_01 index.html
chap1_file = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html'
with open(chap1_file, 'r', encoding='utf-8') as f:
    chap1_text = f.read()

# Fix 3D text
old_guide_link = '<span>📖 الشرح النظري المعتمد والـ 3D للباب الأول</span>'
new_guide_link = '<span>📖 الشرح النظري المعتمد والـ <bdi>3D</bdi> للباب الأول</span>'
if old_guide_link in chap1_text:
    chap1_text = chap1_text.replace(old_guide_link, new_guide_link, 1)
    print("Fixed 3D text in Chapter 01 index.html")

# Fix score cells
old_score_markup = '''    <!-- Score Strip -->
    <div class="score-strip">
      <div class="score-cell">
        <span style="color:var(--emerald-primary);">✔ صحيح:</span>
        <strong id="stat-correct">0</strong>
      </div>
      <div class="score-cell">
        <span style="color:var(--rose-primary);">✖ خطأ:</span>
        <strong id="stat-wrong">0</strong>
      </div>
      <div class="score-cell">
        <span style="color:var(--text-muted);">⏳ المتبقي:</span>
        <strong id="stat-remaining">531</strong>
      </div>
    </div>'''

new_score_markup = '''    <!-- Score Strip -->
    <div class="score-strip">
      <div class="score-cell stat-correct">
        <span style="color:var(--emerald-primary, #10b981);">✔ صحيح</span>
        <strong id="stat-correct">0</strong>
      </div>
      <div class="score-cell stat-wrong">
        <span style="color:var(--rose-primary, #f43f5e);">✖ خطأ</span>
        <strong id="stat-wrong">0</strong>
      </div>
      <div class="score-cell stat-remaining">
        <span style="color:var(--text-muted, #94a3b8);">⏳ المتبقي</span>
        <strong id="stat-remaining">531</strong>
      </div>
    </div>'''

if old_score_markup in chap1_text:
    chap1_text = chap1_text.replace(old_score_markup, new_score_markup, 1)
    print("Updated score strip in Chapter 01 index.html")

with open(chap1_file, 'w', encoding='utf-8') as f:
    f.write(chap1_text)
print("Updated Chapter 01 index.html successfully")

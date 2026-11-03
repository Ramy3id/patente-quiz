import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Update modular-chapter-engine.js
engine_path = 'R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js'
with open(engine_path, 'r', encoding='utf-8') as f:
    engine_code = f.read()

# Change 1: Replace 'عرض مقسم (${groupCount} قسماً)' with 'قوائم مقسمة'
old_text_btn = '<span>🗂️ عرض مقسم (${groupCount} قسماً)</span>'
new_text_btn = '<span>🗂️ قوائم مقسمة</span>'
if old_text_btn in engine_code:
    engine_code = engine_code.replace(old_text_btn, new_text_btn, 1)
    print("SUCCESS: Changed 'عرض مقسم' to 'قوائم مقسمة'")
else:
    print("WARNING: old_text_btn not found")

# Change 2: Center chapter-progress-meta
old_prog_meta = '''            <div class="chapter-progress-meta">
              <span id="chapter-progress-q-meta">🎯 أُتقن: ${progress.answeredCount} من ${progress.totalQuestions} سؤالاً</span>
              <span id="chapter-progress-g-meta">🏆 أُتقن بالكامل: ${progress.completedGroups} من ${progress.totalGroups} قسماً</span>
              <button class="chapter-reset-btn" onclick="resetChapterProgress()" title="إعادة تعيين التقدم لهذا الباب">
                <span>🔄 تصفير الإنجاز</span>
              </button>
            </div>'''

new_prog_meta = '''            <div class="chapter-progress-meta">
              <div class="chapter-progress-stats-row">
                <span id="chapter-progress-q-meta">🎯 أُتقن: ${progress.answeredCount} من ${progress.totalQuestions} سؤالاً</span>
                <span id="chapter-progress-g-meta">🏆 أُتقن بالكامل: ${progress.completedGroups} من ${progress.totalGroups} قسماً</span>
              </div>
              <button class="chapter-reset-btn" onclick="resetChapterProgress()" title="إعادة تعيين التقدم لهذا الباب">
                <span>🔄 تصفير الإنجاز</span>
              </button>
            </div>'''

if old_prog_meta in engine_code:
    engine_code = engine_code.replace(old_prog_meta, new_prog_meta, 1)
    print("SUCCESS: Updated chapter-progress-meta layout")
else:
    print("WARNING: old_prog_meta not found")

# Change 3: Update buildQuestionCard and locked-preview-card to support q-answers-grid and q-feedback-row
old_locked_actions = '''              <div class="q-actions-row">
                <button class="btn-ans btn-ans-v"><span>VERO</span></button>
                <button class="btn-ans btn-ans-f"><span>FALSO</span></button>
              </div>'''

new_locked_actions = '''              <div class="q-actions-row">
                <div class="q-answers-grid">
                  <button class="btn-ans btn-ans-v"><span>VERO</span></button>
                  <button class="btn-ans btn-ans-f"><span>FALSO</span></button>
                </div>
              </div>'''

if old_locked_actions in engine_code:
    engine_code = engine_code.replace(old_locked_actions, new_locked_actions, 1)
    print("SUCCESS: Updated locked card answers grid")
else:
    print("WARNING: old_locked_actions not found")

old_normal_actions = '''            <div class="q-actions-row">
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
            </div>'''

new_normal_actions = '''            <div class="q-actions-row">
              <div class="q-answers-grid">
                <button class="btn-ans btn-ans-v ${ans && ans.userChoice === true ? 'selected' : ''}" onclick="answerQuestion(${q.id}, true)">
                  <span>VERO</span>
                </button>
                <button class="btn-ans btn-ans-f ${ans && ans.userChoice === false ? 'selected' : ''}" onclick="answerQuestion(${q.id}, false)">
                  <span>FALSO</span>
                </button>
              </div>

              <div class="q-feedback-row">
                <span class="${statusClass}" id="status-${q.id}">${statusText}</span>
                <span class="study-badge-direct ${this.isStudyMode ? 'show' : ''} ${q.risposta ? 'is-v' : 'is-f'}" id="study-badge-${q.id}">
                  ${q.risposta ? 'VERO ✅' : 'FALSO ❌'}
                </span>
              </div>

              <button class="btn-explain-toggle" onclick="toggleDrawer(${q.id})">
                <span>💡 الترجمة والشرح وكشف الفخ</span>
              </button>
            </div>'''

if old_normal_actions in engine_code:
    engine_code = engine_code.replace(old_normal_actions, new_normal_actions, 1)
    print("SUCCESS: Updated normal card answers grid & feedback row")
else:
    print("WARNING: old_normal_actions not found")

with open(engine_path, 'w', encoding='utf-8') as f:
    f.write(engine_code)
print("Saved modular-chapter-engine.js")

import re

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix CSS for .ps-filters-row: Remove nowrap and overflow-x: auto, enable flex-wrap: wrap
content = re.sub(
    r'\.ps-filters-row\s*\{[^}]*flex-wrap:\s*nowrap[^}]*\}',
    '''.ps-filters-row {
      display: flex !important;
      flex-wrap: wrap !important;
      justify-content: center !important;
      align-items: center !important;
      gap: 8px !important;
      padding: 4px 0 10px !important;
      overflow: visible !important;
      width: 100% !important;
    }''',
    content
)

# Also ensure .ps-filter-btn looks like modern rounded pills without cutting text
content = re.sub(
    r'\.ps-filter-btn\s*\{[^}]*\}',
    '''.ps-filter-btn {
      padding: 7px 14px;
      border-radius: 999px;
      border: 1px solid var(--ps-card-border);
      background: transparent;
      color: var(--ps-text-sub);
      font-family: inherit;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      flex-shrink: 0;
    }''',
    content,
    count=1
)

# 2. Fix script tag: change async to defer for data_all_questions.js
content = content.replace(
    '<script src="../Capitoli_Divisi/data_all_questions.js" async></script>',
    '<script src="../Capitoli_Divisi/data_all_questions.js" defer></script>'
)

# 3. Fix calculateCounts to safely check ALL_QUESTIONS_DATA
old_calc_pattern = re.compile(
    r'function calculateCounts\(\)\s*\{[\s\S]*?document\.getElementById\("statQuestionsCovered"\)\.innerText = totalQuestionsSet\.size \+ " سؤالاً";\s*\}',
    re.DOTALL
)

new_calc_func = '''function calculateCounts() {
      let totalQuestionsSet = new Set();
      let cntF = 0, cntV = 0, cntE = 0, cntP = 0, cntPairs = 0, cntRep = 0;
      const hasQ = (typeof ALL_QUESTIONS_DATA !== 'undefined' && Array.isArray(ALL_QUESTIONS_DATA) && ALL_QUESTIONS_DATA.length > 0);

      MAGIC_WORDS_DB.forEach(w => {
        if (hasQ) {
          const re = new RegExp(w.regex, "i");
          const matched = ALL_QUESTIONS_DATA.filter(q => re.test(q.q || ""));
          w.questionCount = matched.length;
          matched.forEach(q => totalQuestionsSet.add((q.ch || 1) + "_" + (q.id || 0)));
        } else {
          w.questionCount = w.questionCount || 0;
        }

        if (w.isPair) cntPairs++;
        else if (w.isRepeated) cntRep++;
        else if (w.isPhrase) cntP++;
        else if (w.type === 'falso') cntF++;
        else if (w.type === 'vero') cntV++;

        if (w.hasException) cntE++;
      });

      const elAll = document.getElementById("cntAll");
      if (elAll) elAll.innerText = MAGIC_WORDS_DB.length;
      const elF = document.getElementById("cntFalso");
      if (elF) elF.innerText = cntF;
      const elV = document.getElementById("cntVero");
      if (elV) elV.innerText = cntV;
      const elExc = document.getElementById("cntExc");
      if (elExc) elExc.innerText = cntE;
      const elP = document.getElementById("cntPhrases");
      if (elP) elP.innerText = cntP;
      const elPairs = document.getElementById("cntPairs");
      if (elPairs) elPairs.innerText = cntPairs;
      const elRep = document.getElementById("cntRepeated");
      if (elRep) elRep.innerText = cntRep;
      const elStatWords = document.getElementById("statWordsCount");
      if (elStatWords) elStatWords.innerText = MAGIC_WORDS_DB.length;
      const elStatQ = document.getElementById("statQuestionsCovered");
      if (elStatQ) {
        if (hasQ && totalQuestionsSet.size > 0) {
          elStatQ.innerText = totalQuestionsSet.size + " سؤالاً";
        } else {
          elStatQ.innerText = "457 سؤالاً";
        }
      }
    }'''

content = old_calc_pattern.sub(new_calc_func, content)

# 4. Fix openModal safely
content = content.replace(
    'activeModalQuestions = ALL_QUESTIONS_DATA.filter(q => re.test(q.q || ""));',
    '''if (typeof ALL_QUESTIONS_DATA !== 'undefined' && Array.isArray(ALL_QUESTIONS_DATA)) {
        activeModalQuestions = ALL_QUESTIONS_DATA.filter(q => re.test(q.q || ""));
      } else {
        activeModalQuestions = [];
      }'''
)

# 5. Fix window load listeners
old_listeners = '''window.addEventListener("DOMContentLoaded", () => {
      calculateCounts();
      renderCards();
      initMagicQuestionsIndex();
      updateMarathonDashboardUI();
      if (typeof initSignCounts === 'function') initSignCounts();
      if (typeof initTheoryCounts === 'function') initTheoryCounts();
    });'''

new_listeners = '''function initRadarFull() {
      calculateCounts();
      renderCards();
      if (typeof ALL_QUESTIONS_DATA !== 'undefined' && Array.isArray(ALL_QUESTIONS_DATA) && ALL_QUESTIONS_DATA.length > 0) {
        if (typeof initMagicQuestionsIndex === 'function') initMagicQuestionsIndex();
        if (typeof updateMarathonDashboardUI === 'function') updateMarathonDashboardUI();
      }
      if (typeof initSignCounts === 'function') initSignCounts();
      if (typeof initTheoryCounts === 'function') initTheoryCounts();
    }

    window.addEventListener("DOMContentLoaded", initRadarFull);
    window.addEventListener("load", () => {
      // Re-run when data_all_questions.js finishes loading
      initRadarFull();
    });'''

content = content.replace(old_listeners, new_listeners)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated parole-spia.html successfully!')

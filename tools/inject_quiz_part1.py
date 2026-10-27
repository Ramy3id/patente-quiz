# -*- coding: utf-8 -*-
"""
Build and inject the Part Quiz (Active Mastery) System into modular-chapter-engine.js
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'R:/Ramy/PATENTE/assets/js/modular-chapter-engine.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Engine State to include mastery data and quiz runner state
state_search = "userAnswers: {}, // id -> { userChoice, isCorrect }"
state_replace = """userAnswers: {}, // id -> { userChoice, isCorrect }
    masteredIds: new Set(), // ids solved correctly in part quiz
    mistakeIds: new Set(), // ids answered wrong in part quiz
    activeQuiz: null, // { gKey, questions: [], currentIndex: 0, results: [], isRetestOnly: false }"""

code = code.replace(state_search, state_replace, 1)

# 2. Update loadProgress and saveProgress
old_load = """    loadProgress() {
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
    },"""

new_load = """    loadProgress() {
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
    },"""

code = code.replace(old_load, new_load, 1)

old_save = """    saveProgress() {
      try {
        if (typeof window === 'undefined' || !window.localStorage) return;
        const payload = {
          userAnswers: this.userAnswers,
          userStats: this.userStats,
          updatedAt: Date.now()
        };
        window.localStorage.setItem(this.getStorageKey(), JSON.stringify(payload));
        if (typeof window.updatePortalProgress === 'function') {
          try { window.updatePortalProgress(); } catch (_) {}
        }
      } catch (e) {
        console.warn('ModularChapterEngine: could not save progress to localStorage', e);
      }
    },"""

new_save = """    saveProgress() {
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
    },"""

code = code.replace(old_save, new_save, 1)

# 3. Update resetChapterProgress to clear mastery
old_reset = """      this.userAnswers = {};
      this.userStats = { correct: 0, wrong: 0 };"""

new_reset = """      this.userAnswers = {};
      this.userStats = { correct: 0, wrong: 0 };
      this.masteredIds.clear();
      this.mistakeIds.clear();"""

code = code.replace(old_reset, new_reset, 1)

# 4. Update getOverallProgress to count mastery based on masteredIds
old_overall = """    getOverallProgress() {
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
    },"""

new_overall = """    getOverallProgress() {
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
    },"""

code = code.replace(old_overall, new_overall, 1)

# 5. Update bindGlobals to expose quiz functions
old_bind = "window.renderQuestions = () => self.renderQuestions();"
new_bind = """window.renderQuestions = () => self.renderQuestions();
      window.startPartQuiz = (gKey, count) => self.startPartQuiz(gKey, count);
      window.closePartQuiz = () => self.closePartQuiz();
      window.answerPartQuiz = (choice) => self.answerPartQuiz(choice);
      window.retestPartMissed = (gKey) => self.retestPartMissed(gKey);"""

code = code.replace(old_bind, new_bind, 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Part 1: State, Storage and Globals updated successfully!")

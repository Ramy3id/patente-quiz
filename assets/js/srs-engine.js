/**
 * =======================================================================
 * Patente B Pro - Spaced Repetition System (SRS) & Error Bank Engine
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description نظام التكرار المتباعد الذكي وسجل الأخطاء:
 *  - خوارزمية Leitner Box المعتمدة لتثبيت الذاكرة طويلة المدى
 *  - تسجيل كل سؤال أخطأ فيه الطالب وتصنيفه حسب مستوى الصعوبة
 *  - جدولة مراجعة الأسئلة: المستوى 1 (بعد يوم) -> المستوى 2 (بعد 3 أيام) -> المستوى 3 (بعد أسبوع)
 *  - إزالة السؤال من سجل الأخطاء تلقائياً بعد تجاوزه 3 مرات متتالية بنجاح
 */

class PatenteSRSEngine {
  constructor(storageKey = "patente_b_pro_srs_vault") {
    this.storageKey = storageKey;
    this.intervals = {
      1: 1 * 24 * 60 * 60 * 1000, // Box 1: يوم واحد
      2: 3 * 24 * 60 * 60 * 1000, // Box 2: 3 أيام
      3: 7 * 24 * 60 * 60 * 1000  // Box 3: 7 أيام
    };
  }

  /**
   * جلب قاعدة بيانات الأخطاء المحلية
   */
  getVault() {
    try {
      const raw = localStorage.getItem(this.storageKey);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      console.warn("خطأ في قراءة مخزن SRS:", e);
      return {};
    }
  }

  /**
   * حفظ قاعدة البيانات محلياً
   */
  saveVault(vault) {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(vault));
    } catch (e) {
      console.error("خطأ في حفظ مخزن SRS:", e);
    }
  }

  /**
   * تسجيل نتيجة سؤال (إما إجابة صحيحة أو خاطئة)
   * @param {Object} question كائن السؤال الكامل
   * @param {boolean} isCorrect هل الإجابة صحيحة أم لا
   */
  logQuestionAttempt(question, isCorrect) {
    if (!question || !question.id) return;
    const qId = String(question.id);
    const vault = this.getVault();
    const now = Date.now();

    if (!isCorrect) {
      // إجابة خاطئة: يرجع السؤال للصندوق رقم 1 فوراً
      if (!vault[qId]) {
        vault[qId] = {
          id: question.id,
          capitolo: question.capitolo || question.numero_capitolo || 1,
          domanda: question.domanda,
          immagine: question.immagine || null,
          risposta: question.risposta,
          traduzione: question.traduzione || "",
          spiegazione: question.spiegazione || "",
          trabocchetto: question.trabocchetto || "",
          parole_chiave: question.parole_chiave || [],
          box: 1,
          consecutiveCorrect: 0,
          errorCount: 1,
          lastReviewed: now,
          nextReviewDate: now + this.intervals[1]
        };
      } else {
        vault[qId].box = 1;
        vault[qId].consecutiveCorrect = 0;
        vault[qId].errorCount = (vault[qId].errorCount || 0) + 1;
        vault[qId].lastReviewed = now;
        vault[qId].nextReviewDate = now + this.intervals[1];
      }
    } else {
      // إجابة صحيحة
      if (vault[qId]) {
        vault[qId].consecutiveCorrect = (vault[qId].consecutiveCorrect || 0) + 1;
        vault[qId].lastReviewed = now;

        if (vault[qId].consecutiveCorrect >= 3) {
          // تم إتقان السؤال بالكامل وتثبيته في الذاكرة: يتم تخرجه من الأخطاء
          delete vault[qId];
        } else {
          // ترقية السؤال للصندوق التالي
          vault[qId].box = Math.min((vault[qId].box || 1) + 1, 3);
          vault[qId].nextReviewDate = now + this.intervals[vault[qId].box];
        }
      }
    }

    this.saveVault(vault);
  }

  /**
   * استخراج الأسئلة المستحقة للمراجعة اليوم
   */
  getDueQuestions() {
    const vault = this.getVault();
    const now = Date.now();
    const due = [];

    Object.values(vault).forEach((item) => {
      if (item.nextReviewDate <= now) {
        due.push(item);
      }
    });

    return due;
  }

  /**
   * استخراج جميع الأسئلة الموجودة في سجل الأخطاء
   */
  getAllErrorQuestions() {
    return Object.values(this.getVault());
  }

  /**
   * حساب إحصائيات بنك الأخطاء
   */
  getStats() {
    const all = this.getAllErrorQuestions();
    const due = this.getDueQuestions();
    const byBox = { 1: 0, 2: 0, 3: 0 };

    all.forEach((q) => {
      const b = q.box || 1;
      byBox[b] = (byBox[b] || 0) + 1;
    });

    return {
      totalErrors: all.length,
      dueToday: due.length,
      box1: byBox[1], // مستوى حرج (أخطاء حديثة)
      box2: byBox[2], // مستوى متوسط
      box3: byBox[3]  // مستوى متقدم وقريب من التثبيت
    };
  }

  /**
   * مسح سجل الأخطاء بالكامل
   */
  clearVault() {
    localStorage.removeItem(this.storageKey);
  }
}

// تصدير النظام
if (typeof window !== "undefined") {
  window.PatenteSRSEngine = PatenteSRSEngine;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PatenteSRSEngine;
}

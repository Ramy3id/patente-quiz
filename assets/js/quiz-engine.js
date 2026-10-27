/**
 * =======================================================================
 * Patente B Pro - Core Exam Engine (محرك الامتحان الوزاري الرسمي)
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محاكي الامتحان الوزاري الإيطالي المعتمد:
 *  - 30 سؤالاً ممثلاً من كافة الأبواب
 *  - توقيت تنازلي 20 دقيقة مع تحذير عند آخر 5 دقائق
 *  - معيار النجاح: 0 إلى 3 أخطاء (4 أخطاء فأكثر يعتبر رسوب)
 *  - تنقل حر وتعديل الإجابات قبل التسليم النهائي
 *  - شاشة تحليل الأخطاء و"كشف اللغز"
 */

class PatenteExamEngine {
  constructor(options = {}) {
    this.totalQuestions = options.totalQuestions || 30;
    this.durationMinutes = options.durationMinutes || 20;
    this.maxAllowedErrors = options.maxAllowedErrors || 3;
    
    this.questions = [];
    this.answers = {}; // { questionId: boolean (true for VERO, false for FALSO) }
    this.currentIndex = 0;
    
    this.remainingSeconds = this.durationMinutes * 60;
    this.timerInterval = null;
    this.isSubmitted = false;
    
    this.onTick = options.onTick || null;
    this.onFinish = options.onFinish || null;
  }

  /**
   * تحميل وحقن الأسئلة في المحرك
   * @param {Array} questionsPool بنك الأسئلة المتاح
   */
  loadQuestions(questionsPool) {
    if (!Array.isArray(questionsPool) || questionsPool.length === 0) {
      throw new Error("بنك الأسئلة فارغ أو غير صالح.");
    }
    
    // تطبيق الخوارزمية الوزارية الرسمية المتوازنة (25 باباً + توازن 15 VERO و 15 FALSO)
    this.questions = this.generateMinisterialQuestions(questionsPool);
    this.answers = {};
    this.currentIndex = 0;
    this.isSubmitted = false;
    this.remainingSeconds = this.durationMinutes * 60;
  }

  /**
   * خوارزمية السحب الوزاري الرسمي (تغطية 25 باباً وتوازن 15 VERO و 15 FALSO)
   */
  generateMinisterialQuestions(questionsPool) {
    const byCh = {};
    for (let i = 1; i <= 25; i++) {
      byCh[i] = { vero: [], falso: [] };
    }

    questionsPool.forEach(q => {
      const ch = q.ch || q.capitolo || 1;
      const isVero = (q.a !== undefined ? q.a : q.risposta) === true;
      if (byCh[ch]) {
        if (isVero) byCh[ch].vero.push(q);
        else byCh[ch].falso.push(q);
      }
    });

    const availableChapters = Object.keys(byCh).filter(ch => byCh[ch].vero.length > 0 && byCh[ch].falso.length > 0);
    
    // إذا كان بنك الأسئلة لا يغطي كافة الأبواب الـ 25، نطبق التوازن المباشر للصح والخطأ
    if (availableChapters.length < 25) {
      const veros = questionsPool.filter(q => (q.a !== undefined ? q.a : q.risposta) === true).sort(() => 0.5 - Math.random());
      const falsos = questionsPool.filter(q => (q.a !== undefined ? q.a : q.risposta) === false).sort(() => 0.5 - Math.random());
      const half = Math.floor(this.totalQuestions / 2);
      const targetV = Math.min(half, veros.length);
      const targetF = Math.min(this.totalQuestions - targetV, falsos.length);
      const selected = [...veros.slice(0, targetV), ...falsos.slice(0, targetF)];
      return selected.sort(() => 0.5 - Math.random());
    }

    // الخوارزمية الوزارية الرسمية المعتمدة:
    // الهدف: بالضبط 15 VERO و 15 FALSO
    // 1. سحب سؤال واحد من كل باب من الأبواب الـ 25 (12 صح و 13 خطأ، أو 13 صح و 12 خطأ بالتناوب)
    const is13Vero = Math.random() < 0.5;
    const targetBaseVero = is13Vero ? 13 : 12;
    const chList = Array.from({ length: 25 }, (_, i) => i + 1).sort(() => 0.5 - Math.random());
    const veroChapters = new Set(chList.slice(0, targetBaseVero));

    const selected = [];
    const usedIds = new Set();

    for (let ch = 1; ch <= 25; ch++) {
      const wantVero = veroChapters.has(ch);
      const list = (wantVero ? byCh[ch].vero : byCh[ch].falso).sort(() => 0.5 - Math.random());
      const q = list[0];
      if (q) {
        selected.push(q);
        usedIds.add(q.id);
      }
    }

    // 2. سحب الـ 5 أسئلة التكميلية من الأبواب المحورية الأساسية لتكملة الـ 15/15 تماماً
    const neededVero = 15 - targetBaseVero;
    const neededFalso = 15 - (25 - targetBaseVero);

    // الأبواب الوزارية المحورية: إشارات الخطر (2)، المنع (3)، الإلزام (4)، الأسبقية (5)، السرعة (11)، مسافة الأمان (12)، السير (13)، التقاطعات (14)، التجاوز (15)
    const primaryChapters = [2, 3, 4, 5, 11, 12, 13, 14, 15].sort(() => 0.5 - Math.random());
    const extraVeroChs = primaryChapters.slice(0, neededVero);
    const extraFalsoChs = primaryChapters.slice(neededVero, neededVero + neededFalso);

    extraVeroChs.forEach(ch => {
      const list = byCh[ch].vero.filter(q => !usedIds.has(q.id)).sort(() => 0.5 - Math.random());
      const q = list[0] || byCh[ch].vero[0];
      if (q) {
        selected.push(q);
        usedIds.add(q.id);
      }
    });

    extraFalsoChs.forEach(ch => {
      const list = byCh[ch].falso.filter(q => !usedIds.has(q.id)).sort(() => 0.5 - Math.random());
      const q = list[0] || byCh[ch].falso[0];
      if (q) {
        selected.push(q);
        usedIds.add(q.id);
      }
    });

    // 3. خلط ترتيب الأسئلة في النموذج عشوائياً لتماثل شاشة الاختبار الواقعية
    return selected.sort(() => 0.5 - Math.random());
  }

  /**
   * بدء المؤقت التنازلي للامتحان
   */
  startTimer() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    
    this.timerInterval = setInterval(() => {
      this.remainingSeconds--;
      
      if (typeof this.onTick === "function") {
        this.onTick(this.formatTime(), this.remainingSeconds);
      }
      
      if (this.remainingSeconds <= 0) {
        this.submitExam("TIMEOUT");
      }
    }, 1000);
  }

  /**
   * إيقاف المؤقت
   */
  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  /**
   * تسجيل إجابة لسؤال معين
   * @param {number|string} questionId معرف السؤال
   * @param {boolean} value true=VERO, false=FALSO
   */
  recordAnswer(questionId, value) {
    if (this.isSubmitted) return;
    this.answers[questionId] = Boolean(value);
    
    // Haptic Feedback for Mobile Touch (Apple HIG & Android Haptics)
    if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
      try { navigator.vibrate(12); } catch (_) {}
    }
  }

  /**
   * الحصول على السؤال الحالي
   */
  getCurrentQuestion() {
    return this.questions[this.currentIndex] || null;
  }

  /**
   * الانتقال إلى سؤال محدد بالمؤشر
   * @param {number} index
   */
  goToQuestion(index) {
    if (index >= 0 && index < this.questions.length) {
      this.currentIndex = index;
      return this.getCurrentQuestion();
    }
    return null;
  }

  nextQuestion() {
    return this.goToQuestion(this.currentIndex + 1);
  }

  prevQuestion() {
    return this.goToQuestion(this.currentIndex - 1);
  }

  /**
   * تنسيق الوقت المتبقي MM:SS
   */
  formatTime() {
    const mins = Math.floor(this.remainingSeconds / 60);
    const secs = this.remainingSeconds % 60;
    return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  }

  /**
   * حساب الإحصائيات الأولية للامتحان
   */
  getAnsweredCount() {
    return Object.keys(this.answers).length;
  }

  /**
   * تسليم وتصحيح الامتحان النهائي
   * @param {string} reason 'USER_SUBMIT' | 'TIMEOUT'
   */
  submitExam(reason = "USER_SUBMIT") {
    if (this.isSubmitted) return;
    this.isSubmitted = true;
    this.stopTimer();

    const analysis = {
      timestamp: new Date().toISOString(),
      reason,
      total: this.questions.length,
      answered: this.getAnsweredCount(),
      errors: 0,
      correct: 0,
      unanswered: 0,
      passed: false,
      details: []
    };

    this.questions.forEach((q, idx) => {
      const userAnswer = this.answers[q.id];
      const isAnswered = userAnswer !== undefined;
      const isCorrect = isAnswered && userAnswer === q.risposta;

      if (!isAnswered) {
        analysis.unanswered++;
        analysis.errors++; // في القانون الإيطالي السؤال المتروك يعتبر خطأ
      } else if (isCorrect) {
        analysis.correct++;
      } else {
        analysis.errors++;
      }

      analysis.details.push({
        index: idx + 1,
        id: q.id,
        capitolo: q.capitolo || q.numero_capitolo || q.ch || "عام",
        domanda: q.domanda || q.q || "",
        immagine: q.immagine || q.img || null,
        img: q.img || q.immagine || null,
        userAnswer: isAnswered ? userAnswer : null,
        correctAnswer: (q.risposta !== undefined) ? q.risposta : q.a,
        isCorrect,
        traduzione: q.traduzione || q.tr || "",
        spiegazione: q.spiegazione || q.sp || "",
        trabocchetto: q.trabocchetto || q.tb || "",
        parole_chiave: q.parole_chiave || q.pk || []
      });
    });

    analysis.passed = analysis.errors <= this.maxAllowedErrors;

    // Haptic Feedback based on Exam Result (Pass vs Fail)
    if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
      try {
        if (analysis.passed) {
          navigator.vibrate([20, 30, 40]);
        } else {
          navigator.vibrate([40, 60, 40]);
        }
      } catch (_) {}
    }

    // حفظ النتيجة محلياً
    this.saveResultHistory(analysis);

    if (typeof this.onFinish === "function") {
      this.onFinish(analysis);
    }

    return analysis;
  }

  /**
   * حفظ سجل الامتحان في التخزين المحلي
   */
  saveResultHistory(result) {
    try {
      const key = "patente_b_pro_exam_history";
      const existing = JSON.parse(localStorage.getItem(key) || "[]");
      existing.unshift({
        timestamp: result.timestamp,
        errors: result.errors,
        passed: result.passed,
        answered: result.answered
      });
      // الاحتفاظ بآخر 20 اختبار
      localStorage.setItem(key, JSON.stringify(existing.slice(0, 20)));
    } catch (e) {
      console.warn("تعذر حفظ سجل الاختبار في LocalStorage:", e);
    }
  }
}

// تصدير المحرك للاستخدام العام
if (typeof window !== "undefined") {
  window.PatenteExamEngine = PatenteExamEngine;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PatenteExamEngine;
}

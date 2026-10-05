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
    
    // خلط واختيار 30 سؤالاً عشوائياً
    const shuffled = [...questionsPool].sort(() => 0.5 - Math.random());
    this.questions = shuffled.slice(0, this.totalQuestions);
    this.answers = {};
    this.currentIndex = 0;
    this.isSubmitted = false;
    this.remainingSeconds = this.durationMinutes * 60;
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
        capitolo: q.capitolo || q.numero_capitolo || "عام",
        domanda: q.domanda,
        immagine: q.immagine || null,
        userAnswer: isAnswered ? userAnswer : null,
        correctAnswer: q.risposta,
        isCorrect,
        traduzione: q.traduzione || "",
        spiegazione: q.spiegazione || "",
        trabocchetto: q.trabocchetto || "",
        parole_chiave: q.parole_chiave || []
      });
    });

    analysis.passed = analysis.errors <= this.maxAllowedErrors;

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

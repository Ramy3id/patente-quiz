/**
 * =======================================================================
 * Patente B Pro - Mobile Swipe Flashcards Engine
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محرك بطاقات الفلاش كاردز التفاعلية للموبايل والديسكتوب:
 *  - دعم إيماءات اللمس السريع (Touch Gestures: Swipe Left / Swipe Right)
 *  - سحب لليمين ➡️ إجابة VERO
 *  - سحب لليسار ⬅️ إجابة FALSO
 *  - نقر/قلب البطاقة 🔄 لقراءة الشرح والترجمة وكشف الفخ
 *  - حركة سلسة بمعدل 60 إطاراً في الثانية (GPU Accelerated CSS Transforms)
 */

class PatenteFlashcardsEngine {
  constructor(containerElement, options = {}) {
    this.container = typeof containerElement === "string" 
      ? document.querySelector(containerElement) 
      : containerElement;
      
    this.questions = [];
    this.currentIndex = 0;
    this.threshold = options.threshold || 90; // مسافة السحب لتسجيل الإجابة بكسل
    
    this.touchStartX = 0;
    this.touchStartY = 0;
    this.touchCurrentX = 0;
    this.isDragging = false;
    
    this.onAnswer = options.onAnswer || null; // callback(question, userAnswer, isCorrect)
    this.onComplete = options.onComplete || null;
  }

  /**
   * تحميل الأسئلة في البطاقات
   * @param {Array} questionsList
   */
  loadQuestions(questionsList) {
    if (!Array.isArray(questionsList) || questionsList.length === 0) return;
    this.questions = [...questionsList];
    this.currentIndex = 0;
    this.renderCurrentCard();
  }

  /**
   * عرض البطاقة الحالية
   */
  renderCurrentCard() {
    if (!this.container) return;
    if (this.currentIndex >= this.questions.length) {
      this.renderCompletedState();
      return;
    }

    const q = this.questions[this.currentIndex];
    const total = this.questions.length;
    const progress = Math.round(((this.currentIndex) / total) * 100);

    this.container.innerHTML = `
      <div class="flashcard-wrapper">
        <div class="flashcard-progress-bar">
          <div class="flashcard-progress-fill" style="width: ${progress}%;"></div>
          <span class="flashcard-counter">${this.currentIndex + 1} / ${total}</span>
        </div>

        <div class="flashcard-card-stage">
          <div class="flashcard-card" id="activeFlashcard">
            <!-- الوجه الأمامي: السؤال والصورة -->
            <div class="flashcard-face flashcard-front">
              <div class="flashcard-badge">اسحب لليمين VERO / لليسار FALSO</div>
              ${q.immagine ? `<div class="flashcard-img-box"><img src="${q.immagine}" alt="Segnale" loading="lazy"></div>` : ""}
              <div class="flashcard-it-text">${q.domanda}</div>
              <div class="flashcard-tap-hint">👆 انقر على البطاقة لقلبها وقراءة الشرح والترجمة</div>
            </div>

            <!-- الوجه الخلفي: الشرح، الترجمة، والفخ -->
            <div class="flashcard-face flashcard-back">
              <div class="flashcard-result-badge ${q.risposta ? "badge-vero" : "badge-falso"}">
                الإجابة الصحيحة: ${q.risposta ? "VERO (صح)" : "FALSO (خطأ)"}
              </div>
              <div class="flashcard-ar-translation">
                <strong>📖 الترجمة:</strong> ${q.traduzione || "غير متوفرة"}
              </div>
              <div class="flashcard-explanation">
                <strong>💡 الشرح القانوني:</strong> ${q.spiegazione || "راجع نصوص كود السير."}
              </div>
              ${q.trabocchetto ? `
                <div class="flashcard-trap-box">
                  <strong>⚠️ فخ السؤال:</strong> ${q.trabocchetto}
                </div>
              ` : ""}
              <div class="flashcard-tap-hint">👆 انقر للعودة للسؤال أو اسحب للإجابة</div>
            </div>
          </div>
        </div>

        <!-- أزرار مساعدة سريعة للديسكتوب والموبايل -->
        <div class="flashcard-actions">
          <button type="button" class="fc-btn fc-btn-falso" id="btnSwipeFalso">
            <span class="fc-btn-icon">⬅️</span> FALSO (خطأ)
          </button>
          <button type="button" class="fc-btn fc-btn-flip" id="btnFlipCard">
            <span class="fc-btn-icon">🔄</span> قلب البطاقة
          </button>
          <button type="button" class="fc-btn fc-btn-vero" id="btnSwipeVero">
            VERO (صح) <span class="fc-btn-icon">➡️</span>
          </button>
        </div>
      </div>
    `;

    this.bindCardEvents();
  }

  /**
   * ربط أحداث اللمس والنقر
   */
  bindCardEvents() {
    const card = this.container.querySelector("#activeFlashcard");
    const btnFlip = this.container.querySelector("#btnFlipCard");
    const btnVero = this.container.querySelector("#btnSwipeVero");
    const btnFalso = this.container.querySelector("#btnSwipeFalso");

    if (!card) return;

    // قلب البطاقة
    const toggleFlip = () => card.classList.toggle("is-flipped");
    card.addEventListener("click", (e) => {
      // منع القلب إذا كان المستخدم يسحب
      if (Math.abs(this.touchCurrentX - this.touchStartX) < 10) {
        toggleFlip();
      }
    });
    if (btnFlip) btnFlip.addEventListener("click", toggleFlip);

    // أزرار الضغط السريع
    if (btnVero) btnVero.addEventListener("click", () => this.executeSwipe("right"));
    if (btnFalso) btnFalso.addEventListener("click", () => this.executeSwipe("left"));

    // أحداث اللمس للموبايل (Touch Events)
    card.addEventListener("touchstart", (e) => {
      this.touchStartX = e.touches[0].clientX;
      this.touchStartY = e.touches[0].clientY;
      this.touchCurrentX = this.touchStartX;
      this.isDragging = true;
      card.style.transition = "none";
    }, { passive: true });

    card.addEventListener("touchmove", (e) => {
      if (!this.isDragging) return;
      this.touchCurrentX = e.touches[0].clientX;
      const deltaX = this.touchCurrentX - this.touchStartX;
      const rotate = deltaX * 0.08;
      
      card.style.transform = `translateX(${deltaX}px) rotate(${rotate}deg)`;
      
      // إشارة لونية أثناء السحب
      if (deltaX > 30) {
        card.style.borderColor = "#10B981"; // أخضر VERO
      } else if (deltaX < -30) {
        card.style.borderColor = "#EF4444"; // أحمر FALSO
      } else {
        card.style.borderColor = "rgba(255, 255, 255, 0.15)";
      }
    }, { passive: true });

    card.addEventListener("touchend", () => {
      if (!this.isDragging) return;
      this.isDragging = false;
      const deltaX = this.touchCurrentX - this.touchStartX;

      if (deltaX > this.threshold) {
        this.executeSwipe("right");
      } else if (deltaX < -this.threshold) {
        this.executeSwipe("left");
      } else {
        // إعادة البطاقة لمكانها إذا لم يتجاوز السحب الحد الأدنى
        card.style.transition = "transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s";
        card.style.transform = "translateX(0px) rotate(0deg)";
        card.style.borderColor = "rgba(255, 255, 255, 0.15)";
      }
    });
  }

  /**
   * تنفيذ حركة الخروج وتسجيل الإجابة
   * @param {'right'|'left'} direction 
   */
  executeSwipe(direction) {
    const card = this.container.querySelector("#activeFlashcard");
    const q = this.questions[this.currentIndex];
    const userAnswer = direction === "right"; // right = VERO (true), left = FALSO (false)
    const isCorrect = userAnswer === q.risposta;

    if (card) {
      card.style.transition = "transform 0.4s ease-out, opacity 0.4s";
      const outX = direction === "right" ? window.innerWidth + 200 : -(window.innerWidth + 200);
      card.style.transform = `translateX(${outX}px) rotate(${direction === "right" ? 35 : -35}deg)`;
      card.style.opacity = "0";
    }

    if (typeof this.onAnswer === "function") {
      this.onAnswer(q, userAnswer, isCorrect);
    }

    setTimeout(() => {
      this.currentIndex++;
      this.renderCurrentCard();
    }, 280);
  }

  /**
   * شاشة اكتمال مراجعة البطاقات
   */
  renderCompletedState() {
    this.container.innerHTML = `
      <div class="flashcard-completed-box">
        <div class="fc-complete-icon">🎉</div>
        <h3>اكتملت مراجعة البطاقات بنجاح!</h3>
        <p>لقد قمت بمراجعة كافة الأسئلة المحددة في هذا القسم.</p>
        <button type="button" class="fc-btn fc-btn-restart" id="btnRestartCards">
          🔄 إعادة المراجعة من البداية
        </button>
      </div>
    `;

    const btnRestart = this.container.querySelector("#btnRestartCards");
    if (btnRestart) {
      btnRestart.addEventListener("click", () => {
        this.currentIndex = 0;
        this.renderCurrentCard();
      });
    }

    if (typeof this.onComplete === "function") {
      this.onComplete();
    }
  }
}

// تصدير المحرك
if (typeof window !== "undefined") {
  window.PatenteFlashcardsEngine = PatenteFlashcardsEngine;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PatenteFlashcardsEngine;
}

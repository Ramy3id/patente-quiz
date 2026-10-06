/**
 * =======================================================================
 * Patente B Pro - Mobile Swipe Flashcards Engine
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محرك بطاقات الفلاش كاردز التفاعلية للموبايل والديسكتوب:
 *  - دعم إيماءات اللمس السريع (Touch Gestures: Swipe Left / Swipe Right)
 *  - سحب لليمين ➡️ إجابة VERO
 *  - سحب لليسار ⬅️ إجابة FALSO
 *  - نقر/قلب البطاقة 🔄 لقراءة الشرح والترجمة وكشف الفخ (Touch + Click)
 *  - دعم كامل لقلب البطاقة باللمس وزر القلب على جميع الهواتف
 */

class PatenteFlashcardsEngine {
  constructor(containerElement, options = {}) {
    this.container = typeof containerElement === "string" 
      ? document.querySelector(containerElement) 
      : containerElement;
      
    this.questions = [];
    this.currentIndex = 0;
    this.threshold = options.threshold || 80;
    this.isFlipped = false;
    
    this.touchStartX = 0;
    this.touchStartY = 0;
    this.touchCurrentX = 0;
    this.touchCurrentY = 0;
    this.isDragging = false;
    
    this.onAnswer = options.onAnswer || null;
    this.onComplete = options.onComplete || null;
  }

  loadQuestions(questionsList) {
    if (!Array.isArray(questionsList) || questionsList.length === 0) return;
    this.questions = [...questionsList];
    this.currentIndex = 0;
    this.renderCurrentCard();
  }

  renderCurrentCard() {
    if (!this.container) return;
    if (this.currentIndex >= this.questions.length) {
      this.renderCompletedState();
      return;
    }

    this.isFlipped = false;
    const q = this.questions[this.currentIndex];
    const total = this.questions.length;
    const progress = Math.round(((this.currentIndex) / total) * 100);

    const imgFilename = q.immagine ? q.immagine.split('/').pop().trim() : null;
    const imgPath = imgFilename ? `../img_sign/${imgFilename}` : null;

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
              ${imgPath ? `<div class="flashcard-img-box"><img src="${imgPath}" alt="Segnale" loading="lazy" onerror="this.parentElement.style.display='none'"></div>` : ""}
              <div class="flashcard-it-text">${q.domanda}</div>
              <div class="flashcard-tap-hint">👆 المس البطاقة أو اضغط زر القلب للشرح</div>
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
              <div class="flashcard-tap-hint">👆 المس للعودة للسؤال أو اسحب للإجابة</div>
            </div>
          </div>
        </div>

        <!-- أزرار مساعدة سريعة للديسكتوب والموبايل -->
        <div class="flashcard-actions">
          <button type="button" class="fc-btn fc-btn-falso" id="btnSwipeFalso">
            <span class="fc-btn-icon">⬅️</span> FALSO
          </button>
          <button type="button" class="fc-btn fc-btn-flip" id="btnFlipCard">
            <span class="fc-btn-icon">🔄</span> قلب البطاقة
          </button>
          <button type="button" class="fc-btn fc-btn-vero" id="btnSwipeVero">
            VERO <span class="fc-btn-icon">➡️</span>
          </button>
        </div>
      </div>
    `;

    this.bindCardEvents();
  }

  bindCardEvents() {
    const card = this.container.querySelector("#activeFlashcard");
    const btnFlip = this.container.querySelector("#btnFlipCard");
    const btnVero = this.container.querySelector("#btnSwipeVero");
    const btnFalso = this.container.querySelector("#btnSwipeFalso");

    if (!card) return;

    // دالة قلب البطاقة الموحدة
    const toggleFlip = (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      this.isFlipped = !this.isFlipped;
      card.style.transform = ""; // إزالة أي Inline Transform للسماح لـ CSS بالدوران
      if (this.isFlipped) {
        card.classList.add("is-flipped");
      } else {
        card.classList.remove("is-flipped");
      }
    };

    // ربط زر قلب البطاقة (Click & Touch)
    if (btnFlip) {
      btnFlip.addEventListener("click", toggleFlip);
      btnFlip.addEventListener("touchend", (e) => {
        e.preventDefault();
        toggleFlip(e);
      });
    }

    // أزرار الضغط السريع
    if (btnVero) {
      btnVero.addEventListener("click", () => this.executeSwipe("right"));
      btnVero.addEventListener("touchend", (e) => {
        e.preventDefault();
        this.executeSwipe("right");
      });
    }
    if (btnFalso) {
      btnFalso.addEventListener("click", () => this.executeSwipe("left"));
      btnFalso.addEventListener("touchend", (e) => {
        e.preventDefault();
        this.executeSwipe("left");
      });
    }

    // النقر على البطاقة (ديسكتوب)
    card.addEventListener("click", (e) => {
      if (Math.abs(this.touchCurrentX - this.touchStartX) < 10 && Math.abs(this.touchCurrentY - this.touchStartY) < 10) {
        toggleFlip(e);
      }
    });

    // أحداث اللمس للموبايل (Touch Gestures)
    card.addEventListener("touchstart", (e) => {
      if (e.touches.length === 1) {
        this.touchStartX = e.touches[0].clientX;
        this.touchStartY = e.touches[0].clientY;
        this.touchCurrentX = this.touchStartX;
        this.touchCurrentY = this.touchStartY;
        this.isDragging = true;
        card.style.transition = "none";
      }
    }, { passive: true });

    card.addEventListener("touchmove", (e) => {
      if (!this.isDragging || e.touches.length !== 1) return;
      this.touchCurrentX = e.touches[0].clientX;
      this.touchCurrentY = e.touches[0].clientY;
      const deltaX = this.touchCurrentX - this.touchStartX;
      const deltaY = this.touchCurrentY - this.touchStartY;
      
      // التمرير الأفقي فقط إذا كانت الحركة أفقية غالبة
      if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 8) {
        const rotate = deltaX * 0.08;
        const flipY = this.isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
        card.style.transform = `translateX(${deltaX}px) rotate(${rotate}deg) ${flipY}`;
        
        if (deltaX > 25) {
          card.style.borderColor = "#10B981";
        } else if (deltaX < -25) {
          card.style.borderColor = "#EF4444";
        } else {
          card.style.borderColor = "rgba(255, 255, 255, 0.15)";
        }
      }
    }, { passive: true });

    card.addEventListener("touchend", (e) => {
      if (!this.isDragging) return;
      this.isDragging = false;
      const deltaX = this.touchCurrentX - this.touchStartX;
      const deltaY = this.touchCurrentY - this.touchStartY;

      if (Math.abs(deltaX) > this.threshold) {
        this.executeSwipe(deltaX > 0 ? "right" : "left");
      } else if (Math.abs(deltaX) < 10 && Math.abs(deltaY) < 10) {
        // نقرة لمس سريعة على الموبايل -> قلب البطاقة
        toggleFlip(e);
      } else {
        // إعادة البطاقة لمكانها
        card.style.transition = "transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s";
        card.style.transform = "";
        card.style.borderColor = "rgba(255, 255, 255, 0.12)";
      }
    });
  }

  executeSwipe(direction) {
    const card = this.container.querySelector("#activeFlashcard");
    const q = this.questions[this.currentIndex];
    const userAnswer = direction === "right";
    const isCorrect = userAnswer === q.risposta;

    if (card) {
      card.style.transition = "transform 0.35s ease-out, opacity 0.35s";
      const outX = direction === "right" ? window.innerWidth + 200 : -(window.innerWidth + 200);
      const flipY = this.isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
      card.style.transform = `translateX(${outX}px) rotate(${direction === "right" ? 30 : -30}deg) ${flipY}`;
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

  renderCompletedState() {
    this.container.innerHTML = `
      <div class="flashcard-completed-box" style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 20px; padding: 40px 20px; text-align: center;">
        <div style="font-size: 54px; margin-bottom: 12px;">🎉</div>
        <h3 style="color:#10B981; margin-bottom:8px; font-size:22px; font-weight:800;">اكتملت مراجعة البطاقات بنجاح!</h3>
        <p style="color:#94A3B8; margin-bottom:20px;">لقد قمت بمراجعة كافة الأسئلة المحددة في هذا القسم.</p>
        <button type="button" class="fc-btn" style="background: linear-gradient(135deg, #38BDF8, #2563EB); color: #fff; width:100%; max-width:300px; margin:0 auto;" id="btnRestartCards">
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

if (typeof window !== "undefined") {
  window.PatenteFlashcardsEngine = PatenteFlashcardsEngine;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PatenteFlashcardsEngine;
}

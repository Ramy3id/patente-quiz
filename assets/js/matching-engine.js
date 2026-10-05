/**
 * =======================================================================
 * Patente B Pro - Speed Matching Mini-Game Engine
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محرك لعبة المطابقة السريعة لتحدي الذاكرة وتثبيت المصطلحات:
 *  - مطابقة الإشارة بمعناها الصحيح
 *  - مطابقة المصطلح الإيطالي بالترجمة العربية في سباق مع الوقت
 *  - نظام النقاط والكومبو (Combo Score Multiplier)
 */

class PatenteMatchingGameEngine {
  constructor(containerElement, options = {}) {
    this.container = typeof containerElement === "string" 
      ? document.querySelector(containerElement) 
      : containerElement;

    this.pairs = [];
    this.selectedCard = null;
    this.matchedCount = 0;
    this.score = 0;
    this.streak = 0;
    this.timerSeconds = options.durationSeconds || 45;
    this.timerInterval = null;

    this.onScoreUpdate = options.onScoreUpdate || null;
    this.onGameOver = options.onGameOver || null;
  }

  /**
   * تحميل جولة جديدة من البطاقات (عادة 6 إلى 8 أزواج)
   * @param {Array} items قائمة العناصر { id, itText, arText, image }
   */
  startNewRound(items) {
    if (!Array.isArray(items) || items.length === 0) return;
    this.matchedCount = 0;
    this.streak = 0;
    this.score = 0;
    this.selectedCard = null;

    // تفكيك الأزواج إلى بطاقات منفصلة
    const cards = [];
    items.forEach((item, idx) => {
      // بطاقة الطرف الأول (الإيطالي أو الصورة)
      cards.push({
        pairId: `pair_${idx}`,
        type: "source",
        content: item.image 
          ? `<img src="${item.image}" alt="Signal" class="match-img">`
          : `<span class="match-it-text">${item.itText}</span>`
      });

      // بطاقة الطرف الثاني (الترجمة العربية أو المعنى)
      cards.push({
        pairId: `pair_${idx}`,
        type: "target",
        content: `<span class="match-ar-text">${item.arText}</span>`
      });
    });

    // خلط البطاقات عشوائياً
    this.cards = cards.sort(() => 0.5 - Math.random());
    this.renderBoard();
    this.startTimer();
  }

  renderBoard() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="matching-game-wrap">
        <div class="matching-header">
          <div class="matching-timer">⏳ <span id="matchTimerVal">${this.timerSeconds}</span>s</div>
          <div class="matching-score">⭐ النقاط: <span id="matchScoreVal">${this.score}</span></div>
          <div class="matching-streak">🔥 الكومبو: x<span id="matchStreakVal">${Math.max(1, this.streak)}</span></div>
        </div>
        <div class="matching-grid" id="matchingGrid">
          ${this.cards.map((card, idx) => `
            <div class="match-card" data-index="${idx}" data-pair="${card.pairId}">
              <div class="match-card-content">${card.content}</div>
            </div>
          `).join("")}
        </div>
      </div>
    `;

    this.bindEvents();
  }

  bindEvents() {
    const grid = this.container.querySelector("#matchingGrid");
    if (!grid) return;

    grid.querySelectorAll(".match-card").forEach((cardEl) => {
      cardEl.addEventListener("click", () => this.handleCardClick(cardEl));
    });
  }

  handleCardClick(cardEl) {
    if (cardEl.classList.contains("is-matched") || cardEl.classList.contains("is-selected")) {
      return;
    }

    if (!this.selectedCard) {
      // البطاقة الأولى المختارة
      this.selectedCard = cardEl;
      cardEl.classList.add("is-selected");
    } else {
      // البطاقة الثانية
      const firstPair = this.selectedCard.dataset.pair;
      const secondPair = cardEl.dataset.pair;

      if (firstPair === secondPair && this.selectedCard !== cardEl) {
        // تطابق صحيح!
        this.selectedCard.classList.remove("is-selected");
        this.selectedCard.classList.add("is-matched");
        cardEl.classList.add("is-matched");

        this.streak++;
        this.score += 10 * this.streak;
        this.matchedCount += 2;
        this.selectedCard = null;

        this.updateHeader();

        // هل اكتملت الجولة؟
        if (this.matchedCount === this.cards.length) {
          this.endGame(true);
        }
      } else {
        // خطأ
        cardEl.classList.add("is-wrong");
        this.selectedCard.classList.add("is-wrong");
        this.streak = 0;
        this.updateHeader();

        setTimeout(() => {
          if (this.selectedCard) this.selectedCard.classList.remove("is-selected", "is-wrong");
          cardEl.classList.remove("is-wrong");
          this.selectedCard = null;
        }, 500);
      }
    }
  }

  updateHeader() {
    const sEl = this.container.querySelector("#matchScoreVal");
    const stEl = this.container.querySelector("#matchStreakVal");
    if (sEl) sEl.textContent = this.score;
    if (stEl) stEl.textContent = Math.max(1, this.streak);

    if (typeof this.onScoreUpdate === "function") {
      this.onScoreUpdate(this.score, this.streak);
    }
  }

  startTimer() {
    clearInterval(this.timerInterval);
    const tEl = this.container.querySelector("#matchTimerVal");

    this.timerInterval = setInterval(() => {
      this.timerSeconds--;
      if (tEl) tEl.textContent = this.timerSeconds;

      if (this.timerSeconds <= 0) {
        this.endGame(false);
      }
    }, 1000);
  }

  endGame(isWin) {
    clearInterval(this.timerInterval);
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="matching-game-over">
        <div class="game-over-icon">${isWin ? "🏆" : "⌛"}</div>
        <h3>${isWin ? "رائع! أنهيت المطابقة بنجاح!" : "انتهى الوقت!"}</h3>
        <p class="final-score">إجمالي النقاط المحققة: <strong>${this.score}</strong> نقطة</p>
      </div>
    `;

    if (typeof this.onGameOver === "function") {
      this.onGameOver({ isWin, score: this.score });
    }
  }
}

// تصدير المحرك
if (typeof window !== "undefined") {
  window.PatenteMatchingGameEngine = PatenteMatchingGameEngine;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PatenteMatchingGameEngine;
}

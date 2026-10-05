/**
 * =======================================================================
 * Patente B Pro - Animated 2D Intersection Simulator Engine
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محاكي التقاطعات الحركي التفاعلي:
 *  - رسم تقاطعات المرور الشهيرة (مثل Fig 638, Fig 515, Fig 646) بـ SVG فائق الوضوح
 *  - تحريك مسارات السيارات واحدة تلو الأخرى حسب الأسبقية القانونية (قاعدة اليمين الفارغ)
 *  - إضاءة اليمين الحر باللون الأخضر والمسار المعطل بالأحمر
 *  - أزرار تحكم: (تشغيل الحركة ▶️، خطوة بخطوة ⏭️، إعادة ضبط 🔄)
 */

class PatenteIntersectionSimulator {
  constructor(containerElement, intersectionData) {
    this.container = typeof containerElement === "string"
      ? document.querySelector(containerElement)
      : containerElement;

    this.data = intersectionData || this.getDefaultIntersection();
    this.currentStep = 0;
    this.isPlaying = false;
    this.animationTimer = null;

    this.render();
  }

  /**
   * بيانات التقاطع الافتراضي (الشكل الشهير 638: تقاطع بـ 4 سيارات)
   */
  getDefaultIntersection() {
    return {
      id: "fig_638",
      title: "تقاطع الشكل 638 (قاعدة اليمين الخالي)",
      description: "تطبيق قاعدة الأسبقية لليمين: من لديه اليمين فارغ يمر أولاً.",
      orderDescription: "ترتيب المرور الصحيح: R أولاً، ثم A، ثم C، وأخيراً D.",
      vehicles: [
        { id: "R", name: "السيارة R (صفراء)", color: "#F59E0B", start: { x: 300, y: 150 }, end: { x: 100, y: 150 }, path: "M 320 200 L 80 200", step: 1, freeRight: true },
        { id: "A", name: "السيارة A (حمراء)", color: "#EF4444", start: { x: 200, y: 320 }, end: { x: 200, y: 80 }, path: "M 200 320 L 200 80", step: 2, freeRight: false },
        { id: "C", name: "السيارة C (زرقاء)", color: "#3B82F6", start: { x: 80, y: 200 }, end: { x: 320, y: 200 }, path: "M 80 200 L 320 200", step: 3, freeRight: false },
        { id: "D", name: "السيارة D (خضراء)", color: "#10B981", start: { x: 200, y: 80 }, end: { x: 200, y: 320 }, path: "M 200 80 L 200 320", step: 4, freeRight: false }
      ]
    };
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="intersection-sim-wrapper">
        <div class="sim-header">
          <div class="sim-title">🚦 ${this.data.title}</div>
          <div class="sim-badge" id="simStatusBadge">الخطوة: في الانتظار</div>
        </div>

        <div class="sim-viewport">
          <svg viewBox="0 0 400 400" class="intersection-svg" id="intersectionSvg">
            <!-- أرضية التقاطع والأسفلت -->
            <rect x="0" y="0" width="400" height="400" fill="#1E293B" />
            
            <!-- أذرع التقاطع الصليبي -->
            <rect x="140" y="0" width="120" height="400" fill="#0F172A" />
            <rect x="0" y="140" width="400" height="120" fill="#0F172A" />

            <!-- خطوط المسارات البيضاء المتقطعة -->
            <line x1="200" y1="0" x2="200" y2="140" stroke="#FFFFFF" stroke-dasharray="8,8" stroke-width="3" />
            <line x1="200" y1="260" x2="200" y2="400" stroke="#FFFFFF" stroke-dasharray="8,8" stroke-width="3" />
            <line x1="0" y1="200" x2="140" y2="200" stroke="#FFFFFF" stroke-dasharray="8,8" stroke-width="3" />
            <line x1="260" y1="200" x2="400" y2="200" stroke="#FFFFFF" stroke-dasharray="8,8" stroke-width="3" />

            <!-- مركز التقاطع المفتوح -->
            <circle cx="200" cy="200" r="30" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2" />

            <!-- المركبات والمسارات الحركية -->
            ${this.data.vehicles.map((v) => `
              <g class="sim-vehicle-group" id="veh_${v.id}">
                <!-- مسار الحركة المتوقع -->
                <path d="${v.path}" fill="none" stroke="${v.color}" stroke-width="3" stroke-dasharray="4,4" opacity="0.4" id="path_${v.id}" />
                
                <!-- مجسم السيارة -->
                <circle cx="${v.start.x}" cy="${v.start.y}" r="18" fill="${v.color}" stroke="#FFFFFF" stroke-width="2" class="veh-circle" id="circle_${v.id}" />
                <text x="${v.start.x}" y="${v.start.y + 5}" font-family="JetBrains Mono, monospace" font-size="14" font-weight="bold" fill="#FFFFFF" text-anchor="middle" id="text_${v.id}">${v.id}</text>
              </g>
            `).join("")}
          </svg>
        </div>

        <div class="sim-explanation-panel">
          <div class="sim-rule-info" id="simRuleInfo">${this.data.orderDescription}</div>
        </div>

        <div class="sim-controls">
          <button type="button" class="sim-btn sim-btn-play" id="btnPlaySim">▶️ تشغيل الحركة المتتابعة</button>
          <button type="button" class="sim-btn sim-btn-step" id="btnStepSim">⏭️ خطوة بخطوة</button>
          <button type="button" class="sim-btn sim-btn-reset" id="btnResetSim">🔄 إعادة ضبط</button>
        </div>
      </div>
    `;

    this.bindControls();
  }

  bindControls() {
    const btnPlay = this.container.querySelector("#btnPlaySim");
    const btnStep = this.container.querySelector("#btnStepSim");
    const btnReset = this.container.querySelector("#btnResetSim");

    if (btnPlay) btnPlay.addEventListener("click", () => this.togglePlay());
    if (btnStep) btnStep.addEventListener("click", () => this.stepForward());
    if (btnReset) btnReset.addEventListener("click", () => this.resetSimulation());
  }

  stepForward() {
    const totalSteps = this.data.vehicles.length;
    if (this.currentStep >= totalSteps) {
      this.resetSimulation();
      return;
    }

    this.currentStep++;
    const currentVeh = this.data.vehicles.find((v) => v.step === this.currentStep);

    if (currentVeh) {
      const circle = this.container.querySelector(`#circle_${currentVeh.id}`);
      const text = this.container.querySelector(`#text_${currentVeh.id}`);
      const badge = this.container.querySelector("#simStatusBadge");
      const info = this.container.querySelector("#simRuleInfo");

      if (circle && text) {
        circle.style.transition = "cx 1s ease-in-out, cy 1s ease-in-out";
        text.style.transition = "x 1s ease-in-out, y 1s ease-in-out";

        circle.setAttribute("cx", currentVeh.end.x);
        circle.setAttribute("cy", currentVeh.end.y);
        text.setAttribute("x", currentVeh.end.x);
        text.setAttribute("y", currentVeh.end.y + 5);
      }

      if (badge) {
        badge.textContent = `تمر الآن: ${currentVeh.name}`;
        badge.style.background = currentVeh.color;
        badge.style.color = "#FFFFFF";
      }

      if (info) {
        info.innerHTML = `<strong>الخطوة ${this.currentStep}:</strong> تعبر ${currentVeh.name} لأن يمينها أصبح خالياً تماماً بعد حركة من قبلها.`;
      }
    }
  }

  togglePlay() {
    if (this.isPlaying) {
      clearInterval(this.animationTimer);
      this.isPlaying = false;
      const btn = this.container.querySelector("#btnPlaySim");
      if (btn) btn.textContent = "▶️ استئناف الحركة";
    } else {
      this.isPlaying = true;
      const btn = this.container.querySelector("#btnPlaySim");
      if (btn) btn.textContent = "⏸️ إيقاف مؤقت";

      this.animationTimer = setInterval(() => {
        if (this.currentStep >= this.data.vehicles.length) {
          clearInterval(this.animationTimer);
          this.isPlaying = false;
          if (btn) btn.textContent = "🔄 إعادة التشغيل";
        } else {
          this.stepForward();
        }
      }, 1400);
    }
  }

  resetSimulation() {
    clearInterval(this.animationTimer);
    this.isPlaying = false;
    this.currentStep = 0;

    this.data.vehicles.forEach((v) => {
      const circle = this.container.querySelector(`#circle_${v.id}`);
      const text = this.container.querySelector(`#text_${v.id}`);
      if (circle && text) {
        circle.style.transition = "none";
        text.style.transition = "none";
        circle.setAttribute("cx", v.start.x);
        circle.setAttribute("cy", v.start.y);
        text.setAttribute("x", v.start.x);
        text.setAttribute("y", v.start.y + 5);
      }
    });

    const badge = this.container.querySelector("#simStatusBadge");
    const info = this.container.querySelector("#simRuleInfo");
    const btnPlay = this.container.querySelector("#btnPlaySim");

    if (badge) {
      badge.textContent = "الخطوة: في الانتظار";
      badge.style.background = "rgba(255,255,255,0.1)";
    }
    if (info) info.textContent = this.data.orderDescription;
    if (btnPlay) btnPlay.textContent = "▶️ تشغيل الحركة المتتابعة";
  }
}

// تصدير المحرك
if (typeof window !== "undefined") {
  window.PatenteIntersectionSimulator = PatenteIntersectionSimulator;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PatenteIntersectionSimulator;
}

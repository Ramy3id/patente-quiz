/**
 * =======================================================================
 * Patente B Pro - Interactive 3D / Isometric Road & Traffic Simulator
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محاكي الطريق والمسارات ثلاثي الأبعاد التفاعلي (Capitolo 01):
 *  - رسم مقطع الطريق الإيطالي بأبعاد ثلاثية واقعية (Isometric 3D Perspective)
 *  - محاكاة حركة السيارات الحية في مسارات السير العادي والتجاوز
 *  - استعراض الأشكال الوزارية (Fig 550, Fig 552, Fig 562) ثلاثية الأبعاد
 *  - سيناريوهات تفاعلية: (السير العادي، مناورة التجاوز، المنعطفات، التوقف في الطوارئ)
 *  - فحص أجزاء الطريق بضغطة زر مع كشف الفخاخ المرورية
 *  - زوايا رؤية متعددة: (3D Isometric, علوي 2D Aerial, منظور السائق Driver)
 *  - متوافق 100% مع الهواتف الذكية وأجهزة الكمبيوتر مع تحكم باللمس والصوت
 */

class PatenteRoad3DSimulator {
  constructor(containerElement, options = {}) {
    this.container = typeof containerElement === "string"
      ? document.querySelector(containerElement)
      : containerElement;

    this.currentScenario = options.initialScenario || "sorpasso_normale";
    this.cameraView = "isometric"; // 'isometric', 'topdown', 'cockpit'
    this.isNightMode = false;
    this.simSpeed = 1;
    this.selectedZone = null;
    this.animationId = null;

    // Simulation Clock & Vehicles
    this.simTime = 0;
    this.vehicles = [];

    this.scenarios = {
      sorpasso_normale: {
        id: "sorpasso_normale",
        title: "مناورة التجاوز الصحيحة (Art. 148 CdS)",
        subtitle: "الالتزام بالسير في المسار الأيمن واستخدام الأيسر للتجاوز فقط",
        figText: "الشكل الوزاري 550 • طريق بـ 4 مسارات",
        description: "السير العادي إلزامي في المسار الأيمن (Corsia di destra). عند التجاوز، ننتقل للمسار الأيسر مع تشغيل إشارة الانعطاف (Freccia)، ثم نعود للمسار الأيمن بمجرد اكتمال المناورة.",
        ruleBadge: "قاعدة إلزامية: السير العادي في أقصى اليمين الحر",
        trapAlert: "⚠️ فخ الامتحان: في طريق متعدد المسارات مثل Fig 550، التجاوز مسموح به حتى في المنعطفات والقمم (anche in curva e sui dossi) لأنه لا يتطلب تجاوز الخط المتصل أو الدخول في الاتجاه المعاكس!",
        numLanes: 4,
        isDivided: false,
        hasEmergency: true
      },
      carreggiate_separate: {
        id: "carreggiate_separate",
        title: "طريق بنهري طريق منفصلين (Fig 552)",
        subtitle: "حاجز وسطي خرساني (Spartitraffico) يقسم الطريق لنهرين مستقلين",
        figText: "الشكل الوزاري 552 • نهرين و 6 مسارات",
        description: "وجود الحاجز الفاصل (Spartitraffico) يجعل الطريق مكوناً من نهري طريق (Due Carreggiate). كل نهر ذو اتجاه واحد (Senso Unico) يضم 3 مسارات: أيمن للسير العادي، وأوسط وأيسر للتجاوز.",
        ruleBadge: "ميزة هندسية: نهرا طريق مستقلان باتجاه واحد",
        trapAlert: "⚠️ فخ الامتحان: لا تخلط بين عدد المسارات وعدد الأنهار! هنا الطريق يضم 2 أنهُر طريق (Carreggiate) و 6 مسارات (Corsie).",
        numLanes: 6,
        isDivided: true,
        hasEmergency: true
      },
      emergenza_guasto: {
        id: "emergenza_guasto",
        title: "حارة الطوارئ والتوقف العارض (Corsia di Emergenza)",
        subtitle: "حظر السير والوقوف؛ مخصصة حصراً للأعطال والحالات الطارئة",
        figText: "الأوتوستراد والطرق السريعة الرئيسية",
        description: "حارة الطوارئ ليست جزءاً من نهر الطريق (Fuori dalla Carreggiata). يُسمح بالوقوف فيها فقط في حالات العطل المفاجئ (Guasto) أو الوعكة الصحية الخطيرة (Malessere)، بحد أقصى 3 ساعات مع ارتداء السترة العاكسة.",
        ruleBadge: "قانون السير: حظر السير والتجاوز في حارة الطوارئ",
        trapAlert: "⚠️ فخ الامتحان: هل حارة الطوارئ جزء من نهر الطريق (Fa parte della carreggiata)؟ الإجابة قطعاً FALSO!",
        numLanes: 4,
        isDivided: true,
        hasEmergency: true
      }
    };

    this.zonesInfo = {
      marciapiede: {
        name: "رصيف المشاة (Marciapiede)",
        badge: "خارج نهر الطريق",
        color: "#f59e0b",
        desc: "جزء من الطريق مخصص لحركة المشاة فقط. يُمنع سير أو وقوف المركبات عليه إلا في حالة وجود خطوط ركن مخصصة ترسمها البلدية."
      },
      banchina: {
        name: "القارعة الجانبية (Banchina)",
        badge: "خارج نهر الطريق",
        color: "#fb923c",
        desc: "المساحة الواقعة خارج الخط الأبيض المتصل للحد الجانبي للطريق. لا تنتمي لنهر الطريق، ويحظر السير عليها أو وقوف السيارات ليلاً."
      },
      corsia_destra: {
        name: "حارة السير العادي (Corsia di Marcia Ordinaria)",
        badge: "داخل نهر الطريق",
        color: "#10b981",
        desc: "المسار الإلزامي لكل مركبة تسير في الظروف العادية، ويجب التزامه دائماً ما لم تكن هناك مناورة تجاوز نشطة."
      },
      corsia_sorpasso: {
        name: "حارة التجاوز (Corsia di Sorpasso)",
        badge: "داخل نهر الطريق",
        color: "#38bdf8",
        desc: "المسار المخصص فقط لتجاوز المركبات الأبطأ، ويجب إخلاؤه والعودة لليمين فور إتمام المناورة."
      },
      spartitraffico: {
        name: "الحاجز الفاصل (Spartitraffico)",
        badge: "منشأة فاصلة هندسية",
        color: "#ef4444",
        desc: "حاجز هندسي ثابت (خرساني أو حديقة) يفصل الطريق إلى نهري طريق مستقلين. يحظر اجتيازه أو الدوران فوقه نهائياً."
      },
      emergenza: {
        name: "حارة الطوارئ (Corsia di Emergenza)",
        badge: "خارج نهر الطريق",
        color: "#eab308",
        desc: "مخصصة لمركبات الإسعاف والشرطة، ولتوقف المركبات المعطلة فقط لمدة لا تزيد عن 3 ساعات. لا تتبع نهر الطريق."
      }
    };

    this.init();
  }

  init() {
    if (!this.container) return;
    this.renderLayout();
    this.setupCanvas();
    this.setupEvents();
    this.resetVehicles();
    this.startAnimationLoop();
  }

  renderLayout() {
    this.container.innerHTML = `
      <div class="road3d-wrapper">
        <!-- 3D Header -->
        <div class="road3d-header">
          <div class="road3d-title-block">
            <div class="road3d-badge">
              <span>🎮 3D INTERACTIVE SIMULATOR</span>
              <span class="live-dot"></span>
            </div>
            <h3 class="road3d-heading" id="road3dTitle">محاكي مقطع الطريق وحركة المرور ثلاثي الأبعاد</h3>
            <p class="road3d-subheading" id="road3dSubtitle">استكشاف مباشر لقواعد السير، مناورات التجاوز، والتشريح الهندسي</p>
          </div>

          <!-- Scenario Switcher Buttons -->
          <div class="road3d-scenarios-nav">
            <button class="road3d-sc-btn ${this.currentScenario === 'sorpasso_normale' ? 'active' : ''}" data-sc="sorpasso_normale">
              <span>🏎️</span>
              <span>مناورة التجاوز (Fig 550)</span>
            </button>
            <button class="road3d-sc-btn ${this.currentScenario === 'carreggiate_separate' ? 'active' : ''}" data-sc="carreggiate_separate">
              <span>🛣️</span>
              <span>أنهار منفصلة (Fig 552)</span>
            </button>
            <button class="road3d-sc-btn ${this.currentScenario === 'emergenza_guasto' ? 'active' : ''}" data-sc="emergenza_guasto">
              <span>🚨</span>
              <span>حارة الطوارئ (Emergenza)</span>
            </button>
          </div>
        </div>

        <!-- Canvas Viewport with Overlay Controls -->
        <div class="road3d-viewport-container">
          <canvas id="road3dCanvas" class="road3d-canvas"></canvas>

          <!-- Floating Camera & Tool Bar -->
          <div class="road3d-controls-overlay">
            <div class="road3d-cam-group">
              <button class="road3d-tool-btn active" id="btnCamIso" title="منظور ثلاثي الأبعاد مجسم">
                <span>📐 3D مجسم</span>
              </button>
              <button class="road3d-tool-btn" id="btnCamTop" title="رؤية علوية مسقط أفقي 2D">
                <span>🛰️ علوي 2D</span>
              </button>
            </div>

            <div class="road3d-action-group">
              <button class="road3d-tool-btn" id="btnNightToggle" title="تبديل الوضع الليلي ومصابيح السيارات">
                <span>🌙 ليل / نهار</span>
              </button>
              <button class="road3d-tool-btn" id="btnRestartAnim" title="إعادة تشغيل المناورة">
                <span>🔄 إعادة المناورة</span>
              </button>
            </div>
          </div>

          <!-- Interactive Zone Hotspots Overlay -->
          <div class="road3d-hotspots-bar">
            <span class="hotspot-label">🔎 فحص أجزاء الطريق:</span>
            <button class="hotspot-chip" data-zone="marciapiede">الرصيف (Marciapiede)</button>
            <button class="hotspot-chip" data-zone="banchina">القارعة (Banchina)</button>
            <button class="hotspot-chip" data-zone="corsia_destra">حارة السير (Marcia)</button>
            <button class="hotspot-chip" data-zone="corsia_sorpasso">حارة التجاوز (Sorpasso)</button>
            <button class="hotspot-chip" data-zone="spartitraffico">الحاجز الفاصل (Spartitraffico)</button>
            <button class="hotspot-chip" data-zone="emergenza">الطوارئ (Emergenza)</button>
          </div>
        </div>

        <!-- Dynamic Scenario Information & Trap Card -->
        <div class="road3d-info-card" id="road3dInfoCard">
          <div class="info-card-header">
            <div class="info-card-title-group">
              <h4 class="info-title" id="infoTitleText">مناورة التجاوز الصحيحة (Art. 148 CdS)</h4>
              <span class="info-fig-pill" id="infoFigPill">الشكل الوزاري 550</span>
            </div>
            <span class="info-rule-badge" id="infoRuleBadge">قاعدة: السير في أقصى اليمين الحر</span>
          </div>

          <p class="info-desc" id="infoDescText">
            السير العادي إلزامي في المسار الأيمن (Corsia di destra). عند التجاوز، ننتقل للمسار الأيسر مع تشغيل إشارة الانعطاف (Freccia)، ثم نعود للمسار الأيمن بمجرد اكتمال المناورة.
          </p>

          <div class="info-trap-alert" id="infoTrapAlert">
            ⚠️ فخ الامتحان: في طريق متعدد المسارات مثل Fig 550، التجاوز مسموح به حتى في المنعطفات والقمم (anche in curva e sui dossi) لأنه لا يتطلب غزو الاتجاه المعاكس!
          </div>

          <!-- Zone Detail Popover (Shown when clicking chips) -->
          <div class="zone-inspection-box" id="zoneInspectionBox" style="display:none;">
            <div class="zone-insp-header">
              <strong id="zoneInspTitle" style="color:var(--emerald-primary);"></strong>
              <span class="zone-insp-pill" id="zoneInspBadge"></span>
            </div>
            <p id="zoneInspDesc" style="font-size:0.86rem; color:var(--text-secondary); margin-top:4px;"></p>
          </div>
        </div>
      </div>
    `;

    this.injectStyles();
  }

  injectStyles() {
    if (document.getElementById("road3d-styles")) return;
    const style = document.createElement("style");
    style.id = "road3d-styles";
    style.innerHTML = `
      .road3d-wrapper {
        background: radial-gradient(circle at 50% 0%, #1e1e2d 0%, #0d0d12 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        overflow: hidden;
        margin: 28px 0;
        box-shadow: 0 20px 48px rgba(0,0,0,0.6);
        position: relative;
        font-family: inherit;
        direction: rtl;
      }
      .road3d-header {
        padding: 22px 24px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      @media (min-width: 900px) {
        .road3d-header {
          flex-direction: row;
          align-items: center;
          justify-content: space-between;
        }
      }
      .road3d-title-block { display: flex; flex-direction: column; gap: 4px; }
      .road3d-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 800;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.28);
        padding: 3px 10px;
        border-radius: 20px;
        width: fit-content;
      }
      .live-dot {
        width: 7px;
        height: 7px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10b981;
        animation: pulseLive 1.5s infinite;
      }
      @keyframes pulseLive {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.8); }
      }
      .road3d-heading {
        font-size: 1.25rem;
        font-weight: 800;
        color: #fff;
        margin: 0;
      }
      .road3d-subheading {
        font-size: 0.85rem;
        color: #a1a1aa;
        margin: 0;
      }
      .road3d-scenarios-nav {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }
      .road3d-sc-btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #d4d4d8;
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 0.82rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 6px;
        font-family: inherit;
      }
      .road3d-sc-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.25);
        color: #fff;
      }
      .road3d-sc-btn.active {
        background: rgba(56, 189, 248, 0.18);
        border-color: #38bdf8;
        color: #38bdf8;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.25);
      }
      .road3d-viewport-container {
        position: relative;
        width: 100%;
        height: 380px;
        background: #09090d;
        overflow: hidden;
      }
      @media (min-width: 768px) {
        .road3d-viewport-container { height: 460px; }
      }
      .road3d-canvas {
        width: 100%;
        height: 100%;
        display: block;
      }
      .road3d-controls-overlay {
        position: absolute;
        top: 14px;
        right: 14px;
        left: 14px;
        display: flex;
        justify-content: space-between;
        pointer-events: none;
        z-index: 10;
      }
      .road3d-cam-group, .road3d-action-group {
        display: flex;
        gap: 6px;
        pointer-events: auto;
      }
      .road3d-tool-btn {
        background: rgba(15, 15, 20, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #e4e4e7;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.18s ease;
        font-family: inherit;
      }
      .road3d-tool-btn:hover {
        background: rgba(30, 30, 40, 0.9);
        border-color: #fff;
        color: #fff;
      }
      .road3d-tool-btn.active {
        background: #38bdf8;
        color: #09090d;
        border-color: #38bdf8;
      }
      .road3d-hotspots-bar {
        position: absolute;
        bottom: 12px;
        right: 12px;
        left: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
        overflow-x: auto;
        padding-bottom: 4px;
        z-index: 10;
        scrollbar-width: none;
      }
      .road3d-hotspots-bar::-webkit-scrollbar { display: none; }
      .hotspot-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #a1a1aa;
        white-space: nowrap;
        background: rgba(0,0,0,0.6);
        padding: 4px 8px;
        border-radius: 6px;
      }
      .hotspot-chip {
        background: rgba(24, 24, 32, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #e4e4e7;
        backdrop-filter: blur(8px);
        font-size: 0.73rem;
        font-weight: 600;
        padding: 5px 10px;
        border-radius: 20px;
        white-space: nowrap;
        cursor: pointer;
        transition: all 0.15s ease;
        font-family: inherit;
      }
      .hotspot-chip:hover, .hotspot-chip.active {
        background: rgba(99, 102, 241, 0.35);
        border-color: #818cf8;
        color: #fff;
      }
      .road3d-info-card {
        padding: 20px 24px;
        background: rgba(18, 18, 24, 0.95);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .info-card-header {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
      }
      .info-card-title-group {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
      }
      .info-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #f4f4f5;
        margin: 0;
      }
      .info-fig-pill {
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
      }
      .info-rule-badge {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34d399;
        font-size: 0.76rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
      }
      .info-desc {
        color: #d4d4d8;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0;
      }
      .info-trap-alert {
        background: rgba(244, 63, 94, 0.1);
        border: 1px solid rgba(244, 63, 94, 0.3);
        color: #fca5a5;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        line-height: 1.5;
      }
      .zone-inspection-box {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 12px 16px;
        border-radius: 10px;
        margin-top: 4px;
      }
      .zone-insp-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .zone-insp-pill {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        background: rgba(255,255,255,0.1);
        color: #fff;
      }
    `;
    document.head.appendChild(style);
  }

  setupCanvas() {
    this.canvas = this.container.querySelector("#road3dCanvas");
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");

    const resize = () => {
      const rect = this.canvas.getBoundingClientRect();
      this.canvas.width = rect.width * (window.devicePixelRatio || 1);
      this.canvas.height = rect.height * (window.devicePixelRatio || 1);
      this.ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
      this.w = rect.width;
      this.h = rect.height;
    };

    window.addEventListener("resize", resize);
    resize();
  }

  setupEvents() {
    // Scenario buttons
    const scBtns = this.container.querySelectorAll(".road3d-sc-btn");
    scBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        const sc = btn.dataset.sc;
        this.switchScenario(sc);
        scBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        if (window.soundEngine) window.soundEngine.click();
      });
    });

    // Camera buttons
    const btnIso = this.container.querySelector("#btnCamIso");
    const btnTop = this.container.querySelector("#btnCamTop");
    btnIso.addEventListener("click", () => {
      this.cameraView = "isometric";
      btnIso.classList.add("active");
      btnTop.classList.remove("active");
      if (window.soundEngine) window.soundEngine.click();
    });
    btnTop.addEventListener("click", () => {
      this.cameraView = "topdown";
      btnTop.classList.add("active");
      btnIso.classList.remove("active");
      if (window.soundEngine) window.soundEngine.click();
    });

    // Night mode
    const btnNight = this.container.querySelector("#btnNightToggle");
    btnNight.addEventListener("click", () => {
      this.isNightMode = !this.isNightMode;
      btnNight.classList.toggle("active", this.isNightMode);
      if (window.soundEngine) window.soundEngine.toggle();
    });

    // Restart animation
    const btnRestart = this.container.querySelector("#btnRestartAnim");
    btnRestart.addEventListener("click", () => {
      this.resetVehicles();
      if (window.soundEngine) window.soundEngine.click();
    });

    // Hotspot chips
    const chips = this.container.querySelectorAll(".hotspot-chip");
    chips.forEach(chip => {
      chip.addEventListener("click", () => {
        const zoneKey = chip.dataset.zone;
        this.selectZone(zoneKey);
        chips.forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        if (window.soundEngine) window.soundEngine.click();
      });
    });
  }

  switchScenario(scKey) {
    if (!this.scenarios[scKey]) return;
    this.currentScenario = scKey;
    const sc = this.scenarios[scKey];

    // Update UI text
    this.container.querySelector("#road3dTitle").innerText = sc.title;
    this.container.querySelector("#road3dSubtitle").innerText = sc.subtitle;
    this.container.querySelector("#infoTitleText").innerText = sc.title;
    this.container.querySelector("#infoFigPill").innerText = sc.figText;
    this.container.querySelector("#infoRuleBadge").innerText = sc.ruleBadge;
    this.container.querySelector("#infoDescText").innerText = sc.description;
    this.container.querySelector("#infoTrapAlert").innerHTML = sc.trapAlert;

    this.resetVehicles();
  }

  selectZone(zoneKey) {
    this.selectedZone = zoneKey;
    const box = this.container.querySelector("#zoneInspectionBox");
    const info = this.zonesInfo[zoneKey];
    if (!info) return;

    box.style.display = "block";
    this.container.querySelector("#zoneInspTitle").innerText = info.name;
    this.container.querySelector("#zoneInspBadge").innerText = info.badge;
    this.container.querySelector("#zoneInspDesc").innerText = info.desc;
  }

  resetVehicles() {
    this.simTime = 0;
    this.vehicles = [];

    if (this.currentScenario === "sorpasso_normale") {
      // Car A (White sedan: slow in right lane)
      this.vehicles.push({
        id: "carA",
        name: "سيارة السير العادي A",
        color: "#ffffff",
        x: 180,
        lane: 1, // right lane
        targetLane: 1,
        speed: 1.2,
        isBlinking: false
      });
      // Car B (Blue sports: overtakes Car A)
      this.vehicles.push({
        id: "carB",
        name: "سيارة التجاوز B",
        color: "#38bdf8",
        x: 40,
        lane: 1, // starts behind A in right lane
        targetLane: 1,
        speed: 2.2,
        isBlinking: false,
        phase: 0 // 0: approach, 1: shift left, 2: pass, 3: shift right
      });
    } else if (this.currentScenario === "carreggiate_separate") {
      // 3 lanes in our carreggiata
      this.vehicles.push({
        id: "car1",
        color: "#10b981",
        x: 120,
        lane: 1, // far right
        speed: 1.4
      });
      this.vehicles.push({
        id: "car2",
        color: "#fbbf24",
        x: 60,
        lane: 2, // middle lane overtaking
        speed: 2.0
      });
      this.vehicles.push({
        id: "car3",
        color: "#f43f5e",
        x: 20,
        lane: 3, // fast left lane
        speed: 2.6
      });
    } else if (this.currentScenario === "emergenza_guasto") {
      // Broken down car in emergency lane
      this.vehicles.push({
        id: "broken",
        name: "سيارة معطلة في الطوارئ",
        color: "#f59e0b",
        x: 220,
        lane: 0, // emergency lane
        speed: 0,
        isHazardOn: true
      });
      // Moving traffic in normal lane
      this.vehicles.push({
        id: "cruiser",
        color: "#38bdf8",
        x: 80,
        lane: 1,
        speed: 1.8
      });
    }
  }

  startAnimationLoop() {
    const loop = () => {
      this.updatePhysics();
      this.draw();
      this.animationId = requestAnimationFrame(loop);
    };
    this.animationId = requestAnimationFrame(loop);
  }

  updatePhysics() {
    this.simTime += 0.016;

    if (this.currentScenario === "sorpasso_normale") {
      const carA = this.vehicles.find(v => v.id === "carA");
      const carB = this.vehicles.find(v => v.id === "carB");

      if (carA && carB) {
        carA.x += carA.speed;
        if (carA.x > 700) carA.x = -60;

        // Overtaking State Machine for Car B
        if (carB.phase === 0) {
          carB.x += carB.speed;
          if (carA.x - carB.x < 110) {
            carB.phase = 1; // start moving to left lane
            carB.isBlinking = "left";
          }
        } else if (carB.phase === 1) {
          carB.x += carB.speed;
          carB.lane += 0.04;
          if (carB.lane >= 2) {
            carB.lane = 2;
            carB.phase = 2; // passing in left lane
            carB.isBlinking = false;
          }
        } else if (carB.phase === 2) {
          carB.x += carB.speed;
          if (carB.x - carA.x > 100) {
            carB.phase = 3; // return to right lane
            carB.isBlinking = "right";
          }
        } else if (carB.phase === 3) {
          carB.x += carB.speed;
          carB.lane -= 0.04;
          if (carB.lane <= 1) {
            carB.lane = 1;
            carB.phase = 0; // complete
            carB.isBlinking = false;
          }
        }

        if (carB.x > 720) {
          carB.x = -100;
          carB.phase = 0;
          carB.lane = 1;
          carB.isBlinking = false;
        }
      }
    } else {
      this.vehicles.forEach(v => {
        if (v.speed > 0) {
          v.x += v.speed;
          if (v.x > 700) v.x = -80;
        }
      });
    }
  }

  draw() {
    if (!this.ctx || !this.w || !this.h) return;
    const ctx = this.ctx;
    const w = this.w;
    const h = this.h;

    ctx.clearRect(0, 0, w, h);

    // Background Sky / Horizon
    const skyGrad = ctx.createLinearGradient(0, 0, 0, h);
    if (this.isNightMode) {
      skyGrad.addColorStop(0, "#050508");
      skyGrad.addColorStop(0.5, "#0b0c16");
      skyGrad.addColorStop(1, "#121324");
    } else {
      skyGrad.addColorStop(0, "#0f172a");
      skyGrad.addColorStop(0.5, "#1e293b");
      skyGrad.addColorStop(1, "#090d16");
    }
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, w, h);

    // Save Context for 3D Camera Transformation
    ctx.save();

    if (this.cameraView === "isometric") {
      // 3D Perspective Projection
      ctx.translate(w / 2, h * 0.72);
      ctx.scale(1, 0.58);
      ctx.rotate(-0.35);
    } else {
      // Topdown 2D
      ctx.translate(w * 0.1, h * 0.35);
    }

    this.drawRoadComponents(ctx);
    this.drawVehicles(ctx);

    ctx.restore();

    // Draw Night Glow Overlay
    if (this.isNightMode) {
      ctx.fillStyle = "rgba(5, 5, 12, 0.4)";
      ctx.fillRect(0, 0, w, h);
    }
  }

  drawRoadComponents(ctx) {
    const roadLen = 950;
    const laneWidth = 52;

    // Road Layers Coordinates (Y axis)
    // -50: Marciapiede (Sidewalk)
    // -20: Banchina / Emergenza
    // 0: Carreggiata Start
    // 0 -> 104: Lanes 1 & 2
    // 104 -> 120: Spartitraffico (Median)
    // 120 -> 224: Opposing Carreggiata

    // 1. Marciapiede (Sidewalk)
    const isMarciapiedeActive = this.selectedZone === "marciapiede";
    ctx.fillStyle = isMarciapiedeActive ? "#f59e0b" : (this.isNightMode ? "#1f2937" : "#334155");
    ctx.fillRect(-150, -60, roadLen, 25);
    // Curb stones
    ctx.fillStyle = "#64748b";
    ctx.fillRect(-150, -37, roadLen, 4);

    // 2. Banchina / Emergenza (Shoulder)
    const isBanchinaActive = this.selectedZone === "banchina" || this.selectedZone === "emergenza";
    ctx.fillStyle = isBanchinaActive ? "#f97316" : (this.isNightMode ? "#111827" : "#1e293b");
    ctx.fillRect(-150, -33, roadLen, 30);

    // Edge Line (Continuous White Solid Line: Limite Carreggiata)
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(-150, -3, roadLen, 3);

    // 3. Carreggiata Asphalt (Main Roadway)
    const isCarreggiataActive = this.selectedZone === "corsia_destra" || this.selectedZone === "corsia_sorpasso";
    ctx.fillStyle = this.isNightMode ? "#09090b" : "#0f172a";
    ctx.fillRect(-150, 0, roadLen, 110);

    // Lane 1 Highlight (Corsia di Destra)
    if (this.selectedZone === "corsia_destra") {
      ctx.fillStyle = "rgba(16, 185, 129, 0.25)";
      ctx.fillRect(-150, 0, roadLen, laneWidth);
    }

    // Broken Line (Striscia Discontinua between Lane 1 & 2)
    ctx.fillStyle = "#ffffff";
    for (let x = -150; x < roadLen - 150; x += 40) {
      ctx.fillRect(x, laneWidth - 1.5, 20, 3);
    }

    // Lane 2 Highlight (Corsia di Sorpasso)
    if (this.selectedZone === "corsia_sorpasso") {
      ctx.fillStyle = "rgba(56, 189, 248, 0.25)";
      ctx.fillRect(-150, laneWidth, roadLen, laneWidth);
    }

    // 4. Center Median / Lines (Spartitraffico or Double Solid Line)
    if (this.currentScenario === "carreggiate_separate") {
      // Physical Barrier (Spartitraffico Guardrail)
      const isSpartiActive = this.selectedZone === "spartitraffico";
      ctx.fillStyle = isSpartiActive ? "#ef4444" : "#475569";
      ctx.fillRect(-150, 110, roadLen, 24);
      // Guardrail metallic reflection
      ctx.fillStyle = "#94a3b8";
      ctx.fillRect(-150, 120, roadLen, 4);
    } else {
      // Double Solid Line (Doppia Striscia Continua)
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(-150, 107, roadLen, 3);
      ctx.fillRect(-150, 113, roadLen, 3);
    }

    // 5. Opposing Lanes Asphalt
    ctx.fillStyle = this.isNightMode ? "#09090b" : "#0f172a";
    ctx.fillRect(-150, 134, roadLen, 108);

    // Opposing broken line
    ctx.fillStyle = "#ffffff";
    for (let x = -150; x < roadLen - 150; x += 40) {
      ctx.fillRect(x, 134 + laneWidth - 1.5, 20, 3);
    }

    // Opposing edge line
    ctx.fillRect(-150, 242, roadLen, 3);

    // Opposing Shoulder
    ctx.fillStyle = this.isNightMode ? "#111827" : "#1e293b";
    ctx.fillRect(-150, 245, roadLen, 30);
  }

  drawVehicles(ctx) {
    const laneWidth = 52;
    const laneOffset = 26;

    this.vehicles.forEach(v => {
      // Y position calculated from lane number
      // lane 0: emergency (-16)
      // lane 1: right (26)
      // lane 2: left (78)
      // lane 3: 3rd lane (130)
      let vy = 0;
      if (v.lane === 0) vy = -16;
      else vy = (v.lane - 0.5) * laneWidth;

      const vx = v.x;

      ctx.save();
      ctx.translate(vx, vy);

      // Car Shadow
      ctx.fillStyle = "rgba(0, 0, 0, 0.55)";
      ctx.beginPath();
      ctx.ellipse(22, 2, 28, 12, 0, 0, Math.PI * 2);
      ctx.fill();

      // Car Body (3D extrusion look)
      ctx.fillStyle = v.color;
      ctx.beginPath();
      ctx.roundRect(0, -11, 44, 22, 5);
      ctx.fill();

      // Windshield & Roof
      ctx.fillStyle = "#0f172a";
      ctx.beginPath();
      ctx.roundRect(10, -9, 22, 18, 3);
      ctx.fill();

      // Roof top
      ctx.fillStyle = v.color;
      ctx.beginPath();
      ctx.roundRect(14, -8, 14, 16, 2);
      ctx.fill();

      // Headlights (Front is +X)
      ctx.fillStyle = "#fef08a";
      ctx.fillRect(42, -9, 3, 4);
      ctx.fillRect(42, 5, 3, 4);

      // Night Headlight Beams
      if (this.isNightMode || v.isHazardOn) {
        const beamGrad = ctx.createRadialGradient(45, 0, 5, 140, 0, 90);
        beamGrad.addColorStop(0, "rgba(254, 240, 138, 0.45)");
        beamGrad.addColorStop(1, "rgba(254, 240, 138, 0)");
        ctx.fillStyle = beamGrad;
        ctx.beginPath();
        ctx.moveTo(45, -8);
        ctx.lineTo(150, -40);
        ctx.lineTo(150, 40);
        ctx.lineTo(45, 8);
        ctx.closePath();
        ctx.fill();
      }

      // Taillights (Red)
      ctx.fillStyle = "#ef4444";
      ctx.fillRect(-2, -9, 2, 4);
      ctx.fillRect(-2, 5, 2, 4);

      // Turn Signals / Blinker (Freccia)
      if (v.isBlinking) {
        const isBlinkOn = Math.floor(Date.now() / 250) % 2 === 0;
        if (isBlinkOn) {
          ctx.fillStyle = "#f59e0b";
          if (v.isBlinking === "left" || v.isHazardOn) {
            ctx.beginPath();
            ctx.arc(42, -10, 4, 0, Math.PI * 2);
            ctx.arc(-1, -10, 4, 0, Math.PI * 2);
            ctx.fill();
          }
          if (v.isBlinking === "right" || v.isHazardOn) {
            ctx.beginPath();
            ctx.arc(42, 10, 4, 0, Math.PI * 2);
            ctx.arc(-1, 10, 4, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }

      ctx.restore();
    });
  }

  destroy() {
    if (this.animationId) cancelAnimationFrame(this.animationId);
  }
}

// Auto-initialize if element with ID road-3d-simulator-container exists
document.addEventListener("DOMContentLoaded", () => {
  const target = document.getElementById("road-3d-simulator-container");
  if (target) {
    window.road3dInstance = new PatenteRoad3DSimulator(target);
  }
});

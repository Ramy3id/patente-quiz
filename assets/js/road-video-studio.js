/**
 * =======================================================================
 * Patente B Pro - 3D Maneuver & Vehicle Motion Simulator
 * (ستوديو محاكاة حركات ومناورات السيارات التوضيحي ثلاثي الأبعاد)
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محاكي حركي سينمائي فائق الدقة (60 FPS Canvas) يركز حصرياً على:
 *  - توضيح حركة السيارات ومسارات المناورات عملياً (كيف تتم المناورة خطوة بخطوة)
 *  - الحفاظ على مسافة الأمان وسرعة رد الفعل والفرملة
 *  - السير الصحيح في الحارات وتجاوز الترام والدخول لحارة الطوارئ
 *  - التحكم الزمني التفاعلي: تشغيل/إيقاف، إرجاع، تسريع/تبطيء (0.5x Slow-Motion)، وشريط تمرير زمني
 *  - ربط فوري بالمخطط الوزاري الرسمي وأسئلة الامتحان
 */

class PatenteVideoStudio {
  constructor(containerElement) {
    this.container = typeof containerElement === "string"
      ? document.querySelector(containerElement)
      : containerElement;

    this.activeId = "sorpasso_curva";
    this.isPlaying = true;
    this.playbackSpeed = 1.0;
    this.showTelemetry = true;
    this.simTime = 0; // 0 to 1
    this.animFrameId = null;
    this.lastTimestamp = 0;

    // Interactive variations
    this.tailgatingMode = false; // for distance sim

    this.maneuvers = [
      {
        id: "sorpasso_curva",
        title: "مناورة التجاوز في المنعطف والتلال (Fig. 550)",
        titleIt: "Sorpasso in curva su carreggiata a 4 corsie",
        badge: "الأكثر تكراراً في الامتحان",
        duration: "محاكاة حركية 60FPS",
        thumbnail: "../Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/immagini/550.png",
        article: "Art. 148 & Art. 143 Codice della Strada",
        summary: "شاهد بدقة حركة السيارة المتجاوزة: الطريق مقسم إلى مسارين لكل اتجاه مع خط مزدوج متصل، وبالتالي تتم المناورة داخل نفس الاتجاه دون اجتياز الخط أو غزو مسار الاتجاه المقابل، وهو ما يفسر جواز التجاوز حتى في المنعطفات والتلال.",
        phases: [
          { from: 0.0, to: 0.25, ar: "المرحلة 1: الاقتراب في المسار الأيمن وتشغيل الغماز الأيسر (Frecce a sinistra)", it: "Avvicinamento e indicatore di direzione" },
          { from: 0.25, to: 0.45, ar: "المرحلة 2: الانتقال السلس للمسار الأيسر دون ملامسة الخط المزدوج", it: "Cambio corsia di sorpasso in sicurezza" },
          { from: 0.45, to: 0.75, ar: "المرحلة 3: إتمام التجاوز داخل المنحنى مع الحفاظ التام على المسار", it: "Sorpasso completato nella curva senza invadere l'opposto" },
          { from: 0.75, to: 1.0, ar: "المرحلة 4: تشغيل الغماز الأيمن والعودة بأمان للمسار الأيمن", it: "Rientro nella corsia di destra con freccia a destra" }
        ],
        keyPoints: [
          "السير العادي إلزامي في المسار الأيمن (Corsia di destra).",
          "المسار الأيسر مخصص حصراً للتجاوز (Corsia di sorpasso).",
          "التجاوز مسموح به في المنعطفات والتلال (Consentito in curva e sui dossi) لأن كل اتجاه يمتلك مسارين مستقلين."
        ],
        quizTrap: {
          qIt: "In una carreggiata del tipo rappresentato si può sorpassare anche in curva",
          qAr: "في نهر طريق من النوع الموضح (شكل 550) يجوز التجاوز حتى في المنعطفات",
          ans: true,
          explanation: "صحيح (VERO)! لأن كل اتجاه يحتوي على مسارين مستقلين، والتجاوز يتم دون عبور الخط المزدوج أو ملاقاة سيارات قادمة في وجهك."
        }
      },
      {
        id: "distanza_sicurezza",
        title: "مسافة الأمان وسرعة رد الفعل والفرملة (Distanza di Sicurezza)",
        titleIt: "Spazio di reazione, frenatura e arresto",
        badge: "قاعدة السلامة الجوهرية",
        duration: "محاكاة حركية 60FPS",
        thumbnail: "../Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/immagini/302.png",
        article: "Art. 149 Codice della Strada",
        summary: "محاكاة حركية توضح ماذا يحدث عند فرملة سيارة المقدمة فجأة: تتبع حركة السيارة الخلفية خلال زمن رد الفعل (1 ثانية تقريباً بدون نقص بالسرعة) ثم مسافة الفرملة حتى التوقف الآمن دون اصطدام.",
        phases: [
          { from: 0.0, to: 0.35, ar: "المرحلة 1: سير السيارتين بسرعة 90 كم/س مع الحفاظ على مسافة الأمان بالأخضر", it: "Marcia regolare a 90 km/h con distanza corretta" },
          { from: 0.35, to: 0.55, ar: "المرحلة 2: فرملة مفاجئة للسيارة الأمامية + زمن رد فعل السائق الخلفي (أصفر)", it: "Frenata improvvisa + Spazio di reazione (1 sec)" },
          { from: 0.55, to: 0.85, ar: "المرحلة 3: اشتعال أضواء فرامل السيارة الخلفية وبدء التباطؤ (برتقالي)", it: "Spazio di frenatura attivo" },
          { from: 0.85, to: 1.0, ar: "المرحلة 4: التوقف التام بأمان مع بقاء مسافة احتياطية تمنع الاصطدام", it: "Arresto completo in totale sicurezza" }
        ],
        keyPoints: [
          "مسافة الأمان يجب ألا تقل على الأقل عن مسافة زمن رد الفعل (Spazio percorso nel tempo di reazione).",
          "زمن رد الفعل الطبيعي للإنسان هو حوالي ثانية واحدة.",
          "مسافة التوقف الكلية = مسافة رد الفعل + مسافة الفرملة (Spazio totale di arresto)."
        ],
        quizTrap: {
          qIt: "La distanza di sicurezza deve essere aumentata se il veicolo che precede è un autocarro pesante",
          qAr: "يجب زيادة مسافة الأمان إذا كانت المركبة التي تسير أمامك شاحنة ثقيلة",
          ans: true,
          explanation: "صحيح (VERO)! لأن الشاحنات تحجب الرؤية للأمام وقد تسقط حمولتها أو تتوقف بشكل يحتاج مسافة رؤية أكبر."
        }
      },
      {
        id: "corsia_destra",
        title: "التمركز في الحارة والسير أقصى اليمين (Occupa la corsia più libera a destra)",
        titleIt: "Uso delle corsie in autostrada a tre corsie",
        badge: "قواعد السير الأساسية",
        duration: "محاكاة حركية 60FPS",
        thumbnail: "../Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/immagini/552.png",
        article: "Art. 143 Codice della Strada",
        summary: "توضيح لحركة المركبات على طريق سريع بثلاث حارات: السير العادي يكون دائماً في الحارة الأكثر حرية على اليمين، واستخدام الحارة الوسطى واليسرى حصراً للتجاوز، مع العودة الفورية لليمين.",
        phases: [
          { from: 0.0, to: 0.25, ar: "المرحلة 1: السير في الحارة اليمنى الحرة (الالتزام بالقاعدة الأساسية)", it: "Marcia normale nella corsia più a destra" },
          { from: 0.25, to: 0.55, ar: "المرحلة 2: الاقتراب من مركبة بطيئة والانتقال للحارة الوسطى للتجاوز", it: "Spostamento in corsia centrale per sorpasso" },
          { from: 0.55, to: 0.75, ar: "المرحلة 3: إنهاء التجاوز والابتعاد عن المركبة المتجاوزة", it: "Completamento manovra di sorpasso" },
          { from: 0.75, to: 1.0, ar: "المرحلة 4: الرجوع الفوري للحارة اليمنى الحرة وترك الحارات الأخرى خالية", it: "Rientro immediato a destra" }
        ],
        keyPoints: [
          "يجب السير دائماً في الحارة الأكثر خلوّاً إلى اليمين (Corsia più libera a destra).",
          "الحارات الإضافية لليسار مخصصة حصراً للتجاوز.",
          "البقاء في المسار الأوسط بدون حاجة يُعد مخالفة مرورية تستوجب سحب النقاط."
        ],
        quizTrap: {
          qIt: "Su un'autostrada a tre corsie per senso di marcia si può percorrere la corsia di mezzo se quella di destra è libera",
          qAr: "على طريق سريع بثلاث حارات لكل اتجاه، يجوز السير في الحارة الوسطى حتى لو كانت الحارة اليمنى خالية",
          ans: false,
          explanation: "خطأ (FALSO)! يجب دائماً السير في الحارة الأكثر خلوّاً على اليمين وعدم احتلال الحارة الوسطى دون داعٍ."
        }
      },
      {
        id: "tram_salvagente",
        title: "تجاوز الترام في وجود رصيف الأمان (Sorpasso Tram con Salvagente)",
        titleIt: "Sorpasso del tram in fermata con o senza salvagente",
        badge: "فخ امتحاني كلاسيكي",
        duration: "محاكاة حركية 60FPS",
        thumbnail: "../Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/immagini/302.png",
        article: "Art. 148 comma 9 CdS",
        summary: "محاكاة حركية للمركبة عند الاقتراب من ترام متوقف لركوب ونزول الركاب: يظهر رصيف الأمان (Salvagente) كحاجز حماية، مما يسمح للسيارة بتجاوز الترام من اليمين بأمان تام دون انتظار.",
        phases: [
          { from: 0.0, to: 0.30, ar: "المرحلة 1: اقتراب السيارة والترام من محطة ركوب الركاب في المدينة", it: "Avvicinamento tram e auto alla fermata" },
          { from: 0.30, to: 0.60, ar: "المرحلة 2: توقف الترام + صعود الركاب فوق رصيف الأمان المرتفع (Salvagente)", it: "Tram fermo con passeggeri protetti sul salvagente" },
          { from: 0.60, to: 0.85, ar: "المرحلة 3: مرور السيارة بأمان من يمين الترام دون لمس الركاب المحميين", it: "Sorpasso a destra consentito in presenza del salvagente" },
          { from: 0.85, to: 1.0, ar: "المرحلة 4: استمرار السير ومغادرة المحطة", it: "Proseguimento della marcia" }
        ],
        keyPoints: [
          "تجاوز الترام من اليمين مسموح به إذا كان هناك رصيف أمان (Salvagente).",
          "إذا لم يكن هناك رصيف أمان وكان الترام متوقفاً، يُحظر التجاوز تماماً حتى انتهاء صعود ونزول الركاب وتحرك الترام.",
          "يجوز تجاوز الترام من اليسار فقط إذا كان نهر الطريق باتجاه واحد (Senso unico) أو كان هناك متسع كافٍ دون غزو المسار المعاكس."
        ],
        quizTrap: {
          qIt: "È consentito il sorpasso a destra del tram fermo per la salita dei passeggeri se esiste il salvagente",
          qAr: "يُسمح بتجاوز الترام من جهة اليمين وهو متوقف لركوب الركاب إذا وُجد رصيف أمان (Salvagente)",
          ans: true,
          explanation: "صحيح (VERO)! لأن رصيف الأمان المرتفع يحمي الركاب من الاصطدام بالمركبات المارة على اليمين."
        }
      },
      {
        id: "corsia_emergenza",
        title: "الدخول الاضطراري لحارة الطوارئ والتوقف القانوني (Corsia di Emergenza - Fig. 305)",
        titleIt: "Uso corretto della corsia di emergenza in caso di guasto o malessere",
        badge: "قواعد الأوتوستراد",
        duration: "محاكاة حركية 60FPS",
        thumbnail: "../Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/immagini/305.png",
        article: "Art. 176 Codice della Strada",
        summary: "شاهد الحركة العملية للسيارة عند حدوث عطل ميكانيكي أو وعكة صحية: تشغيل إشارات التنبيه الرباعية الوامضة (4 Frecce)، التباطؤ التدريجي، الانعطاف بزاوية هادئة لحارة الطوارئ، والتوقف قرب الحافة اليمنى.",
        phases: [
          { from: 0.0, to: 0.25, ar: "المرحلة 1: حدوث عطل مفاجئ وتشغيل إشارات التنبيه الرباعية (4 Frecce)", it: "Guasto improvviso e accensione 4 frecce" },
          { from: 0.25, to: 0.55, ar: "المرحلة 2: تخفيف السرعة والانتقال التدريجي لحارة الطوارئ", it: "Decelerazione e ingresso graduale nella corsia di emergenza" },
          { from: 0.55, to: 0.80, ar: "المرحلة 3: التوقف بمحاذاة الحافة اليمنى لتأمين مسافة مرور لسيارات الإسعاف", it: "Arresto a filo destro della corsia di emergenza" },
          { from: 0.80, to: 1.0, ar: "المرحلة 4: وضع مثلث التحذير (Triangolo) على بعد 50 متراً خلف المركبة", it: "Segnalazione con triangolo di emergenza" }
        ],
        keyPoints: [
          "يُحظر السير أو التجاوز في حارة الطوارئ قطعياً تحت طائلة الغرامة وسحب النقاط.",
          "الوقوف مسموح فقط للأعطال والوعكات الصحية لمدة أقصاها 3 ساعات.",
          "ارتداء السترة العاكسة ذات المعايير الأوروبية (Giubbotto) إلزامي عند النزول من المركبة."
        ],
        quizTrap: {
          qIt: "La corsia di emergenza può essere utilizzata per il sorpasso in caso di traffico",
          qAr: "يجوز استخدام حارة الطوارئ للتجاوز في حالات الازدحام المروري",
          ans: false,
          explanation: "خطأ فادح (FALSO)! يُحظر التجاوز في حارة الطوارئ تحت أي ظرف، واستخدامها مقتصر فقط على سيارات الإسعاف أو التوقف الاضطراري."
        }
      }
    ];

    this.render();
  }

  getCurrentManeuver() {
    return this.maneuvers.find(m => m.id === this.activeId) || this.maneuvers[0];
  }

  render() {
    if (!this.container) return;
    const m = this.getCurrentManeuver();

    this.container.innerHTML = `
      <div class="vstudio-wrapper">
        <!-- Top Bar Header -->
        <div class="vstudio-top-bar">
          <div class="vstudio-header-text">
            <div class="vstudio-badge">
              <span>🚗 3D MANEUVER SIMULATOR</span>
              <span class="vstudio-live-pill">حـركـات الـسـيـارات الـتـوضـيـحـيـة</span>
            </div>
            <h3 class="vstudio-heading">محاكي مناورات وحركات المركبات التوضيحي ثلاثي الأبعاد</h3>
            <p class="vstudio-subheading">محاكاة تفاعلية لحركة السيارات ومسارات السير ومسافة الأمان في الامتحان الوزاري بدقة 60 إطاراً في الثانية</p>
          </div>

          <!-- Maneuver Navigation Tabs -->
          <div class="vstudio-playlist-nav">
            ${this.maneuvers.map(item => `
              <button class="vstudio-clip-btn ${item.id === this.activeId ? 'active' : ''}" data-maneuver-id="${item.id}">
                <span class="clip-icon">🚦</span>
                <span class="clip-btn-text">
                  <strong>${item.title}</strong>
                  <small>${item.titleIt}</small>
                </span>
                <span class="clip-time-tag">${item.badge}</span>
              </button>
            `).join('')}
          </div>
        </div>

        <!-- Main Grid: Simulation Canvas on Left, Legal & Quiz on Right -->
        <div class="vstudio-main-grid">
          <!-- Left Column: Simulation Canvas & Controls -->
          <div class="vstudio-screen-col">
            <div class="vstudio-screen-card">
              <!-- Canvas Container -->
              <div class="vstudio-canvas-container">
                <canvas id="vstudioCanvas" class="vstudio-canvas"></canvas>

                <!-- On-Screen Telemetry HUD -->
                <div class="vsim-hud-overlay">
                  <div class="vsim-hud-badge" id="vsimPhaseBadge">
                    <span class="vsim-phase-num">المرحلة 1</span>
                    <span class="vsim-phase-text" id="vsimPhaseText">جارٍ بدء المناورة...</span>
                  </div>
                  <div class="vsim-hud-telemetry" id="vsimTelemetryBox">
                    <div class="vsim-speed-pill">
                      <span class="vsim-speed-val" id="vsimSpeedVal">70</span>
                      <span class="vsim-speed-unit">km/h</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Interactive Controls Strip -->
              <div class="vstudio-tools-strip">
                <div class="vtools-left">
                  <button class="vtool-action-btn ${this.isPlaying ? 'active' : ''}" id="vsimPlayBtn" title="تشغيل / إيقاف مؤقت">
                    <span id="vsimPlayIcon">${this.isPlaying ? '⏸ إيقاف' : '▶ تشغيل'}</span>
                  </button>
                  <button class="vtool-action-btn" id="vsimRestartBtn" title="إعادة تشغيل المناورة من البداية">
                    <span>⏪ إعادة</span>
                  </button>
                  <button class="vtool-action-btn ${this.playbackSpeed === 0.5 ? 'active' : ''}" id="vsimSpeedBtn" title="حركة بطيئة لتشريح التفاصيل">
                    <span id="vsimSpeedLabel">${this.playbackSpeed === 0.5 ? '⏱ 0.5x بطيء' : '⏱ 1.0x عادي'}</span>
                  </button>
                  <button class="vtool-action-btn ${this.showTelemetry ? 'active' : ''}" id="vsimTelemetryBtn" title="إظهار/إخفاء أبعاد الأمان">
                    <span>📐 مسافات الأمان</span>
                  </button>
                </div>
                <div class="vtools-right">
                  <div class="vsim-scrubber-wrapper">
                    <span class="scrub-label">موضع المناورة:</span>
                    <input type="range" min="0" max="1000" value="0" class="vsim-scrubber" id="vsimScrubber" title="اسحب للتنقل الزمني">
                  </div>
                </div>
              </div>

              <!-- Embedded Official Ministerial Diagram -->
              <div class="vstudio-fig-display-card">
                <div class="vfig-card-header">
                  <span class="vfig-tag">📐 المخطط الوزاري الرسمي المعتمد (Figura Ministeriale)</span>
                  <span class="vfig-sub-tag">الرسم الهندسي المطابق لسؤال الامتحان</span>
                </div>
                <div class="vfig-img-frame">
                  <img src="${m.thumbnail}" alt="${m.title}" class="vfig-full-img">
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: Synchronized Legal Rule & Exam Trap Card -->
          <div class="vstudio-details-col">
            <div class="vstudio-rule-card">
              <div class="vcard-header">
                <div class="vcard-art-pill">${m.article}</div>
                <h4 class="vcard-title">${m.title}</h4>
                <div class="vcard-it-name">${m.titleIt}</div>
              </div>

              <p class="vcard-summary">${m.summary}</p>

              <!-- Step by Step Movement Breakdown -->
              <div class="vcard-phases-box">
                <div class="phases-box-title">🎬 مراحل حركة السيارة خطوة بخطوة:</div>
                <div class="phases-list">
                  ${m.phases.map((ph, idx) => `
                    <div class="phase-step-item" id="phaseStep-${idx}">
                      <div class="phase-step-num">${idx + 1}</div>
                      <div class="phase-step-info">
                        <div class="phase-step-ar">${ph.ar}</div>
                        <div class="phase-step-it">${ph.it}</div>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>

              <div class="vcard-bullet-box">
                <div class="bullet-box-title">📌 النقاط الجوهرية التي يجب حفظها:</div>
                <ul class="vcard-bullets">
                  ${m.keyPoints.map(p => `<li>${p}</li>`).join('')}
                </ul>
              </div>

              <!-- Interactive Instant Quiz Challenge -->
              <div class="vstudio-quiz-box" id="vstudioQuizBox">
                <div class="quiz-box-header">
                  <span>⚡ تحدي الفخ المرتبط بهذه المناورة:</span>
                  <span class="quiz-badge">سؤال وزاري متكرر</span>
                </div>

                <div class="quiz-q-it">${m.quizTrap.qIt}</div>
                <div class="quiz-q-ar">${m.quizTrap.qAr}</div>

                <div class="quiz-btns-row">
                  <button class="vquiz-btn vquiz-btn-v" onclick="window.vstudioInstance.answerChallenge(true)">
                    <span>VERO (صحيح)</span>
                  </button>
                  <button class="vquiz-btn vquiz-btn-f" onclick="window.vstudioInstance.answerChallenge(false)">
                    <span>FALSO (خطأ)</span>
                  </button>
                </div>

                <div class="quiz-feedback-strip" id="vstudioQuizFeedback" style="display:none;"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    this.injectStyles();
    this.bindEvents();
    this.initCanvasSimulator();
  }

  injectStyles() {
    if (document.getElementById("vstudio-sim-styles")) return;
    const style = document.createElement("style");
    style.id = "vstudio-sim-styles";
    style.innerHTML = `
      .vstudio-wrapper {
        background: radial-gradient(circle at 50% 0%, #151824 0%, #090a0f 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 22px;
        overflow: hidden;
        margin: 32px 0;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7);
        direction: rtl;
        font-family: inherit;
      }
      .vstudio-top-bar {
        padding: 24px 28px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        gap: 20px;
      }
      .vstudio-header-text { display: flex; flex-direction: column; gap: 6px; }
      .vstudio-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        font-weight: 800;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        width: fit-content;
      }
      .vstudio-live-pill {
        color: #10b981;
        font-size: 0.7rem;
        display: flex;
        align-items: center;
        gap: 4px;
      }
      .vstudio-heading {
        font-size: 1.45rem;
        font-weight: 800;
        color: #fff;
        margin: 0;
      }
      .vstudio-subheading {
        color: #94a3b8;
        font-size: 0.88rem;
        margin: 0;
      }
      .vstudio-playlist-nav {
        display: flex;
        gap: 10px;
        overflow-x: auto;
        padding-bottom: 6px;
        scrollbar-width: thin;
      }
      .vstudio-clip-btn {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 10px 14px;
        color: #cbd5e1;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 240px;
        text-align: right;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      }
      .vstudio-clip-btn:hover {
        background: rgba(56, 189, 248, 0.1);
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
      }
      .vstudio-clip-btn.active {
        background: rgba(56, 189, 248, 0.18);
        border-color: #38bdf8;
        color: #fff;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.25);
      }
      .clip-icon { font-size: 1.2rem; }
      .clip-btn-text {
        display: flex;
        flex-direction: column;
        flex: 1;
        gap: 2px;
      }
      .clip-btn-text strong {
        font-size: 0.84rem;
        font-weight: 700;
        line-height: 1.3;
      }
      .clip-btn-text small {
        font-size: 0.72rem;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
      }
      .clip-time-tag {
        font-size: 0.68rem;
        font-family: 'JetBrains Mono', monospace;
        background: rgba(0, 0, 0, 0.4);
        padding: 2px 6px;
        border-radius: 6px;
        color: #38bdf8;
      }
      .vstudio-main-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 24px;
        padding: 24px;
      }
      @media (min-width: 1024px) {
        .vstudio-main-grid {
          grid-template-columns: 1.35fr 1fr;
          align-items: start;
        }
      }
      .vstudio-screen-card {
        background: #07080c;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6);
      }
      .vstudio-canvas-container {
        position: relative;
        width: 100%;
        height: 380px;
        background: #0f1118;
        overflow: hidden;
      }
      .vstudio-canvas {
        width: 100%;
        height: 100%;
        display: block;
      }
      .vsim-hud-overlay {
        position: absolute;
        top: 14px;
        left: 14px;
        right: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        pointer-events: none;
      }
      .vsim-hud-badge {
        background: rgba(10, 12, 18, 0.88);
        border: 1px solid rgba(56, 189, 248, 0.4);
        backdrop-filter: blur(8px);
        padding: 6px 14px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #fff;
        font-size: 0.8rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
      }
      .vsim-phase-num {
        background: #38bdf8;
        color: #03121f;
        font-weight: 800;
        font-size: 0.72rem;
        padding: 2px 6px;
        border-radius: 10px;
      }
      .vsim-speed-pill {
        background: rgba(10, 12, 18, 0.88);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        color: #34d399;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 4px;
      }
      .vstudio-tools-strip {
        padding: 12px 16px;
        background: rgba(14, 16, 22, 0.95);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
      }
      .vtools-left, .vtools-right {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }
      .vtool-action-btn {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #e2e8f0;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 700;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.18s ease;
      }
      .vtool-action-btn:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: #38bdf8;
        color: #fff;
      }
      .vtool-action-btn.active {
        background: rgba(56, 189, 248, 0.25);
        border-color: #38bdf8;
        color: #38bdf8;
      }
      .vsim-scrubber-wrapper {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.75rem;
        color: #94a3b8;
      }
      .vsim-scrubber {
        width: 140px;
        accent-color: #38bdf8;
        cursor: pointer;
      }
      .vstudio-fig-display-card {
        padding: 16px;
        background: rgba(11, 13, 18, 0.95);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        gap: 10px;
      }
      .vfig-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
      }
      .vfig-tag {
        font-size: 0.8rem;
        font-weight: 800;
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
      }
      .vfig-sub-tag {
        font-size: 0.72rem;
        color: #94a3b8;
      }
      .vfig-img-frame {
        width: 100%;
        min-height: 160px;
        background: #000;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
      }
      .vfig-full-img {
        max-width: 100%;
        max-height: 220px;
        object-fit: contain;
        border-radius: 6px;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5));
      }
      .vstudio-rule-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      .vcard-header { display: flex; flex-direction: column; gap: 4px; }
      .vcard-art-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #10b981;
        font-weight: 800;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 3px 10px;
        border-radius: 6px;
        width: fit-content;
      }
      .vcard-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #fff;
        margin: 4px 0 0 0;
      }
      .vcard-it-name {
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
      }
      .vcard-summary {
        font-size: 0.88rem;
        line-height: 1.7;
        color: #cbd5e1;
        margin: 0;
      }
      .vcard-phases-box {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 14px;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }
      .phases-box-title {
        font-size: 0.84rem;
        font-weight: 700;
        color: #38bdf8;
      }
      .phases-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }
      .phase-step-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 8px;
        border-radius: 8px;
        transition: all 0.2s ease;
      }
      .phase-step-item.active {
        background: rgba(56, 189, 248, 0.12);
        border-right: 3px solid #38bdf8;
      }
      .phase-step-num {
        background: rgba(255, 255, 255, 0.1);
        color: #fff;
        font-size: 0.72rem;
        font-weight: 800;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }
      .phase-step-item.active .phase-step-num {
        background: #38bdf8;
        color: #03121f;
      }
      .phase-step-ar {
        font-size: 0.8rem;
        color: #e2e8f0;
        font-weight: 600;
      }
      .phase-step-it {
        font-size: 0.7rem;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
      }
      .vcard-bullet-box {
        background: rgba(56, 189, 248, 0.05);
        border-right: 3px solid #38bdf8;
        border-radius: 0 10px 10px 0;
        padding: 12px 16px;
      }
      .bullet-box-title {
        font-size: 0.84rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 8px;
      }
      .vcard-bullets {
        margin: 0;
        padding-right: 18px;
        display: flex;
        flex-direction: column;
        gap: 6px;
        font-size: 0.82rem;
        color: #cbd5e1;
        line-height: 1.5;
      }
      .vstudio-quiz-box {
        background: rgba(244, 63, 94, 0.06);
        border: 1px solid rgba(244, 63, 94, 0.25);
        border-radius: 12px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .quiz-box-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.82rem;
        font-weight: 800;
        color: #fb7185;
      }
      .quiz-badge {
        font-size: 0.68rem;
        background: rgba(244, 63, 94, 0.2);
        padding: 2px 8px;
        border-radius: 6px;
      }
      .quiz-q-it {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.86rem;
        font-weight: 700;
        color: #fff;
        line-height: 1.4;
      }
      .quiz-q-ar {
        font-size: 0.82rem;
        color: #cbd5e1;
      }
      .quiz-btns-row {
        display: flex;
        gap: 12px;
      }
      .vquiz-btn {
        flex: 1;
        padding: 10px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.18s ease;
      }
      .vquiz-btn-v {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34d399;
      }
      .vquiz-btn-v:hover { background: #10b981; color: #064e3b; }
      .vquiz-btn-f {
        background: rgba(244, 63, 94, 0.2);
        border: 1px solid rgba(244, 63, 94, 0.4);
        color: #f87171;
      }
      .vquiz-btn-f:hover { background: #f43f5e; color: #fff; }
      .quiz-feedback-strip {
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 0.84rem;
        line-height: 1.5;
        font-weight: 600;
      }
      .quiz-feedback-strip.correct {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #6ee7b7;
      }
      .quiz-feedback-strip.wrong {
        background: rgba(244, 63, 94, 0.2);
        border: 1px solid rgba(244, 63, 94, 0.4);
        color: #fca5a5;
      }
    `;
    document.head.appendChild(style);
  }

  bindEvents() {
    // Playlist buttons
    const btns = this.container.querySelectorAll(".vstudio-clip-btn");
    btns.forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.dataset.maneuverId;
        this.switchManeuver(id);
        if (window.soundEngine) window.soundEngine.click();
      });
    });

    // Play/Pause button
    const playBtn = this.container.querySelector("#vsimPlayBtn");
    if (playBtn) {
      playBtn.addEventListener("click", () => {
        this.isPlaying = !this.isPlaying;
        playBtn.classList.toggle("active", this.isPlaying);
        const iconSpan = this.container.querySelector("#vsimPlayIcon");
        if (iconSpan) iconSpan.textContent = this.isPlaying ? '⏸ إيقاف' : '▶ تشغيل';
        if (window.soundEngine) window.soundEngine.click();
      });
    }

    // Restart button
    const restartBtn = this.container.querySelector("#vsimRestartBtn");
    if (restartBtn) {
      restartBtn.addEventListener("click", () => {
        this.simTime = 0;
        this.isPlaying = true;
        const iconSpan = this.container.querySelector("#vsimPlayIcon");
        if (iconSpan) iconSpan.textContent = '⏸ إيقاف';
        if (window.soundEngine) window.soundEngine.click();
      });
    }

    // Speed button
    const speedBtn = this.container.querySelector("#vsimSpeedBtn");
    if (speedBtn) {
      speedBtn.addEventListener("click", () => {
        this.playbackSpeed = (this.playbackSpeed === 1.0) ? 0.5 : 1.0;
        speedBtn.classList.toggle("active", this.playbackSpeed === 0.5);
        const label = this.container.querySelector("#vsimSpeedLabel");
        if (label) label.textContent = this.playbackSpeed === 0.5 ? '⏱ 0.5x بطيء' : '⏱ 1.0x عادي';
        if (window.soundEngine) window.soundEngine.click();
      });
    }

    // Telemetry button
    const telBtn = this.container.querySelector("#vsimTelemetryBtn");
    if (telBtn) {
      telBtn.addEventListener("click", () => {
        this.showTelemetry = !this.showTelemetry;
        telBtn.classList.toggle("active", this.showTelemetry);
        if (window.soundEngine) window.soundEngine.click();
      });
    }

    // Scrubber
    const scrubber = this.container.querySelector("#vsimScrubber");
    if (scrubber) {
      scrubber.addEventListener("input", (e) => {
        this.simTime = parseFloat(e.target.value) / 1000;
        this.isPlaying = false;
        const iconSpan = this.container.querySelector("#vsimPlayIcon");
        if (iconSpan) iconSpan.textContent = '▶ تشغيل';
      });
    }
  }

  switchManeuver(id) {
    if (this.activeId === id) return;
    this.activeId = id;
    this.simTime = 0;
    this.isPlaying = true;
    if (this.animFrameId) cancelAnimationFrame(this.animFrameId);
    this.render();
  }

  answerChallenge(userChoice) {
    const m = this.getCurrentManeuver();
    const fb = this.container.querySelector("#vstudioQuizFeedback");
    if (!fb) return;

    fb.style.display = "block";
    const isCorrect = (userChoice === m.quizTrap.ans);

    if (isCorrect) {
      if (window.soundEngine) window.soundEngine.correct();
      fb.className = "quiz-feedback-strip correct";
      fb.innerHTML = `✅ <strong>إجابة صحيحة وممتازة!</strong> ${m.quizTrap.explanation}`;
    } else {
      if (window.soundEngine) window.soundEngine.wrong();
      fb.className = "quiz-feedback-strip wrong";
      fb.innerHTML = `❌ <strong>إجابة خاطئة!</strong> الصحيح هو (${m.quizTrap.ans ? 'VERO' : 'FALSO'}). ${m.quizTrap.explanation}`;
    }
  }

  /* =========================================================
   * CANVAS 60 FPS SIMULATION ENGINE
   * ========================================================= */
  initCanvasSimulator() {
    const canvas = this.container.querySelector("#vstudioCanvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    this.lastTimestamp = performance.now();

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);
    };

    resize();
    window.addEventListener("resize", resize);

    const loop = (timestamp) => {
      const dt = (timestamp - this.lastTimestamp) / 1000;
      this.lastTimestamp = timestamp;

      if (this.isPlaying) {
        // Full loop in ~12 seconds
        const speedFactor = 0.08 * this.playbackSpeed;
        this.simTime += dt * speedFactor;
        if (this.simTime > 1.0) this.simTime = 0;

        const scrubber = this.container.querySelector("#vsimScrubber");
        if (scrubber) scrubber.value = Math.floor(this.simTime * 1000);
      }

      this.updateHudAndPhases();
      this.drawSimulation(ctx, canvas);

      this.animFrameId = requestAnimationFrame(loop);
    };

    this.animFrameId = requestAnimationFrame(loop);
  }

  updateHudAndPhases() {
    const m = this.getCurrentManeuver();
    const currentPhase = m.phases.find(p => this.simTime >= p.from && this.simTime <= p.to) || m.phases[0];
    const phaseIdx = m.phases.indexOf(currentPhase);

    const phaseNumSpan = this.container.querySelector(".vsim-phase-num");
    const phaseTextSpan = this.container.querySelector("#vsimPhaseText");
    if (phaseNumSpan) phaseNumSpan.textContent = `المرحلة ${phaseIdx + 1}`;
    if (phaseTextSpan) phaseTextSpan.textContent = currentPhase.ar;

    // Highlight active phase in sidebar
    m.phases.forEach((_, idx) => {
      const el = this.container.querySelector(`#phaseStep-${idx}`);
      if (el) el.classList.toggle("active", idx === phaseIdx);
    });

    // Speed HUD
    const speedVal = this.container.querySelector("#vsimSpeedVal");
    if (speedVal) {
      if (this.activeId === "distanza_sicurezza") {
        if (this.simTime > 0.55) {
          const dec = Math.max(0, Math.floor(90 * (1 - (this.simTime - 0.55) / 0.3)));
          speedVal.textContent = dec;
        } else {
          speedVal.textContent = "90";
        }
      } else if (this.activeId === "sorpasso_curva") {
        speedVal.textContent = (this.simTime > 0.25 && this.simTime < 0.75) ? "85" : "70";
      } else if (this.activeId === "corsia_destra") {
        speedVal.textContent = (this.simTime > 0.25 && this.simTime < 0.75) ? "110" : "90";
      } else if (this.activeId === "tram_salvagente") {
        speedVal.textContent = "30";
      } else if (this.activeId === "corsia_emergenza") {
        speedVal.textContent = this.simTime > 0.3 ? Math.max(0, Math.floor(100 * (1 - (this.simTime - 0.3) / 0.4))) : "100";
      }
    }
  }

  drawSimulation(ctx, canvas) {
    const rect = canvas.getBoundingClientRect();
    const w = rect.width;
    const h = rect.height;

    ctx.clearRect(0, 0, w, h);

    if (this.activeId === "sorpasso_curva") {
      this.drawManeuverSorpassoCurva(ctx, w, h);
    } else if (this.activeId === "distanza_sicurezza") {
      this.drawManeuverDistanza(ctx, w, h);
    } else if (this.activeId === "corsia_destra") {
      this.drawManeuverCorsiaDestra(ctx, w, h);
    } else if (this.activeId === "tram_salvagente") {
      this.drawManeuverTram(ctx, w, h);
    } else if (this.activeId === "corsia_emergenza") {
      this.drawManeuverEmergenza(ctx, w, h);
    }
  }

  /* -------------------------------------------------------------
   * 1. MANEUVER: Sorpasso in Curva (Fig. 550) - 4 Corsie
   * ------------------------------------------------------------- */
  drawManeuverSorpassoCurva(ctx, w, h) {
    // Road background
    ctx.fillStyle = "#12131a";
    ctx.fillRect(0, 0, w, h);

    // Draw 4-lane curved road
    const centerY = h * 0.52;
    const laneWidth = 46;

    // Road surface
    ctx.fillStyle = "#1e2029";
    ctx.beginPath();
    ctx.moveTo(0, centerY - laneWidth * 2);
    ctx.bezierCurveTo(w * 0.35, centerY - laneWidth * 2 - 40, w * 0.65, centerY - laneWidth * 2 + 40, w, centerY - laneWidth * 2);
    ctx.lineTo(w, centerY + laneWidth * 2);
    ctx.bezierCurveTo(w * 0.65, centerY + laneWidth * 2 + 40, w * 0.35, centerY + laneWidth * 2 - 40, 0, centerY + laneWidth * 2);
    ctx.closePath();
    ctx.fill();

    // Road borders
    ctx.strokeStyle = "#475569";
    ctx.lineWidth = 3;
    ctx.stroke();

    // Center DOUBLE CONTINUOUS LINE (Fig. 550)
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 3;
    // Line 1
    ctx.beginPath();
    ctx.moveTo(0, centerY - 2.5);
    ctx.bezierCurveTo(w * 0.35, centerY - 2.5 - 40, w * 0.65, centerY - 2.5 + 40, w, centerY - 2.5);
    ctx.stroke();
    // Line 2
    ctx.beginPath();
    ctx.moveTo(0, centerY + 2.5);
    ctx.bezierCurveTo(w * 0.35, centerY + 2.5 - 40, w * 0.65, centerY + 2.5 + 40, w, centerY + 2.5);
    ctx.stroke();

    // Dashed lines for lanes (Direction 1: bottom, Direction 2: top)
    ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
    ctx.lineWidth = 2;
    ctx.setLineDash([12, 12]);
    // Top direction dashed lane line
    ctx.beginPath();
    ctx.moveTo(0, centerY - laneWidth);
    ctx.bezierCurveTo(w * 0.35, centerY - laneWidth - 40, w * 0.65, centerY - laneWidth + 40, w, centerY - laneWidth);
    ctx.stroke();
    // Bottom direction dashed lane line (Our direction!)
    ctx.beginPath();
    ctx.moveTo(0, centerY + laneWidth);
    ctx.bezierCurveTo(w * 0.35, centerY + laneWidth - 40, w * 0.65, centerY + laneWidth + 40, w, centerY + laneWidth);
    ctx.stroke();
    ctx.setLineDash([]);

    // Lane Labels & Guidance
    if (this.showTelemetry) {
      ctx.fillStyle = "rgba(16, 185, 129, 0.85)";
      ctx.font = "bold 11px 'JetBrains Mono', monospace";
      ctx.textAlign = "left";
      ctx.fillText("🟢 Corsia Destra (سير عادي)", 18, centerY + laneWidth * 1.6);
      ctx.fillStyle = "rgba(56, 189, 248, 0.85)";
      ctx.fillText("🔵 Corsia Sinistra (تجاوز مسموح في المنعطف)", 18, centerY + laneWidth * 0.6);
      ctx.fillStyle = "rgba(239, 68, 68, 0.85)";
      ctx.fillText("⛔ Senso Opposto (اتجاه معاكس مفصول بخط مزدوج)", 18, centerY - laneWidth * 1.5);
    }

    // Road curve helper function for bottom carriageway
    const getPointOnRoad = (t, laneOffset) => {
      const x = t * (w + 100) - 50;
      // Bezier curve Y calculation
      const p0 = centerY;
      const p1 = centerY - 40;
      const p2 = centerY + 40;
      const p3 = centerY;
      const u = t;
      const yBase = Math.pow(1 - u, 3) * p0 + 3 * Math.pow(1 - u, 2) * u * p1 + 3 * (1 - u) * Math.pow(u, 2) * p2 + Math.pow(u, 3) * p3;
      
      // Calculate tangent angle for car rotation
      const dy = 3 * Math.pow(1 - u, 2) * (p1 - p0) + 6 * (1 - u) * u * (p2 - p1) + 3 * Math.pow(u, 2) * (p3 - p2);
      const angle = Math.atan2(dy, (w + 100) / 100);
      return { x, y: yBase + laneOffset, angle };
    };

    // Slow Car A (Blue) - Cruises in right lane
    const tA = (this.simTime * 0.7 + 0.2) % 1.0;
    const ptA = getPointOnRoad(tA, laneWidth * 1.45);
    this.drawCar(ctx, ptA.x, ptA.y, ptA.angle, "#38bdf8", false, false, false, "Veicolo A (بطيء 60km/h)");

    // Overtaking Car B (Red)
    let laneOffsetB = laneWidth * 1.45; // Starts in right lane
    let isBlinkingLeft = false;
    let isBlinkingRight = false;

    if (this.simTime < 0.25) {
      // Phase 1: approaching in right lane
      laneOffsetB = laneWidth * 1.45;
      isBlinkingLeft = (this.simTime > 0.12);
    } else if (this.simTime < 0.45) {
      // Phase 2: smoothly transitioning to left lane
      const trans = (this.simTime - 0.25) / 0.20;
      laneOffsetB = laneWidth * 1.45 - trans * laneWidth;
      isBlinkingLeft = true;
    } else if (this.simTime < 0.75) {
      // Phase 3: overtaking inside the curve in left lane
      laneOffsetB = laneWidth * 0.45;
      isBlinkingLeft = false;
    } else if (this.simTime < 0.90) {
      // Phase 4: transitioning back to right lane
      const trans = (this.simTime - 0.75) / 0.15;
      laneOffsetB = laneWidth * 0.45 + trans * laneWidth;
      isBlinkingRight = true;
    } else {
      laneOffsetB = laneWidth * 1.45;
      isBlinkingRight = false;
    }

    const tB = (this.simTime * 1.05) % 1.0;
    const ptB = getPointOnRoad(tB, laneOffsetB);
    this.drawCar(ctx, ptB.x, ptB.y, ptB.angle, "#ef4444", false, isBlinkingLeft, isBlinkingRight, "Veicolo B (المتجاوز 85km/h)");

    // Draw visual Trajectory path
    if (this.showTelemetry) {
      ctx.strokeStyle = "rgba(16, 185, 129, 0.4)";
      ctx.lineWidth = 2.5;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      for (let s = 0; s <= 1.0; s += 0.05) {
        let off = laneWidth * 1.45;
        if (s > 0.25 && s <= 0.45) off = laneWidth * 1.45 - ((s - 0.25) / 0.2) * laneWidth;
        else if (s > 0.45 && s <= 0.75) off = laneWidth * 0.45;
        else if (s > 0.75 && s <= 0.90) off = laneWidth * 0.45 + ((s - 0.75) / 0.15) * laneWidth;
        const p = getPointOnRoad(s, off);
        if (s === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();
      ctx.setLineDash([]);
    }
  }

  /* -------------------------------------------------------------
   * 2. MANEUVER: Distanza di Sicurezza & Arresto
   * ------------------------------------------------------------- */
  drawManeuverDistanza(ctx, w, h) {
    ctx.fillStyle = "#12131a";
    ctx.fillRect(0, 0, w, h);

    const roadY = h * 0.55;
    const roadH = 110;

    // Straight highway
    ctx.fillStyle = "#1e2029";
    ctx.fillRect(0, roadY - roadH / 2, w, roadH);

    // Edge lines
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, roadY - roadH / 2); ctx.lineTo(w, roadY - roadH / 2);
    ctx.moveTo(0, roadY + roadH / 2); ctx.lineTo(w, roadY + roadH / 2);
    ctx.stroke();

    // Center dashed line
    ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
    ctx.lineWidth = 2;
    ctx.setLineDash([16, 14]);
    ctx.beginPath();
    ctx.moveTo(0, roadY); ctx.lineTo(w, roadY);
    ctx.stroke();
    ctx.setLineDash([]);

    // Lead Car A position
    let xA = w * 0.65;
    let isBrakingA = (this.simTime > 0.35);

    // Follower Car B position
    let xB = w * 0.25;
    let isBrakingB = (this.simTime > 0.55);

    if (this.simTime < 0.35) {
      // Normal cruise
      const cruiseOffset = (this.simTime / 0.35) * 80;
      xA = w * 0.60 + cruiseOffset;
      xB = w * 0.20 + cruiseOffset;
    } else {
      // Braking sequence
      xA = w * 0.68;
      if (this.simTime < 0.55) {
        // Car B reaction time (moves at constant speed towards A!)
        const reactProgress = (this.simTime - 0.35) / 0.20;
        xB = w * 0.28 + reactProgress * 45;
      } else {
        // Car B braking phase
        const brakeProgress = Math.min(1.0, (this.simTime - 0.55) / 0.35);
        xB = w * 0.325 + brakeProgress * 30;
      }
    }

    const lanePos = roadY + 28;

    // Draw Lead Car
    this.drawCar(ctx, xA, lanePos, 0, "#eab308", isBrakingA, false, false, "Veicolo Davanti (توقف مفاجئ)");

    // Draw Follower Car
    this.drawCar(ctx, xB, lanePos, 0, "#38bdf8", isBrakingB, false, false, "Veicolo Dietro (السائق التابع)");

    // Telemetry Brackets
    if (this.showTelemetry) {
      const dist = Math.max(10, Math.floor(xA - xB - 45));

      // Distance Bracket between cars
      ctx.strokeStyle = (dist < 30) ? "#ef4444" : "#10b981";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(xB + 24, lanePos + 32);
      ctx.lineTo(xA - 24, lanePos + 32);
      ctx.stroke();

      // Bracket ticks
      ctx.beginPath();
      ctx.moveTo(xB + 24, lanePos + 26); ctx.lineTo(xB + 24, lanePos + 38);
      ctx.moveTo(xA - 24, lanePos + 26); ctx.lineTo(xA - 24, lanePos + 38);
      ctx.stroke();

      // Distance tag
      ctx.fillStyle = (dist < 30) ? "#ef4444" : "#10b981";
      ctx.font = "bold 12px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(`📐 مسافة الأمان الحقيقية: ~${Math.floor(dist * 0.4)} متراً`, (xA + xB) / 2, lanePos + 48);

      // Reaction and Braking Breakdown Bar
      if (this.simTime > 0.35) {
        const barY = roadY - 45;
        ctx.fillStyle = "rgba(10, 12, 18, 0.9)";
        ctx.fillRect(w * 0.15, barY - 14, w * 0.7, 34);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
        ctx.strokeRect(w * 0.15, barY - 14, w * 0.7, 34);

        // Yellow segment: Reaction distance
        ctx.fillStyle = "#eab308";
        ctx.fillRect(w * 0.17, barY - 6, 120, 16);
        ctx.fillStyle = "#000";
        ctx.font = "bold 10px 'JetBrains Mono', monospace";
        ctx.fillText("زمن رد الفعل (1 sec)", w * 0.17 + 60, barY + 6);

        // Orange segment: Braking distance
        ctx.fillStyle = "#f97316";
        ctx.fillRect(w * 0.17 + 124, barY - 6, 160, 16);
        ctx.fillStyle = "#fff";
        ctx.fillText("مسافة الفرملة (Frenatura)", w * 0.17 + 204, barY + 6);

        // Green segment: Remaining safety margin
        ctx.fillStyle = "#10b981";
        ctx.fillRect(w * 0.17 + 288, barY - 6, 80, 16);
        ctx.fillText("أمان كافٍ", w * 0.17 + 328, barY + 6);
      }
    }
  }

  /* -------------------------------------------------------------
   * 3. MANEUVER: Corsia più libera a destra (3 Corsie)
   * ------------------------------------------------------------- */
  drawManeuverCorsiaDestra(ctx, w, h) {
    ctx.fillStyle = "#12131a";
    ctx.fillRect(0, 0, w, h);

    const roadY = h * 0.52;
    const laneW = 42;

    // 3-lane Autostrada
    ctx.fillStyle = "#1e2029";
    ctx.fillRect(0, roadY - laneW * 1.5, w, laneW * 3);

    // Guardrail borders
    ctx.strokeStyle = "#94a3b8";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, roadY - laneW * 1.5); ctx.lineTo(w, roadY - laneW * 1.5);
    ctx.moveTo(0, roadY + laneW * 1.5); ctx.lineTo(w, roadY + laneW * 1.5);
    ctx.stroke();

    // 2 dashed divider lines
    ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
    ctx.lineWidth = 2;
    ctx.setLineDash([14, 14]);
    ctx.beginPath();
    ctx.moveTo(0, roadY - laneW * 0.5); ctx.lineTo(w, roadY - laneW * 0.5);
    ctx.moveTo(0, roadY + laneW * 0.5); ctx.lineTo(w, roadY + laneW * 0.5);
    ctx.stroke();
    ctx.setLineDash([]);

    // Lane Names
    if (this.showTelemetry) {
      ctx.font = "bold 10px 'JetBrains Mono', monospace";
      ctx.textAlign = "left";
      ctx.fillStyle = "rgba(16, 185, 129, 0.85)";
      ctx.fillText("1️⃣ Corsia Destra (إلزامية عند خلوّها)", 14, roadY + laneW * 1.1);
      ctx.fillStyle = "rgba(56, 189, 248, 0.85)";
      ctx.fillText("2️⃣ Corsia Centrale (للتجاوز فقط)", 14, roadY + 4);
      ctx.fillStyle = "rgba(168, 85, 247, 0.85)";
      ctx.fillText("3️⃣ Corsia Sinistra (للتجاوز الإضافي)", 14, roadY - laneW * 0.9);
    }

    // Slow truck in right lane
    const truckX = (w * 0.55);
    this.drawTruck(ctx, truckX, roadY + laneW, 0, "#64748b", "شاحنة بطيئة (80 km/h)");

    // Car executing the law:
    let carLaneY = roadY + laneW; // Right lane
    let isBlinkLeft = false;
    let isBlinkRight = false;

    if (this.simTime < 0.25) {
      carLaneY = roadY + laneW;
      isBlinkLeft = (this.simTime > 0.15);
    } else if (this.simTime < 0.45) {
      const tr = (this.simTime - 0.25) / 0.20;
      carLaneY = roadY + laneW - tr * laneW;
      isBlinkLeft = true;
    } else if (this.simTime < 0.70) {
      carLaneY = roadY;
      isBlinkLeft = false;
      isBlinkRight = (this.simTime > 0.60);
    } else if (this.simTime < 0.85) {
      const tr = (this.simTime - 0.70) / 0.15;
      carLaneY = roadY + tr * laneW;
      isBlinkRight = true;
    } else {
      carLaneY = roadY + laneW;
      isBlinkRight = false;
    }

    const carX = (this.simTime * (w + 120) - 60);
    this.drawCar(ctx, carX, carLaneY, 0, "#10b981", false, isBlinkLeft, isBlinkRight, "Veicolo (سلوك مثالي 110km/h)");
  }

  /* -------------------------------------------------------------
   * 4. MANEUVER: Sorpasso Tram con Salvagente
   * ------------------------------------------------------------- */
  drawManeuverTram(ctx, w, h) {
    ctx.fillStyle = "#12131a";
    ctx.fillRect(0, 0, w, h);

    const roadY = h * 0.52;
    const tramTrackY = roadY - 45;
    const carLaneY = roadY + 45;

    // Road asphalt
    ctx.fillStyle = "#1e2029";
    ctx.fillRect(0, roadY - 95, w, 190);

    // Tram Rails
    ctx.strokeStyle = "#64748b";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, tramTrackY - 10); ctx.lineTo(w, tramTrackY - 10);
    ctx.moveTo(0, tramTrackY + 10); ctx.lineTo(w, tramTrackY + 10);
    ctx.stroke();

    // Salvagente Safety Refuge Island (between tram and car lane)
    const salvagenteX = w * 0.42;
    const salvagenteW = 180;
    const salvagenteH = 28;
    const salvagenteY = roadY - 14;

    ctx.fillStyle = "#27272a";
    ctx.strokeStyle = "#eab308";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.roundRect(salvagenteX, salvagenteY, salvagenteW, salvagenteH, 8);
    ctx.fill();
    ctx.stroke();

    // Striped yellow/black curb markings
    ctx.fillStyle = "#fbbf24";
    for (let i = 0; i < salvagenteW; i += 24) {
      ctx.fillRect(salvagenteX + i, salvagenteY, 12, 4);
      ctx.fillRect(salvagenteX + i, salvagenteY + salvagenteH - 4, 12, 4);
    }

    // Pedestrians on Salvagente
    ctx.fillStyle = "#38bdf8";
    ctx.beginPath();
    ctx.arc(salvagenteX + 45, salvagenteY + 14, 5, 0, Math.PI * 2);
    ctx.arc(salvagenteX + 90, salvagenteY + 14, 5, 0, Math.PI * 2);
    ctx.arc(salvagenteX + 135, salvagenteY + 14, 5, 0, Math.PI * 2);
    ctx.fill();

    // Label on Salvagente
    ctx.fillStyle = "#fbbf24";
    ctx.font = "bold 10px 'JetBrains Mono', monospace";
    ctx.textAlign = "center";
    ctx.fillText("🛡️ Salvagente (رصيف حماية الركاب)", salvagenteX + salvagenteW / 2, salvagenteY - 8);

    // Tram stopped on tracks
    this.drawTram(ctx, salvagenteX + 80, tramTrackY, "🚊 TRAM (متوقف لصعود الركاب)");

    // Car overtaking tram from the RIGHT
    const carX = (this.simTime * (w + 140) - 70);
    this.drawCar(ctx, carX, carLaneY, 0, "#ef4444", false, false, false, "Auto (تجاوز يميناً مسموح)");

    // Guidance text
    if (this.showTelemetry) {
      ctx.fillStyle = "#10b981";
      ctx.font = "bold 11px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText("✅ التجاوز مسموح من اليمين لأن رصيف الأمان يحمي الركاب تماماً", w * 0.5, roadY + 86);
    }
  }

  /* -------------------------------------------------------------
   * 5. MANEUVER: Corsia di Emergenza (Fig. 305)
   * ------------------------------------------------------------- */
  drawManeuverEmergenza(ctx, w, h) {
    ctx.fillStyle = "#12131a";
    ctx.fillRect(0, 0, w, h);

    const roadY = h * 0.52;
    const laneW = 46;

    // Driving lane + Emergency lane
    ctx.fillStyle = "#1e2029";
    ctx.fillRect(0, roadY - laneW, w, laneW * 2);

    // Left divider (dashed)
    ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
    ctx.lineWidth = 2;
    ctx.setLineDash([14, 14]);
    ctx.beginPath();
    ctx.moveTo(0, roadY - laneW); ctx.lineTo(w, roadY - laneW);
    ctx.stroke();
    ctx.setLineDash([]);

    // Solid line dividing Driving Lane from Emergency Lane (Codice della Strada)
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.moveTo(0, roadY); ctx.lineTo(w, roadY);
    ctx.stroke();

    // Emergency lane right curb
    ctx.strokeStyle = "#f59e0b";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, roadY + laneW); ctx.lineTo(w, roadY + laneW);
    ctx.stroke();

    if (this.showTelemetry) {
      ctx.font = "bold 10px 'JetBrains Mono', monospace";
      ctx.textAlign = "left";
      ctx.fillStyle = "rgba(16, 185, 129, 0.9)";
      ctx.fillText("🟢 Corsia di Marcia (حارة السير العادي)", 14, roadY - 16);
      ctx.fillStyle = "rgba(245, 158, 11, 0.9)";
      ctx.fillText("🟠 Corsia di Emergenza (مخصصة فقط للأعطال والوعكات)", 14, roadY + 32);
    }

    // Car path
    let carY = roadY - laneW / 2;
    let is4Frecce = (this.simTime > 0.15);
    let isBraking = (this.simTime > 0.25);

    if (this.simTime < 0.30) {
      carY = roadY - laneW / 2;
    } else if (this.simTime < 0.65) {
      const tr = (this.simTime - 0.30) / 0.35;
      carY = (roadY - laneW / 2) + tr * laneW;
    } else {
      carY = roadY + laneW / 2;
    }

    let carX = w * 0.20;
    if (this.simTime < 0.65) {
      carX = w * 0.15 + (this.simTime / 0.65) * (w * 0.45);
    } else {
      carX = w * 0.60; // Stopped in emergency lane
    }

    this.drawCar(ctx, carX, carY, 0, "#38bdf8", isBraking, is4Frecce, is4Frecce, "Veicolo in Avaria (عطل)");

    // Draw Emergency Triangle (Triangolo di emergenza) behind car
    if (this.simTime > 0.75) {
      const triX = carX - 90;
      const triY = carY;
      ctx.strokeStyle = "#ef4444";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(triX, triY - 10);
      ctx.lineTo(triX + 10, triY + 8);
      ctx.lineTo(triX - 10, triY + 8);
      ctx.closePath();
      ctx.stroke();

      ctx.fillStyle = "#ef4444";
      ctx.font = "bold 9px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText("⚠️ Triangolo (50m)", triX, triY + 20);
    }
  }

  /* =========================================================
   * VEHICLE DRAWING ROUTINES (Cars, Trucks, Tram)
   * ========================================================= */
  drawCar(ctx, x, y, angle, color, isBraking, blinkLeft, blinkRight, label) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);

    const length = 46;
    const width = 24;

    // Car drop shadow
    ctx.shadowColor = "rgba(0, 0, 0, 0.75)";
    ctx.shadowBlur = 10;
    ctx.shadowOffsetY = 4;

    // Car Body
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(-length / 2, -width / 2, length, width, 6);
    ctx.fill();

    // Reset shadow
    ctx.shadowColor = "transparent";

    // Roof & Windshields
    ctx.fillStyle = "#0f172a";
    ctx.beginPath();
    ctx.roundRect(-length * 0.25, -width * 0.38, length * 0.5, width * 0.76, 4);
    ctx.fill();

    // Front headlights beam
    ctx.fillStyle = "rgba(254, 240, 138, 0.22)";
    ctx.beginPath();
    ctx.moveTo(length / 2, -width * 0.4);
    ctx.lineTo(length / 2 + 35, -width * 0.8);
    ctx.lineTo(length / 2 + 35, width * 0.8);
    ctx.lineTo(length / 2, width * 0.4);
    ctx.closePath();
    ctx.fill();

    // Headlight bulbs
    ctx.fillStyle = "#fef08a";
    ctx.fillRect(length / 2 - 2, -width * 0.45, 3, 5);
    ctx.fillRect(length / 2 - 2, width * 0.45 - 5, 3, 5);

    // Brake lights (Red glow if braking)
    if (isBraking) {
      ctx.fillStyle = "#ef4444";
      ctx.shadowColor = "#ef4444";
      ctx.shadowBlur = 14;
      ctx.fillRect(-length / 2 - 2, -width * 0.45, 4, 6);
      ctx.fillRect(-length / 2 - 2, width * 0.45 - 6, 4, 6);
      ctx.shadowColor = "transparent";
    } else {
      ctx.fillStyle = "#991b1b";
      ctx.fillRect(-length / 2, -width * 0.45, 2, 5);
      ctx.fillRect(-length / 2, width * 0.45 - 5, 2, 5);
    }

    // Blinking turn signals (Amber flash)
    const isFlash = (Math.floor(Date.now() / 280) % 2 === 0);
    if (blinkLeft && isFlash) {
      ctx.fillStyle = "#f59e0b";
      ctx.shadowColor = "#f59e0b";
      ctx.shadowBlur = 12;
      ctx.beginPath();
      ctx.arc(length * 0.35, -width * 0.52, 4, 0, Math.PI * 2);
      ctx.arc(-length * 0.35, -width * 0.52, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowColor = "transparent";
    }
    if (blinkRight && isFlash) {
      ctx.fillStyle = "#f59e0b";
      ctx.shadowColor = "#f59e0b";
      ctx.shadowBlur = 12;
      ctx.beginPath();
      ctx.arc(length * 0.35, width * 0.52, 4, 0, Math.PI * 2);
      ctx.arc(-length * 0.35, width * 0.52, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowColor = "transparent";
    }

    // Vehicle label
    if (label && this.showTelemetry) {
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 9px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(label, 0, -width * 0.75);
    }

    ctx.restore();
  }

  drawTruck(ctx, x, y, angle, color, label) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);

    const len = 70;
    const wid = 28;

    ctx.shadowColor = "rgba(0, 0, 0, 0.7)";
    ctx.shadowBlur = 10;
    ctx.shadowOffsetY = 4;

    // Cargo trailer
    ctx.fillStyle = color;
    ctx.fillRect(-len / 2, -wid / 2, len * 0.65, wid);

    // Cabin
    ctx.fillStyle = "#475569";
    ctx.fillRect(len * 0.18, -wid / 2, len * 0.30, wid);

    ctx.shadowColor = "transparent";

    if (label && this.showTelemetry) {
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 9px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(label, 0, -wid * 0.75);
    }

    ctx.restore();
  }

  drawTram(ctx, x, y, label) {
    ctx.save();
    ctx.translate(x, y);

    const len = 120;
    const wid = 28;

    ctx.shadowColor = "rgba(0, 0, 0, 0.7)";
    ctx.shadowBlur = 10;
    ctx.shadowOffsetY = 4;

    // Tram Yellow Body
    ctx.fillStyle = "#eab308";
    ctx.beginPath();
    ctx.roundRect(-len / 2, -wid / 2, len, wid, 6);
    ctx.fill();

    ctx.shadowColor = "transparent";

    // Roof & Windows
    ctx.fillStyle = "#1e293b";
    for (let i = -len * 0.4; i < len * 0.4; i += 20) {
      ctx.fillRect(i, -wid * 0.4, 12, wid * 0.8);
    }

    if (label && this.showTelemetry) {
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 9px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(label, 0, -wid * 0.85);
    }

    ctx.restore();
  }
}

// Auto Initialize
document.addEventListener("DOMContentLoaded", () => {
  const target = document.getElementById("vstudio-container");
  if (target) {
    window.vstudioInstance = new PatenteVideoStudio(target);
  }
});

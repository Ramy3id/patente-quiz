/**
 * Patente B - First Aid & Sobriety Studio (Chapter 22)
 * 60 FPS HTML5 Canvas Simulator with Web Audio API Integration
 * Topics: Tasso Alcolemico, Tempo di Reazione, Visione a Tunnel, Primo Soccorso Stradale
 */

(function () {
  'use strict';

  // Audio helper
  const playSfx = (type) => {
    if (window.soundEngine && typeof window.soundEngine.click === 'function') {
      window.soundEngine.click();
    }
  };

  class FirstAidStudio {
    constructor(containerId) {
      this.container = document.getElementById(containerId);
      if (!this.container) return;

      this.activeTab = 'bac'; // 'bac' | 'tunnel' | 'protocol'
      this.bac = 0.5; // g/l
      this.driverType = 'neo'; // 'neo' | 'ord'
      this.speed = 90; // km/h
      this.animFrame = null;
      this.animTime = 0;

      // Protocol state
      this.selectedEmergency = 'pls'; // 'pls' | 'emorragia' | 'shock' | 'casco' | 'ustioni' | 'occhio'

      this.init();
    }

    init() {
      this.renderSkeleton();
      this.bindEvents();
      this.startLoop();
      this.updateUI();
    }

    renderSkeleton() {
      this.container.innerHTML = `
        <div class="fa-studio-card">
          <!-- Top Studio Header -->
          <div class="fa-studio-header">
            <div class="fa-studio-title-box">
              <div class="fa-studio-badge">
                <span class="fa-pulse-dot"></span>
                <span>المختبر التفاعلي المتقدم 60 FPS • الباب 22</span>
              </div>
              <h2 class="fa-studio-main-title">مختبر الكحول، زمن رد الفعل، وبروتوكولات الإسعاف الأولي</h2>
              <p class="fa-studio-sub-title">محاكاة فيزيائية وبيولوجية دقيقة لتأثير الكحول على زمن الفرملة والمجال البصري، وشجرة القرار لإنقاذ مصابي الحوادث</p>
            </div>
            <!-- Mode Switcher Tabs -->
            <div class="fa-tab-group">
              <button class="fa-tab-btn active" data-tab="bac">
                <span class="fa-tab-icon">🍷</span>
                <span>نسبة الكحول والفرملة</span>
              </button>
              <button class="fa-tab-btn" data-tab="tunnel">
                <span class="fa-tab-icon">👀</span>
                <span>الرؤية النفقية البصرية</span>
              </button>
              <button class="fa-tab-btn" data-tab="protocol">
                <span class="fa-tab-icon">🚑</span>
                <span>بروتوكول الإسعاف 112</span>
              </button>
            </div>
          </div>

          <!-- Main Studio Stage -->
          <div class="fa-stage-layout">
            <!-- Left/Top: Canvas Simulation -->
            <div class="fa-canvas-wrapper">
              <canvas id="faCanvas" width="860" height="420"></canvas>
              <div class="fa-canvas-overlay" id="faCanvasOverlay"></div>
            </div>

            <!-- Right/Bottom: Control Center & Legal Feedback -->
            <div class="fa-controls-panel" id="faControlsPanel">
              <!-- Content dynamically rendered via updateUI() -->
            </div>
          </div>
        </div>
      `;
      this.canvas = document.getElementById('faCanvas');
      this.ctx = this.canvas.getContext('2d');
    }

    bindEvents() {
      const tabs = this.container.querySelectorAll('.fa-tab-btn');
      tabs.forEach((tab) => {
        tab.addEventListener('click', (e) => {
          playSfx();
          tabs.forEach((t) => t.classList.remove('active'));
          const currentTab = e.currentTarget;
          currentTab.classList.add('active');
          this.activeTab = currentTab.getAttribute('data-tab');
          this.updateUI();
        });
      });
    }

    startLoop() {
      const loop = (timestamp) => {
        this.animTime = timestamp * 0.001;
        this.renderCanvas();
        this.animFrame = requestAnimationFrame(loop);
      };
      this.animFrame = requestAnimationFrame(loop);
    }

    updateUI() {
      const panel = document.getElementById('faControlsPanel');
      if (!panel) return;

      if (this.activeTab === 'bac') {
        panel.innerHTML = this.renderBacControls();
        this.bindBacEvents();
      } else if (this.activeTab === 'tunnel') {
        panel.innerHTML = this.renderTunnelControls();
        this.bindTunnelEvents();
      } else if (this.activeTab === 'protocol') {
        panel.innerHTML = this.renderProtocolControls();
        this.bindProtocolEvents();
      }
    }

    // -------------------------------------------------------------
    // TAB 1: BAC & REACTION TIME
    // -------------------------------------------------------------
    renderBacControls() {
      const isNeo = this.driverType === 'neo';
      const bacVal = this.bac.toFixed(1);

      // Calculations
      // Normal reaction time: 1.0s. Increases by ~0.5s per 0.5 g/l
      const reactionTime = 1.0 + this.bac * 1.1; // e.g. 0.0 -> 1.0s, 0.5 -> 1.55s, 1.5 -> 2.65s
      const speedMs = (this.speed * 1000) / 3600;
      const reactionDist = speedMs * reactionTime;
      const brakingDist = (this.speed * this.speed) / (254 * 0.7); // dry asphalt f=0.7
      const totalStopDist = reactionDist + brakingDist;

      // Legal status
      let statusBadge = '';
      let legalDesc = '';
      let penalties = '';

      if (isNeo) {
        if (this.bac === 0.0) {
          statusBadge = `<div class="fa-legal-tag legal-safe">✅ نظامي تماماً (Tasso Zero: 0.0 g/l)</div>`;
          legalDesc = `سائق جديد ملتزم بنسبة الصفر المطلق. لا توجد أي مخالفة.`;
          penalties = `<div class="fa-penalties-box green-box">✔ لا توجد عقوبات أو خصم نقاط.</div>`;
        } else if (this.bac < 0.5) {
          statusBadge = `<div class="fa-legal-tag legal-warn">⚠️ مخالفة صريحة (مبدأ الصفر المطلق)</div>`;
          legalDesc = `يحظر القانون أي نسبة فوق 0.0 للسائقين الجدد في أول 3 سنوات ودون سن 21 سنة.`;
          penalties = `
            <div class="fa-penalties-box orange-box">
              <strong>• الغرامة:</strong> 168 إلى 672 يورو.<br>
              <strong>• خصم النقاط:</strong> 10 نقاط كاملة (مضاعفة للسائق الجديد).<br>
              <strong>• تعليق الرخصة:</strong> لا يعلق إلا في حال تكرار المخالفة.
            </div>`;
        } else if (this.bac <= 0.8) {
          statusBadge = `<div class="fa-legal-tag legal-danger">🚨 مخالفة إدارية مشددة (0.5 - 0.8 g/l)</div>`;
          legalDesc = `تجاوز الحد المعتاد مع مضاعفة العقوبات لأنك سائق جديد (Neopatentato).`;
          penalties = `
            <div class="fa-penalties-box red-box">
              <strong>• الغرامة:</strong> 724 إلى 2.898 يورو (+ زيادة الثلث).<br>
              <strong>• تعليق الرخصة:</strong> 4 إلى 8 أشهر.<br>
              <strong>• خصم النقاط:</strong> 20 نقطة كاملة (تصفير رصيد الرخصة!).
            </div>`;
        } else if (this.bac <= 1.5) {
          statusBadge = `<div class="fa-legal-tag legal-crime">⚖️ جريمة جنائية (Reato Penale: 0.8 - 1.5 g/l)</div>`;
          legalDesc = `جريمة جنائية تستوجب الإحالة للمحكمة الجنائية والحبس الفوري.`;
          penalties = `
            <div class="fa-penalties-box red-box">
              <strong>• الحبس:</strong> حتى 6 أشهر.<br>
              <strong>• الغرامة:</strong> 1.066 إلى 4.266 يورو.<br>
              <strong>• تعليق الرخصة:</strong> 8 إلى 18 شهراً.<br>
              <strong>• خصم النقاط:</strong> 20 نقطة كاملة.
            </div>`;
        } else {
          statusBadge = `<div class="fa-legal-tag legal-extreme">🛑 الجريمة الجنائية القصوى (> 1.5 g/l)</div>`;
          legalDesc = `أعلى درجات الجناية المرورية مع مصادرة المركبة.`;
          penalties = `
            <div class="fa-penalties-box extreme-box">
              <strong>• الحبس:</strong> من 6 أشهر إلى سنة.<br>
              <strong>• الغرامة:</strong> 2.000 إلى 8.000 يورو.<br>
              <strong>• تعليق الرخصة:</strong> سنة إلى سنتين (إلغاء تام عند التكرار).<br>
              <strong>• مصادرة المركبة:</strong> مصادرة إجبارية نهائية (Confisca).
            </div>`;
        }
      } else {
        // Conducente Ordinario
        if (this.bac <= 0.5) {
          statusBadge = `<div class="fa-legal-tag legal-safe">✅ ضمن الحد القانوني المسموح (<= 0.5 g/l)</div>`;
          legalDesc = `ضمن الحد الأقصى المسموح للسائق العادي (0.5 جم/لتر).`;
          penalties = `<div class="fa-penalties-box green-box">✔ لا توجد عقوبات إدارية أو جنائية.</div>`;
        } else if (this.bac <= 0.8) {
          statusBadge = `<div class="fa-legal-tag legal-warn">⚠️ مخالفة إدارية (0.5 - 0.8 g/l)</div>`;
          legalDesc = `مخالفة إدارية لا تشكل جريمة جنائية ولكنها توجب سحب الرخصة.`;
          penalties = `
            <div class="fa-penalties-box orange-box">
              <strong>• الغرامة:</strong> 543 إلى 2.170 يورو.<br>
              <strong>• تعليق الرخصة:</strong> 3 إلى 6 أشهر.<br>
              <strong>• خصم النقاط:</strong> 10 نقاط.
            </div>`;
        } else if (this.bac <= 1.5) {
          statusBadge = `<div class="fa-legal-tag legal-crime">⚖️ جريمة جنائية (0.8 - 1.5 g/l)</div>`;
          legalDesc = `جريمة جنائية تستوجب الإدانة القضائية.`;
          penalties = `
            <div class="fa-penalties-box red-box">
              <strong>• الحبس:</strong> حتى 6 أشهر.<br>
              <strong>• الغرامة:</strong> 800 إلى 3.200 يورو.<br>
              <strong>• تعليق الرخصة:</strong> 6 أشهر إلى سنة.<br>
              <strong>• خصم النقاط:</strong> 10 نقاط.
            </div>`;
        } else {
          statusBadge = `<div class="fa-legal-tag legal-extreme">🛑 الجريمة الجنائية القصوى (> 1.5 g/l)</div>`;
          legalDesc = `أقصى عقوبة مع مصادرة السيارة وخصم النقاط.`;
          penalties = `
            <div class="fa-penalties-box extreme-box">
              <strong>• الحبس:</strong> 6 أشهر إلى سنة كاملة.<br>
              <strong>• الغرامة:</strong> 1.500 إلى 6.000 يورو.<br>
              <strong>• تعليق الرخصة:</strong> سنة إلى سنتين.<br>
              <strong>• المصادرة:</strong> مصادرة المركبة (Confisca).
            </div>`;
        }
      }

      return `
        <div class="fa-control-section">
          <div class="fa-control-title">نوع السائق ومستوى التركيز:</div>
          <div class="fa-btn-toggle-row">
            <button class="fa-toggle-btn ${isNeo ? 'active' : ''}" id="btnDriverNeo">
              سائق جديد (Neopatentato)
            </button>
            <button class="fa-toggle-btn ${!isNeo ? 'active' : ''}" id="btnDriverOrd">
              سائق معتاد (Ordinario)
            </button>
          </div>

          <div class="fa-slider-box">
            <div class="fa-slider-labels">
              <span>نسبة الكحول في الدم:</span>
              <span class="fa-slider-val" id="bacDisplayVal">${bacVal} g/l</span>
            </div>
            <input type="range" class="fa-slider" id="bacSlider" min="0.0" max="2.0" step="0.1" value="${bacVal}">
            <div class="fa-slider-ticks">
              <span>0.0 (Zero)</span>
              <span>0.5 (Limite)</span>
              <span>0.8 (Penale)</span>
              <span>1.5+ (Confisca)</span>
            </div>
          </div>

          <div class="fa-slider-box">
            <div class="fa-slider-labels">
              <span>سرعة السير (Velocità):</span>
              <span class="fa-slider-val">${this.speed} km/h</span>
            </div>
            <div class="fa-btn-speed-row">
              <button class="fa-speed-btn ${this.speed === 50 ? 'active' : ''}" data-spd="50">50 km/h (مدينة)</button>
              <button class="fa-speed-btn ${this.speed === 90 ? 'active' : ''}" data-spd="90">90 km/h (خارج المدينة)</button>
              <button class="fa-speed-btn ${this.speed === 130 ? 'active' : ''}" data-spd="130">130 km/h (أوتوستراد)</button>
            </div>
          </div>
        </div>

        <div class="fa-metrics-grid">
          <div class="fa-metric-card">
            <span class="fa-metric-label">زمن رد الفعل (Tempo di Reazione)</span>
            <span class="fa-metric-val ${reactionTime > 1.2 ? 'danger-val' : 'safe-val'}">${reactionTime.toFixed(2)} ثانية</span>
            <span class="fa-metric-sub">يزداد بنسبة +${Math.round(((reactionTime - 1.0) / 1.0) * 100)}% بسبب الكحول</span>
          </div>
          <div class="fa-metric-card">
            <span class="fa-metric-label">مسافة رد الفعل (Spazio di Reazione)</span>
            <span class="fa-metric-val">${reactionDist.toFixed(1)} متر</span>
            <span class="fa-metric-sub">تقطعها السيارة قبل لمس الفرامل!</span>
          </div>
          <div class="fa-metric-card">
            <span class="fa-metric-label">مسافة التوقف الكلية (Arresto Totale)</span>
            <span class="fa-metric-val ${totalStopDist > 70 ? 'danger-val' : ''}">${totalStopDist.toFixed(1)} متر</span>
            <span class="fa-metric-sub">مسافة رد الفعل + مسافة الفرملة</span>
          </div>
        </div>

        <div class="fa-legal-summary">
          ${statusBadge}
          <p class="fa-legal-desc">${legalDesc}</p>
          ${penalties}
        </div>
      `;
    }

    bindBacEvents() {
      const btnNeo = document.getElementById('btnDriverNeo');
      const btnOrd = document.getElementById('btnDriverOrd');
      const slider = document.getElementById('bacSlider');

      if (btnNeo && btnOrd) {
        btnNeo.addEventListener('click', () => {
          playSfx();
          this.driverType = 'neo';
          this.updateUI();
        });
        btnOrd.addEventListener('click', () => {
          playSfx();
          this.driverType = 'ord';
          this.updateUI();
        });
      }

      if (slider) {
        slider.addEventListener('input', (e) => {
          this.bac = parseFloat(e.target.value);
          const disp = document.getElementById('bacDisplayVal');
          if (disp) disp.textContent = `${this.bac.toFixed(1)} g/l`;
          this.updateUI();
        });
      }

      const spdBtns = this.container.querySelectorAll('.fa-speed-btn');
      spdBtns.forEach((btn) => {
        btn.addEventListener('click', (e) => {
          playSfx();
          this.speed = parseInt(e.currentTarget.getAttribute('data-spd'), 10);
          this.updateUI();
        });
      });
    }

    // -------------------------------------------------------------
    // TAB 2: TUNNEL VISION SIMULATOR
    // -------------------------------------------------------------
    renderTunnelControls() {
      const bacVal = this.bac.toFixed(1);
      // Field of view: 180 deg at 0.0, down to 40 deg at 1.8
      const fov = Math.max(35, Math.round(180 - this.bac * 75));
      const lateralPerception = Math.max(10, Math.round(100 - this.bac * 50));

      return `
        <div class="fa-control-section">
          <div class="fa-control-title">محاكاة ظاهرة الرؤية النفقية (Visione a Tunnel):</div>
          <p class="fa-panel-lead">
            الكحول يؤثر مباشرة على القشرة البصرية؛ فتفقد العين تدريجياً القدرة على التقاط الأجسام والمشاة المتحركين في المحيط الجانبي، وتتركز الرؤية في نقطة دائرية ضيقة في الأمام.
          </p>

          <div class="fa-slider-box">
            <div class="fa-slider-labels">
              <span>مستوى تركيز الكحول الحالي:</span>
              <span class="fa-slider-val">${bacVal} g/l</span>
            </div>
            <input type="range" class="fa-slider" id="tunnelBacSlider" min="0.0" max="2.0" step="0.1" value="${bacVal}">
            <div class="fa-slider-ticks">
              <span>0.0 (رؤية كاملة 180°)</span>
              <span>0.8 (نفق متوسط)</span>
              <span>1.5+ (نفق ضيق قاتل)</span>
            </div>
          </div>
        </div>

        <div class="fa-metrics-grid">
          <div class="fa-metric-card">
            <span class="fa-metric-label">زاوية المجال البصري (Campo Visivo)</span>
            <span class="fa-metric-val ${fov < 90 ? 'danger-val' : 'safe-val'}">${fov}°</span>
            <span class="fa-metric-sub">${fov < 90 ? 'انحسار جانبي خطير' : 'مجال طبيعي'}</span>
          </div>
          <div class="fa-metric-card">
            <span class="fa-metric-label">كفاءة الرؤية الجانبية (Visione Laterale)</span>
            <span class="fa-metric-val ${lateralPerception < 50 ? 'danger-val' : ''}">${lateralPerception}%</span>
            <span class="fa-metric-sub">إدراك المشاة والسيارات في التقاطعات</span>
          </div>
        </div>

        <div class="fa-trap-box-interactive">
          <div class="fa-trap-header">⚠️ فخ الامتحان الوزاري المؤكد:</div>
          <p>
            يقول واضع الامتحان: <em>"L'assunzione di alcool amplia il campo visivo laterale"</em> -> الإجابة حتماً <strong>FALSO</strong>! الكحول يضيق المجال البصري (Restringe il campo visivo) ويحدث الرؤية النفقية!
          </p>
        </div>
      `;
    }

    bindTunnelEvents() {
      const slider = document.getElementById('tunnelBacSlider');
      if (slider) {
        slider.addEventListener('input', (e) => {
          this.bac = parseFloat(e.target.value);
          this.updateUI();
        });
      }
    }

    // -------------------------------------------------------------
    // TAB 3: FIRST AID 112 PROTOCOL
    // -------------------------------------------------------------
    renderProtocolControls() {
      const protocols = {
        pls: {
          title: 'وضعية الإفاقة الجانبية (Posizione Laterale di Sicurezza - PLS)',
          badge: 'فاقد للوعي ولكن يتنفس بانتظام',
          doText: `• تمديد المصاب على جنبه مع ثني الساق والذراع العلوية لدعمه.<br>• إمالة الرأس بلطف للخلف وفتح الفم لأسفل لضمان مجرى هواء سالك.<br>• فحص التنفس ومراقبته باستمرار لحين وصول الإسعاف.`,
          dontText: `❌ يحظر تطبيقها لمن توقف نبضه وقلبه.<br>❌ يحظر سكب ماء بارد أو عطور على وجهه لإيقاظه.<br>❌ تجنب تحريك الرقبة إذا اشتبه بكسر عمود فقري إلا إذا كان يتقيأ.`,
          examTrap: `الامتحان يركز: وضعية PLS تستخدم فقط للشخص الفاقد للوعي الذي يتنفس (Incosciente ma respira)!`
        },
        emorragia: {
          title: 'إيقاف النزيف الدموي الخارجي (Emorragia Esterna)',
          badge: 'نزيف حاد شرياني أو وريدي',
          doText: `• الضغط المباشر على الجرح بقطعة شاش معقمة أو قماش نظيف (Tamponamento).<br>• رفع الطرف المصاب النازف أعلى من مستوى القلب لتقليل ضغط الدم.<br>• وضع المصاب مستلقياً على ظهره لتفادي فقدان الوعي.`,
          dontText: `❌ يحظر نزع أي جسم غريب (زجاج أو معدن) مغروز في الجرح (Non rimuovere il corpo estraneo).<br>❌ يحظر وضع البن أو المواد الغريبة داخل الجروح المفتوحة.`,
          examTrap: `الجسم المغروز في الجرح يعمل كسدادة للشريان الممزق؛ نزعه يؤدي لنزيف صاعق وموت فوري!`
        },
        shock: {
          title: 'حالة الصدمة وهبوط التروية (Stato di Shock)',
          badge: 'شحوب، عرق بارد، نبض سريع وضعيف',
          doText: `• تمديد المصاب أرضاً ورفع ساقيه 20 إلى 30 سم (وضعية ترندلنبورغ).<br>• تغطية المصاب ببطانية حرارية لمنع انخفاض حرارة الجسم (Ipotermia).<br>• التحدث معه بهدوء لطمأنته وتخفيف الرعب النفسي.`,
          dontText: `❌ يحظر إعطاؤه أي مشروب كحولي أو قهوة ساخنة (Non somministrare alcolici).<br>❌ يحظر إعطاؤه أدوية مسكنة للألم (Non somministrare farmaci).<br>❌ يحظر إجباره على الوقوف أو المشي.`,
          examTrap: `إعطاء الخمر للمصاب بالصدمة يوسع الأوعية ويسرع الوفاة؛ احفظ (Gambe sollevate e coperta)!`
        },
        casco: {
          title: 'خوذة سائق الدراجة المصاب (Casco del Motociclista)',
          badge: 'سقوط سائق دراجة نارية على الطريق',
          doText: `• القاعدة المطلقة: عدم نزع الخوذة الواقية إطلاقاً (Non togliere il casco).<br>• فتح القناع الزجاجي الشفاف (Visiera) فقط لتسهيل التنفس وفحص الوعي.<br>• تثبيت الرأس والرقبة لمنع أي حركة غير مقصودة.`,
          dontText: `❌ يحظر نزع الخوذة حتى لو طلب المصاب ذلك أو كان متألماً.<br>❌ لا تنزع الخوذة إلا في حالة واحدة قصوى: توقف تام للتنفس يتطلب الإنعاش القلبي الرئوي.`,
          examTrap: `نزع الخوذة يحرك الفقرات العنقية ويكسر الحبل الشوكي مسبباً الشلل الرباعي أو الوفاة الفورية!`
        },
        ustioni: {
          title: 'إسعاف المصاب بالحروق (Infortunato con Ustioni)',
          badge: 'نيران مشتعلة أو ملامسة أجزاء ملتهبة',
          doText: `• إخماد النيران بدحرجة المصاب على الأرض أو تغطيته ببطانية.<br>• سكب ماء بارد ونظيف على مكان الحرق لمدة 10 - 15 دقيقة لتبريد الأنسجة.<br>• تغطية الجرح بشاش معقم نظيف غير لاصق.`,
          dontText: `❌ يحظر شد ونزع الملابس الملتصقة بالجلد المحترق (Non staccare i vestiti).<br>❌ يحظر وضع الزبدة أو الزيوت أو المراهم على الحرق الحديث.<br>❌ يحظر فقء أو فتح البثور والفقاعات المائية (Non forare le vescicole).`,
          examTrap: `الملابس الملتصقة تترك مكانها وتقص من حولها، والبثور تحمي الجلد من التلوث ويحظر لمسها!`
        },
        occhio: {
          title: 'دخول جسم غريب في العين (Corpo Estraneo nell\'Occhio)',
          badge: 'شظايا زجاج أو أتربة في قرنية العين',
          doText: `• منع المصاب قطعياً من فرك أو دعك عينه المصابة.<br>• تضميد كلتا العينين معاً (Entrambi gli occhi) بشاش معقم نظيف.<br>• نقل المصاب فوراً إلى مركز طوارئ عيون متخصص.`,
          dontText: `❌ يحظر محاولة نزع الجسم الغريب بأعواد قطنية أو ملاقط معدنية.<br>❌ يحظر وضع قطرات دوائية أو غسول كيميائي بدون إشراف طبي.`,
          examTrap: `تضميد كلتا العينين يمنع الحركة المتزامنة التلقائية (Movimenti coordinati) للعين السليمة مع المصابة!`
        }
      };

      const curr = protocols[this.selectedEmergency] || protocols.pls;

      return `
        <div class="fa-control-section">
          <div class="fa-control-title">اختر الحالة الإسعافية الطارئة لاستكشاف البروتوكول:</div>
          <div class="fa-btn-proto-grid">
            <button class="fa-proto-btn ${this.selectedEmergency === 'pls' ? 'active' : ''}" data-proto="pls">
              🛌 فاقد للوعي (PLS)
            </button>
            <button class="fa-proto-btn ${this.selectedEmergency === 'emorragia' ? 'active' : ''}" data-proto="emorragia">
              🩸 نزيف دموي
            </button>
            <button class="fa-proto-btn ${this.selectedEmergency === 'shock' ? 'active' : ''}" data-proto="shock">
              🫀 حالة صدمة
            </button>
            <button class="fa-proto-btn ${this.selectedEmergency === 'casco' ? 'active' : ''}" data-proto="casco">
              🏍️ خوذة الدراجة
            </button>
            <button class="fa-proto-btn ${this.selectedEmergency === 'ustioni' ? 'active' : ''}" data-proto="ustioni">
              🔥 حروق نارية
            </button>
            <button class="fa-proto-btn ${this.selectedEmergency === 'occhio' ? 'active' : ''}" data-proto="occhio">
              👁️ إصابة العين
            </button>
          </div>
        </div>

        <div class="fa-proto-card">
          <div class="fa-proto-header">
            <h4>${curr.title}</h4>
            <span class="fa-proto-badge">${curr.badge}</span>
          </div>

          <div class="fa-proto-actions-grid">
            <div class="fa-action-col fa-do-col">
              <h5>✅ التصرف الطبي الإلزامي (Cosa fare):</h5>
              <p>${curr.doText}</p>
            </div>
            <div class="fa-action-col fa-dont-col">
              <h5>❌ المحظورات القاتلة (Cosa NON fare):</h5>
              <p>${curr.dontText}</p>
            </div>
          </div>

          <div class="fa-trap-box-interactive" style="margin-top:12px;">
            <div class="fa-trap-header">💡 سر الامتحان الوزاري:</div>
            <p>${curr.examTrap}</p>
          </div>
        </div>
      `;
    }

    bindProtocolEvents() {
      const pBtns = this.container.querySelectorAll('.fa-proto-btn');
      pBtns.forEach((btn) => {
        btn.addEventListener('click', (e) => {
          playSfx();
          this.selectedEmergency = e.currentTarget.getAttribute('data-proto');
          this.updateUI();
        });
      });
    }

    // -------------------------------------------------------------
    // CANVAS RENDERING ENGINE (60 FPS)
    // -------------------------------------------------------------
    renderCanvas() {
      const w = this.canvas.width;
      const h = this.canvas.height;
      const ctx = this.ctx;

      ctx.clearRect(0, 0, w, h);

      if (this.activeTab === 'bac') {
        this.drawBacScene(w, h, ctx);
      } else if (this.activeTab === 'tunnel') {
        this.drawTunnelScene(w, h, ctx);
      } else if (this.activeTab === 'protocol') {
        this.drawProtocolScene(w, h, ctx);
      }
    }

    drawBacScene(w, h, ctx) {
      // Background: Road highway perspective
      const skyGrad = ctx.createLinearGradient(0, 0, 0, h * 0.45);
      skyGrad.addColorStop(0, '#090d16');
      skyGrad.addColorStop(1, '#1e293b');
      ctx.fillStyle = skyGrad;
      ctx.fillRect(0, 0, w, h * 0.45);

      // Stars/City lights in horizon
      ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
      for (let i = 0; i < 20; i++) {
        const sx = (i * 47) % w;
        const sy = 20 + ((i * 31) % 80);
        ctx.fillRect(sx, sy, 2, 2);
      }

      // Ground & Asphalt
      const roadGrad = ctx.createLinearGradient(0, h * 0.45, 0, h);
      roadGrad.addColorStop(0, '#111827');
      roadGrad.addColorStop(1, '#0b0f19');
      ctx.fillStyle = roadGrad;
      ctx.fillRect(0, h * 0.45, w, h * 0.55);

      // Perspective Road Trajectory
      const horizonY = h * 0.45;
      const vpX = w * 0.5;

      ctx.beginPath();
      ctx.moveTo(vpX - 40, horizonY);
      ctx.lineTo(vpX + 40, horizonY);
      ctx.lineTo(w * 0.85, h);
      ctx.lineTo(w * 0.15, h);
      ctx.closePath();
      ctx.fillStyle = '#1e293b';
      ctx.fill();

      // Road side guardrails
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(vpX - 40, horizonY);
      ctx.lineTo(w * 0.15, h);
      ctx.moveTo(vpX + 40, horizonY);
      ctx.lineTo(w * 0.85, h);
      ctx.stroke();

      // Animated Road Markings
      const dashOffset = (this.animTime * (this.speed * 1.5)) % 60;
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 4;
      ctx.setLineDash([25, 25]);
      ctx.lineDashOffset = -dashOffset;

      ctx.beginPath();
      ctx.moveTo(vpX, horizonY);
      ctx.lineTo(vpX, h);
      ctx.stroke();
      ctx.setLineDash([]);

      // Obstacle ahead on the road
      const obsY = h * 0.62;
      const obsW = 60;
      const obsH = 40;
      ctx.fillStyle = '#f43f5e';
      ctx.fillRect(vpX - obsW / 2, obsY, obsW, obsH);
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 12px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('⚠️ عائق', vpX, obsY + 24);

      // Distance Markers & Comparison Cars
      const isNeo = this.driverType === 'neo';
      const reactionTime = 1.0 + this.bac * 1.1;
      const speedMs = (this.speed * 1000) / 3600;
      const reactionDist = speedMs * reactionTime;
      const brakingDist = (this.speed * this.speed) / (254 * 0.7);
      const totalDist = reactionDist + brakingDist;

      // Draw braking comparison chart in upper canvas
      const boxW = w * 0.9;
      const boxH = 110;
      const boxX = w * 0.05;
      const boxY = 15;

      ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.3)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(boxX, boxY, boxW, boxH, 8);
      ctx.fill();
      ctx.stroke();

      // Bar 1: Sober Driver (1.0s reaction)
      const soberReactDist = speedMs * 1.0;
      const soberTotal = soberReactDist + brakingDist;
      const scale = (boxW - 180) / Math.max(160, totalDist * 1.2);

      ctx.textAlign = 'right';
      ctx.font = '12px Inter, sans-serif';
      ctx.fillStyle = '#94a3b8';
      ctx.fillText('سائق يقظ (0.0 g/l):', boxX + 130, boxY + 38);

      const bar1X = boxX + 140;
      // React portion (Green)
      ctx.fillStyle = '#10b981';
      ctx.fillRect(bar1X, boxY + 24, soberReactDist * scale, 16);
      // Brake portion (Sky)
      ctx.fillStyle = '#0284c7';
      ctx.fillRect(bar1X + soberReactDist * scale, boxY + 24, brakingDist * scale, 16);

      ctx.fillStyle = '#fff';
      ctx.textAlign = 'left';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.fillText(`${soberTotal.toFixed(1)}m`, bar1X + soberTotal * scale + 8, boxY + 37);

      // Bar 2: Current Intoxicated Driver
      ctx.textAlign = 'right';
      ctx.font = '12px Inter, sans-serif';
      ctx.fillStyle = this.bac > 0.0 ? '#f43f5e' : '#10b981';
      ctx.fillText(`السائق الحالي (${this.bac.toFixed(1)} g/l):`, boxX + 130, boxY + 76);

      const bar2X = boxX + 140;
      // React portion (Red/Orange)
      ctx.fillStyle = this.bac > 0.0 ? '#f43f5e' : '#10b981';
      ctx.fillRect(bar2X, boxY + 62, reactionDist * scale, 16);
      // Brake portion (Sky)
      ctx.fillStyle = '#0284c7';
      ctx.fillRect(bar2X + reactionDist * scale, boxY + 62, brakingDist * scale, 16);

      ctx.fillStyle = '#fff';
      ctx.textAlign = 'left';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.fillText(`${totalDist.toFixed(1)}m`, bar2X + totalDist * scale + 8, boxY + 75);

      // Difference indicator
      const extraDist = totalDist - soberTotal;
      if (extraDist > 0.1) {
        ctx.fillStyle = '#fbbf24';
        ctx.font = 'bold 11px Inter, sans-serif';
        ctx.fillText(`(+${extraDist.toFixed(1)} متر إضافية قاتلة!)`, bar2X + totalDist * scale + 65, boxY + 75);
      }

      // Legend in box
      ctx.font = '10px Inter, sans-serif';
      ctx.fillStyle = '#10b981';
      ctx.fillRect(boxX + 140, boxY + 94, 10, 10);
      ctx.fillStyle = '#94a3b8';
      ctx.fillText('مسافة زمن رد الفعل', boxX + 155, boxY + 103);

      ctx.fillStyle = '#0284c7';
      ctx.fillRect(boxX + 270, boxY + 94, 10, 10);
      ctx.fillStyle = '#94a3b8';
      ctx.fillText('مسافة الفرملة الميكانيكية', boxX + 285, boxY + 103);
    }

    drawTunnelScene(w, h, ctx) {
      // Night Road view with side pedestrians and intersection
      const skyGrad = ctx.createLinearGradient(0, 0, 0, h * 0.5);
      skyGrad.addColorStop(0, '#050811');
      skyGrad.addColorStop(1, '#0f172a');
      ctx.fillStyle = skyGrad;
      ctx.fillRect(0, 0, w, h * 0.5);

      // Road
      const roadY = h * 0.5;
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, roadY, w, h * 0.5);

      // Streetlights and side elements
      ctx.fillStyle = '#334155';
      ctx.fillRect(0, roadY - 40, w, 40); // buildings outline

      // Animated Road Markings
      const vpX = w * 0.5;
      const vpY = roadY;
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(vpX, vpY);
      ctx.lineTo(w * 0.5, h);
      ctx.stroke();

      // Lateral hazards (Pedestrian on left, cyclist/car on right)
      // Left pedestrian
      const pedX = w * 0.18;
      const pedY = h * 0.7;
      ctx.fillStyle = '#f59e0b';
      // Head
      ctx.beginPath();
      ctx.arc(pedX, pedY - 30, 8, 0, Math.PI * 2);
      ctx.fill();
      // Body
      ctx.fillRect(pedX - 6, pedY - 20, 12, 28);
      // Pedestrian label
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('🚶 أحد المشاة', pedX, pedY + 22);

      // Right vehicle entering from side street
      const carX = w * 0.82;
      const carY = h * 0.68;
      ctx.fillStyle = '#38bdf8';
      ctx.fillRect(carX - 25, carY - 15, 50, 30);
      // Headlights
      ctx.fillStyle = '#fef08a';
      ctx.fillRect(carX - 23, carY - 5, 8, 8);
      ctx.fillRect(carX + 15, carY - 5, 8, 8);
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('🚗 سيارة جانبية', carX, carY + 30);

      // Center car ahead
      ctx.fillStyle = '#ef4444';
      ctx.fillRect(vpX - 25, h * 0.65, 50, 32);
      ctx.fillStyle = '#fee2e2';
      ctx.fillRect(vpX - 20, h * 0.65 + 6, 8, 6);
      ctx.fillRect(vpX + 12, h * 0.65 + 6, 8, 6);

      // NOW APPLY TUNNEL VISION VIGNETTE
      // As bac increases (0.0 to 2.0), outer radius shrinks and darkness deepens
      const maxRadius = Math.max(w, h);
      const innerRadius = Math.max(60, (maxRadius * 0.45) - (this.bac * 120));
      const outerRadius = Math.max(innerRadius + 40, (maxRadius * 0.7) - (this.bac * 100));

      const grad = ctx.createRadialGradient(vpX, h * 0.6, innerRadius, vpX, h * 0.6, outerRadius);
      grad.addColorStop(0, 'rgba(0, 0, 0, 0)');
      grad.addColorStop(0.5, `rgba(0, 0, 0, ${Math.min(0.85, this.bac * 0.5)})`);
      grad.addColorStop(1, `rgba(0, 0, 0, ${Math.min(0.98, 0.2 + this.bac * 0.65)})`);

      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      // Warning text overlay if peripheral is blinded
      if (this.bac >= 0.8) {
        ctx.fillStyle = 'rgba(244, 63, 94, 0.9)';
        ctx.font = 'bold 14px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('⚠️ انعدام كامل لإدراك المشاة والسيارات الجانبية (Cecità periferica)!', vpX, 35);
      }
    }

    drawProtocolScene(w, h, ctx) {
      // First aid visualization scene
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, w, h);

      // Diagnostic Heartbeat Pulse Wave at Top
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 2;
      ctx.beginPath();
      const waveY = 40;
      for (let x = 0; x < w; x++) {
        const freq = (x + this.animTime * 140) % 200;
        let y = waveY;
        if (freq > 80 && freq < 90) y = waveY - 20;
        else if (freq >= 90 && freq < 100) y = waveY + 25;
        else if (freq >= 100 && freq < 110) y = waveY - 12;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      // Protocol info card rendered on canvas
      const currProto = this.selectedEmergency;
      const cx = w * 0.5;

      ctx.fillStyle = '#fff';
      ctx.font = 'bold 18px Inter, sans-serif';
      ctx.textAlign = 'center';

      let title = '';
      let sub = '';
      let icon = '';

      if (currProto === 'pls') {
        icon = '🛌';
        title = 'وضعية الإفاقة الجانبية (Posizione Laterale di Sicurezza)';
        sub = 'الرأس مائل للخلف • الفم مفتوح لأسفل • مجرى الهواء سالك';
      } else if (currProto === 'emorragia') {
        icon = '🩸';
        title = 'الضغط المباشر على موضع النزيف (Tamponamento Diretto)';
        sub = 'شاش معقم • رفع الطرف لأعلى • حظر نزع الأجسام المغروزة';
      } else if (currProto === 'shock') {
        icon = '🫀';
        title = 'علاج الصدمة بوضعية ترندلنبورغ (Stato di Shock)';
        sub = 'رفع الساقين 20-30 سم • بطانية حرارية • حظر إعطاء أي كحوليات!';
      } else if (currProto === 'casco') {
        icon = '🏍️';
        title = 'حماية الفقرات العنقية لسائق الدراجة (Casco Protettivo)';
        sub = 'حظر مطلق لنزع الخوذة لتفادي شلل الحبل الشوكي';
      } else if (currProto === 'ustioni') {
        icon = '🔥';
        title = 'إسعاف الحروق النارية (Ustioni da Fuoco)';
        sub = 'ماء بارد 15 دقيقة • حظر شد الملابس الملتصقة • حظر فقء البثور';
      } else if (currProto === 'occhio') {
        icon = '👁️';
        title = 'تضميد كلتا العينين معاً (Bendaggio Binoculare)';
        sub = 'تغطية العين المصابة والسليمة لمنع الحركات التوافقية المتزامنة';
      }

      ctx.fillText(`${icon} ${title}`, cx, 110);
      ctx.font = '13px Inter, sans-serif';
      ctx.fillStyle = '#38bdf8';
      ctx.fillText(sub, cx, 140);

      // Interactive Flow Diagram Boxes
      const cardW = 240;
      const cardH = 160;
      const yOffset = 180;

      // Box 1: Assessment
      this.drawDiagramBox(ctx, cx - cardW * 1.3, yOffset, cardW, cardH, '1. التقييم الأولي', 'فحص الوعي والتنفس\nالاتصال برقم 112\nتأمين الموقع بالسترة والمثلث', '#0284c7');

      // Box 2: Mandatory Action
      this.drawDiagramBox(ctx, cx - cardW * 0.5, yOffset, cardW, cardH, '2. الإجراء الطبي الصحيح', 'تطبيق البروتوكول المحدد\nتثبيت واستقرار المصاب\nمراقبة المؤشرات الحيوية', '#10b981');

      // Box 3: Fatal Traps (What NOT to do)
      this.drawDiagramBox(ctx, cx + cardW * 0.3, yOffset, cardW, cardH, '3. المحظورات القاتلة ⚠️', 'لا تعط أدوية مسكنة\nلا تعط مشروبات كحولية\nلا تنزع خوذة أو أجساماً مغروزة', '#f43f5e');
    }

    drawDiagramBox(ctx, x, y, w, h, title, text, color) {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.7)';
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.roundRect(x, y, w, h, 8);
      ctx.fill();
      ctx.stroke();

      // Top Header
      ctx.fillStyle = color;
      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(title, x + w / 2, y + 28);

      // Lines of text
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '12px Inter, sans-serif';
      const lines = text.split('\n');
      lines.forEach((line, idx) => {
        ctx.fillText(line, x + w / 2, y + 65 + idx * 24);
      });
    }
  }

  // Initialize on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      new FirstAidStudio('firstAidStudioContainer');
    });
  } else {
    new FirstAidStudio('firstAidStudioContainer');
  }
})();

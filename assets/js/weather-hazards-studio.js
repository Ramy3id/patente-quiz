/**
 * Patente B - Weather Hazards & Emergency Studio (Chapter 21)
 * 60 FPS HTML5 Canvas Simulator with Web Audio API Integration
 * Topics: Aquaplaning, Nebbia fitta, Ghiaccio/Neve, Vento laterale, Triangolo di emergenza, Sicurezza in galleria
 */

(function () {
  'use strict';

  // Audio helper
  const playSfx = () => {
    if (window.soundEngine && typeof window.soundEngine.click === 'function') {
      window.soundEngine.click();
    }
  };

  class WeatherHazardsStudio {
    constructor(containerId) {
      this.container = document.getElementById(containerId);
      if (!this.container) return;

      this.activeTab = 'aquaplaning'; // 'aquaplaning' | 'fog-wind' | 'emergency'
      
      // Aquaplaning parameters
      this.speed = 90; // km/h
      this.tread = 4.0; // mm (1.6 to 8.0)
      this.waterDepth = 5; // mm
      this.vehicleWeight = 'light'; // 'light' | 'heavy'

      // Fog & Wind parameters
      this.weatherMode = 'fog'; // 'fog' | 'wind' | 'ice'
      this.fogVis = 40; // meters
      this.lightsMode = 'anabbaglianti'; // 'anabbaglianti' | 'abbaglianti' | 'retronebbia'
      this.windSpeed = 70; // km/h
      this.vehicleType = 'caravan'; // 'car' | 'caravan' | 'moto'

      // Emergency parameters
      this.roadType = 'extraurbana'; // 'extraurbana' | 'autostrada' | 'galleria'

      this.animFrame = null;
      this.animTime = 0;

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
        <div class="wh-studio-card">
          <!-- Studio Header -->
          <div class="wh-studio-header">
            <div class="wh-studio-title-box">
              <div class="wh-studio-badge">
                <span class="wh-pulse-dot"></span>
                <span>المختبر التفاعلي المتقدم 60 FPS • الباب 21</span>
              </div>
              <h2 class="wh-studio-main-title">مختبر فيزياء الطقس المعاكس، الانزلاق المائي وطوارئ الطرق والأنفاق</h2>
              <p class="wh-studio-sub-title">محاكاة فيزيائية 60 إطاراً بالثانية لقوى الطفو الهيدروديناميكي للإطارات، القيادة في الضباب والرياح، وقواعد مثلث الخطر والأنفاق</p>
            </div>
            <!-- Mode Switcher Tabs -->
            <div class="wh-tab-group">
              <button class="wh-tab-btn active" data-tab="aquaplaning">
                <span class="wh-tab-icon">🌧️</span>
                <span>الانزلاق المائي (Aquaplaning)</span>
              </button>
              <button class="wh-tab-btn" data-tab="fog-wind">
                <span class="wh-tab-icon">🌫️</span>
                <span>الضباب والرياح والجليد</span>
              </button>
              <button class="wh-tab-btn" data-tab="emergency">
                <span class="wh-tab-icon">🔺</span>
                <span>المثلث والأنفاق (Emergenza)</span>
              </button>
            </div>
          </div>

          <!-- Stage Layout -->
          <div class="wh-stage-layout">
            <!-- Canvas Simulation Box -->
            <div class="wh-canvas-wrapper">
              <canvas id="whCanvas" width="860" height="420"></canvas>
            </div>

            <!-- Interactive Control Panel -->
            <div class="wh-controls-panel" id="whControlsPanel">
              <!-- Dynamically populated via updateUI() -->
            </div>
          </div>
        </div>
      `;
      this.canvas = document.getElementById('whCanvas');
      this.ctx = this.canvas.getContext('2d');
    }

    bindEvents() {
      const tabs = this.container.querySelectorAll('.wh-tab-btn');
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
      const panel = document.getElementById('whControlsPanel');
      if (!panel) return;

      if (this.activeTab === 'aquaplaning') {
        panel.innerHTML = this.renderAquaplaningControls();
        this.bindAquaplaningEvents();
      } else if (this.activeTab === 'fog-wind') {
        panel.innerHTML = this.renderFogWindControls();
        this.bindFogWindEvents();
      } else if (this.activeTab === 'emergency') {
        panel.innerHTML = this.renderEmergencyControls();
        this.bindEmergencyEvents();
      }
    }

    // -------------------------------------------------------------
    // TAB 1: AQUAPLANING
    // -------------------------------------------------------------
    renderAquaplaningControls() {
      // Calculate aquaplaning risk & contact patch %
      // Critical hydroplaning speed formula approx: V_crit = 10 * sqrt(P_tire) - degradation factor
      // Lighter vehicles aquaplane earlier! Low tread accelerates it drastically!
      const weightBonus = this.vehicleWeight === 'heavy' ? 15 : 0;
      const treadBonus = (this.tread - 1.6) * 6; // up to ~38 km/h bonus for 8mm tread
      const criticalSpeed = Math.round(65 + weightBonus + treadBonus - (this.waterDepth * 2));

      const isAquaplaning = this.speed >= criticalSpeed;
      const contactPatch = Math.max(0, Math.min(100, Math.round(100 - ((this.speed - (criticalSpeed - 20)) / 25) * 100)));

      let statusBadge = '';
      if (contactPatch > 60) {
        statusBadge = `<div class="wh-legal-tag legal-safe">✅ تماسك طبيعي (Aderenza Ottimale)</div>`;
      } else if (contactPatch > 15) {
        statusBadge = `<div class="wh-legal-tag legal-warn">⚠️ خطر انزلاق وشيك (Pericolo Slittamento)</div>`;
      } else {
        statusBadge = `<div class="wh-legal-tag legal-danger">🚨 انزلاق مائي تام (Aquaplaning Totale: 0% تماس!)</div>`;
      }

      return `
        <div class="wh-control-section">
          <div class="wh-control-title">السرعة وعمق مداس الإطار (Battistrada):</div>
          
          <div class="wh-slider-box">
            <div class="wh-slider-labels">
              <span>سرعة السير (Velocità):</span>
              <span class="wh-slider-val">${this.speed} km/h</span>
            </div>
            <input type="range" class="wh-slider" id="speedSlider" min="40" max="140" step="5" value="${this.speed}">
            <div class="wh-slider-ticks">
              <span>40</span>
              <span>70</span>
              <span>100</span>
              <span>130 km/h</span>
            </div>
          </div>

          <div class="wh-btn-toggle-row">
            <button class="wh-toggle-btn ${this.tread === 8.0 ? 'active' : ''}" data-tread="8.0">
              إطار جديد (8 mm)
            </button>
            <button class="wh-toggle-btn ${this.tread === 4.0 ? 'active' : ''}" data-tread="4.0">
              إطار متوسط (4 mm)
            </button>
            <button class="wh-toggle-btn ${this.tread === 1.6 ? 'active' : ''}" data-tread="1.6">
              الحد الأدنى القانوني (1.6 mm) ⚠️
            </button>
          </div>

          <div class="wh-btn-toggle-row">
            <button class="wh-toggle-btn ${this.vehicleWeight === 'light' ? 'active' : ''}" id="btnWeightLight">
              🚗 سيارة خفيفة (أسرع في الطفو)
            </button>
            <button class="wh-toggle-btn ${this.vehicleWeight === 'heavy' ? 'active' : ''}" id="btnWeightHeavy">
              🚙 سيارة ثقيلة / دفع رباعي
            </button>
          </div>
        </div>

        <div class="wh-metrics-grid">
          <div class="wh-metric-card">
            <span class="wh-metric-label">نسبة التماس بالإسفلت</span>
            <span class="wh-metric-val ${contactPatch < 30 ? 'danger-val' : 'safe-val'}">${contactPatch}%</span>
            <span class="wh-metric-sub">${contactPatch === 0 ? 'العجلة تطفو تماماً فوق الماء' : 'مساحة التصاق كافية'}</span>
          </div>
          <div class="wh-metric-card">
            <span class="wh-metric-label">السرعة الحرجة للطفو</span>
            <span class="wh-metric-val">${criticalSpeed} km/h</span>
            <span class="wh-metric-sub">يبدأ عندها الإطار بفقدان التحكم</span>
          </div>
          <div class="wh-metric-card">
            <span class="wh-metric-label">استجابة المقود والفرامل</span>
            <span class="wh-metric-val ${isAquaplaning ? 'danger-val' : ''}">${isAquaplaning ? 'صفر (شلل تام)' : 'فعالة'}</span>
            <span class="wh-metric-sub">يدور المقود دون أي توجيه!</span>
          </div>
        </div>

        <div class="wh-summary-box">
          ${statusBadge}
          <div class="wh-trap-box-interactive">
            <div class="wh-trap-header">⚠️ فخ الامتحان الوزاري الأبرز في الباب 21:</div>
            <p>
              يقول واضع الامتحان: <em>"Il fenomeno dell'aquaplaning si verifica più facilmente nei veicoli più pesanti"</em> -> الإجابة حتماً <strong>FALSO</strong>!<br>
              السيارة <strong>الأخف وزناً (Più leggeri)</strong> تعوم وتنزلق أسهل بكثير لأن وزنها لا يضغط طبقة الماء لطردها جانبياً!
            </p>
          </div>
        </div>
      `;
    }

    bindAquaplaningEvents() {
      const spd = document.getElementById('speedSlider');
      if (spd) {
        spd.addEventListener('input', (e) => {
          this.speed = parseInt(e.target.value, 10);
          this.updateUI();
        });
      }

      const tBtns = this.container.querySelectorAll('[data-tread]');
      tBtns.forEach((b) => {
        b.addEventListener('click', (e) => {
          playSfx();
          this.tread = parseFloat(e.currentTarget.getAttribute('data-tread'));
          this.updateUI();
        });
      });

      const bLight = document.getElementById('btnWeightLight');
      const bHeavy = document.getElementById('btnWeightHeavy');
      if (bLight && bHeavy) {
        bLight.addEventListener('click', () => {
          playSfx();
          this.vehicleWeight = 'light';
          this.updateUI();
        });
        bHeavy.addEventListener('click', () => {
          playSfx();
          this.vehicleWeight = 'heavy';
          this.updateUI();
        });
      }
    }

    // -------------------------------------------------------------
    // TAB 2: FOG, WIND & ICE
    // -------------------------------------------------------------
    renderFogWindControls() {
      return `
        <div class="wh-control-section">
          <div class="wh-control-title">اختر الظرف المناخي المعاكس:</div>
          <div class="wh-btn-toggle-row">
            <button class="wh-toggle-btn ${this.weatherMode === 'fog' ? 'active' : ''}" data-wmode="fog">
              🌫️ الضباب الكثيف (Nebbia)
            </button>
            <button class="wh-toggle-btn ${this.weatherMode === 'wind' ? 'active' : ''}" data-wmode="wind">
              💨 الرياح الجانبية (Vento)
            </button>
            <button class="wh-toggle-btn ${this.weatherMode === 'ice' ? 'active' : ''}" data-wmode="ice">
              ❄️ الجليد الأسود (Ghiaccio)
            </button>
          </div>

          ${this.weatherMode === 'fog' ? `
            <div class="wh-slider-box" style="margin-top:12px;">
              <div class="wh-slider-labels">
                <span>مسافة الرؤية في الضباب (Visibilità):</span>
                <span class="wh-slider-val">${this.fogVis} متر</span>
              </div>
              <input type="range" class="wh-slider" id="fogSlider" min="20" max="120" step="10" value="${this.fogVis}">
              <div class="wh-slider-ticks">
                <span>20m (كثيف جداً)</span>
                <span>50m (حد كشافات الخلف)</span>
                <span>120m (ضباب خفيف)</span>
              </div>
            </div>

            <div class="wh-control-title" style="margin-top:10px;">إعداد الكشافات والأنوار:</div>
            <div class="wh-btn-toggle-row">
              <button class="wh-toggle-btn ${this.lightsMode === 'anabbaglianti' ? 'active' : ''}" data-lmode="anabbaglianti">
                💡 المنخفضة (Anabbaglianti) ✅
              </button>
              <button class="wh-toggle-btn ${this.lightsMode === 'abbaglianti' ? 'active' : ''}" data-lmode="abbaglianti">
                🔦 العالية (Abbaglianti) ❌ فخ!
              </button>
              <button class="wh-toggle-btn ${this.lightsMode === 'retronebbia' ? 'active' : ''}" data-lmode="retronebbia">
                🔴 ضباب خلفي (Retronebbia)
              </button>
            </div>
          ` : ''}

          ${this.weatherMode === 'wind' ? `
            <div class="wh-slider-box" style="margin-top:12px;">
              <div class="wh-slider-labels">
                <span>شدة الرياح الجانبية على الجسر:</span>
                <span class="wh-slider-val">${this.windSpeed} km/h</span>
              </div>
              <input type="range" class="wh-slider" id="windSlider" min="30" max="110" step="10" value="${this.windSpeed}">
            </div>

            <div class="wh-control-title" style="margin-top:10px;">نوع المركبة المتأثرة بالرياح:</div>
            <div class="wh-btn-toggle-row">
              <button class="wh-toggle-btn ${this.vehicleType === 'caravan' ? 'active' : ''}" data-vtype="caravan">
                🚐 كارفان / شاحنة بستائر (الأخطر)
              </button>
              <button class="wh-toggle-btn ${this.vehicleType === 'moto' ? 'active' : ''}" data-vtype="moto">
                🏍️ دراجة نارية (معرضة للسقوط)
              </button>
              <button class="wh-toggle-btn ${this.vehicleType === 'car' ? 'active' : ''}" data-vtype="car">
                🚗 سيارة ركاب عادية
              </button>
            </div>
          ` : ''}

          ${this.weatherMode === 'ice' ? `
            <div class="wh-summary-box" style="margin-top:12px;">
              <div class="wh-legal-tag legal-danger">❄️ معامل الاحتكاك على الجليد يهبط إلى 0.1!</div>
              <p style="font-size:0.86rem; color:#cbd5e1; line-height:1.6; margin:8px 0 0;">
                • مسافة الفرملة تتضاعف حتى <strong>10 أضعاف</strong> مقارنة بالإسفلت الجاف!<br>
                • يتكون الجليد أولاً على <strong>الجسور (Ponti e viadotti)</strong> والمناطق المظللة المعرضة لتيارات الهواء البارد قبل الطرق العادية.<br>
                • تركيب سلاسل الثلج (Catene da neve) يكون إجبارياً على <strong>عجلات الدفع (Ruote motrici)</strong>.
              </p>
            </div>
          ` : ''}
        </div>

        <div class="wh-trap-box-interactive" style="margin-top:14px;">
          <div class="wh-trap-header">💡 قاعدة الامتحان الوزاري الإلزامية:</div>
          <p>
            ${this.weatherMode === 'fog' ? `
              في الضباب يحظر تماماً استخدام الضوء العالي (Abbaglianti) لأنه يصطدم بقطرات الماء في الهواء مكوناً جداراً أبيضاً ساطعاً يعمي السائق! ويسمح بتشغيل كشاف الضباب الخلفي الأحمر (Luce retronebbia) فقط إذا كانت الرؤية <strong>أقل من 50 متراً</strong>!
            ` : this.weatherMode === 'wind' ? `
              الرياح الجانبية تشكل أقصى خطورة عند <strong>الخروج من الأنفاق</strong>، وأثناء <strong>اجتياز الجسور والمنحدرات</strong>، وعند <strong>تجاوز المركبات الثقيلة ذات المساحة الجانبية الكبيرة (Furgoni e telonati)</strong>!
            ` : `
              سلاسل الثلج تركب فقط على عجلات الدفع؛ والسرعة القصوى المسموح بها مع السلاسل هي <strong>50 كم/س</strong> في جميع الطرق!
            `}
          </p>
        </div>
      `;
    }

    bindFogWindEvents() {
      const wBtns = this.container.querySelectorAll('[data-wmode]');
      wBtns.forEach((b) => {
        b.addEventListener('click', (e) => {
          playSfx();
          this.weatherMode = e.currentTarget.getAttribute('data-wmode');
          this.updateUI();
        });
      });

      const fogS = document.getElementById('fogSlider');
      if (fogS) {
        fogS.addEventListener('input', (e) => {
          this.fogVis = parseInt(e.target.value, 10);
          this.updateUI();
        });
      }

      const lBtns = this.container.querySelectorAll('[data-lmode]');
      lBtns.forEach((b) => {
        b.addEventListener('click', (e) => {
          playSfx();
          this.lightsMode = e.currentTarget.getAttribute('data-lmode');
          this.updateUI();
        });
      });

      const windS = document.getElementById('windSlider');
      if (windS) {
        windS.addEventListener('input', (e) => {
          this.windSpeed = parseInt(e.target.value, 10);
          this.updateUI();
        });
      }

      const vBtns = this.container.querySelectorAll('[data-vtype]');
      vBtns.forEach((b) => {
        b.addEventListener('click', (e) => {
          playSfx();
          this.vehicleType = e.currentTarget.getAttribute('data-vtype');
          this.updateUI();
        });
      });
    }

    // -------------------------------------------------------------
    // TAB 3: EMERGENCY TRIANGLE & TUNNELS
    // -------------------------------------------------------------
    renderEmergencyControls() {
      return `
        <div class="wh-control-section">
          <div class="wh-control-title">موقع العطل أو الطوارئ:</div>
          <div class="wh-btn-toggle-row">
            <button class="wh-toggle-btn ${this.roadType === 'extraurbana' ? 'active' : ''}" data-rtype="extraurbana">
              🛣️ طريق خارج المدينة (Extraurbana)
            </button>
            <button class="wh-toggle-btn ${this.roadType === 'autostrada' ? 'active' : ''}" data-rtype="autostrada">
              🏁 أوتوستراد (Autostrada)
            </button>
            <button class="wh-toggle-btn ${this.roadType === 'galleria' ? 'active' : ''}" data-rtype="galleria">
              🚇 داخل نفق (Galleria)
            </button>
          </div>
        </div>

        <div class="wh-summary-box" style="margin-top:14px;">
          ${this.roadType !== 'galleria' ? `
            <div class="wh-legal-tag legal-safe">🔺 قواعد وضع مثلث الخطر المتنقل (Triangolo):</div>
            <ul style="font-size:0.84rem; color:#cbd5e1; line-height:1.7; padding-right:20px; margin:8px 0 0;">
              <li><strong>المسافة من السيارة:</strong> يوضع على مسافة <strong>لا تقل عن 50 متراً</strong> خلف المركبة العاطلة.</li>
              <li><strong>مسافة الرؤية:</strong> يجب أن يكون مرئياً للمركبات القادمة من مسافة <strong>لا تقل عن 100 متر</strong>.</li>
              <li><strong>الموضع العرضي:</strong> يوضع على بعد <strong>متر واحد على الأقل</strong> من الحافة اليسرى للحارة (داخل الحارة المشغولة).</li>
              <li><strong>السترة العاكسة (Giubbotto):</strong> يجب ارتداؤها <strong>قبل النزول</strong> من السيارة ليلاً أو في ظروف الرؤية المنخفضة!</li>
            </ul>
          ` : `
            <div class="wh-legal-tag legal-danger">🚇 بروتوكول السلامة والحرائق داخل النفق:</div>
            <ul style="font-size:0.84rem; color:#cbd5e1; line-height:1.7; padding-right:20px; margin:8px 0 0;">
              <li><strong>في حال تعطل السيارة:</strong> الوصول إلى خليج التوقف (Piazzola) وإطفاء المحرك وتشغيل أضواء الطوارئ.</li>
              <li><strong>كابينة النجدة (SOS):</strong> استخدام الهاتف المخصص وليس الهاتف النقال لتحديد الموقع أوتوماتيكياً.</li>
              <li><strong>في حال اندلاع حريق:</strong> ترك مفاتيح التشغيل داخل السيارة لتسهيل إخلائها، واستخدام مسار الهروب المضاء (Via di fuga) باتجاه مخرج الطوارئ!</li>
            </ul>
          `}
        </div>

        <div class="wh-trap-box-interactive" style="margin-top:12px;">
          <div class="wh-trap-header">⚠️ فخ الامتحان الوزاري:</div>
          <p>
            ${this.roadType !== 'galleria' ? `
              احفظ الأرقام الذهبية: المسافة من السيارة <strong>50 متراً</strong>، ومسافة الرؤية <strong>100 متر</strong>! أي رقم آخر (مثل 20 متراً أو 30 متراً) هو إجابة <strong>FALSO</strong>!
            ` : `
              في حريق النفق: لا تغلق أبواب السيارة ولا تأخذ المفتاح معك؛ اتركه بالمقود حتى تتمكن فرق الإطفاء من سحب السيارات المحترقة!
            `}
          </p>
        </div>
      `;
    }

    bindEmergencyEvents() {
      const rBtns = this.container.querySelectorAll('[data-rtype]');
      rBtns.forEach((b) => {
        b.addEventListener('click', (e) => {
          playSfx();
          this.roadType = e.currentTarget.getAttribute('data-rtype');
          this.updateUI();
        });
      });
    }

    // -------------------------------------------------------------
    // CANVAS ENGINE (60 FPS)
    // -------------------------------------------------------------
    renderCanvas() {
      const w = this.canvas.width;
      const h = this.canvas.height;
      const ctx = this.ctx;

      ctx.clearRect(0, 0, w, h);

      if (this.activeTab === 'aquaplaning') {
        this.drawAquaplaningScene(w, h, ctx);
      } else if (this.activeTab === 'fog-wind') {
        this.drawFogWindScene(w, h, ctx);
      } else if (this.activeTab === 'emergency') {
        this.drawEmergencyScene(w, h, ctx);
      }
    }

    drawAquaplaningScene(w, h, ctx) {
      // Cross-section of tire rolling over wet road
      // Background dark lab
      ctx.fillStyle = '#090d16';
      ctx.fillRect(0, 0, w, h);

      // Asphalt Road Base
      const roadY = h * 0.72;
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, roadY, w, h - roadY);

      // Asphalt texture dots
      ctx.fillStyle = '#334155';
      for (let i = 0; i < 40; i++) {
        const ax = (i * 22) % w;
        const ay = roadY + 8 + ((i * 13) % 40);
        ctx.fillRect(ax, ay, 3, 2);
      }

      // Water Layer on top of asphalt
      const waterH = Math.max(10, this.waterDepth * 4);
      const waterY = roadY - waterH;

      const waterGrad = ctx.createLinearGradient(0, waterY, 0, roadY);
      waterGrad.addColorStop(0, 'rgba(56, 189, 248, 0.45)');
      waterGrad.addColorStop(1, 'rgba(2, 132, 199, 0.85)');
      ctx.fillStyle = waterGrad;
      ctx.fillRect(0, waterY, w, waterH);

      // Tire Wheel Assembly
      const tireCenterX = w * 0.45;
      const weightBonus = this.vehicleWeight === 'heavy' ? 15 : 0;
      const treadBonus = (this.tread - 1.6) * 6;
      const criticalSpeed = Math.round(65 + weightBonus + treadBonus - (this.waterDepth * 2));
      const isPlaning = this.speed >= criticalSpeed;

      // Tire lifts above asphalt when aquaplaning!
      const liftAmount = isPlaning ? Math.min(18, (this.speed - criticalSpeed) * 0.5 + 4) : 0;
      const tireRadius = 110;
      const tireCenterY = roadY - tireRadius - liftAmount;

      // Draw Tire Rubber Outer Ring
      ctx.save();
      ctx.translate(tireCenterX, tireCenterY);
      // Rotation angle based on speed and time
      const rotAngle = (this.animTime * (this.speed * 0.15)) % (Math.PI * 2);
      ctx.rotate(rotAngle);

      // Outer Rubber
      ctx.beginPath();
      ctx.arc(0, 0, tireRadius, 0, Math.PI * 2);
      ctx.fillStyle = '#0f172a';
      ctx.fill();
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 6;
      ctx.stroke();

      // Tire Tread Grooves
      const grooves = 16;
      ctx.strokeStyle = '#0284c7';
      ctx.lineWidth = Math.max(2, this.tread);
      for (let g = 0; g < grooves; g++) {
        const a = (g * Math.PI * 2) / grooves;
        const x1 = Math.cos(a) * (tireRadius - 16);
        const y1 = Math.sin(a) * (tireRadius - 16);
        const x2 = Math.cos(a) * tireRadius;
        const y2 = Math.sin(a) * tireRadius;
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
      }

      // Wheel Rim (Metallic)
      ctx.beginPath();
      ctx.arc(0, 0, tireRadius * 0.55, 0, Math.PI * 2);
      ctx.fillStyle = '#64748b';
      ctx.fill();
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 4;
      ctx.stroke();

      // Spokes
      for (let s = 0; s < 5; s++) {
        const sa = (s * Math.PI * 2) / 5;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(Math.cos(sa) * tireRadius * 0.55, Math.sin(sa) * tireRadius * 0.55);
        ctx.strokeStyle = '#cbd5e1';
        ctx.lineWidth = 6;
        ctx.stroke();
      }

      ctx.restore();

      // Dynamic Hydrodynamic Water Wedge under tire!
      if (isPlaning || this.speed > criticalSpeed - 20) {
        ctx.fillStyle = 'rgba(56, 189, 248, 0.95)';
        ctx.beginPath();
        ctx.moveTo(tireCenterX - 90, roadY);
        ctx.lineTo(tireCenterX + 40, roadY);
        ctx.lineTo(tireCenterX + 20, roadY - liftAmount - 4);
        ctx.lineTo(tireCenterX - 70, roadY - waterH);
        ctx.closePath();
        ctx.fill();

        // Water Splash sprays forward and up
        ctx.fillStyle = 'rgba(186, 230, 253, 0.8)';
        for (let sp = 0; sp < 12; sp++) {
          const spX = tireCenterX - 80 - Math.random() * 60;
          const spY = roadY - Math.random() * 50;
          ctx.beginPath();
          ctx.arc(spX, spY, 3, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Dashboard Floating Status & Steering Wheel status
      const dashX = w * 0.05;
      const dashY = 20;
      const dashW = 260;
      const dashH = 100;

      ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
      ctx.strokeStyle = isPlaning ? 'rgba(244, 63, 94, 0.5)' : 'rgba(56, 189, 248, 0.3)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.roundRect(dashX, dashY, dashW, dashH, 10);
      ctx.fill();
      ctx.stroke();

      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.fillStyle = isPlaning ? '#f43f5e' : '#38bdf8';
      ctx.textAlign = 'right';
      ctx.fillText(isPlaning ? '⚠️ إنذار: العجلة تطفو (Aquaplaning)' : '✔ التماسك مستقر (Aderenza OK)', dashX + dashW - 14, dashY + 28);

      ctx.font = '11px Inter, sans-serif';
      ctx.fillStyle = '#cbd5e1';
      ctx.fillText(`عمق مداس الإطار: ${this.tread} مم`, dashX + dashW - 14, dashY + 52);
      ctx.fillText(`السرعة الحالية: ${this.speed} كم/س`, dashX + dashW - 14, dashY + 72);

      if (isPlaning) {
        ctx.fillStyle = '#fecdd3';
        ctx.fillText('انعدام تام لقوة التوجيه والفرملة!', dashX + dashW - 14, dashY + 90);
      }
    }

    drawFogWindScene(w, h, ctx) {
      if (this.weatherMode === 'fog') {
        this.drawFogScene(w, h, ctx);
      } else if (this.weatherMode === 'wind') {
        this.drawWindScene(w, h, ctx);
      } else {
        this.drawIceScene(w, h, ctx);
      }
    }

    drawFogScene(w, h, ctx) {
      // Perspective Road inside Fog
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, 0, w, h);

      const vpX = w * 0.5;
      const vpY = h * 0.45;

      // Road Trajectory
      ctx.beginPath();
      ctx.moveTo(vpX - 30, vpY);
      ctx.lineTo(vpX + 30, vpY);
      ctx.lineTo(w * 0.85, h);
      ctx.lineTo(w * 0.15, h);
      ctx.closePath();
      ctx.fillStyle = '#0f172a';
      ctx.fill();

      // Road Delineator posts on edges
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 3;
      ctx.setLineDash([20, 20]);
      ctx.beginPath();
      ctx.moveTo(vpX, vpY);
      ctx.lineTo(vpX, h);
      ctx.stroke();
      ctx.setLineDash([]);

      // Headlight Beam Simulation from driver's viewpoint
      if (this.lightsMode === 'anabbaglianti') {
        // Low beam: cuts low, illuminates road surface
        const beamGrad = ctx.createRadialGradient(vpX, h * 0.85, 40, vpX, h * 0.6, 260);
        beamGrad.addColorStop(0, 'rgba(254, 240, 138, 0.4)');
        beamGrad.addColorStop(1, 'rgba(254, 240, 138, 0)');
        ctx.fillStyle = beamGrad;
        ctx.fillRect(w * 0.15, h * 0.45, w * 0.7, h * 0.55);
      } else if (this.lightsMode === 'abbaglianti') {
        // High beam: hits fog particles, creates glaring white blindness wall!
        const glareGrad = ctx.createRadialGradient(vpX, h * 0.5, 20, vpX, h * 0.5, 340);
        glareGrad.addColorStop(0, 'rgba(255, 255, 255, 0.95)');
        glareGrad.addColorStop(0.6, 'rgba(241, 245, 249, 0.85)');
        glareGrad.addColorStop(1, 'rgba(203, 213, 225, 0.5)');
        ctx.fillStyle = glareGrad;
        ctx.fillRect(0, 0, w, h);

        ctx.fillStyle = '#dc2626';
        ctx.font = 'bold 16px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('⚠️ جدار أبيض ساطع وانبهار ضوئي تام (Muro Bianco Riflesso)!', vpX, h * 0.3);
        return;
      }

      // Preceding Car in Fog
      const carDistY = vpY + (this.fogVis / 120) * (h * 0.35);
      const carW = 40 + (carDistY - vpY) * 0.3;
      const carH = carW * 0.6;

      ctx.fillStyle = '#dc2626';
      ctx.fillRect(vpX - carW / 2, carDistY, carW, carH);

      // Rear red fog light if visibility < 50m
      if (this.lightsMode === 'retronebbia' || this.fogVis < 50) {
        ctx.fillStyle = '#ff0000';
        ctx.shadowColor = '#ff0000';
        ctx.shadowBlur = 18;
        ctx.beginPath();
        ctx.arc(vpX, carDistY + carH * 0.5, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // Fog Overlay Thickness
      const fogDensity = Math.max(0.2, 1.0 - this.fogVis / 120);
      ctx.fillStyle = `rgba(148, 163, 184, ${fogDensity})`;
      ctx.fillRect(0, 0, w, h);
    }

    drawWindScene(w, h, ctx) {
      // Viaduct Bridge with Crosswind & Windsock
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, w, h);

      // Sky
      const skyGrad = ctx.createLinearGradient(0, 0, 0, h * 0.6);
      skyGrad.addColorStop(0, '#1e293b');
      skyGrad.addColorStop(1, '#334155');
      ctx.fillStyle = skyGrad;
      ctx.fillRect(0, 0, w, h * 0.6);

      // Bridge Road
      const bridgeY = h * 0.6;
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, bridgeY, w, 24);
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, bridgeY + 24, w, h - bridgeY - 24);

      // Bridge Pillars
      ctx.fillStyle = '#475569';
      ctx.fillRect(w * 0.2, bridgeY + 24, 30, h);
      ctx.fillRect(w * 0.7, bridgeY + 24, 30, h);

      // Guardrail
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(0, bridgeY - 14);
      ctx.lineTo(w, bridgeY - 14);
      ctx.stroke();

      // Windsock (Manica a vento) on Bridge
      const poleX = w * 0.85;
      const poleY = bridgeY - 14;
      ctx.strokeStyle = '#cbd5e1';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(poleX, poleY);
      ctx.lineTo(poleX, poleY - 90);
      ctx.stroke();

      // Windsock tilt based on wind speed
      const tiltAngle = (this.windSpeed / 110) * 0.9; // angle in radians
      const sockLen = 50;

      ctx.save();
      ctx.translate(poleX, poleY - 90);
      ctx.rotate(-tiltAngle);

      // Red and White striped windsock
      const stripes = 4;
      for (let st = 0; st < stripes; st++) {
        ctx.fillStyle = st % 2 === 0 ? '#ef4444' : '#ffffff';
        const sx = (st * sockLen) / stripes;
        const sw = sockLen / stripes;
        ctx.beginPath();
        ctx.moveTo(sx, -10 + st * 1.5);
        ctx.lineTo(sx + sw, -10 + (st + 1) * 1.5);
        ctx.lineTo(sx + sw, 10 - (st + 1) * 1.5);
        ctx.lineTo(sx, 10 - st * 1.5);
        ctx.closePath();
        ctx.fill();
      }
      ctx.restore();

      // Vehicle on Bridge drifting due to crosswind
      const drift = (this.windSpeed / 110) * (this.vehicleType === 'caravan' ? 45 : this.vehicleType === 'moto' ? 35 : 15);
      const vX = w * 0.4 - drift;
      const vY = bridgeY - 35;

      if (this.vehicleType === 'caravan') {
        // Large boxy van/caravan
        ctx.fillStyle = '#38bdf8';
        ctx.fillRect(vX, vY - 30, 80, 50);
        ctx.fillStyle = '#e0f2fe';
        ctx.fillRect(vX + 50, vY - 20, 24, 20); // window
      } else if (this.vehicleType === 'moto') {
        // Motorcycle tilted
        ctx.fillStyle = '#f59e0b';
        ctx.fillRect(vX + 20, vY - 10, 30, 20);
      } else {
        // Car
        ctx.fillStyle = '#10b981';
        ctx.fillRect(vX, vY - 10, 60, 30);
      }

      // Wind Vector Arrows
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.6)';
      ctx.lineWidth = 2;
      for (let a = 0; a < 5; a++) {
        const arX = w * 0.1 + a * 140;
        const arY = bridgeY - 60 - (a % 2) * 20;
        ctx.beginPath();
        ctx.moveTo(arX, arY);
        ctx.lineTo(arX + 50, arY);
        ctx.lineTo(arX + 40, arY - 6);
        ctx.stroke();
      }
    }

    drawIceScene(w, h, ctx) {
      // Road covered in black ice
      ctx.fillStyle = '#0b0f19';
      ctx.fillRect(0, 0, w, h);

      // Snowy landscape
      ctx.fillStyle = '#e2e8f0';
      ctx.fillRect(0, h * 0.5, w, h * 0.5);

      // Icy Asphalt road
      const vpX = w * 0.5;
      const vpY = h * 0.5;
      ctx.beginPath();
      ctx.moveTo(vpX - 35, vpY);
      ctx.lineTo(vpX + 35, vpY);
      ctx.lineTo(w * 0.8, h);
      ctx.lineTo(w * 0.2, h);
      ctx.closePath();
      ctx.fillStyle = '#1e293b';
      ctx.fill();

      // Shiny Ice Layer reflection
      const iceGrad = ctx.createLinearGradient(0, vpY, 0, h);
      iceGrad.addColorStop(0, 'rgba(186, 230, 253, 0.3)');
      iceGrad.addColorStop(1, 'rgba(224, 242, 254, 0.65)');
      ctx.fillStyle = iceGrad;
      ctx.fill();

      // Car spinning / skidding on ice
      const carX = vpX;
      const carY = h * 0.72;
      ctx.save();
      ctx.translate(carX, carY);
      ctx.rotate(0.25); // skidding angle
      ctx.fillStyle = '#ef4444';
      ctx.fillRect(-35, -20, 70, 40);
      ctx.restore();

      // Skid marks
      ctx.strokeStyle = 'rgba(15, 23, 42, 0.4)';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(carX - 20, carY + 20);
      ctx.quadraticCurveTo(carX - 40, h * 0.85, carX - 10, h);
      ctx.stroke();

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 15px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('❄️ فقدان الالتصاق التام على الجليد (Fondo Ghiacciato)', vpX, 40);
    }

    drawEmergencyScene(w, h, ctx) {
      // Road scene with 50m / 100m distance markers
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, w, h);

      const roadY = h * 0.55;
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, roadY, w, 70);

      // Stalled Car at Right
      const carX = w * 0.8;
      const carY = roadY + 12;
      ctx.fillStyle = '#e11d48';
      ctx.fillRect(carX, carY, 70, 40);
      // Hazard blinkers flashing
      const blink = Math.sin(this.animTime * 6) > 0;
      if (blink) {
        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(carX + 6, carY + 8, 4, 0, Math.PI * 2);
        ctx.arc(carX + 6, carY + 32, 4, 0, Math.PI * 2);
        ctx.fill();
      }

      // Warning Triangle at 50m distance (Left of car)
      const triX = w * 0.35;
      const triY = roadY + 20;

      // Draw red reflective triangle
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 5;
      ctx.beginPath();
      ctx.moveTo(triX, triY - 26);
      ctx.lineTo(triX - 16, triY + 8);
      ctx.lineTo(triX + 16, triY + 8);
      ctx.closePath();
      ctx.stroke();

      // Measurement line 50m
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([6, 6]);
      ctx.beginPath();
      ctx.moveTo(triX, roadY + 85);
      ctx.lineTo(carX, roadY + 85);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('مسافة لا تقل عن 50 متراً (Minimo 50m)', (triX + carX) / 2, roadY + 105);

      // Measurement line 100m (Visibility from incoming cars)
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([6, 6]);
      ctx.beginPath();
      ctx.moveTo(w * 0.05, roadY - 15);
      ctx.lineTo(triX, roadY - 15);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = '#10b981';
      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.fillText('مرئي من مسافة 100 متر على الأقل (Visibile a 100m)', (w * 0.05 + triX) / 2, roadY - 25);
    }
  }

  // Initialize on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      new WeatherHazardsStudio('weatherHazardsStudioContainer');
    });
  } else {
    new WeatherHazardsStudio('weatherHazardsStudioContainer');
  }
})();

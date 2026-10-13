/**
 * =======================================================================
 * Patente B Pro - Eco-Driving & Environmental Physics Studio (الباب 24)
 * =======================================================================
 * 60 FPS HTML5 Canvas Interactive Physics Simulator:
 * 1. Aerodynamics & Eco-Driving Wind Tunnel (الانسيابية الهوائية والقيادة الاقتصادية)
 * 2. Catalytic Converter Thermal Efficiency (علبة البيئة والمحول الحفاز)
 * 3. Diesel Particulate Filter (DPF) Soot & Regeneration (فلتر الجسيمات الدقيقة وتجديده)
 * =======================================================================
 */

class EcoDrivingStudio {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;

    this.activeTab = 'aero'; // 'aero' | 'catalizzatore' | 'dpf'
    this.animationId = null;
    this.lastTime = 0;

    // Aerodynamics & Eco-Driving State
    this.aero = {
      speed: 90, // km/h (50 | 90 | 130)
      roofBox: false, // portapacchi / portasci (+18%)
      windowsOpen: false, // finestrini aperti (+12%)
      lowTires: false, // pressione insufficiente (+9%)
      acEnabled: false, // climatizzatore (+11%)
      aggressiveDriving: false, // accelerazioni e frenate brusche (+28%)
      windParticles: [],
      roadOffset: 0,
      carX: 200,
      carY: 155,
      wheelAngle: 0,
      sootPuffs: []
    };

    // Catalytic Converter State
    this.cat = {
      engineState: 'hot', // 'cold' (<200°C) | 'hot' (>600°C)
      temp: 650, // Celsius
      gasParticles: [],
      conversionRate: 98 // %
    };

    // DPF State
    this.dpf = {
      mode: 'highway', // 'city' (clogging) | 'highway' (regenerating)
      sootLevel: 25, // % (0 - 100)
      temp: 620, // Celsius
      sootParticles: []
    };

    this.initAudio();
    this.renderLayout();
    this.initCanvas();
    this.bindEvents();
    this.startLoop();
  }

  initAudio() {
    this.audioCtx = null;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.audioCtx = new AudioCtx();
    } catch (e) {
      console.warn("Web Audio not supported", e);
    }
  }

  playChime(type) {
    if (!this.audioCtx) return;
    try {
      if (this.audioCtx.state === 'suspended') this.audioCtx.resume();
      const now = this.audioCtx.currentTime;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);

      if (type === 'eco-success') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(523.25, now);
        osc.frequency.exponentialRampToValueAtTime(659.25, now + 0.12);
        osc.frequency.exponentialRampToValueAtTime(783.99, now + 0.25);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
        osc.start(now);
        osc.stop(now + 0.35);
      } else if (type === 'drag-turb') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(140, now);
        osc.frequency.exponentialRampToValueAtTime(80, now + 0.15);
        gain.gain.setValueAtTime(0.05, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
        osc.start(now);
        osc.stop(now + 0.15);
      } else if (type === 'toggle') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.08);
        gain.gain.setValueAtTime(0.04, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
        osc.start(now);
        osc.stop(now + 0.08);
      }
    } catch (e) {
      console.warn(e);
    }
  }

  renderLayout() {
    this.container.innerHTML = `
      <div class="eco-studio-card">
        <!-- Studio Header & Tab Switcher -->
        <div class="eco-studio-header">
          <div class="eco-title-group">
            <div class="eco-badge-tag">مختبر الفيزياء البيئية وكود السير 2026</div>
            <h3 class="eco-main-title">المحاكي التفاعلي 60 FPS: ديناميكا مقاومة الهواء واستهلاك الوقود</h3>
          </div>
          <div class="eco-tabs-nav">
            <button class="eco-tab-btn active" data-tab="aero">
              <span class="tab-icon">🌪️</span>
              <span class="tab-label">نفق الرياح والقيادة الاقتصادية</span>
            </button>
            <button class="eco-tab-btn" data-tab="catalizzatore">
              <span class="tab-icon">🔥</span>
              <span class="tab-label">المحول الحفاز (Marmitta Catalitica)</span>
            </button>
            <button class="eco-tab-btn" data-tab="dpf">
              <span class="tab-icon">🛡️</span>
              <span class="tab-label">فلتر الديزل (Filtro DPF/FAP)</span>
            </button>
          </div>
        </div>

        <!-- Canvas Container -->
        <div class="eco-canvas-wrapper">
          <canvas id="ecoCanvas" width="900" height="320"></canvas>
          
          <!-- Live Telemetry Overlays for Aero Tab -->
          <div class="eco-telemetry-hud" id="hudAero">
            <div class="hud-stat-box">
              <span class="hud-stat-label">السرعة المحددة</span>
              <span class="hud-stat-val" id="hudSpeed">90 <small>km/h</small></span>
            </div>
            <div class="hud-stat-box highlight-amber">
              <span class="hud-stat-label">معدل الاستهلاك</span>
              <span class="hud-stat-val" id="hudConsumo">5.4 <small>L/100km</small></span>
            </div>
            <div class="hud-stat-box highlight-rose">
              <span class="hud-stat-label">انبعاث الكربون</span>
              <span class="hud-stat-val" id="hudCo2">128 <small>g CO₂/km</small></span>
            </div>
            <div class="hud-stat-box highlight-green" id="hudExtraBox">
              <span class="hud-stat-label">زيادة الاستهلاك</span>
              <span class="hud-stat-val" id="hudExtraPct">+0% <small>(مثالي)</small></span>
            </div>
          </div>

          <!-- Live Telemetry Overlays for Catalyst Tab -->
          <div class="eco-telemetry-hud" id="hudCat" style="display:none;">
            <div class="hud-stat-box">
              <span class="hud-stat-label">حرارة المحول</span>
              <span class="hud-stat-val" id="hudCatTemp">650 <small>°C</small></span>
            </div>
            <div class="hud-stat-box highlight-green">
              <span class="hud-stat-label">كفاءة التنقية</span>
              <span class="hud-stat-val" id="hudCatRate">98% <small>تحويل آمن</small></span>
            </div>
            <div class="hud-stat-box highlight-rose">
              <span class="hud-stat-label">الغازات المعالجة</span>
              <span class="hud-stat-val">CO, HC, NOₓ</span>
            </div>
            <div class="hud-stat-box">
              <span class="hud-stat-label">الغازات الناتجة</span>
              <span class="hud-stat-val" style="color:#38bdf8;">CO₂, H₂O, N₂</span>
            </div>
          </div>

          <!-- Live Telemetry Overlays for DPF Tab -->
          <div class="eco-telemetry-hud" id="hudDpf" style="display:none;">
            <div class="hud-stat-box">
              <span class="hud-stat-label">حرارة العادم</span>
              <span class="hud-stat-val" id="hudDpfTemp">620 <small>°C</small></span>
            </div>
            <div class="hud-stat-box highlight-amber">
              <span class="hud-stat-label">تراكم السناج</span>
              <span class="hud-stat-val" id="hudDpfSoot">25% <small>نظيف</small></span>
            </div>
            <div class="hud-stat-box highlight-green">
              <span class="hud-stat-label">حالة الفلتر</span>
              <span class="hud-stat-val" id="hudDpfState">تجديد ذاتي نشط</span>
            </div>
          </div>
        </div>

        <!-- Controls Toolbar: Aerodynamics & Eco-Driving -->
        <div class="eco-controls-panel" id="panelAero">
          <div class="ctrl-group">
            <span class="ctrl-label">🚗 سرعة السير:</span>
            <div class="ctrl-btn-row">
              <button class="eco-btn-opt" data-speed="50">50 كم/س (مدينة)</button>
              <button class="eco-btn-opt active" data-speed="90">90 كم/س (طريق سريع)</button>
              <button class="eco-btn-opt" data-speed="130">130 كم/س (أوتوستراد)</button>
            </div>
          </div>

          <div class="ctrl-group">
            <span class="ctrl-label">⚡ عوامل مقاومة السحب والهدر:</span>
            <div class="ctrl-btn-row">
              <button class="eco-btn-toggle" id="btnRoofBox" data-feature="roofBox">
                <span>📦</span> حامل أمتعة سقف (+18%)
              </button>
              <button class="eco-btn-toggle" id="btnWindows" data-feature="windowsOpen">
                <span>🪟</span> نوافذ مفتوحة (+12%)
              </button>
              <button class="eco-btn-toggle" id="btnTires" data-feature="lowTires">
                <span>🛞</span> ضغط إطارات منخفض (+9%)
              </button>
              <button class="eco-btn-toggle" id="btnAC" data-feature="acEnabled">
                <span>❄️</span> مكيف الهواء (+11%)
              </button>
              <button class="eco-btn-toggle" id="btnDriving" data-feature="aggressiveDriving">
                <span>🏎️</span> قيادة عنيفة بتسارع حاد (+28%)
              </button>
            </div>
          </div>
        </div>

        <!-- Controls Toolbar: Catalytic Converter -->
        <div class="eco-controls-panel" id="panelCat" style="display:none;">
          <div class="ctrl-group">
            <span class="ctrl-label">🌡️ درجة حرارة تشغيل المحول الحفاز:</span>
            <div class="ctrl-btn-row">
              <button class="eco-btn-opt" data-cat="cold">❄️ تشغيل بارد (< 200°C) - انعدام الفاعلية</button>
              <button class="eco-btn-opt active" data-cat="hot">🔥 حرارة مثالية (> 600°C) - تنقية تامة</button>
            </div>
          </div>
          <div class="cat-explanation-pill">
            💡 <strong>قاعدة وزارية حاسمة:</strong> المحول الحفاز لا ينقي الغازات في الدقائق الأولى بعد تشغيل المحرك؛ ويحتاج لحرارة هائلة ليبدأ التفاعل الكيميائي.
          </div>
        </div>

        <!-- Controls Toolbar: DPF Diesel Filter -->
        <div class="eco-controls-panel" id="panelDpf" style="display:none;">
          <div class="ctrl-group">
            <span class="ctrl-label">🛣️ نمط القيادة ومسار السيارة:</span>
            <div class="ctrl-btn-row">
              <button class="eco-btn-opt" data-dpf="city">🏙️ مشاوير قصيرة بالمدينة (انسداد بالسناج)</button>
              <button class="eco-btn-opt active" data-dpf="highway">🛣️ سفر على طريق سريع (تجديد ذاتي وحرق السناج)</button>
            </div>
          </div>
          <div class="cat-explanation-pill">
            💡 <strong>فخ الامتحان الوزاري:</strong> إذا أضاءت لمبة DPF، يجب قيادة السيارة على الأوتوستراد لعدة كيلومترات لإتمام عملية التجديد (Rigenerazione).
          </div>
        </div>

        <!-- Educational Insight Banner -->
        <div class="eco-insight-bar" id="ecoInsightBar">
          <span class="insight-icon">🌱</span>
          <span class="insight-text" id="ecoInsightText">
            <strong>الوضع المثالي:</strong> القيادة الاقتصادية السلسة مع إغلاق النوافذ بالسرعات العالية وضبط ضغط الإطارات توفر ما يصل إلى 40% من الوقود سنوياً.
          </span>
        </div>
      </div>
    `;
  }

  initCanvas() {
    this.canvas = document.getElementById('ecoCanvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    // Create initial wind particles
    this.aero.windParticles = [];
    for (let i = 0; i < 45; i++) {
      this.aero.windParticles.push({
        x: Math.random() * 900,
        y: Math.random() * 260,
        speed: 8 + Math.random() * 8,
        length: 20 + Math.random() * 30,
        opacity: 0.2 + Math.random() * 0.5,
        turbulent: false
      });
    }

    // Initialize gas particles for Catalyst & DPF
    this.cat.gasParticles = [];
    for (let i = 0; i < 50; i++) {
      this.cat.gasParticles.push({
        x: 100 + Math.random() * 600,
        y: 150 + (Math.random() - 0.5) * 24,
        speed: 3 + Math.random() * 3,
        type: Math.random() > 0.4 ? 'toxic' : 'clean'
      });
    }
  }

  bindEvents() {
    // Tab switching
    const tabBtns = this.container.querySelectorAll('.eco-tab-btn');
    tabBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const target = btn.dataset.tab;
        this.activeTab = target;
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Toggle HUDs
        document.getElementById('hudAero').style.display = target === 'aero' ? 'flex' : 'none';
        document.getElementById('hudCat').style.display = target === 'catalizzatore' ? 'flex' : 'none';
        document.getElementById('hudDpf').style.display = target === 'dpf' ? 'flex' : 'none';

        // Toggle Panels
        document.getElementById('panelAero').style.display = target === 'aero' ? 'flex' : 'none';
        document.getElementById('panelCat').style.display = target === 'catalizzatore' ? 'flex' : 'none';
        document.getElementById('panelDpf').style.display = target === 'dpf' ? 'flex' : 'none';

        this.playChime('toggle');
        this.updateInsight();
      });
    });

    // Speed buttons (Aero Tab)
    const speedBtns = this.container.querySelectorAll('[data-speed]');
    speedBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        speedBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.aero.speed = parseInt(btn.dataset.speed, 10);
        this.playChime('toggle');
        this.updateAeroMetrics();
      });
    });

    // Feature Toggles (Aero Tab)
    const toggleBtns = this.container.querySelectorAll('.eco-btn-toggle');
    toggleBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const feat = btn.dataset.feature;
        this.aero[feat] = !this.aero[feat];
        btn.classList.toggle('active', this.aero[feat]);
        if (this.aero[feat]) {
          this.playChime('drag-turb');
        } else {
          this.playChime('eco-success');
        }
        this.updateAeroMetrics();
      });
    });

    // Catalyst mode buttons
    const catBtns = this.container.querySelectorAll('[data-cat]');
    catBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        catBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.cat.engineState = btn.dataset.cat;
        if (this.cat.engineState === 'hot') {
          this.cat.temp = 650;
          this.cat.conversionRate = 98;
          this.playChime('eco-success');
        } else {
          this.cat.temp = 140;
          this.cat.conversionRate = 18;
          this.playChime('drag-turb');
        }
        document.getElementById('hudCatTemp').innerHTML = `${this.cat.temp} <small>°C</small>`;
        document.getElementById('hudCatRate').innerHTML = `${this.cat.conversionRate}% <small>${this.cat.engineState === 'hot' ? 'تحويل آمن' : 'تلوث مرتفع'}</small>`;
      });
    });

    // DPF mode buttons
    const dpfBtns = this.container.querySelectorAll('[data-dpf]');
    dpfBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        dpfBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.dpf.mode = btn.dataset.dpf;
        if (this.dpf.mode === 'highway') {
          this.dpf.sootLevel = 15;
          this.dpf.temp = 620;
          document.getElementById('hudDpfState').innerText = "تجديد ذاتي نشط (حرق السناج)";
          this.playChime('eco-success');
        } else {
          this.dpf.sootLevel = 88;
          this.dpf.temp = 220;
          document.getElementById('hudDpfState').innerText = "تحذير: انسداد الفلتر بالسناج!";
          this.playChime('drag-turb');
        }
        document.getElementById('hudDpfTemp').innerHTML = `${this.dpf.temp} <small>°C</small>`;
        document.getElementById('hudDpfSoot').innerHTML = `${this.dpf.sootLevel}% <small>${this.dpf.mode === 'highway' ? 'نظيف' : 'مسدود'}</small>`;
      });
    });
  }

  updateAeroMetrics() {
    // Base consumption at speed
    let baseLiters = 4.0;
    if (this.aero.speed === 90) baseLiters = 5.2;
    if (this.aero.speed === 130) baseLiters = 7.1;

    let extraPct = 0;
    if (this.aero.roofBox) extraPct += 18;
    if (this.aero.windowsOpen) {
      extraPct += this.aero.speed === 130 ? 15 : (this.aero.speed === 90 ? 10 : 4);
    }
    if (this.aero.lowTires) extraPct += 9;
    if (this.aero.acEnabled) extraPct += 11;
    if (this.aero.aggressiveDriving) extraPct += 28;

    const totalLiters = (baseLiters * (1 + extraPct / 100)).toFixed(1);
    const co2Grams = Math.round(totalLiters * 23.8); // ~23.8 g CO2 per 0.1L fuel

    document.getElementById('hudSpeed').innerHTML = `${this.aero.speed} <small>km/h</small>`;
    document.getElementById('hudConsumo').innerHTML = `${totalLiters} <small>L/100km</small>`;
    document.getElementById('hudCo2').innerHTML = `${co2Grams} <small>g CO₂/km</small>`;
    
    const extraHud = document.getElementById('hudExtraPct');
    const extraBox = document.getElementById('hudExtraBox');
    if (extraPct === 0) {
      extraHud.innerHTML = `+0% <small>(مثالي)</small>`;
      extraBox.className = 'hud-stat-box highlight-green';
    } else if (extraPct <= 25) {
      extraHud.innerHTML = `+${extraPct}% <small>(معتدل)</small>`;
      extraBox.className = 'hud-stat-box highlight-amber';
    } else {
      extraHud.innerHTML = `+${extraPct}% <small>(هدر فادح)</small>`;
      extraBox.className = 'hud-stat-box highlight-rose';
    }

    this.updateInsight();
  }

  updateInsight() {
    const textEl = document.getElementById('ecoInsightText');
    if (!textEl) return;

    if (this.activeTab === 'aero') {
      if (this.aero.roofBox) {
        textEl.innerHTML = `<strong>فخ الامتحان الوزاري:</strong> حامل الأمتعة على السقف (Portapacchi) يزيد مقاومة الهواء والاستهلاك حتى لو كان فارغاً (Anche se scarico)! يجب فكه فور انتهاء الحاجة إليه.`;
      } else if (this.aero.windowsOpen && this.aero.speed === 130) {
        textEl.innerHTML = `<strong>مقاومة الهواء والنوافذ:</strong> فتح النوافذ بالسرعات العالية على الأوتوستراد يحدث دوامات هوائية ترفع الاستهلاك أكثر من تشغيل مكيف الهواء نفسه!`;
      } else if (this.aero.lowTires) {
        textEl.innerHTML = `<strong>ضغط الإطارات:</strong> القيادة بضغط منخفض تزيد مساحة احتكاك الإطار ومقاومة الدوران (Resistenza al rotolamento) وتهدر الوقود وتتلف الإطار.`;
      } else if (this.aero.aggressiveDriving) {
        textEl.innerHTML = `<strong>القيادة العنيفة:</strong> التسارع المفاجئ والفرملة المتعاقبة ترفع استهلاك الوقود والانبعاثات بنسبة تتجاوز 30%؛ والتعشيق المبكر للغيارات العالية (Marce alte) يوفر الوقود.`;
      } else {
        textEl.innerHTML = `<strong>الوضع المثالي:</strong> انسيابية هوائية نظيفة، إطارات مضبوطة، وقيادة سلسة بالغيارات العالية مع التباطؤ برفع القدم (Cut-off) تحقق أقل انبعاثات وأعلى توفير.`;
      }
    } else if (this.activeTab === 'catalizzatore') {
      textEl.innerHTML = `<strong>المحول الحفاز (Marmitta catalitica):</strong> يعتمد على حرارة فائقة (>600°C) لتحويل غازات CO و HC و NOₓ إلى غازات غير ضارة. وتجنب ركن السيارة فوق الأعشاب الجافة لتفادي الحرائق.`;
    } else if (this.activeTab === 'dpf') {
      textEl.innerHTML = `<strong>فلتر الجسيمات الدقيقة (DPF):</strong> يحجز السناج والدخان الأسود بمحركات الديزل؛ ويحتاج للسير على الطرق السريعة لإتمام دورة التنظيف الذاتي (Rigenerazione).`;
    }
  }

  startLoop() {
    const loop = (timestamp) => {
      const dt = (timestamp - this.lastTime) / 1000;
      this.lastTime = timestamp;

      this.update(dt || 0.016);
      this.draw();

      this.animationId = requestAnimationFrame(loop);
    };
    this.animationId = requestAnimationFrame(loop);
  }

  update(dt) {
    if (this.activeTab === 'aero') {
      const speedMultiplier = this.aero.speed / 50;
      this.aero.roadOffset = (this.aero.roadOffset + 380 * speedMultiplier * dt) % 120;
      this.aero.wheelAngle += 15 * speedMultiplier * dt;

      // Update wind particles
      for (let p of this.aero.windParticles) {
        p.x -= p.speed * speedMultiplier * 1.6;
        if (p.x < -40) {
          p.x = 940;
          p.y = 80 + Math.random() * 160;
          p.turbulent = false;
        }

        // Deflect wind over car
        const cx = this.aero.carX;
        const cy = this.aero.carY;
        if (p.x > cx - 60 && p.x < cx + 220) {
          // Flow over hood & roof
          if (p.y > cy - 35 && p.y < cy + 45) {
            if (this.aero.roofBox && p.x > cx + 30 && p.x < cx + 160) {
              p.y -= 18 * dt * 60; // push over roof box
              p.turbulent = true;
            } else {
              p.y -= 8 * dt * 60;
            }
          }
        }

        // Create turbulent swirling behind car
        if (p.x > cx + 200 && p.x < cx + 450) {
          if (this.aero.roofBox || this.aero.windowsOpen) {
            p.y += Math.sin(p.x * 0.08) * 3.5;
            p.turbulent = true;
          }
        }
      }

      // Aggressive driving soot puffs
      if (this.aero.aggressiveDriving) {
        if (Math.random() < 0.25) {
          this.aero.sootPuffs.push({
            x: this.aero.carX + 195,
            y: this.aero.carY + 38,
            radius: 5,
            opacity: 0.8,
            vx: 2 + Math.random() * 3,
            vy: (Math.random() - 0.5) * 1.5
          });
        }
      }
      for (let s of this.aero.sootPuffs) {
        s.x += s.vx;
        s.y += s.vy;
        s.radius += 0.4;
        s.opacity -= 0.015;
      }
      this.aero.sootPuffs = this.aero.sootPuffs.filter(s => s.opacity > 0);

    } else if (this.activeTab === 'catalizzatore') {
      // Move catalyst gas particles
      for (let p of this.cat.gasParticles) {
        p.x += p.speed;
        if (p.x > 840) {
          p.x = 80;
          p.y = 155 + (Math.random() - 0.5) * 22;
          p.type = 'toxic';
        }
        // Conversion inside catalytic monolith (x: 420 to 560)
        if (p.x > 480 && p.type === 'toxic') {
          if (this.cat.engineState === 'hot') {
            if (Math.random() < 0.95) p.type = 'clean';
          } else {
            // Cold engine barely converts
            if (Math.random() < 0.20) p.type = 'clean';
          }
        }
      }
    } else if (this.activeTab === 'dpf') {
      // DPF soot accumulation / burnoff
      for (let p of this.cat.gasParticles) {
        p.x += p.speed;
        if (p.x > 840) {
          p.x = 80;
          p.y = 155 + (Math.random() - 0.5) * 22;
          p.type = 'soot';
        }
      }
    }
  }

  draw() {
    this.ctx.clearRect(0, 0, 900, 320);

    if (this.activeTab === 'aero') {
      this.drawAeroScene();
    } else if (this.activeTab === 'catalizzatore') {
      this.drawCatalystScene();
    } else if (this.activeTab === 'dpf') {
      this.drawDpfScene();
    }
  }

  drawAeroScene() {
    const ctx = this.ctx;

    // 1. Sky & Road Background
    const bgGrad = ctx.createLinearGradient(0, 0, 0, 320);
    bgGrad.addColorStop(0, '#060a12');
    bgGrad.addColorStop(0.65, '#0b1324');
    bgGrad.addColorStop(0.66, '#151f33');
    bgGrad.addColorStop(1, '#0d1522');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, 900, 320);

    // 2. Road surface (y: 200 to 320)
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 205, 900, 115);

    // Road dashed center line
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
    ctx.lineWidth = 4;
    ctx.setLineDash([40, 40]);
    ctx.lineDashOffset = -this.aero.roadOffset;
    ctx.beginPath();
    ctx.moveTo(0, 260);
    ctx.lineTo(900, 260);
    ctx.stroke();
    ctx.setLineDash([]); // reset

    // Ground kerb / guardrail line
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, 205);
    ctx.lineTo(900, 205);
    ctx.stroke();

    // 3. Wind Streamlines
    for (let p of this.aero.windParticles) {
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(p.x + p.length, p.y);
      if (p.turbulent) {
        ctx.strokeStyle = 'rgba(244, 63, 94, 0.65)'; // red/pink turbulence
        ctx.lineWidth = 2.5;
      } else {
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)'; // cyan smooth stream
        ctx.lineWidth = 1.6;
      }
      ctx.stroke();
    }

    // 4. Draw Vehicle (Modern Aerodynamic Car Profile)
    const cx = this.aero.carX;
    const cy = this.aero.carY;

    ctx.save();

    // Car Body Shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.65)';
    ctx.beginPath();
    ctx.ellipse(cx + 85, cy + 48, 115, 12, 0, 0, Math.PI * 2);
    ctx.fill();

    // Car Main Body (Metallic Cobalt Blue)
    const carGrad = ctx.createLinearGradient(cx, cy - 25, cx, cy + 45);
    carGrad.addColorStop(0, '#38bdf8');
    carGrad.addColorStop(0.3, '#0284c7');
    carGrad.addColorStop(1, '#075985');
    ctx.fillStyle = carGrad;

    ctx.beginPath();
    // Front bumper
    ctx.moveTo(cx - 30, cy + 35);
    ctx.lineTo(cx - 38, cy + 28);
    ctx.quadraticCurveTo(cx - 35, cy + 12, cx - 15, cy + 10); // hood curve
    ctx.lineTo(cx + 25, cy + 8); // hood top
    ctx.quadraticCurveTo(cx + 45, cy - 18, cx + 75, cy - 20); // windshield slope
    ctx.lineTo(cx + 145, cy - 20); // roof line
    ctx.quadraticCurveTo(cx + 175, cy - 10, cx + 195, cy + 15); // rear slope
    ctx.lineTo(cx + 205, cy + 35); // rear bumper
    ctx.lineTo(cx + 175, cy + 35); // rear wheel arch right
    ctx.arc(cx + 155, cy + 35, 22, 0, Math.PI, true); // rear wheel arch
    ctx.lineTo(cx + 40, cy + 35); // rocker panel
    ctx.arc(cx + 18, cy + 35, 22, 0, Math.PI, true); // front wheel arch
    ctx.lineTo(cx - 30, cy + 35);
    ctx.closePath();
    ctx.fill();

    // Subtle edge highlight
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Windows (Glass)
    ctx.fillStyle = '#0f172a';
    ctx.beginPath();
    ctx.moveTo(cx + 48, cy + 6);
    ctx.lineTo(cx + 73, cy - 16);
    ctx.lineTo(cx + 105, cy - 16);
    ctx.lineTo(cx + 105, cy + 6);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(cx + 110, cy + 6);
    ctx.lineTo(cx + 110, cy - 16);
    ctx.lineTo(cx + 142, cy - 16);
    ctx.lineTo(cx + 168, cy + 6);
    ctx.closePath();
    ctx.fill();

    // If Windows are open: draw open window gap and cabin turbulent vortex
    if (this.aero.windowsOpen) {
      ctx.fillStyle = 'rgba(244, 63, 94, 0.4)';
      ctx.fillRect(cx + 52, cy - 6, 48, 10);
      ctx.fillRect(cx + 112, cy - 6, 48, 10);

      // Cabin turbulence indicator
      ctx.strokeStyle = '#f43f5e';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(cx + 80, cy, 12, 0, Math.PI * 1.5);
      ctx.stroke();
    }

    // Headlight & Taillight
    ctx.fillStyle = '#fef08a';
    ctx.beginPath();
    ctx.ellipse(cx - 32, cy + 18, 5, 8, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ef4444';
    ctx.beginPath();
    ctx.ellipse(cx + 203, cy + 20, 4, 7, 0, 0, Math.PI * 2);
    ctx.fill();

    // 5. Roof Cargo Box (Portapacchi / Portasci)
    if (this.aero.roofBox) {
      // Roof cross bars
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(cx + 80, cy - 20);
      ctx.lineTo(cx + 80, cy - 26);
      ctx.moveTo(cx + 140, cy - 20);
      ctx.lineTo(cx + 140, cy - 26);
      ctx.stroke();

      // Sleek cargo box
      const boxGrad = ctx.createLinearGradient(cx + 60, cy - 44, cx + 160, cy - 24);
      boxGrad.addColorStop(0, '#0f172a');
      boxGrad.addColorStop(0.5, '#334155');
      boxGrad.addColorStop(1, '#0f172a');
      ctx.fillStyle = boxGrad;
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 1.5;

      ctx.beginPath();
      ctx.roundRect(cx + 60, cy - 42, 105, 18, [8, 14, 6, 6]);
      ctx.fill();
      ctx.stroke();

      // Tag on roof box
      ctx.fillStyle = '#f59e0b';
      ctx.font = 'bold 9px monospace';
      ctx.fillText('PORTAPACCHI +18%', cx + 70, cy - 30);
    }

    // 6. Wheels (Front & Rear)
    this.drawWheel(cx + 18, cy + 35, this.aero.wheelAngle, this.aero.lowTires);
    this.drawWheel(cx + 155, cy + 35, this.aero.wheelAngle, this.aero.lowTires);

    // 7. A/C Compressor Indicator under hood
    if (this.aero.acEnabled) {
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText('❄️ A/C (+11%)', cx - 15, cy - 8);
    }

    ctx.restore();

    // 8. Draw Soot Puffs for aggressive driving
    for (let s of this.aero.sootPuffs) {
      ctx.fillStyle = `rgba(15, 23, 42, ${s.opacity})`;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  drawWheel(wx, wy, angle, isLowPressure) {
    const ctx = this.ctx;
    ctx.save();
    ctx.translate(wx, wy);

    // Tire Outer Rubber
    ctx.fillStyle = '#0f172a';
    ctx.beginPath();
    if (isLowPressure) {
      // Bulging, squashed contact patch at bottom
      ctx.ellipse(0, 2, 19, 16.5, 0, 0, Math.PI * 2);
    } else {
      ctx.arc(0, 0, 18, 0, Math.PI * 2);
    }
    ctx.fill();
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Alloy Rim
    ctx.fillStyle = '#64748b';
    ctx.beginPath();
    ctx.arc(0, 0, 11, 0, Math.PI * 2);
    ctx.fill();

    // Spokes (spinning)
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 2;
    for (let i = 0; i < 5; i++) {
      const a = angle + (i * Math.PI * 2) / 5;
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(Math.cos(a) * 10, Math.sin(a) * 10);
      ctx.stroke();
    }

    // Heat friction glow if under-inflated
    if (isLowPressure) {
      ctx.strokeStyle = '#f43f5e';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(0, 14, 10, 0.2, Math.PI - 0.2);
      ctx.stroke();
    }

    ctx.restore();
  }

  drawCatalystScene() {
    const ctx = this.ctx;

    // Dark technical workbench background
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, 900, 320);

    // Exhaust Pipe System
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 32;
    ctx.lineCap = 'round';

    ctx.beginPath();
    // Engine manifold entry
    ctx.moveTo(80, 160);
    ctx.lineTo(360, 160);
    ctx.stroke();

    ctx.beginPath();
    // Exit pipe to silencer
    ctx.moveTo(560, 160);
    ctx.lineTo(840, 160);
    ctx.stroke();

    // Engine Block Indicator (Left)
    ctx.fillStyle = '#1e293b';
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(30, 100, 90, 120, 8);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('محرك السيارة', 75, 145);
    ctx.font = '10px monospace';
    ctx.fillStyle = '#94a3b8';
    ctx.fillText('(Motore)', 75, 165);

    // Catalytic Converter Chamber (Center: x 360 to 560)
    const isHot = this.cat.engineState === 'hot';
    const catGrad = ctx.createLinearGradient(360, 110, 560, 210);
    if (isHot) {
      catGrad.addColorStop(0, '#f97316');
      catGrad.addColorStop(0.5, '#ef4444');
      catGrad.addColorStop(1, '#ea580c');
    } else {
      catGrad.addColorStop(0, '#334155');
      catGrad.addColorStop(1, '#1e293b');
    }

    // Outer Chamber
    ctx.fillStyle = catGrad;
    ctx.strokeStyle = isHot ? '#f59e0b' : '#64748b';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.roundRect(360, 110, 200, 100, 16);
    ctx.fill();
    ctx.stroke();

    // Honeycomb Ceramic Monolith grid
    ctx.strokeStyle = isHot ? 'rgba(254, 240, 138, 0.45)' : 'rgba(255, 255, 255, 0.15)';
    ctx.lineWidth = 1;
    for (let x = 385; x < 540; x += 12) {
      ctx.beginPath();
      ctx.moveTo(x, 120);
      ctx.lineTo(x, 200);
      ctx.stroke();
    }

    // Heat glow effect if hot
    if (isHot) {
      ctx.fillStyle = 'rgba(239, 68, 68, 0.18)';
      ctx.beginPath();
      ctx.arc(460, 160, 95, 0, Math.PI * 2);
      ctx.fill();
    }

    // Labels
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 13px sans-serif';
    ctx.fillText('المحول الحفاز (Marmitta Catalitica)', 460, 95);

    // Thermal sensor indicator
    ctx.fillStyle = isHot ? '#ef4444' : '#38bdf8';
    ctx.font = 'bold 11px monospace';
    ctx.fillText(`درجة الحرارة: ${this.cat.temp}°C (${isHot ? 'فعال 98%' : 'بارد وغير فعال 18%'})`, 460, 230);

    // Flow particles
    for (let p of this.cat.gasParticles) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      if (p.type === 'toxic') {
        ctx.fillStyle = '#ef4444'; // Toxic CO / NOx
      } else {
        ctx.fillStyle = '#38bdf8'; // Clean H2O / CO2 / N2
      }
      ctx.fill();
    }

    // Legend at bottom
    ctx.textAlign = 'left';
    ctx.fillStyle = '#ef4444';
    ctx.beginPath();
    ctx.arc(220, 280, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#e2e8f0';
    ctx.font = '11px sans-serif';
    ctx.fillText('غازات سامة داخلة (CO, HC, NOₓ)', 235, 284);

    ctx.fillStyle = '#38bdf8';
    ctx.beginPath();
    ctx.arc(580, 280, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#e2e8f0';
    ctx.fillText('غازات آمنة خارجة (CO₂, H₂O, N₂)', 595, 284);
  }

  drawDpfScene() {
    const ctx = this.ctx;

    // Dark workshop background
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, 900, 320);

    // Exhaust Pipe
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 34;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(80, 160);
    ctx.lineTo(350, 160);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(560, 160);
    ctx.lineTo(840, 160);
    ctx.stroke();

    // DPF Steel Canister (Center: x 350 to 560)
    const isHighway = this.dpf.mode === 'highway';
    ctx.fillStyle = isHighway ? '#ea580c' : '#1e293b';
    ctx.strokeStyle = isHighway ? '#f59e0b' : '#64748b';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.roundRect(350, 105, 210, 110, 18);
    ctx.fill();
    ctx.stroke();

    // Ceramic Porous Walls (Alternating plugged channels)
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 2;
    for (let y = 120; y < 205; y += 14) {
      ctx.beginPath();
      ctx.moveTo(370, y);
      ctx.lineTo(540, y);
      ctx.stroke();
    }

    // Soot level accumulation inside filter
    const sootAlpha = this.dpf.sootLevel / 100;
    ctx.fillStyle = `rgba(0, 0, 0, ${sootAlpha * 0.9})`;
    ctx.beginPath();
    ctx.roundRect(380, 118, 150, 84, 8);
    ctx.fill();

    // High temp burning particles if regenerating
    if (isHighway) {
      ctx.fillStyle = '#fbbf24';
      for (let i = 0; i < 20; i++) {
        const sx = 390 + Math.random() * 130;
        const sy = 125 + Math.random() * 70;
        ctx.beginPath();
        ctx.arc(sx, sy, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Labels & Status
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('فلتر الجسيمات الدقيقة للديزل (Filtro Antiparticolato DPF)', 455, 88);

    ctx.font = 'bold 12px monospace';
    if (isHighway) {
      ctx.fillStyle = '#34d399';
      ctx.fillText('حالة التشغيل: تجديد ذاتي نشط (Rigenerazione in corso) - احتراق السناج عند 620°C', 455, 240);
    } else {
      ctx.fillStyle = '#f43f5e';
      ctx.fillText('حالة التشغيل: مشاوير قصيرة بالمدينة - تراكم السناج وانسداد الفلتر (Intasamento)', 455, 240);
    }
  }
}

// Global initialization
window.EcoDrivingStudio = EcoDrivingStudio;
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('ecoStudioContainer')) {
    window.ecoStudio = new EcoDrivingStudio('ecoStudioContainer');
  }
});

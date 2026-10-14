/**
 * Patente B Pro - Chapter 8: Interactive Direction & Information Signs Studio (60 FPS)
 * استوديو إشارات الإرشاد والمعلومات وتفكيك شفرات الألوان الستة للباب الثامن
 * Architecture: Modular Canvas Engine, Web Audio API Sound Generator, 60 FPS requestAnimationFrame
 */

(function () {
  'use strict';

  // Web Audio Sound Engine
  class IndicazioneAudioEngine {
    constructor() {
      this.ctx = null;
    }

    init() {
      if (!this.ctx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) {
          this.ctx = new AudioContext();
        }
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
    }

    playClick() {
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(350, this.ctx.currentTime + 0.05);
      gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.05);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.05);
    }

    playChime() {
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(523.25, this.ctx.currentTime); // C5
      osc.frequency.setValueAtTime(659.25, this.ctx.currentTime + 0.08); // E5
      osc.frequency.setValueAtTime(783.99, this.ctx.currentTime + 0.16); // G5
      gain.gain.setValueAtTime(0.14, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.35);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.35);
    }
  }

  // Main Indicazione Signs Studio
  class IndicazioneStudio {
    constructor() {
      this.canvas = document.getElementById('indicazioneStudioCanvas');
      if (!this.canvas) return;
      this.ctx = this.canvas.getContext('2d');
      this.audio = new IndicazioneAudioEngine();
      this.currentTab = 'colori'; // 'colori' | 'centro' | 'preselezione'

      // Mode 1: Color Codes State
      this.currentColor = 'verde'; // 'verde' | 'blu' | 'bianco' | 'giallo' | 'marrone' | 'nero'
      this.carX = 40;
      this.carSpeed = 2.8;

      // Mode 2: Centro Abitato State
      this.isEnteringTown = true; // true: Inizio, false: Fine
      this.townCarX = 60;
      this.townSpeed = 90; // Animated speed gauge

      // Mode 3: Preselezione State
      this.chosenLane = 'center'; // 'left' | 'center' | 'exit'
      this.preCarX = 40;
      this.preCarY = 220;

      this.initDPI();
      this.bindEvents();
      this.startLoop();
    }

    initDPI() {
      const dpr = window.devicePixelRatio || 1;
      const rect = this.canvas.getBoundingClientRect();
      const width = rect.width || 800;
      const height = 380;
      this.canvas.width = width * dpr;
      this.canvas.height = height * dpr;
      this.ctx.scale(dpr, dpr);
      this.width = width;
      this.height = height;
    }

    bindEvents() {
      // Tab switcher
      const tabBtns = document.querySelectorAll('.indicazione-tab-btn');
      tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          tabBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          this.currentTab = btn.getAttribute('data-tab');
          this.updateControlPanels();
        });
      });

      // Color switcher
      const colorBtns = document.querySelectorAll('.color-code-btn');
      colorBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          this.audio.init();
          this.audio.playChime();
          colorBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          this.currentColor = btn.getAttribute('data-color');
          this.updateColorInfo();
        });
      });

      // Inizio / Fine Centro Abitato toggle
      const btnInizioTown = document.getElementById('btnInizioTown');
      const btnFineTown = document.getElementById('btnFineTown');
      if (btnInizioTown && btnFineTown) {
        btnInizioTown.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.isEnteringTown = true;
          btnInizioTown.classList.add('active');
          btnFineTown.classList.remove('active');
          this.townCarX = 40;
          this.updateTownInfo();
        });
        btnFineTown.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.isEnteringTown = false;
          btnFineTown.classList.add('active');
          btnInizioTown.classList.remove('active');
          this.townCarX = 40;
          this.updateTownInfo();
        });
      }

      // Preselezione Lane Chooser
      const preBtns = document.querySelectorAll('.pre-lane-btn');
      preBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          preBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          this.chosenLane = btn.getAttribute('data-lane');
          this.preCarX = 40;
          this.updatePreselezioneInfo();
        });
      });

      window.addEventListener('resize', () => {
        this.initDPI();
      });
    }

    updateControlPanels() {
      const pColori = document.getElementById('controlsColori');
      const pCentro = document.getElementById('controlsCentro');
      const pPre = document.getElementById('controlsPreselezione');
      if (pColori) pColori.style.display = this.currentTab === 'colori' ? 'block' : 'none';
      if (pCentro) pCentro.style.display = this.currentTab === 'centro' ? 'block' : 'none';
      if (pPre) pPre.style.display = this.currentTab === 'preselezione' ? 'block' : 'none';
    }

    updateColorInfo() {
      const box = document.getElementById('colorInfoBox');
      if (!box) return;
      const dict = {
        verde: {
          title: '🟢 اللون الأخضر (VERDE): الطرق السريعة (Autostrade)',
          rules: 'السرعة القصوى: 130 كم/س | إلزامية إشعال أضواء التقاطع (Anabbaglianti) نهاراً وليلاً | حظر الدراجات الصغيرة والمشاة وحيوانات الجر.',
          sign: 'مثال: لافتات مداخل ومخارج الأوتوستراد (A1, A14) ومسافات المدن الكبرى (Milano, Bologna).'
        },
        blu: {
          title: '🔵 اللون الأزرق (BLU): الطرق الخارجية (Strade Extraurbane)',
          rules: 'السرعة القصوى: 110 كم/س (للطرق الرئيسية Principali) و 90 كم/س (للطرق الثانوية Secondarie) | أضواء التقاطع إجبارية نهاراً خارج المدينة.',
          sign: 'مثال: لافتات التقاطعات ومسافات الطرق الحكومية والإقليمية (SS 16, SP).'
        },
        bianco: {
          title: '⚪ اللون الأبيض (BIANCO): الطرق الحضرية والمعالم المحلية (Strade Urbane)',
          rules: 'السرعة القصوى: 50 كم/س | حظر استخدام المنبه الصوتي (الكلاكس) إلا في حالات الضرورة القصوى لتفادي حادث وشيك.',
          sign: 'مثال: لافتة مدخل المدينة [ ROMA ]، المستشفيات (Pronto Soccorso)، المدافن، ومحطات القطار.'
        },
        giallo: {
          title: '🟡 اللون الأصفر (GIALLO): ورش العمل والتحويلات المؤقتة (Cantieri Stradali)',
          rules: 'إشارات مؤقتة تلغي وتسبق الإشارات الثابتة الدائمة | تتطلب تخفيضاً فورياً للسرعة ومضاعفة مسافة الأمان.',
          sign: 'مثال: لافتات تحويل مسار السير (Deviazione) وإغلاق الحارات المؤقت.'
        },
        marrone: {
          title: '🟤 اللون البني (MARRONE): المعالم السياحية والتاريخية والحدائق (Mete Turistiche)',
          rules: 'ترشد السائقين نحو المتاحف، الآثار، الكنائس القديمة، المحميات الطبيعية، والحدائق الوطنية الإيطالية.',
          sign: 'مثال: [ PARCO NAZIONALE ABRUZZO ] أو [ SCAVI DI POMPEI ].'
        },
        nero: {
          title: '⚫ اللون الأسود أو الرمادي (NERO/GRIGIO): المناطق الصناعية والتجارية',
          rules: 'خلفية بيضاء مع كتابة أو رمز أسود/رمادي يوجه نحو المناطق الحرفية والمستودعات والمصانع ومناطق الشحن.',
          sign: 'مثال: [ ZONA INDUSTRIALE ] أو [ CENTRO COMMERCIALE ].'
        }
      };
      const info = dict[this.currentColor] || dict.verde;
      box.innerHTML = `
        <div class="indicazione-status-card" style="border-right: 4px solid var(--sky-primary);">
          <h4 style="color:#f8fafc; font-size:1.05rem; margin-bottom:6px;">${info.title}</h4>
          <p style="color:#cbd5e1; margin-bottom:6px;"><strong>القواعد الإلزامية:</strong> ${info.rules}</p>
          <p style="color:#94a3b8; font-size:0.88rem;"><strong>اللافتات التطبيقية:</strong> ${info.sign}</p>
        </div>
      `;
    }

    updateTownInfo() {
      const box = document.getElementById('townInfoBox');
      if (!box) return;
      if (this.isEnteringTown) {
        box.innerHTML = `
          <div class="indicazione-status-card" style="border-right: 4px solid #10b981;">
            <h4 style="color:#a7f3d0;">🏡 بداية التجمع السكني (Inizio Centro Abitato - [ ROMA ])</h4>
            <p><strong>الآثار القانونية الفورية:</strong> ينخفض الحد الأقصى للسرعة تلقائياً إلى <strong>50 كم/س</strong>، ويُمنع تماماً استخدام آلة التنبيه الصوتي (الكلاكس)، وتضاء أضواء التقاطع ليلاً.</p>
            <div style="color:#fca5a5; font-size:0.86rem; margin-top:4px;">⚠️ فخ الامتحان: القول بأن السرعة تصبح 70 كم/س تلقائياً هو FALSO (هي 50 كم/س ما لم تنص إشارة أخرى).</div>
          </div>
        `;
      } else {
        box.innerHTML = `
          <div class="indicazione-status-card" style="border-right: 4px solid #f43f5e;">
            <h4 style="color:#fecdd3;">🛣️ نهاية التجمع السكني (Fine Centro Abitato - [ ROMA مشطوبة بأحمر ])</h4>
            <p><strong>الآثار القانونية الفورية:</strong> ترتفع السرعة القانونية إلى <strong>90 كم/س</strong> (على الطرق الثانوية)، ويصبح استخدام المنبه الصوتي مباحاً نهاراً لتفادي الخطر، وتصبح أضواء التقاطع إلزامية نهاراً وليلاً.</p>
          </div>
        `;
      }
    }

    updatePreselezioneInfo() {
      const box = document.getElementById('preInfoBox');
      if (!box) return;
      const dict = {
        left: 'الحارة اليسرى (Corsia di sinistra): مخصصة للتوجه المباشر نحو وسط المدينة (CENTRO) والتجاوز السريع.',
        center: 'الحارة الوسطى (Corsia centrale): مخصصة للسير المباشر والمتابعة نحو الأوتوستراد (TUTTE LE DIREZIONI / AUTOSTRADA).',
        exit: 'حارة التباطؤ والخروج (Corsia di decelerazione): مخصصة للمغادرة الآمنة نحو مخرج المستشفى والمحليات (USCITA OSPEDALE).'
      };
      box.innerHTML = `
        <div class="indicazione-status-card" style="border-right: 4px solid #38bdf8;">
          <h4 style="color:#bae6fd;">🧭 الحارة المختارة: ${dict[this.chosenLane]}</h4>
          <p style="color:#94a3b8; font-size:0.88rem;">يجب اتخاذ الحارة قبل الخطوط المتصلة؛ بمجرد أن يصبح الخط الأرضي متصلاً (Striscia continua) يُمنع تغيير الحارة نهائياً.</p>
        </div>
      `;
    }

    startLoop() {
      const render = () => {
        this.ctx.clearRect(0, 0, this.width, this.height);

        if (this.currentTab === 'colori') {
          this.renderTabColori();
        } else if (this.currentTab === 'centro') {
          this.renderTabCentro();
        } else if (this.currentTab === 'preselezione') {
          this.renderTabPreselezione();
        }

        requestAnimationFrame(render);
      };
      requestAnimationFrame(render);
    }

    // ==========================================
    // TAB 1: COLOR CODES SIMULATOR
    // ==========================================
    renderTabColori() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // Road background styling based on selected color
      let skyColor1 = '#0f172a';
      let skyColor2 = '#1e293b';
      let roadColor = '#334155';
      let signBgColor = '#166534'; // Green by default
      let signTextColor = '#ffffff';
      let signText = 'MILANO 45 km';
      let signSub = 'AUTOSTRADA A1';
      let speedLimit = '130';

      if (this.currentColor === 'verde') {
        signBgColor = '#15803d'; // Green
        signText = 'MILANO 45 km';
        signSub = 'AUTOSTRADA A1';
        speedLimit = '130';
      } else if (this.currentColor === 'blu') {
        signBgColor = '#1d4ed8'; // Blue
        signText = 'PESCARA 28 km';
        signSub = 'STRADA STATALE SS16';
        speedLimit = '90';
      } else if (this.currentColor === 'bianco') {
        signBgColor = '#f8fafc'; // White
        signTextColor = '#0f172a';
        signText = 'CENTRO / OSPEDALE';
        signSub = 'VIA ROMA';
        speedLimit = '50';
      } else if (this.currentColor === 'giallo') {
        signBgColor = '#facc15'; // Yellow
        signTextColor = '#0f172a';
        signText = 'DEVIAZIONE 500 m';
        signSub = 'CANTIERE STRADALE';
        speedLimit = '40';
      } else if (this.currentColor === 'marrone') {
        signBgColor = '#78350f'; // Brown
        signText = 'PARCO NAZIONALE';
        signSub = 'SCAVI ARCHEOLOGICI';
        speedLimit = '60';
      } else if (this.currentColor === 'nero') {
        signBgColor = '#e2e8f0'; // Light grey/white with black
        signTextColor = '#0f172a';
        signText = 'ZONA INDUSTRIALE';
        signSub = 'INTERPORTO MERCI';
        speedLimit = '50';
      }

      // Sky
      const skyGrad = ctx.createLinearGradient(0, 0, 0, 200);
      skyGrad.addColorStop(0, skyColor1);
      skyGrad.addColorStop(1, skyColor2);
      ctx.fillStyle = skyGrad;
      ctx.fillRect(0, 0, w, 200);

      // Road
      ctx.fillStyle = roadColor;
      ctx.fillRect(0, 200, w, h - 200);

      // Dashed lane lines
      ctx.strokeStyle = '#f8fafc';
      ctx.lineWidth = 4;
      ctx.setLineDash([25, 25]);
      ctx.beginPath();
      ctx.moveTo(0, 290);
      ctx.lineTo(w, 290);
      ctx.stroke();
      ctx.setLineDash([]);

      // Overhead Sign Gantry at x = w * 0.6
      const gx = w * 0.6;
      ctx.fillStyle = '#64748b';
      ctx.fillRect(gx - 6, 40, 12, 170);

      // Sign Board
      const sw = 220;
      const sh = 90;
      const sx = gx - sw / 2;
      const sy = 40;

      ctx.fillStyle = signBgColor;
      ctx.strokeStyle = '#f8fafc';
      ctx.lineWidth = 3;
      ctx.fillRect(sx, sy, sw, sh);
      ctx.strokeRect(sx, sy, sw, sh);

      // Sign text
      ctx.fillStyle = signTextColor;
      ctx.font = 'bold 16px Cairo, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(signText, sx + sw / 2, sy + 38);
      ctx.font = 'bold 12px Cairo, sans-serif';
      ctx.fillText(signSub, sx + sw / 2, sy + 64);

      // Speed limit badge mounted next to sign
      ctx.fillStyle = '#ef4444';
      ctx.beginPath();
      ctx.arc(sx + sw + 26, sy + sh / 2, 22, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#f8fafc';
      ctx.beginPath();
      ctx.arc(sx + sw + 26, sy + sh / 2, 18, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 13px Cairo, sans-serif';
      ctx.fillText(speedLimit, sx + sw + 26, sy + sh / 2 + 5);

      // Car motion
      this.carX += this.carSpeed;
      if (this.carX > w + 40) {
        this.carX = -40;
      }
      this.drawCar(this.carX, 290);
    }

    // ==========================================
    // TAB 2: CENTRO ABITATO
    // ==========================================
    renderTabCentro() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // Sky
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, 0, w, 220);

      // Road
      ctx.fillStyle = '#334155';
      ctx.fillRect(0, 220, w, h - 220);

      // Signpost at x = w * 0.45
      const sx = w * 0.45;
      ctx.fillStyle = '#64748b';
      ctx.fillRect(sx - 4, 90, 8, 140);

      // Town Sign Rect [ ROMA ]
      const sw = 160;
      const sh = 65;
      ctx.fillStyle = '#f8fafc';
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 3;
      ctx.fillRect(sx - sw / 2, 90, sw, sh);
      ctx.strokeRect(sx - sw / 2, 90, sw, sh);

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 24px Cairo, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('ROMA', sx, 132);

      // If Fine Centro Abitato: Red diagonal slash line across name
      if (!this.isEnteringTown) {
        ctx.strokeStyle = '#dc2626';
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(sx - sw / 2 + 10, 90 + sh - 8);
        ctx.lineTo(sx + sw / 2 - 10, 90 + 8);
        ctx.stroke();
      }

      // Car Motion towards sign
      this.townCarX += 2.2;
      if (this.townCarX > w + 40) {
        this.townCarX = -40;
      }

      // Determine vehicle state (before sign vs after sign)
      const passedSign = this.townCarX > sx;
      let currentSpeed = 0;
      let hornBlocked = false;

      if (this.isEnteringTown) {
        currentSpeed = passedSign ? 50 : 90;
        hornBlocked = passedSign;
      } else {
        currentSpeed = passedSign ? 90 : 50;
        hornBlocked = !passedSign;
      }

      this.drawCar(this.townCarX, 290);

      // Live Speed & Rule HUD on top right
      ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.5;
      ctx.roundRect(w - 240, 20, 220, 80, 8);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 12px Cairo, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText('السرعة اللحظية المسموحة:', w - 225, 42);

      ctx.fillStyle = currentSpeed === 50 ? '#f59e0b' : '#10b981';
      ctx.font = 'bold 22px Cairo, sans-serif';
      ctx.fillText(`${currentSpeed} km/h`, w - 225, 72);

      ctx.fillStyle = hornBlocked ? '#f43f5e' : '#a7f3d0';
      ctx.font = 'bold 11px Cairo, sans-serif';
      ctx.fillText(hornBlocked ? '🔇 يُمنع استخدام الكلاكس' : '🔊 الكلاكس مسموح للضرورة', w - 120, 70);
    }

    // ==========================================
    // TAB 3: PRESELEZIONE DELLE CORSIE
    // ==========================================
    renderTabPreselezione() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // 3 Lanes
      ctx.fillStyle = '#334155';
      ctx.fillRect(0, 0, w, h);

      // Lane dividers
      const l1 = 120;
      const l2 = 230;
      const l3 = 340;

      ctx.strokeStyle = '#f8fafc';
      ctx.lineWidth = 3;
      ctx.setLineDash([20, 20]);
      ctx.beginPath();
      ctx.moveTo(0, l1);
      ctx.lineTo(w, l1);
      ctx.moveTo(0, l2);
      ctx.lineTo(w, l2);
      ctx.stroke();
      ctx.setLineDash([]);

      // Overhead Gantry with 3 preselection arrows at x = w * 0.4
      const gx = w * 0.4;
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(gx - 4, 0, 8, h);

      // Sign Boards for each lane
      // Lane 1: CENTRO (Left)
      this.drawLaneGantryBox(gx, 60, 'CENTRO', '⬆️');
      // Lane 2: AUTOSTRADA (Center)
      this.drawLaneGantryBox(gx, 175, 'AUTOSTRADA', '⬆️');
      // Lane 3: USCITA (Exit / Right)
      this.drawLaneGantryBox(gx, 285, 'USCITA', '↗️');

      // Target Car position
      let targetY = 175;
      if (this.chosenLane === 'left') targetY = 60;
      if (this.chosenLane === 'exit') targetY = 285;

      this.preCarX += 2.4;
      if (this.preCarX > w + 40) {
        this.preCarX = -40;
      }

      // Smooth steering transition towards target lane
      this.preCarY += (targetY - this.preCarY) * 0.05;

      this.drawCar(this.preCarX, this.preCarY);
    }

    drawLaneGantryBox(x, y, text, arrow) {
      const ctx = this.ctx;
      ctx.save();
      ctx.translate(x, y);

      ctx.fillStyle = '#1d4ed8';
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.fillRect(-50, -25, 100, 50);
      ctx.strokeRect(-50, -25, 100, 50);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px Cairo, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(text, 0, -2);
      ctx.fillText(arrow, 0, 16);
      ctx.restore();
    }

    drawCar(x, y, color = '#2563eb') {
      const ctx = this.ctx;
      ctx.save();
      ctx.translate(x, y);

      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.roundRect(-22, -11, 44, 22, 4);
      ctx.fill();

      // Cabin
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(-10, -8, 20, 16);

      // Headlights
      ctx.fillStyle = '#fef08a';
      ctx.fillRect(20, -9, 3, 5);
      ctx.fillRect(20, 4, 3, 5);

      ctx.restore();
    }
  }

  // Auto init
  document.addEventListener('DOMContentLoaded', () => {
    new IndicazioneStudio();
  });
})();

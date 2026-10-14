/**
 * Patente B Pro - Chapter 9: Interactive Roadworks & Complementary Delineators Studio (60 FPS)
 * استوديو إشارات ورش العمل والشواخص التكميلية التفاعلي المتقدم للباب التاسع
 * Architecture: Modular Canvas Engine, Web Audio API Sound Generator, 60 FPS requestAnimationFrame
 */

(function () {
  'use strict';

  // Web Audio Sound Engine
  class RoadworksAudioEngine {
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
      osc.frequency.setValueAtTime(750, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(320, this.ctx.currentTime + 0.05);
      gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.05);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.05);
    }

    playBlinker() {
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(900, this.ctx.currentTime);
      gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.04);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.04);
    }

    playAlert() {
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(450, this.ctx.currentTime);
      osc.frequency.setValueAtTime(900, this.ctx.currentTime + 0.1);
      gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.25);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.25);
    }
  }

  // Main Roadworks & Delineators Studio
  class RoadworksStudio {
    constructor() {
      this.canvas = document.getElementById('roadworksStudioCanvas');
      if (!this.canvas) return;
      this.ctx = this.canvas.getContext('2d');
      this.audio = new RoadworksAudioEngine();
      this.currentTab = 'cantiere'; // 'cantiere' | 'delineatori' | 'semaforo'

      // Mode 1: Cantiere State
      this.laneClosure = 'right'; // 'right' | 'left' | 'mobile'
      this.carProgress = 0; // 0 to 1
      this.arrowBlink = 0;

      // Mode 2: Delineatori State
      this.delineatorType = 'doppio'; // 'doppio' | 'unico' | 'margine' | 'galleria' | 'neve'
      this.isNight = true;

      // Mode 3: Semaforo State
      this.semaforoColor = 'red'; // 'red' | 'green'
      this.semaforoTimer = 0;

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
      const tabBtns = document.querySelectorAll('.cantiere-tab-btn');
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

      // Lane closure selector
      const btnCloseRight = document.getElementById('btnCloseRight');
      const btnCloseLeft = document.getElementById('btnCloseLeft');
      const btnCloseMobile = document.getElementById('btnCloseMobile');
      if (btnCloseRight && btnCloseLeft && btnCloseMobile) {
        btnCloseRight.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.laneClosure = 'right';
          btnCloseRight.classList.add('active');
          btnCloseLeft.classList.remove('active');
          btnCloseMobile.classList.remove('active');
          this.carProgress = 0;
          this.updateCantiereInfo();
        });
        btnCloseLeft.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.laneClosure = 'left';
          btnCloseLeft.classList.add('active');
          btnCloseRight.classList.remove('active');
          btnCloseMobile.classList.remove('active');
          this.carProgress = 0;
          this.updateCantiereInfo();
        });
        btnCloseMobile.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.laneClosure = 'mobile';
          btnCloseMobile.classList.add('active');
          btnCloseRight.classList.remove('active');
          btnCloseLeft.classList.remove('active');
          this.carProgress = 0;
          this.updateCantiereInfo();
        });
      }

      // Delineator Type Selector
      const delinBtns = document.querySelectorAll('.delin-type-btn');
      delinBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          delinBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          this.delineatorType = btn.getAttribute('data-type');
          this.updateDelineatorInfo();
        });
      });

      // Night / Day Toggle
      const btnNightToggle = document.getElementById('btnNightToggle');
      if (btnNightToggle) {
        btnNightToggle.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.isNight = !this.isNight;
          btnNightToggle.textContent = this.isNight ? '🌙 رؤية ليلية (أضواء وعواكس)' : '☀️ رؤية نهارية (إضاءة كاملة)';
        });
      }

      window.addEventListener('resize', () => {
        this.initDPI();
      });
    }

    updateControlPanels() {
      const pCantiere = document.getElementById('controlsCantiere');
      const pDelineatori = document.getElementById('controlsDelineatori');
      const pSemaforo = document.getElementById('controlsSemaforo');
      if (pCantiere) pCantiere.style.display = this.currentTab === 'cantiere' ? 'block' : 'none';
      if (pDelineatori) pDelineatori.style.display = this.currentTab === 'delineatori' ? 'block' : 'none';
      if (pSemaforo) pSemaforo.style.display = this.currentTab === 'semaforo' ? 'block' : 'none';
    }

    updateCantiereInfo() {
      const box = document.getElementById('cantiereStatusBox');
      if (!box) return;
      if (this.laneClosure === 'right') {
        box.innerHTML = `
          <div class="cantiere-alert-card yellow">
            <span class="ca-icon">🚧</span>
            <div>
              <strong>إغلاق المسار الأيمن (Fig. 285 - Chiusura corsia destra):</strong>
              <p>توضح اللوحة الصفراء إغلاق الحارة اليمنى لأعمال الحفريات؛ يُلزم السائقون بالانحياز التدريجي نحو اليسار (Rientro a sinistra) بعد تهدئة السرعة وتفقد حركة السير في المرآة الجانبية.</p>
            </div>
          </div>
        `;
      } else if (this.laneClosure === 'left') {
        box.innerHTML = `
          <div class="cantiere-alert-card yellow">
            <span class="ca-icon">🚧</span>
            <div>
              <strong>إغلاق المسار الأيسر (Fig. 285 - Chiusura corsia sinistra):</strong>
              <p>توضح اللوحة إغلاق حارة التجاوز اليسرى؛ تلزم المركبات القادمة على اليسار بالانتقال للحارة الوسطى أو اليمنى بحذر تام.</p>
            </div>
          </div>
        `;
      } else {
        box.innerHTML = `
          <div class="cantiere-alert-card orange">
            <span class="ca-icon">🚚</span>
            <div>
              <strong>ورشة عمل متنقلة بسهم ضوئي وميض (Fig. 280 - Cantiere mobile):</strong>
              <p>شاحنة صيانة تسير بسرعة بطيئة ومزودة بسهم ضوئي وميض يوجه السائقين للجهة الإجبارية لتجاوز الشاحنة بأمان تام.</p>
            </div>
          </div>
        `;
      }
    }

    updateDelineatorInfo() {
      const box = document.getElementById('delineatorStatusBox');
      if (!box) return;
      const dict = {
        doppio: {
          title: '🔴 شواخص المنعطفات لطريق ذي اتجاهين (Fig. 293 - Doppio Senso)',
          desc: 'القاعدة الوزارية: أسهم بيضاء على خلفية حمراء تدل دائماً وبشكل قاطع على أن الطريق ذو اتجاهين للسير (Doppio Senso)!',
          trap: '⚠️ فخ الامتحان: القول بأنها تدل على طريق ذو اتجاه واحد هو FALSO صريح.'
        },
        unico: {
          title: '⚪ شواخص المنعطفات لطريق ذي اتجاه واحد (Fig. 289 - Senso Unico)',
          desc: 'القاعدة الوزارية: أسهم سوداء على خلفية بيضاء تدل حصراً على أن الطريق ذو اتجاه واحد للسير (Senso Unico)!',
          trap: '⚠️ فخ الامتحان: الخلط بين الأبيض/الأسود (اتجاه واحد) والأحمر/الأبيض (اتجاهين).'
        },
        margine: {
          title: '🦯 شواخص حواف وجوانب الطريق (Fig. 290 - Delineatori di Margine)',
          desc: 'القاعدة الذهبية: على اليمين عاكس أحمر (Destra = Rosso)، وعلى اليسار عاكس أبيض (Sinistra = Bianco).',
          trap: '⚠️ فخ الامتحان: عكس الألوان (القول بأن الأحمر على اليسار) هو FALSO قاطع.'
        },
        galleria: {
          title: '💡 شواخص الأنفاق المضيئة (Fig. 291 - Delineatori per Gallerie)',
          desc: 'تستخدم عواكس صفراء فسفورية أو أضواء LED صفراء على جداري النفق لتعزيز وضوح المنحنيات وجوانب المسار.',
          trap: '⚠️ ميزة هامة: إضاءة صفراء وميضة أو ثابتة لتأمين الرؤية تحت الظلام.'
        },
        neve: {
          title: '❄️ شواخص الطرق الجبلية المعرضة للثلوج (Fig. 292 - Delineatori da Neve)',
          desc: 'أعمدة فائقة الطول مخططة باللونين الأصفر والأسود لتحديد حدود الطريق حتى مع تراكم طبقات الثلج العالية.',
          trap: '⚠️ فخ الامتحان: القول بأنها تنبه لوجود ممر مشاة أو حاجز قطار هو FALSO.'
        }
      };
      const info = dict[this.delineatorType] || dict.doppio;
      box.innerHTML = `
        <div class="cantiere-alert-card blue">
          <span class="ca-icon">🎯</span>
          <div>
            <strong>${info.title}:</strong>
            <p>${info.desc}</p>
            <div style="margin-top:6px; color:#fca5a5; font-size:0.86rem;">${info.trap}</div>
          </div>
        </div>
      `;
    }

    startLoop() {
      const render = () => {
        this.ctx.clearRect(0, 0, this.width, this.height);

        if (this.currentTab === 'cantiere') {
          this.renderTabCantiere();
        } else if (this.currentTab === 'delineatori') {
          this.renderTabDelineatori();
        } else if (this.currentTab === 'semaforo') {
          this.renderTabSemaforo();
        }

        requestAnimationFrame(render);
      };
      requestAnimationFrame(render);
    }

    // ==========================================
    // TAB 1: CANTIERE (ROADWORKS & LANE CLOSURE)
    // ==========================================
    renderTabCantiere() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // Road background (2-lane dual carriageway)
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, 0, w, 60);

      // Asphalt
      ctx.fillStyle = '#334155';
      ctx.fillRect(0, 60, w, 260);

      // Yellow temporary roadwork markings
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 4;
      ctx.setLineDash([20, 20]);
      ctx.beginPath();
      ctx.moveTo(0, 190);
      ctx.lineTo(w, 190); // Lane divider between Lane 1 (top) and Lane 2 (bottom)
      ctx.stroke();
      ctx.setLineDash([]);

      // Grass / verge bottom
      ctx.fillStyle = '#166534';
      ctx.fillRect(0, 320, w, h - 320);

      // Roadwork zone setup
      const cantiereStartX = w * 0.45;
      const isRightClosed = this.laneClosure === 'right';
      const isMobile = this.laneClosure === 'mobile';

      // Blocked lane area
      const blockedY = isRightClosed ? 190 : 60;
      const blockedH = 130;

      ctx.fillStyle = 'rgba(239, 68, 68, 0.15)';
      ctx.fillRect(cantiereStartX, blockedY, w - cantiereStartX, blockedH);

      // Draw Cones tapering into the lane
      const coneCount = 7;
      for (let i = 0; i < coneCount; i++) {
        const cx = cantiereStartX - 140 + i * 22;
        let cy = 0;
        if (isRightClosed) {
          cy = 300 - i * 16;
        } else {
          cy = 80 + i * 16;
        }
        this.drawCone(cx, cy);
      }

      // Draw Red & White Striped Barrier at cantiereStartX + 20
      this.drawBarrier(cantiereStartX + 30, blockedY + 20, 160, blockedH - 40);

      // Mobile roadwork truck if active
      if (isMobile) {
        this.drawMobileTruck(cantiereStartX + 100, 190);
      }

      // Approaching Yellow Sign Fig. 285 at x = 100
      this.drawFig285Sign(100, 310, isRightClosed ? 'right' : 'left');

      // Animated Car Progress
      this.carProgress += 0.006;
      if (this.carProgress > 1.0) {
        this.carProgress = 0;
      }

      // Car Path calculation
      let carX = -30 + this.carProgress * (w + 60);
      let carY = isRightClosed ? 250 : 120; // Starts in closed lane

      // Steering / filtering into open lane before the cones
      const taperStartX = cantiereStartX - 160;
      const taperEndX = cantiereStartX - 20;

      if (carX >= taperStartX && carX <= taperEndX) {
        const ratio = (carX - taperStartX) / (taperEndX - taperStartX);
        if (isRightClosed) {
          carY = 250 - ratio * 130; // Filters from bottom lane to top lane (120)
        } else {
          carY = 120 + ratio * 130; // Filters from top lane to bottom lane (250)
        }
      } else if (carX > taperEndX) {
        carY = isRightClosed ? 120 : 250; // Stays in open lane
      }

      this.drawCar(carX, carY, carX < taperEndX ? '#2563eb' : '#10b981');
    }

    drawCone(x, y) {
      const ctx = this.ctx;
      ctx.save();
      ctx.translate(x, y);
      ctx.fillStyle = '#ea580c';
      ctx.beginPath();
      ctx.moveTo(0, -18);
      ctx.lineTo(-9, 14);
      ctx.lineTo(9, 14);
      ctx.closePath();
      ctx.fill();
      // White reflective bands
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(-4, -6, 8, 4);
      ctx.fillRect(-7, 4, 14, 5);
      // Base plate
      ctx.fillStyle = '#c2410c';
      ctx.fillRect(-11, 14, 22, 4);
      ctx.restore();
    }

    drawBarrier(x, y, w, h) {
      const ctx = this.ctx;
      ctx.save();
      ctx.fillStyle = '#f8fafc';
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2;
      ctx.fillRect(x, y, w, h);
      ctx.strokeRect(x, y, w, h);

      // Red stripes
      ctx.fillStyle = '#dc2626';
      const stripeW = 22;
      for (let sx = x - 20; sx < x + w + 20; sx += stripeW * 2) {
        ctx.beginPath();
        ctx.moveTo(sx, y);
        ctx.lineTo(sx + stripeW, y);
        ctx.lineTo(sx + stripeW - 20, y + h);
        ctx.lineTo(sx - 20, y + h);
        ctx.closePath();
        ctx.fill();
      }

      // Red flashing lantern
      ctx.fillStyle = Math.floor(Date.now() / 250) % 2 === 0 ? '#ef4444' : '#7f1d1d';
      ctx.beginPath();
      ctx.arc(x + w / 2, y - 10, 8, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    drawFig285Sign(x, y, closedSide) {
      const ctx = this.ctx;
      ctx.save();
      ctx.translate(x, y);
      // Yellow Roadwork Sign Rect
      ctx.fillStyle = '#fbbf24';
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2;
      ctx.fillRect(-35, -45, 70, 50);
      ctx.strokeRect(-35, -45, 70, 50);

      // Lanes Arrows
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 3;
      if (closedSide === 'right') {
        // Left arrow goes straight
        ctx.beginPath();
        ctx.moveTo(-16, -10);
        ctx.lineTo(-16, -35);
        ctx.stroke();
        // Right arrow bends into left lane
        ctx.beginPath();
        ctx.moveTo(16, -10);
        ctx.lineTo(16, -22);
        ctx.lineTo(-6, -35);
        ctx.stroke();
      } else {
        // Right arrow goes straight
        ctx.beginPath();
        ctx.moveTo(16, -10);
        ctx.lineTo(16, -35);
        ctx.stroke();
        // Left arrow bends into right lane
        ctx.beginPath();
        ctx.moveTo(-16, -10);
        ctx.lineTo(-16, -22);
        ctx.lineTo(6, -35);
        ctx.stroke();
      }
      ctx.restore();
    }

    drawMobileTruck(x, y) {
      const ctx = this.ctx;
      ctx.save();
      ctx.translate(x, y);
      // Truck body
      ctx.fillStyle = '#f59e0b';
      ctx.fillRect(-40, -18, 80, 36);
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(-45, -12, 12, 24); // Cabin
      // Flashing illuminated sign
      ctx.fillStyle = '#020617';
      ctx.fillRect(-20, -14, 48, 28);
      // Flashing arrow
      ctx.fillStyle = Math.floor(Date.now() / 200) % 2 === 0 ? '#38bdf8' : '#e0f2fe';
      ctx.beginPath();
      ctx.moveTo(16, -8);
      ctx.lineTo(-6, 0);
      ctx.lineTo(16, 8);
      ctx.closePath();
      ctx.fill();
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

      // Blinker light if filtering
      if (Math.floor(Date.now() / 180) % 2 === 0) {
        ctx.fillStyle = '#f97316';
        ctx.fillRect(-6, -13, 4, 3);
      }

      ctx.restore();
    }

    // ==========================================
    // TAB 2: DELINEATORI (CURVE & MARGIN MARKERS)
    // ==========================================
    renderTabDelineatori() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // Background depending on Night/Day
      if (this.isNight) {
        ctx.fillStyle = '#090d16';
        ctx.fillRect(0, 0, w, h);
      } else {
        ctx.fillStyle = '#334155';
        ctx.fillRect(0, 0, w, h);
      }

      // Curved road drawing
      ctx.fillStyle = this.isNight ? '#1e293b' : '#475569';
      ctx.beginPath();
      ctx.moveTo(0, 140);
      ctx.bezierCurveTo(w * 0.35, 140, w * 0.65, 340, w, 340);
      ctx.lineTo(w, 400);
      ctx.lineTo(0, 400);
      ctx.closePath();
      ctx.fill();

      // Headlight Beam Cone if Night
      if (this.isNight) {
        const grad = ctx.createRadialGradient(120, 260, 20, 380, 260, 320);
        grad.addColorStop(0, 'rgba(255, 255, 220, 0.45)');
        grad.addColorStop(1, 'rgba(255, 255, 220, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.moveTo(80, 260);
        ctx.lineTo(460, 130);
        ctx.lineTo(460, 390);
        ctx.closePath();
        ctx.fill();
      }

      // Delineator Points along curve
      const pts = [
        { x: w * 0.25, y: 130 },
        { x: w * 0.42, y: 170 },
        { x: w * 0.58, y: 220 },
        { x: w * 0.74, y: 280 },
        { x: w * 0.90, y: 330 }
      ];

      pts.forEach((pt, idx) => {
        this.drawDelineatorItem(pt.x, pt.y, this.delineatorType);
      });

      // Car at bottom left with lights
      this.drawCar(100, 260, '#38bdf8');
    }

    drawDelineatorItem(x, y, type) {
      const ctx = this.ctx;
      ctx.save();
      ctx.translate(x, y);

      if (type === 'doppio') {
        // Red background with white chevron (Fig. 293: Doppio senso)
        ctx.fillStyle = '#dc2626';
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 1.5;
        ctx.fillRect(-22, -16, 44, 32);
        ctx.strokeRect(-22, -16, 44, 32);

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.moveTo(-10, -10);
        ctx.lineTo(4, 0);
        ctx.lineTo(-10, 10);
        ctx.lineTo(-2, 10);
        ctx.lineTo(12, 0);
        ctx.lineTo(-2, -10);
        ctx.closePath();
        ctx.fill();

        // Retroreflective glow
        if (this.isNight) {
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
          ctx.strokeRect(-23, -17, 46, 34);
        }
      } else if (type === 'unico') {
        // White background with black chevron (Fig. 289: Senso unico)
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 1.5;
        ctx.fillRect(-22, -16, 44, 32);
        ctx.strokeRect(-22, -16, 44, 32);

        ctx.fillStyle = '#0f172a';
        ctx.beginPath();
        ctx.moveTo(-10, -10);
        ctx.lineTo(4, 0);
        ctx.lineTo(-10, 10);
        ctx.lineTo(-2, 10);
        ctx.lineTo(12, 0);
        ctx.lineTo(-2, -10);
        ctx.closePath();
        ctx.fill();
      } else if (type === 'margine') {
        // Roadside post: Destra = Rosso (Right is Red)
        ctx.fillStyle = '#f8fafc';
        ctx.fillRect(-4, -20, 8, 40);
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(-4, -20, 8, 8); // Black cap
        // Red reflector
        ctx.fillStyle = '#ef4444';
        ctx.fillRect(-3, -8, 6, 12);
        if (this.isNight) {
          ctx.fillStyle = 'rgba(239, 68, 68, 0.5)';
          ctx.beginPath();
          ctx.arc(0, -2, 8, 0, Math.PI * 2);
          ctx.fill();
        }
      } else if (type === 'galleria') {
        // Yellow amber reflector for tunnel (Fig. 291)
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(-10, -12, 20, 24);
        ctx.fillStyle = '#eab308';
        ctx.fillRect(-6, -8, 12, 16);
        if (this.isNight) {
          ctx.fillStyle = 'rgba(234, 179, 8, 0.6)';
          ctx.beginPath();
          ctx.arc(0, 0, 10, 0, Math.PI * 2);
          ctx.fill();
        }
      } else if (type === 'neve') {
        // Tall snow pole yellow and black bands (Fig. 292)
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(-4, -50, 8, 80);
        ctx.fillStyle = '#facc15';
        ctx.fillRect(-4, -40, 8, 12);
        ctx.fillRect(-4, -16, 8, 12);
      }

      ctx.restore();
    }

    // ==========================================
    // TAB 3: SEMAFORO DI CANTIERE
    // ==========================================
    renderTabSemaforo() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // Alternating One-Way Road (Senso unico alternato)
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, 0, w, 80);

      // Narrow road (single open lane)
      ctx.fillStyle = '#334155';
      ctx.fillRect(0, 80, w, 220);

      // Roadwork barrier blocking top half of road
      this.drawBarrier(w * 0.35, 90, w * 0.4, 70);

      // Temporary Traffic Light at x = w * 0.3
      const semX = w * 0.28;
      const semY = 170;

      // Pole
      ctx.fillStyle = '#64748b';
      ctx.fillRect(semX - 4, semY - 20, 8, 120);

      // Box
      ctx.fillStyle = '#0f172a';
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 2;
      ctx.fillRect(semX - 16, semY - 70, 32, 70);
      ctx.strokeRect(semX - 16, semY - 70, 32, 70);

      // Auto cycle lights every 3 seconds
      this.semaforoTimer += 0.016;
      const isRed = Math.floor(this.semaforoTimer / 3) % 2 === 0;

      // Red Light
      ctx.fillStyle = isRed ? '#ef4444' : '#450a0a';
      ctx.beginPath();
      ctx.arc(semX, semY - 54, 8, 0, Math.PI * 2);
      ctx.fill();

      // Yellow Light
      ctx.fillStyle = '#713f12';
      ctx.beginPath();
      ctx.arc(semX, semY - 35, 8, 0, Math.PI * 2);
      ctx.fill();

      // Green Light
      ctx.fillStyle = !isRed ? '#10b981' : '#064e3b';
      ctx.beginPath();
      ctx.arc(semX, semY - 16, 8, 0, Math.PI * 2);
      ctx.fill();

      // Warning Sign Fig. 297 placed 150m ahead
      const signX = 80;
      const signY = 240;
      ctx.save();
      ctx.translate(signX, signY);
      // Triangle
      ctx.fillStyle = '#dc2626';
      ctx.beginPath();
      ctx.moveTo(0, -32);
      ctx.lineTo(-28, 20);
      ctx.lineTo(28, 20);
      ctx.closePath();
      ctx.fill();
      // Inner yellow triangle
      ctx.fillStyle = '#fde047';
      ctx.beginPath();
      ctx.moveTo(0, -20);
      ctx.lineTo(-18, 14);
      ctx.lineTo(18, 14);
      ctx.closePath();
      ctx.fill();
      // Mini traffic light inside
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(-3, -10, 6, 18);
      ctx.restore();

      // Car waiting or passing
      let carX = isRed ? semX - 70 : semX + 160;
      this.drawCar(carX, 240, isRed ? '#ef4444' : '#10b981');

      // Status text
      ctx.fillStyle = isRed ? '#f87171' : '#6ee7b7';
      ctx.font = 'bold 14px Cairo, sans-serif';
      ctx.textAlign = 'center';
      const label = isRed ? '⛔ الضوء أحمر: توقف إلزامي قبل بداية مضيق ورشة العمل' : '🟢 الضوء أخضر: تقدم بحذر عبر مسار السير التبادلي الفردي (Senso Unico Alternato)';
      ctx.fillText(label, w / 2, 340);
    }
  }

  // Auto init
  document.addEventListener('DOMContentLoaded', () => {
    new RoadworksStudio();
  });
})();

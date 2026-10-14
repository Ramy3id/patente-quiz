/**
 * Patente B Pro - Chapter 10: Interactive Supplementary Panels Studio (60 FPS)
 * استوديو اللوحات الإضافية التفاعلي المتقدم للباب العاشر
 * Architecture: Modular Canvas Engine, Web Audio API Sound Generator, 60 FPS requestAnimationFrame
 */

(function () {
  'use strict';

  // Sound Engine using Web Audio API
  class PanelsAudioEngine {
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
      osc.frequency.exponentialRampToValueAtTime(300, this.ctx.currentTime + 0.05);
      gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.05);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.05);
    }

    playAlert() {
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(440, this.ctx.currentTime);
      osc.frequency.setValueAtTime(880, this.ctx.currentTime + 0.1);
      gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.25);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.25);
    }

    playTow() {
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(180, this.ctx.currentTime);
      osc.frequency.linearRampToValueAtTime(320, this.ctx.currentTime + 0.4);
      gain.gain.setValueAtTime(0.18, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.45);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.45);
    }

    playPass() {
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(523.25, this.ctx.currentTime); // C5
      osc.frequency.setValueAtTime(659.25, this.ctx.currentTime + 0.1); // E5
      gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.35);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.35);
    }
  }

  // Main Studio Controller
  class PanelsStudio {
    constructor() {
      this.canvas = document.getElementById('panelsStudioCanvas');
      if (!this.canvas) return;
      this.ctx = this.canvas.getContext('2d');
      this.audio = new PanelsAudioEngine();
      this.currentTab = 'distanza'; // 'distanza' | 'orari' | 'andamento'

      // Mode 1: Distanza vs Estesa State
      this.distMode = 'distanza'; // 'distanza' (no arrows) vs 'estesa' (with arrows)
      this.distValue = 300; // meters
      this.carX = 40; // pixel position
      this.carSpeed = 2.4;
      this.isDriving = true;

      // Mode 2: Fasce Orarie & Rimozione State
      this.dayType = 'lavorativo'; // 'lavorativo' | 'festivo'
      this.currentHour = 10.5; // 10:30 AM
      this.hasTowZone = true;
      this.isParking = true;
      this.towTruckProgress = 0; // 0 to 1

      // Mode 3: Andamento Incrocio State
      this.bendDirection = 'left'; // 'left' | 'right'
      this.simulatingIncrocio = false;
      this.incrocioProgress = 0;

      this.initDPI();
      this.bindEvents();
      this.startLoop();
    }

    initDPI() {
      const dpr = window.devicePixelRatio || 1;
      const rect = this.canvas.getBoundingClientRect();
      const width = rect.width || 800;
      const height = 400;
      this.canvas.width = width * dpr;
      this.canvas.height = height * dpr;
      this.ctx.scale(dpr, dpr);
      this.width = width;
      this.height = height;
    }

    bindEvents() {
      // Tab switcher
      const tabBtns = document.querySelectorAll('.panels-tab-btn');
      tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
          this.audio.init();
          this.audio.playClick();
          tabBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          this.currentTab = btn.getAttribute('data-tab');
          this.updateControlPanels();
        });
      });

      // Distanza vs Estesa toggle
      const btnDistanza = document.getElementById('btnModeDistanza');
      const btnEstesa = document.getElementById('btnModeEstesa');
      if (btnDistanza && btnEstesa) {
        btnDistanza.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.distMode = 'distanza';
          btnDistanza.classList.add('active');
          btnEstesa.classList.remove('active');
          this.carX = 40;
          this.updateDistInfo();
        });
        btnEstesa.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.distMode = 'estesa';
          btnEstesa.classList.add('active');
          btnDistanza.classList.remove('active');
          this.carX = 40;
          this.updateDistInfo();
        });
      }

      // Distance Slider
      const distSlider = document.getElementById('panelsDistSlider');
      if (distSlider) {
        distSlider.addEventListener('input', (e) => {
          this.distValue = parseInt(e.target.value, 10);
          const valLabel = document.getElementById('panelsDistVal');
          if (valLabel) valLabel.textContent = this.distValue + ' m';
          this.updateDistInfo();
        });
      }

      // Day Type Selector
      const btnLavorativo = document.getElementById('btnDayLavorativo');
      const btnFestivo = document.getElementById('btnDayFestivo');
      if (btnLavorativo && btnFestivo) {
        btnLavorativo.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.dayType = 'lavorativo';
          btnLavorativo.classList.add('active');
          btnFestivo.classList.remove('active');
          this.evaluateParking();
        });
        btnFestivo.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.dayType = 'festivo';
          btnFestivo.classList.add('active');
          btnLavorativo.classList.remove('active');
          this.evaluateParking();
        });
      }

      // Hour Slider
      const hourSlider = document.getElementById('panelsHourSlider');
      if (hourSlider) {
        hourSlider.addEventListener('input', (e) => {
          this.currentHour = parseFloat(e.target.value);
          const hourLabel = document.getElementById('panelsHourVal');
          if (hourLabel) {
            const h = Math.floor(this.currentHour);
            const m = Math.floor((this.currentHour - h) * 60);
            hourLabel.textContent = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
          }
          this.evaluateParking();
        });
      }

      // Bend Direction Selector
      const btnBendLeft = document.getElementById('btnBendLeft');
      const btnBendRight = document.getElementById('btnBendRight');
      if (btnBendLeft && btnBendRight) {
        btnBendLeft.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.bendDirection = 'left';
          btnBendLeft.classList.add('active');
          btnBendRight.classList.remove('active');
          this.simulatingIncrocio = false;
          this.incrocioProgress = 0;
          this.updateIncrocioInfo();
        });
        btnBendRight.addEventListener('click', () => {
          this.audio.init();
          this.audio.playClick();
          this.bendDirection = 'right';
          btnBendRight.classList.add('active');
          btnBendLeft.classList.remove('active');
          this.simulatingIncrocio = false;
          this.incrocioProgress = 0;
          this.updateIncrocioInfo();
        });
      }

      // Simulate Incrocio Button
      const btnSimIncrocio = document.getElementById('btnSimIncrocio');
      if (btnSimIncrocio) {
        btnSimIncrocio.addEventListener('click', () => {
          this.audio.init();
          this.audio.playPass();
          this.simulatingIncrocio = true;
          this.incrocioProgress = 0;
        });
      }

      window.addEventListener('resize', () => {
        this.initDPI();
      });
    }

    updateControlPanels() {
      const panelDistanza = document.getElementById('controlsDistanza');
      const panelOrari = document.getElementById('controlsOrari');
      const panelAndamento = document.getElementById('controlsAndamento');
      if (panelDistanza) panelDistanza.style.display = this.currentTab === 'distanza' ? 'block' : 'none';
      if (panelOrari) panelOrari.style.display = this.currentTab === 'orari' ? 'block' : 'none';
      if (panelAndamento) panelAndamento.style.display = this.currentTab === 'andamento' ? 'block' : 'none';
    }

    updateDistInfo() {
      const infoBox = document.getElementById('panelsDistExplanation');
      if (!infoBox) return;
      if (this.distMode === 'distanza') {
        infoBox.innerHTML = `
          <div class="pe-status-title" style="color:#38bdf8;">📌 لوحة مسافة (Pannello di Distanza - Fig. 121) [ ${this.distValue} m ]</div>
          <p><strong>القاعدة الذهبية:</strong> وجود الرقم <em>بدون أي أسهم جانبية</em> يعني أن الخطر <strong>لا يبدأ هنا</strong>، بل يبدأ بعد قطع مسافة <strong>${this.distValue} متراً</strong> كاملة من موقع الإشارة.</p>
          <div class="pe-trap-reminder">⚠️ فخ الامتحان: عبارة "indica la lunghezza del cantiere" هي FALSO، لأن اللوحة بدون أسهم تحدد البعد حتى بداية الخطر فقط!</div>
        `;
      } else {
        infoBox.innerHTML = `
          <div class="pe-status-title" style="color:#10b981;">📌 لوحة امتداد وطول (Pannello di Estesa - Fig. 122) [ ↑ ${this.distValue} m ↑ ]</div>
          <p><strong>القاعدة الذهبية:</strong> وجود <em>الأسهم الرأسية الجانبية</em> يعني أن الخطر <strong>يبدأ فوراً عند موقع الإشارة</strong> ويمتد بطول <strong>${this.distValue} متراً</strong> متواصلة.</p>
          <div class="pe-trap-reminder">⚠️ فخ الامتحان: عبارة "il pericolo inizia dopo 300 metri" هي FALSO، لأن الأسهم تعني أنك دخلت منطقة الخطر في التو واللحظة!</div>
        `;
      }
    }

    evaluateParking() {
      // Rule: Divieto di sosta from 08:00 to 20:00 on Lavorativi (Mon-Sat with hammers)
      const isWithinHours = this.currentHour >= 8.0 && this.currentHour <= 20.0;
      const isLavorativo = this.dayType === 'lavorativo';
      const isRestricted = isLavorativo && isWithinHours;

      const evalBox = document.getElementById('panelsParkingStatus');
      if (!evalBox) return;

      if (isRestricted) {
        evalBox.innerHTML = `
          <div class="pe-alert-box red">
            <span class="pe-icon">⛔</span>
            <div>
              <strong>مخالفة وقوف صريحة (DIVIETO DI SOSTA ATTIVO):</strong>
              <p>الساعة الآن تقع ضمن نطاق الدوام الرسمي (08:00 - 20:00) لأيام العمل (المطارق ⚒️). يُمنع الوقوف منعاً باتاً، وتتدخل رافعة المرور <strong>(Rimozione forzata)</strong> لسحب سيارتك وحجزها!</p>
            </div>
          </div>
        `;
        if (this.towTruckProgress === 0) {
          this.audio.playTow();
        }
      } else {
        const reason = !isLavorativo ? 'اليوم عطلة رسمية (Festivo ✝️)' : 'الساعة الحالية خارج أوقات المنع (قبل 08:00 أو بعد 20:00)';
        evalBox.innerHTML = `
          <div class="pe-alert-box green">
            <span class="pe-icon">✅</span>
            <div>
              <strong>الوقوف مباح ومسموح قانونياً (SOSTA CONSENTITA):</strong>
              <p>${reason}. الإشارة الملحقة بلوحة المطارق لا تسري حالياً، ولا يحق للبلدية سحب مركبتك مطلقاً.</p>
            </div>
          </div>
        `;
      }
    }

    updateIncrocioInfo() {
      const infoBox = document.getElementById('panelsIncrocioExplanation');
      if (!infoBox) return;
      const bend = this.bendDirection === 'left' ? 'انحناء المسار الرئيسي جهة اليسار' : 'انحناء المسار الرئيسي جهة اليمين';
      infoBox.innerHTML = `
        <div class="pe-status-title" style="color:#f59e0b;">🧭 خريطة مسار الشارع الرئيسي ذو الأسبقية (Andamento Strada Principale)</div>
        <p><strong>تفسير الشكل:</strong> ${bend}. السيارة القادمة على <strong>الخط العريض (Tratto largo)</strong> تتمتع بحق الأسبقية التامة في عبور التقاطع، بينما السيارات على <strong>الخطوط الرفيعة (Tratti stretti)</strong> ملزمة بانتظار خلو المسار أو التوقف عند إشارة STOP.</p>
      `;
    }

    startLoop() {
      const render = () => {
        this.ctx.clearRect(0, 0, this.width, this.height);

        if (this.currentTab === 'distanza') {
          this.renderTabDistanza();
        } else if (this.currentTab === 'orari') {
          this.renderTabOrari();
        } else if (this.currentTab === 'andamento') {
          this.renderTabAndamento();
        }

        requestAnimationFrame(render);
      };
      requestAnimationFrame(render);
    }

    // ==========================================
    // RENDER TAB 1: DISTANZA VS ESTESA
    // ==========================================
    renderTabDistanza() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // Sky & Horizon
      const skyGrad = ctx.createLinearGradient(0, 0, 0, 180);
      skyGrad.addColorStop(0, '#0f172a');
      skyGrad.addColorStop(1, '#1e293b');
      ctx.fillStyle = skyGrad;
      ctx.fillRect(0, 0, w, 180);

      // Road background
      ctx.fillStyle = '#334155';
      ctx.fillRect(0, 180, w, h - 180);

      // Road markings (white dashed line)
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 4;
      ctx.setLineDash([20, 20]);
      ctx.beginPath();
      ctx.moveTo(0, 280);
      ctx.lineTo(w, 280);
      ctx.stroke();
      ctx.setLineDash([]);

      // Sign Position at x = 160
      const signX = 160;
      const signY = 160;

      // Draw Pole
      ctx.fillStyle = '#94a3b8';
      ctx.fillRect(signX - 4, signY - 110, 8, 130);

      // Draw Danger Sign (Lavori in corso)
      ctx.save();
      ctx.translate(signX, signY - 100);
      ctx.beginPath();
      ctx.moveTo(0, -36);
      ctx.lineTo(-32, 22);
      ctx.lineTo(32, 22);
      ctx.closePath();
      ctx.fillStyle = '#dc2626';
      ctx.fill();

      // Inner yellow triangle
      ctx.beginPath();
      ctx.moveTo(0, -24);
      ctx.lineTo(-22, 16);
      ctx.lineTo(22, 16);
      ctx.closePath();
      ctx.fillStyle = '#fbbf24';
      ctx.fill();

      // Worker symbol
      ctx.fillStyle = '#1e293b';
      ctx.beginPath();
      ctx.arc(0, -4, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillRect(-6, 2, 12, 10);
      ctx.restore();

      // Draw Supplementary Panel
      ctx.save();
      ctx.translate(signX, signY - 32);
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2.5;
      const pw = 74;
      const ph = 28;
      ctx.fillRect(-pw / 2, -ph / 2, pw, ph);
      ctx.strokeRect(-pw / 2, -ph / 2, pw, ph);

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 12px Cairo, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      if (this.distMode === 'distanza') {
        // [ 300 m ]
        ctx.fillText(this.distValue + ' m', 0, 1);
      } else {
        // [ ↑ 300 m ↑ ]
        ctx.fillText(this.distValue + ' m', 0, 1);
        // Left arrow
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(-pw / 2 + 6, ph / 2 - 4);
        ctx.lineTo(-pw / 2 + 6, -ph / 2 + 6);
        ctx.lineTo(-pw / 2 + 3, -ph / 2 + 9);
        ctx.moveTo(-pw / 2 + 6, -ph / 2 + 6);
        ctx.lineTo(-pw / 2 + 9, -ph / 2 + 9);
        ctx.stroke();
        // Right arrow
        ctx.beginPath();
        ctx.moveTo(pw / 2 - 6, ph / 2 - 4);
        ctx.lineTo(pw / 2 - 6, -ph / 2 + 6);
        ctx.lineTo(pw / 2 - 9, -ph / 2 + 9);
        ctx.moveTo(pw / 2 - 6, -ph / 2 + 6);
        ctx.lineTo(pw / 2 - 3, -ph / 2 + 9);
        ctx.stroke();
      }
      ctx.restore();

      // Define Hazard Zone coordinates
      let hazardStartX = 0;
      let hazardEndX = 0;
      const scalePixels = 0.5; // 300m -> 150px
      const hazardSpan = Math.min(this.distValue * scalePixels, w - 200);

      if (this.distMode === 'distanza') {
        // Danger starts AFTER the distance gap
        hazardStartX = signX + hazardSpan;
        hazardEndX = hazardStartX + 220;

        // Draw Approach Gap bracket
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(signX, 195);
        ctx.lineTo(hazardStartX, 195);
        ctx.stroke();

        ctx.fillStyle = '#38bdf8';
        ctx.font = 'bold 11px Cairo, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(`مسافة اقتراب آمنة (${this.distValue} m)`, (signX + hazardStartX) / 2, 212);
      } else {
        // Danger starts IMMEDIATELY at sign
        hazardStartX = signX;
        hazardEndX = signX + hazardSpan;

        // Draw Extension bracket
        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(hazardStartX, 195);
        ctx.lineTo(hazardEndX, 195);
        ctx.stroke();

        ctx.fillStyle = '#10b981';
        ctx.font = 'bold 11px Cairo, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(`امتداد مقطع الخطر (${this.distValue} m)`, (hazardStartX + hazardEndX) / 2, 212);
      }

      // Draw Hazard Zone (Striped roadworks area)
      ctx.fillStyle = 'rgba(239, 68, 68, 0.2)';
      ctx.fillRect(hazardStartX, 220, hazardEndX - hazardStartX, 110);
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 2;
      ctx.strokeRect(hazardStartX, 220, hazardEndX - hazardStartX, 110);

      // Draw Road Cones
      for (let cx = hazardStartX + 20; cx < hazardEndX; cx += 50) {
        ctx.fillStyle = '#f97316';
        ctx.beginPath();
        ctx.moveTo(cx, 225);
        ctx.lineTo(cx - 8, 245);
        ctx.lineTo(cx + 8, 245);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(cx - 5, 233, 10, 4);
      }

      // Hazard Label
      ctx.fillStyle = '#ef4444';
      ctx.font = 'bold 13px Cairo, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('🚧 منطقة أشغال وحفريات (Cantiere Stradale)', (hazardStartX + hazardEndX) / 2, 280);

      // Car Motion
      this.carX += this.carSpeed;
      if (this.carX > w + 40) {
        this.carX = -40;
      }

      // Draw Moving Car
      this.drawCar(this.carX, 240);

      // Check if car entered danger zone
      if (this.carX >= hazardStartX && this.carX <= hazardEndX) {
        ctx.fillStyle = '#ef4444';
        ctx.font = 'bold 12px Cairo, sans-serif';
        ctx.fillText('⚠️ داخل منطقة الخطر!', this.carX, 218);
      }
    }

    drawCar(x, y) {
      const ctx = this.ctx;
      ctx.save();
      ctx.translate(x, y);

      // Body
      ctx.fillStyle = '#2563eb';
      ctx.beginPath();
      ctx.roundRect(-24, -12, 48, 18, 4);
      ctx.fill();

      // Cabin / Roof
      ctx.fillStyle = '#1d4ed8';
      ctx.beginPath();
      ctx.roundRect(-14, -22, 28, 12, 3);
      ctx.fill();

      // Windows
      ctx.fillStyle = '#93c5fd';
      ctx.fillRect(-11, -19, 10, 7);
      ctx.fillRect(2, -19, 10, 7);

      // Wheels
      ctx.fillStyle = '#0f172a';
      ctx.beginPath();
      ctx.arc(-14, 6, 6, 0, Math.PI * 2);
      ctx.arc(14, 6, 6, 0, Math.PI * 2);
      ctx.fill();

      // Headlight
      ctx.fillStyle = '#fef08a';
      ctx.fillRect(22, -6, 3, 5);

      ctx.restore();
    }

    // ==========================================
    // RENDER TAB 2: FASCE ORARIE & RIMOZIONE
    // ==========================================
    renderTabOrari() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // Urban street background
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, 0, w, 220);

      // Sidewalk & Curb
      ctx.fillStyle = '#475569';
      ctx.fillRect(0, 220, w, 60);
      ctx.fillStyle = '#cbd5e1';
      ctx.fillRect(0, 276, w, 6);

      // Asphalt
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 282, w, h - 282);

      // Signpost in center-left
      const sx = 200;
      const sy = 140;

      // Pole
      ctx.fillStyle = '#94a3b8';
      ctx.fillRect(sx - 5, 20, 10, 250);

      // Divieto di Sosta Sign (Circle)
      ctx.fillStyle = '#dc2626';
      ctx.beginPath();
      ctx.arc(sx, 50, 36, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#2563eb';
      ctx.beginPath();
      ctx.arc(sx, 50, 28, 0, Math.PI * 2);
      ctx.fill();
      // Diagonal red bar
      ctx.strokeStyle = '#dc2626';
      ctx.lineWidth = 7;
      ctx.beginPath();
      ctx.moveTo(sx - 20, 50 - 20);
      ctx.lineTo(sx + 20, 50 + 20);
      ctx.stroke();

      // Panel 1: Fascia Oraria (Hammers or Cross)
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2;
      ctx.fillRect(sx - 55, 96, 110, 34);
      ctx.strokeRect(sx - 55, 96, 110, 34);

      if (this.dayType === 'lavorativo') {
        // Crossed hammers icon
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(sx - 42, 106);
        ctx.lineTo(sx - 28, 120);
        ctx.moveTo(sx - 28, 106);
        ctx.lineTo(sx - 42, 120);
        ctx.stroke();
      } else {
        // Latin cross icon
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(sx - 35, 104);
        ctx.lineTo(sx - 35, 122);
        ctx.moveTo(sx - 42, 110);
        ctx.lineTo(sx - 28, 110);
        ctx.stroke();
      }

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 12px Cairo, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('08.00 - 20.00', sx + 12, 117);

      // Panel 2: Zona Rimozione Coatta
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(sx - 55, 138, 110, 36);
      ctx.strokeRect(sx - 55, 138, 110, 36);

      // Tow truck icon
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(sx - 45, 150, 16, 10);
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(sx - 30, 150);
      ctx.lineTo(sx - 16, 142);
      ctx.lineTo(sx - 8, 152);
      ctx.stroke();
      ctx.font = 'bold 9px Cairo, sans-serif';
      ctx.fillText('ZONA RIMOZIONE', sx + 12, 160);

      // Parked Car at x = 450
      const carX = 460;
      const carY = 320;
      this.drawCar(carX, carY);

      // Tow Truck Animation if restricted
      const isWithinHours = this.currentHour >= 8.0 && this.currentHour <= 20.0;
      const isRestricted = this.dayType === 'lavorativo' && isWithinHours;

      if (isRestricted) {
        if (this.towTruckProgress < 1.0) {
          this.towTruckProgress += 0.015;
        }
        const truckX = carX - 110 + this.towTruckProgress * 40;
        this.drawTowTruck(truckX, carY);

        // Tow Hook attached
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(truckX + 38, carY - 25);
        ctx.lineTo(carX - 22, carY - 4);
        ctx.stroke();

        ctx.fillStyle = '#ef4444';
        ctx.font = 'bold 14px Cairo, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('🚨 جاري سحب المركبة المخالفة بالرافعة!', carX + 30, carY - 40);
      } else {
        this.towTruckProgress = 0;
        ctx.fillStyle = '#10b981';
        ctx.font = 'bold 14px Cairo, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('✅ السيارة متوقفة بشكل قانوني وآمن', carX, carY - 35);
      }
    }

    drawTowTruck(x, y) {
      const ctx = this.ctx;
      ctx.save();
      ctx.translate(x, y);

      // Big truck cabin
      ctx.fillStyle = '#f59e0b';
      ctx.beginPath();
      ctx.roundRect(-40, -22, 40, 28, 4);
      ctx.fill();

      // Truck bed
      ctx.fillStyle = '#334155';
      ctx.fillRect(0, -10, 48, 16);

      // Crane arm
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 5;
      ctx.beginPath();
      ctx.moveTo(10, -10);
      ctx.lineTo(38, -25);
      ctx.stroke();

      // Flashing light on top
      ctx.fillStyle = Math.floor(Date.now() / 200) % 2 === 0 ? '#ef4444' : '#fbbf24';
      ctx.beginPath();
      ctx.arc(-20, -26, 4, 0, Math.PI * 2);
      ctx.fill();

      // Wheels
      ctx.fillStyle = '#0f172a';
      ctx.beginPath();
      ctx.arc(-26, 10, 8, 0, Math.PI * 2);
      ctx.arc(26, 10, 8, 0, Math.PI * 2);
      ctx.fill();

      ctx.restore();
    }

    // ==========================================
    // RENDER TAB 3: ANDAMENTO STRADA PRINCIPALE
    // ==========================================
    renderTabAndamento() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;

      // Rural background
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, 0, w, h);

      // Intersection Center
      const ix = w / 2;
      const iy = h / 2;
      const roadW = 60;

      // Draw Secondary Thin Cross Roads (Dark Grey)
      ctx.fillStyle = '#334155';
      ctx.fillRect(ix - roadW / 2, 0, roadW, h); // Vertical
      ctx.fillRect(0, iy - roadW / 2, w, roadW); // Horizontal

      // Draw Main Road Curve (Thick Blue Glowing Lane)
      ctx.fillStyle = '#2563eb';
      if (this.bendDirection === 'left') {
        // Curve from Bottom to Left
        ctx.fillRect(ix - roadW / 2, iy - roadW / 2, roadW, h - iy + roadW / 2); // Bottom branch
        ctx.fillRect(0, iy - roadW / 2, ix + roadW / 2, roadW); // Left branch
      } else {
        // Curve from Bottom to Right
        ctx.fillRect(ix - roadW / 2, iy - roadW / 2, roadW, h - iy + roadW / 2); // Bottom branch
        ctx.fillRect(ix - roadW / 2, iy - roadW / 2, w - ix + roadW / 2, roadW); // Right branch
      }

      // Draw Intersection Sign in Corner
      const signX = 110;
      const signY = 100;

      // Yellow Diamond Diritto di Precedenza
      ctx.save();
      ctx.translate(signX, signY);
      ctx.rotate(Math.PI / 4);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(-22, -22, 44, 44);
      ctx.fillStyle = '#fbbf24';
      ctx.fillRect(-16, -16, 32, 32);
      ctx.restore();

      // Supplementary Panel (Andamento)
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2.5;
      ctx.fillRect(signX - 32, signY + 34, 64, 64);
      ctx.strokeRect(signX - 32, signY + 34, 64, 64);

      // Panel Roads Layout
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 3;
      // Secondary thin roads
      ctx.beginPath();
      ctx.moveTo(signX, signY + 38);
      ctx.lineTo(signX, signY + 94); // Vertical
      ctx.moveTo(signX - 28, signY + 66);
      ctx.lineTo(signX + 28, signY + 66); // Horizontal
      ctx.stroke();

      // Thick Main Road Curve
      ctx.lineWidth = 8;
      ctx.beginPath();
      ctx.moveTo(signX, signY + 94);
      ctx.lineTo(signX, signY + 66);
      if (this.bendDirection === 'left') {
        ctx.lineTo(signX - 28, signY + 66);
      } else {
        ctx.lineTo(signX + 28, signY + 66);
      }
      ctx.stroke();

      // Vehicles at Intersection
      let car1X = ix;
      let car1Y = iy + 110; // Car A on Main Road (Bottom)
      let car2X = this.bendDirection === 'left' ? ix + 120 : ix - 120;
      let car2Y = iy; // Car B on Secondary Road

      if (this.simulatingIncrocio) {
        if (this.incrocioProgress < 1.0) {
          this.incrocioProgress += 0.012;
        }
        // Car A moves first along the curve!
        if (this.incrocioProgress < 0.6) {
          const p = this.incrocioProgress / 0.6;
          car1Y = (iy + 110) - p * 110;
          if (this.bendDirection === 'left') {
            car1X = ix - p * 140;
          } else {
            car1X = ix + p * 140;
          }
        } else {
          // After Car A clears, Car B crosses
          const p = (this.incrocioProgress - 0.6) / 0.4;
          if (this.bendDirection === 'left') {
            car2X = (ix + 120) - p * 240;
          } else {
            car2X = (ix - 120) + p * 240;
          }
        }
      }

      // Draw Car A (Blue - Has Precedence)
      this.drawCar(car1X, car1Y);
      ctx.fillStyle = '#60a5fa';
      ctx.font = 'bold 12px Cairo, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('السيارة A (المسار العريض - أولوية 1)', car1X, car1Y - 26);

      // Draw Car B (Red - Secondary Road)
      ctx.save();
      ctx.translate(car2X, car2Y);
      ctx.fillStyle = '#ef4444';
      ctx.beginPath();
      ctx.roundRect(-24, -12, 48, 18, 4);
      ctx.fill();
      ctx.fillStyle = '#b91c1c';
      ctx.beginPath();
      ctx.roundRect(-14, -22, 28, 12, 3);
      ctx.fill();
      ctx.restore();

      ctx.fillStyle = '#f87171';
      ctx.font = 'bold 12px Cairo, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('السيارة B (مسار فرعي - تنتظر 2)', car2X, car2Y - 26);
    }
  }

  // Auto-init on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    new PanelsStudio();
  });
})();

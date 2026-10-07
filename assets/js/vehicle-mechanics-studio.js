/**
 * =======================================================================
 * Patente B Pro - Vehicle Mechanics & Dynamics Studio (الباب 25)
 * =======================================================================
 * 60 FPS HTML5 Canvas Interactive Physics Simulator:
 * 1. ABS Emergency Braking & Obstacle Evasion (نظام ABS وتفادي الاصطدام)
 * 2. Aquaplaning & Tire Tread Depth Physics (الانزلاق المائي وعمق مداس الإطار)
 * 3. Shock Absorbers Dynamics: Pitch & Roll (ممتصات الصدمات وتمايل المركبة)
 * =======================================================================
 */

class VehicleMechanicsStudio {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;

    this.activeTab = 'abs'; // 'abs' | 'aquaplaning' | 'shocks'
    this.animationId = null;
    this.lastTime = 0;
    
    // ABS Simulation State - AUTO PLAYING LOOP
    this.abs = {
      enabled: true,
      autoPlay: true,
      speed: 90, // target speed in km/h
      roadCondition: 'asciutto', // 'asciutto' (dry), 'bagnato' (wet), 'ghiaccio' (ice)
      carX: 50,
      carY: 180, // initial lane (lower lane)
      carAngle: 0,
      currentSpeed: 90,
      phase: 'driving', // 'driving' | 'braking' | 'finished'
      skidMarks: [],
      obstacleX: 680,
      obstacleY: 180,
      pulsingTire: 0,
      finishTimer: 0,
      crashFlash: 0
    };

    // Aquaplaning Simulation State
    this.aqua = {
      treadDepth: 8.0, // mm (8mm = new, 4mm = fair, 1.6mm = legal min, 0.8mm = worn/illegal)
      speed: 70, // km/h
      waterLevel: 5.0, // mm puddle
      tireRotation: 0,
      liftAmount: 0, // 0 = full grip, 1 = total float (aquaplaning)
      bubbles: []
    };

    // Shock Absorbers Simulation State - CONTINUOUS IMPULSE LOOP
    this.shocks = {
      condition: 'healthy', // 'healthy' | 'worn'
      testType: 'braking', // 'braking' (pitch) | 'cornering' (roll)
      cycleTimer: 0,
      cycleDuration: 3.5, // seconds per bump/brake surge
      bodyRoll: 0,
      bodyPitch: 0
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
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.audioCtx = new AudioContext();
      }
    } catch (e) {
      console.warn("Web Audio not supported", e);
    }
  }

  playChime(type) {
    if (!this.audioCtx) return;
    try {
      if (this.audioCtx.state === 'suspended') {
        this.audioCtx.resume();
      }
      const now = this.audioCtx.currentTime;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);

      if (type === 'abs-pulse') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(80, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.06);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.005, now + 0.06);
        osc.start(now);
        osc.stop(now + 0.06);
      } else if (type === 'skid') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(180, now);
        osc.frequency.linearRampToValueAtTime(110, now + 0.15);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        osc.start(now);
        osc.stop(now + 0.15);
      } else if (type === 'crash') {
        osc.type = 'square';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.exponentialRampToValueAtTime(30, now + 0.35);
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
        osc.start(now);
        osc.stop(now + 0.35);
      }
    } catch(e) {}
  }

  renderLayout() {
    this.container.innerHTML = `
      <div class="vms-studio-wrapper" style="background:linear-gradient(145deg, #0f172a 0%, #1e293b 100%); border:1px solid rgba(56,189,248,0.25); border-radius:18px; padding:22px; box-shadow:0 12px 35px rgba(0,0,0,0.45); font-family:inherit; direction:rtl; margin:28px 0;">
        <!-- Header -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px; margin-bottom:18px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:14px;">
          <div>
            <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(56,189,248,0.12); color:#38bdf8; padding:4px 12px; border-radius:30px; font-size:0.82rem; font-weight:700; border:1px solid rgba(56,189,248,0.3); margin-bottom:6px;">
              <span>🔬 مختبر الفيزياء والميكانيكا الحركية المباشر 60 FPS</span>
            </div>
            <h3 style="margin:0; color:#f8fafc; font-size:1.35rem; font-weight:800; display:flex; align-items:center; gap:8px;">
              <span>محاكي فيزياء وديناميكا المركبة (Simulatore Dinamica del Veicolo)</span>
            </h3>
          </div>
          <!-- Tab Switcher -->
          <div style="display:flex; gap:8px; flex-wrap:wrap; background:rgba(15,23,42,0.8); padding:5px; border-radius:12px; border:1px solid rgba(255,255,255,0.1);">
            <button class="vms-tab-btn active" data-tab="abs" style="background:#0284c7; color:#fff; border:none; padding:8px 16px; border-radius:8px; font-size:0.88rem; font-weight:700; cursor:pointer; transition:all 0.2s;">
              🛑 1. فرملة ABS والتوجيه
            </button>
            <button class="vms-tab-btn" data-tab="aquaplaning" style="background:transparent; color:#94a3b8; border:none; padding:8px 16px; border-radius:8px; font-size:0.88rem; font-weight:700; cursor:pointer; transition:all 0.2s;">
              🌊 2. الانزلاق المائي (Aquaplaning)
            </button>
            <button class="vms-tab-btn" data-tab="shocks" style="background:transparent; color:#94a3b8; border:none; padding:8px 16px; border-radius:8px; font-size:0.88rem; font-weight:700; cursor:pointer; transition:all 0.2s;">
              🚙 3. ممتصات الصدمات (Ammortizzatori)
            </button>
          </div>
        </div>

        <!-- Canvas Display Area -->
        <div style="position:relative; width:100%; border-radius:14px; overflow:hidden; background:#020617; border:1px solid rgba(56,189,248,0.2); box-shadow:inset 0 2px 10px rgba(0,0,0,0.6);">
          <canvas id="vmsCanvas" width="900" height="340" style="width:100%; height:auto; display:block; aspect-ratio:900/340;"></canvas>
          <div id="vmsOverlayText" style="position:absolute; bottom:12px; right:16px; left:16px; display:flex; justify-content:space-between; align-items:center; pointer-events:none; font-size:0.85rem; color:#cbd5e1; text-shadow:0 1px 3px rgba(0,0,0,0.9);">
            <span id="vmsStatusBadge" style="background:rgba(16,185,129,0.25); border:1px solid #10b981; color:#34d399; padding:4px 10px; border-radius:6px; font-weight:700;">حركة مستمرة نشطة</span>
            <span id="vmsTelemetry" style="font-family:monospace; direction:ltr; color:#93c5fd;">SPD: 90 km/h | ABS: ACTIVE</span>
          </div>
        </div>

        <!-- Dynamic Control Panels -->
        <div id="vmsControlPanel" style="margin-top:16px; background:rgba(15,23,42,0.65); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:16px;">
          <!-- Controls injected dynamically per tab -->
        </div>

        <!-- Ministerial Legal & Trap Banner -->
        <div id="vmsExplanationBox" style="margin-top:14px; padding:14px 18px; border-radius:10px; font-size:0.92rem; line-height:1.75; transition:all 0.3s;">
          <!-- Text updated dynamically -->
        </div>
      </div>
    `;
  }

  initCanvas() {
    this.canvas = document.getElementById('vmsCanvas');
    this.ctx = this.canvas.getContext('2d');
    this.updateControlsUI();
    this.updateExplanationUI();
    this.resetSimulation();
  }

  bindEvents() {
    // Tab switching
    this.container.querySelectorAll('.vms-tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        this.container.querySelectorAll('.vms-tab-btn').forEach(b => {
          b.style.background = 'transparent';
          b.style.color = '#94a3b8';
          b.classList.remove('active');
        });
        const target = e.currentTarget;
        target.style.background = '#0284c7';
        target.style.color = '#fff';
        target.classList.add('active');
        this.activeTab = target.dataset.tab;
        this.resetSimulation();
        this.updateControlsUI();
        this.updateExplanationUI();
      });
    });
  }

  updateControlsUI() {
    const panel = document.getElementById('vmsControlPanel');
    if (!panel) return;

    if (this.activeTab === 'abs') {
      panel.innerHTML = `
        <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:14px;">
          <!-- ABS Mode Switch -->
          <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
            <span style="font-weight:700; color:#e2e8f0; font-size:0.9rem;">حالة نظام ABS:</span>
            <button id="vmsBtnAbsOn" style="padding:7px 16px; border-radius:8px; font-weight:700; font-size:0.88rem; cursor:pointer; border:1px solid #10b981; background:${this.abs.enabled ? '#10b981' : 'transparent'}; color:${this.abs.enabled ? '#fff' : '#10b981'}; transition:all 0.2s;">
              ✅ نظام ABS نشط (توجيه وتفادي)
            </button>
            <button id="vmsBtnAbsOff" style="padding:7px 16px; border-radius:8px; font-weight:700; font-size:0.88rem; cursor:pointer; border:1px solid #f43f5e; background:${!this.abs.enabled ? '#f43f5e' : 'transparent'}; color:${!this.abs.enabled ? '#fff' : '#f43f5e'}; transition:all 0.2s;">
              ❌ بدون ABS (انغلاق العجلات Blok)
            </button>
          </div>

          <!-- Speed & Road Conditions -->
          <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
            <div style="display:flex; gap:6px; align-items:center;">
              <span style="font-weight:700; color:#e2e8f0; font-size:0.88rem;">السرعة:</span>
              <input type="range" id="vmsAbsSpeed" min="50" max="130" step="10" value="${this.abs.speed}" style="width:110px; accent-color:#38bdf8; cursor:pointer;">
              <span id="vmsAbsSpeedVal" style="font-family:monospace; font-weight:700; color:#38bdf8; width:55px;">${this.abs.speed} km/h</span>
            </div>

            <div style="display:flex; gap:6px; align-items:center;">
              <span style="font-weight:700; color:#e2e8f0; font-size:0.88rem;">الطريق:</span>
              <select id="vmsRoadSelect" style="background:#1e293b; color:#fff; border:1px solid rgba(255,255,255,0.2); padding:5px 10px; border-radius:8px; font-size:0.85rem; cursor:pointer;">
                <option value="asciutto" ${this.abs.roadCondition==='asciutto'?'selected':''}>جاف (Asciutto)</option>
                <option value="bagnato" ${this.abs.roadCondition==='bagnato'?'selected':''}>مبلل (Bagnato)</option>
                <option value="ghiaccio" ${this.abs.roadCondition==='ghiaccio'?'selected':''}>جليد (Ghiaccio)</option>
              </select>
            </div>
          </div>

          <!-- Action & Playback Controls -->
          <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
            <button id="vmsBtnAutoPlay" style="background:${this.abs.autoPlay ? '#0284c7' : '#334155'}; color:#fff; border:none; padding:7px 14px; border-radius:8px; font-weight:700; font-size:0.85rem; cursor:pointer;">
              ${this.abs.autoPlay ? '⏸️ إيقاف التكرار التلقائي' : '▶️ تشغيل العرض المستمر'}
            </button>
            <button id="vmsBtnBrakeNow" style="background:linear-gradient(135deg, #e11d48, #be123c); color:#fff; border:none; padding:7px 14px; border-radius:8px; font-weight:800; font-size:0.88rem; cursor:pointer; box-shadow:0 3px 10px rgba(225,29,72,0.4);">
              🚨 فرملة طارئة فورية!
            </button>
            <button id="vmsBtnReset" style="background:#1e293b; color:#cbd5e1; border:1px solid rgba(255,255,255,0.15); padding:7px 12px; border-radius:8px; font-weight:700; font-size:0.85rem; cursor:pointer;">
              🔄 إعادة البداية
            </button>
          </div>
        </div>
      `;

      // Event Listeners for ABS
      document.getElementById('vmsBtnAbsOn').addEventListener('click', () => {
        this.abs.enabled = true;
        this.resetSimulation();
        this.updateControlsUI();
        this.updateExplanationUI();
      });
      document.getElementById('vmsBtnAbsOff').addEventListener('click', () => {
        this.abs.enabled = false;
        this.resetSimulation();
        this.updateControlsUI();
        this.updateExplanationUI();
      });
      document.getElementById('vmsAbsSpeed').addEventListener('input', (e) => {
        this.abs.speed = parseInt(e.target.value);
        document.getElementById('vmsAbsSpeedVal').textContent = `${this.abs.speed} km/h`;
        if (this.abs.phase === 'driving') {
          this.abs.currentSpeed = this.abs.speed;
        }
      });
      document.getElementById('vmsRoadSelect').addEventListener('change', (e) => {
        this.abs.roadCondition = e.target.value;
        this.resetSimulation();
      });
      document.getElementById('vmsBtnAutoPlay').addEventListener('click', () => {
        this.abs.autoPlay = !this.abs.autoPlay;
        this.updateControlsUI();
      });
      document.getElementById('vmsBtnBrakeNow').addEventListener('click', () => {
        this.triggerAbsBrake();
      });
      document.getElementById('vmsBtnReset').addEventListener('click', () => {
        this.resetSimulation();
      });

    } else if (this.activeTab === 'aquaplaning') {
      panel.innerHTML = `
        <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:16px;">
          <!-- Tread Depth Presets -->
          <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
            <span style="font-weight:700; color:#e2e8f0; font-size:0.9rem;">عمق مداس الإطار (Battistrada):</span>
            <button class="vms-tread-btn" data-depth="8.0" style="padding:6px 14px; border-radius:8px; font-size:0.85rem; font-weight:700; cursor:pointer; border:1px solid #10b981; background:${this.aqua.treadDepth===8?'#10b981':'transparent'}; color:${this.aqua.treadDepth===8?'#fff':'#10b981'};">8.0 مم (إطار جديد)</button>
            <button class="vms-tread-btn" data-depth="4.0" style="padding:6px 14px; border-radius:8px; font-size:0.85rem; font-weight:700; cursor:pointer; border:1px solid #38bdf8; background:${this.aqua.treadDepth===4?'#38bdf8':'transparent'}; color:${this.aqua.treadDepth===4?'#fff':'#38bdf8'};">4.0 مم (إطار جيد)</button>
            <button class="vms-tread-btn" data-depth="1.6" style="padding:6px 14px; border-radius:8px; font-size:0.85rem; font-weight:700; cursor:pointer; border:1px solid #f59e0b; background:${this.aqua.treadDepth===1.6?'#f59e0b':'transparent'}; color:${this.aqua.treadDepth===1.6?'#fff':'#f59e0b'};">1.6 مم (الحد القانوني ⚠️)</button>
            <button class="vms-tread-btn" data-depth="0.8" style="padding:6px 14px; border-radius:8px; font-size:0.85rem; font-weight:700; cursor:pointer; border:1px solid #ef4444; background:${this.aqua.treadDepth===0.8?'#ef4444':'transparent'}; color:${this.aqua.treadDepth===0.8?'#fff':'#ef4444'};">0.8 مم (تالف ❌)</button>
          </div>

          <!-- Speed Slider -->
          <div style="display:flex; gap:12px; align-items:center;">
            <label style="font-weight:700; color:#e2e8f0; font-size:0.88rem;">سرعة السير:</label>
            <input type="range" id="vmsAquaSpeed" min="40" max="130" step="5" value="${this.aqua.speed}" style="width:140px; accent-color:#38bdf8; cursor:pointer;">
            <span id="vmsAquaSpeedVal" style="font-family:monospace; font-weight:700; color:#38bdf8; width:65px;">${this.aqua.speed} km/h</span>
          </div>
        </div>
      `;

      // Event listeners for Aquaplaning
      panel.querySelectorAll('.vms-tread-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          this.aqua.treadDepth = parseFloat(e.currentTarget.dataset.depth);
          this.updateControlsUI();
          this.updateExplanationUI();
        });
      });
      const speedInput = document.getElementById('vmsAquaSpeed');
      speedInput.addEventListener('input', (e) => {
        this.aqua.speed = parseInt(e.target.value);
        document.getElementById('vmsAquaSpeedVal').textContent = `${this.aqua.speed} km/h`;
        this.updateExplanationUI();
      });

    } else if (this.activeTab === 'shocks') {
      panel.innerHTML = `
        <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:14px;">
          <!-- Shocks condition -->
          <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
            <span style="font-weight:700; color:#e2e8f0; font-size:0.9rem;">حالة ممتص الصدمات:</span>
            <button id="vmsBtnShockGood" style="padding:7px 16px; border-radius:8px; font-weight:700; font-size:0.85rem; cursor:pointer; border:1px solid #10b981; background:${this.shocks.condition==='healthy'?'#10b981':'transparent'}; color:${this.shocks.condition==='healthy'?'#fff':'#10b981'};">
              ✅ ممتص سليم (Ammortizzatore efficiente)
            </button>
            <button id="vmsBtnShockWorn" style="padding:7px 16px; border-radius:8px; font-weight:700; font-size:0.85rem; cursor:pointer; border:1px solid #ef4444; background:${this.shocks.condition==='worn'?'#ef4444':'transparent'}; color:${this.shocks.condition==='worn'?'#fff':'#ef4444'};">
              ❌ ممتص تالف وفارغ (Scarico / usurato)
            </button>
          </div>

          <!-- Dynamic Maneuver -->
          <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
            <span style="font-weight:700; color:#e2e8f0; font-size:0.9rem;">المناورة الديناميكية:</span>
            <button id="vmsBtnPitch" style="padding:7px 14px; border-radius:8px; font-size:0.85rem; font-weight:700; cursor:pointer; border:1px solid #38bdf8; background:${this.shocks.testType==='braking'?'#0284c7':'transparent'}; color:${this.shocks.testType==='braking'?'#fff':'#38bdf8'};">
              🛑 فرملة حادة (الانغماس للأمام Beccheggio)
            </button>
            <button id="vmsBtnRoll" style="padding:7px 14px; border-radius:8px; font-size:0.85rem; font-weight:700; cursor:pointer; border:1px solid #f59e0b; background:${this.shocks.testType==='cornering'?'#d97706':'transparent'}; color:${this.shocks.testType==='cornering'?'#fff':'#f59e0b'};">
              🔄 منعطف مفاجئ (التأرجح الجانبي Rollio)
            </button>
          </div>
        </div>
      `;

      // Event listeners for Shocks
      document.getElementById('vmsBtnShockGood').addEventListener('click', () => {
        this.shocks.condition = 'healthy';
        this.shocks.cycleTimer = 0;
        this.updateControlsUI();
        this.updateExplanationUI();
      });
      document.getElementById('vmsBtnShockWorn').addEventListener('click', () => {
        this.shocks.condition = 'worn';
        this.shocks.cycleTimer = 0;
        this.updateControlsUI();
        this.updateExplanationUI();
      });
      document.getElementById('vmsBtnPitch').addEventListener('click', () => {
        this.shocks.testType = 'braking';
        this.shocks.cycleTimer = 0;
        this.updateControlsUI();
        this.updateExplanationUI();
      });
      document.getElementById('vmsBtnRoll').addEventListener('click', () => {
        this.shocks.testType = 'cornering';
        this.shocks.cycleTimer = 0;
        this.updateControlsUI();
        this.updateExplanationUI();
      });
    }
  }

  updateExplanationUI() {
    const box = document.getElementById('vmsExplanationBox');
    if (!box) return;

    if (this.activeTab === 'abs') {
      if (this.abs.enabled) {
        box.style.background = 'rgba(16,185,129,0.12)';
        box.style.border = '1px solid rgba(16,185,129,0.35)';
        box.style.color = '#a7f3d0';
        box.innerHTML = `
          <strong style="color:#34d399; font-size:1.05rem;">✅ فيزياء نظام ABS في الامتحان الوزاري:</strong><br>
          • <strong>الحفاظ التام على التوجيه (Consente di sterzare):</strong> يمنع انغلاق العجلات، مما يسمح للسائق بالدوران بالمقود وتفادي العائق حتى أثناء ضغط الدواسة بأقصى قوة.<br>
          • <strong>اهتزاز الدواسة (Pulsazione del pedale):</strong> شعورك بنبضات أو ارتعاش في دواسة الفرامل أمر طبيعي تماماً يدل على عمل الصمامات الكهرومغناطيسية ولا يعني خللاً!<br>
          • ⚠️ <strong>فخ وزاري شهير:</strong> نظام ABS لا يضمن تقصير مسافة الفرملة في كل الظروف (قد تطول مسافة الوقوف على الثلوج والحصى السائب)، فائدته الأساسية هي <strong>التحكم في اتجاه المركبة</strong>!
        `;
      } else {
        box.style.background = 'rgba(239,68,68,0.12)';
        box.style.border = '1px solid rgba(239,68,68,0.35)';
        box.style.color = '#fecaca';
        box.innerHTML = `
          <strong style="color:#f87171; font-size:1.05rem;">❌ فيزياء المركبة بدون ABS (أو عند تعطله):</strong><br>
          • <strong>انغلاق العجلات (Bloccaggio delle ruote):</strong> العجلات تتوقف عن الدوران فوراً وتنزلق كقطعة مطاط محترقة فوق الأسفلت.<br>
          • <strong>انعدام التوجيه تماماً (Perdita della direzionalità):</strong> مهما دار السائق بعجلة القيادة يميناً أو يساراً، ستواصل السيارة انزلاقها في خط مستقيم للأمام وتصطدم بالعائق حتماً!<br>
          • <strong>تلف الإطارات:</strong> احتكاك العجلة المنغلقة يسبب تآكلاً موضعياً حاداً (Spiattellamento del pneumatico).
        `;
      }
    } else if (this.activeTab === 'aquaplaning') {
      const isDangerous = this.aqua.treadDepth <= 1.6 || (this.aqua.speed > 80 && this.aqua.treadDepth < 4);
      if (isDangerous) {
        box.style.background = 'rgba(239,68,68,0.12)';
        box.style.border = '1px solid rgba(239,68,68,0.35)';
        box.style.color = '#fecaca';
        box.innerHTML = `
          <strong style="color:#f87171; font-size:1.05rem;">🌊 فيزياء ظاهرة الانزلاق المائي (Aquaplaning) وخطر الغرق السطحي:</strong><br>
          • عند عمق مداس <strong>${this.aqua.treadDepth} مم</strong> وسرعة <strong>${this.aqua.speed} كم/س</strong>: تعجز قنوات الإطار عن طرد المياه للخارج، فيتكون إسفين مائي تحت الإطار يرفعه تماماً عن الأسفلت!<br>
          • <strong>النتيجة الكارثية:</strong> يصبح معامل الاحتكاك صفراً، تدور عجلة القيادة بخفة متناهية (Volante leggero)، وتفقد السيارة الفرامل والتوجيه بالكامل.<br>
          • 💡 <strong>القاعدة الوزارية:</strong> يزداد خطر الأكوابلانينج مع: 1) السرعة العالية، 2) تآكل المداس (أقل من 1.6 مم)، 3) السيارات الخفيفة (Veicoli leggeri)، 4) الإطارات العريضة.
        `;
      } else {
        box.style.background = 'rgba(56,189,248,0.12)';
        box.style.border = '1px solid rgba(56,189,248,0.35)';
        box.style.color = '#bae6fd';
        box.innerHTML = `
          <strong style="color:#38bdf8; font-size:1.05rem;">✅ طرد المياه وتماسك الإطار السليم (Espulsione dell'acqua):</strong><br>
          • عمق مداس <strong>${this.aqua.treadDepth} مم</strong> يفرغ أطنان المياه في الثانية عبر الأخاديد الطولية والعرضية، محققاً التصاقاً متيناً بالأسفلت.<br>
          • <strong>الحدود القانونية الصارمة:</strong><br>
          &nbsp;&nbsp;🚗 السيارات والشاحنات والمقطورات = <strong>1.6 مم</strong><br>
          &nbsp;&nbsp;🏍️ الدراجات النارية (Motoveicoli) = <strong>1.0 مم</strong><br>
          &nbsp;&nbsp;🛵 السيكلوموتوري (Ciclomotori) = <strong>0.5 مم</strong>
        `;
      }
    } else if (this.activeTab === 'shocks') {
      if (this.shocks.condition === 'healthy') {
        box.style.background = 'rgba(16,185,129,0.12)';
        box.style.border = '1px solid rgba(16,185,129,0.35)';
        box.style.color = '#a7f3d0';
        box.innerHTML = `
          <strong style="color:#34d399; font-size:1.05rem;">✅ ممتص الصدمات السليم (Ammortizzatore efficiente):</strong><br>
          • يخمد تذبذبات النوابض (Molle) فوراً، مما يضمن ثبات سطح الإطار على الأرض ويحافظ على دقة حزمة الضوء المنبعثة من المصابيح الأمامية.<br>
          • يحافظ على مسار السيارة مستقراً دون انغماس زائد للواجهة الأمامية أو انزلاق مؤخرة السيارة.
        `;
      } else {
        box.style.background = 'rgba(245,158,11,0.12)';
        box.style.border = '1px solid rgba(245,158,11,0.35)';
        box.style.color = '#fef3c7';
        box.innerHTML = `
          <strong style="color:#fbbf24; font-size:1.05rem;">⚠️ مخاطر ممتصات الصدمات التالفة أو الفارغة (Ammortizzatori scarichi):</strong><br>
          • <strong>الانغماس الحاد للأمام (Beccheggio elevato):</strong> عند الفرملة تهبط مقدمة المركبة بعنف، فتنحرف حزمة المصابيح الأمامية للأسفل وتقل مسافة الرؤية، ويرتفع خطر انزلاق العجلات الخلفية.<br>
          • <strong>التأرجح في المنحنيات (Rollio accentuated):</strong> تتمايل المركبة لجانبها بشدة في المنعطفات، مما قد يؤدي لانقلابها أو انحرافها عن المسار.<br>
          • <strong>تلف غير منتظم للإطارات:</strong> تآكل متموج لسطح الإطار مع زيادة ملحوظة في مسافة التوقف (Aumento dello spazio di frenatura)!
        `;
      }
    }
  }

  resetSimulation() {
    // Reset ABS to start driving from left
    this.abs.carX = 50;
    this.abs.carY = 180; // right lane
    this.abs.carAngle = 0;
    this.abs.currentSpeed = this.abs.speed;
    this.abs.phase = 'driving';
    this.abs.skidMarks = [];
    this.abs.pulsingTire = 0;
    this.abs.finishTimer = 0;
    this.abs.crashFlash = 0;

    // Reset Aquaplaning
    this.aqua.bubbles = [];
    for (let i = 0; i < 20; i++) {
      this.aqua.bubbles.push({
        x: Math.random() * 900,
        y: 280 + Math.random() * 25,
        speed: 2 + Math.random() * 4,
        size: 1 + Math.random() * 3
      });
    }

    // Reset Shocks
    this.shocks.cycleTimer = 0;
    this.shocks.bodyRoll = 0;
    this.shocks.bodyPitch = 0;

    const badge = document.getElementById('vmsStatusBadge');
    if (badge) {
      badge.textContent = 'سير طبيعي على الطريق';
      badge.style.background = 'rgba(16,185,129,0.25)';
      badge.style.borderColor = '#10b981';
      badge.style.color = '#34d399';
    }
  }

  triggerAbsBrake() {
    if (this.abs.phase === 'braking') return;
    this.abs.phase = 'braking';
    const badge = document.getElementById('vmsStatusBadge');
    if (badge) {
      badge.textContent = this.abs.enabled ? '🚨 فرملة طارئة + تفادي بالمقود (ABS نشط)!' : '🚨 فرملة طارئة (انغلاق العجلات وانزلاق مستقيم!)';
      badge.style.background = this.abs.enabled ? 'rgba(56,189,248,0.25)' : 'rgba(239,68,68,0.25)';
      badge.style.borderColor = this.abs.enabled ? '#38bdf8' : '#ef4444';
      badge.style.color = this.abs.enabled ? '#7dd3fc' : '#fca5a5';
    }
    this.playChime(this.abs.enabled ? 'abs-pulse' : 'skid');
  }

  startLoop() {
    const loop = (timestamp) => {
      const dt = Math.min(50, timestamp - (this.lastTime || timestamp));
      this.lastTime = timestamp;
      this.update(dt);
      this.render();
      this.animationId = requestAnimationFrame(loop);
    };
    this.animationId = requestAnimationFrame(loop);
  }

  update(dt) {
    if (this.activeTab === 'abs') {
      this.updateAbs(dt);
    } else if (this.activeTab === 'aquaplaning') {
      this.updateAquaplaning(dt);
    } else if (this.activeTab === 'shocks') {
      this.updateShocks(dt);
    }
  }

  updateAbs(dt) {
    const dtSec = dt / 1000;

    // Road friction
    let friction = 0.85;
    if (this.abs.roadCondition === 'bagnato') friction = 0.52;
    if (this.abs.roadCondition === 'ghiaccio') friction = 0.22;

    if (this.abs.phase === 'driving') {
      // Car is driving at selected speed
      const moveStep = this.abs.currentSpeed * dtSec * 3.8;
      this.abs.carX += moveStep;
      this.abs.carAngle = 0;

      // Auto trigger brake when approaching obstacle at x=340
      if (this.abs.carX >= 340) {
        this.triggerAbsBrake();
      }
    } else if (this.abs.phase === 'braking') {
      // Deceleration rate
      const decel = (this.abs.enabled ? 34 : 26) * friction;
      this.abs.currentSpeed = Math.max(0, this.abs.currentSpeed - (decel * dtSec * 2.8));

      const moveStep = this.abs.currentSpeed * dtSec * 3.8;
      this.abs.carX += moveStep * Math.cos(this.abs.carAngle);
      this.abs.carY += moveStep * Math.sin(this.abs.carAngle);

      if (this.abs.enabled) {
        // WITH ABS: wheels pulse, driver steers to upper lane (y: 180 -> 100)
        this.abs.pulsingTire += dt * 0.05;
        if (Math.random() < 0.2) this.playChime('abs-pulse');

        if (this.abs.carX > 340 && this.abs.carX < 500 && this.abs.carY > 105) {
          // Turn left
          this.abs.carAngle = -0.32;
        } else if (this.abs.carX >= 500 && this.abs.carAngle < 0) {
          // Straighten in overtaking lane
          this.abs.carAngle = 0.04;
          if (this.abs.carY <= 105) this.abs.carAngle = 0;
        } else {
          this.abs.carAngle = 0;
        }
      } else {
        // WITHOUT ABS: wheels locked, skid marks on asphalt, cannot steer at all!
        if (Math.random() < 0.12) this.playChime('skid');
        this.abs.skidMarks.push({
          x1: this.abs.carX - 24,
          y1: this.abs.carY - 14,
          x2: this.abs.carX - 24,
          y2: this.abs.carY + 14
        });
        this.abs.carAngle = 0; // zero steering!
      }

      // Check collision or safe stop
      const distToObstacle = Math.hypot(this.abs.carX - this.abs.obstacleX, this.abs.carY - this.abs.obstacleY);

      if (!this.abs.enabled && distToObstacle < 55) {
        // Crash into obstacle!
        this.abs.phase = 'finished';
        this.abs.currentSpeed = 0;
        this.abs.crashFlash = 1.0;
        this.playChime('crash');
        const badge = document.getElementById('vmsStatusBadge');
        if (badge) {
          badge.textContent = '💥 حادث اصطدام بالعائق! العجلات انغلقت واستحال التوجيه (Bloccaggio)!';
          badge.style.background = 'rgba(239,68,68,0.35)';
          badge.style.borderColor = '#ef4444';
          badge.style.color = '#f87171';
        }
      } else if (this.abs.currentSpeed <= 0.5) {
        // Stopped
        this.abs.phase = 'finished';
        this.abs.currentSpeed = 0;
        const badge = document.getElementById('vmsStatusBadge');
        if (badge) {
          if (this.abs.enabled) {
            badge.textContent = '✅ تفادي وتوقف آمن تماماً! استمر السائق في التوجيه بفضل ABS (Sterzabilità)!';
            badge.style.background = 'rgba(16,185,129,0.3)';
            badge.style.borderColor = '#10b981';
            badge.style.color = '#34d399';
          } else {
            badge.textContent = '⚠️ توقفت السيارة لكنها انزلقت مستقيماً وفقدت السيطرة على مسارها!';
          }
        }
      }
    } else if (this.abs.phase === 'finished') {
      // Hold result, then loop if autoPlay is true
      if (this.abs.crashFlash > 0) this.abs.crashFlash -= dtSec * 1.5;
      this.abs.finishTimer += dtSec;
      if (this.abs.autoPlay && this.abs.finishTimer > 2.8) {
        this.resetSimulation();
      }
    }

    // Telemetry display
    const telemetry = document.getElementById('vmsTelemetry');
    if (telemetry) {
      telemetry.textContent = `SPD: ${Math.round(this.abs.currentSpeed)} km/h | ABS: ${this.abs.enabled ? 'ACTIVE (Sterzabile)' : 'DISABLED (Bloccato)'} | ROAD: ${this.abs.roadCondition.toUpperCase()}`;
    }
  }

  updateAquaplaning(dt) {
    const dtSec = dt / 1000;
    // Critical speed: ~ 45 + treadDepth * 7.5
    let criticalSpeed = 45 + (this.aqua.treadDepth * 7.5);
    let ratio = Math.max(0, Math.min(1, (this.aqua.speed - criticalSpeed + 20) / 35));
    this.aqua.liftAmount += (ratio - this.aqua.liftAmount) * 0.1;

    // Continuous tire rotation
    this.aqua.tireRotation += (this.aqua.speed * 0.08) * (1 - this.aqua.liftAmount * 0.85);

    // Continuous bubbles/spray animation
    this.aqua.bubbles.forEach(b => {
      b.x -= b.speed * (this.aqua.speed / 40);
      if (b.x < 0) b.x = 900;
    });

    const telemetry = document.getElementById('vmsTelemetry');
    if (telemetry) {
      const grip = Math.round((1 - this.aqua.liftAmount) * 100);
      telemetry.textContent = `SPD: ${this.aqua.speed} km/h | TREAD: ${this.aqua.treadDepth} mm | GRIP: ${grip}% | AQUAPLANING: ${Math.round(this.aqua.liftAmount*100)}%`;
    }

    const badge = document.getElementById('vmsStatusBadge');
    if (badge) {
      if (this.aqua.liftAmount > 0.65) {
        badge.textContent = '🌊 طفو مائي تام (Aquaplaning)! انفصال الإطار عن الأسفلت!';
        badge.style.background = 'rgba(239,68,68,0.3)';
        badge.style.borderColor = '#ef4444';
        badge.style.color = '#fca5a5';
      } else if (this.aqua.liftAmount > 0.3) {
        badge.textContent = '⚠️ بداية انزلاق مائي وخلخلة في التماسك (Grip parziale)';
        badge.style.background = 'rgba(245,158,11,0.3)';
        badge.style.borderColor = '#f59e0b';
        badge.style.color = '#fde68a';
      } else {
        badge.textContent = '✅ التصاق ممتاز وطرد كامل للمياه (Aderenza ottimale)';
        badge.style.background = 'rgba(16,185,129,0.25)';
        badge.style.borderColor = '#10b981';
        badge.style.color = '#34d399';
      }
    }
  }

  updateShocks(dt) {
    const dtSec = dt / 1000;
    this.shocks.cycleTimer += dtSec;
    // Repeat cycle every 3.5 seconds
    const t = this.shocks.cycleTimer % this.shocks.cycleDuration;
    const isWorn = this.shocks.condition === 'worn';
    
    if (this.shocks.testType === 'braking') {
      // Pitching (Beccheggio) on braking surge
      if (isWorn) {
        // violent bounce, slow damping
        this.shocks.bodyPitch = Math.sin(t * 7) * 15 * Math.exp(-t * 0.4);
      } else {
        // 1 smooth dip, instant damping
        this.shocks.bodyPitch = Math.sin(t * 9) * 4.5 * Math.exp(-t * 2.2);
      }
    } else {
      // Cornering (Rollio) on sudden turn
      if (isWorn) {
        this.shocks.bodyRoll = Math.sin(t * 6) * 18 * Math.exp(-t * 0.35);
      } else {
        this.shocks.bodyRoll = Math.sin(t * 8) * 5 * Math.exp(-t * 2.2);
      }
    }

    const telemetry = document.getElementById('vmsTelemetry');
    if (telemetry) {
      telemetry.textContent = `MANEUVER: ${this.shocks.testType.toUpperCase()} | SHOCKS: ${this.shocks.condition.toUpperCase()} | PITCH: ${this.shocks.bodyPitch.toFixed(1)}° | ROLL: ${this.shocks.bodyRoll.toFixed(1)}°`;
    }

    const badge = document.getElementById('vmsStatusBadge');
    if (badge) {
      if (isWorn) {
        badge.textContent = this.shocks.testType === 'braking' ? '⚠️ تمايل أمامي عنيف (Beccheggio) وانخفاض مدى الأضواء!' : '⚠️ ميلان جانبي خطير (Rollio) وفقدان الاتزان!';
        badge.style.background = 'rgba(239,68,68,0.25)';
        badge.style.borderColor = '#ef4444';
        badge.style.color = '#fca5a5';
      } else {
        badge.textContent = '✅ تماسك وتوازن مستقر ومخمد فوراً (Stabilità controllata)';
        badge.style.background = 'rgba(16,185,129,0.25)';
        badge.style.borderColor = '#10b981';
        badge.style.color = '#34d399';
      }
    }
  }

  render() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    if (this.activeTab === 'abs') {
      this.renderAbs();
    } else if (this.activeTab === 'aquaplaning') {
      this.renderAquaplaning();
    } else if (this.activeTab === 'shocks') {
      this.renderShocks();
    }
  }

  renderAbs() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    // Road surface
    let roadGrad = ctx.createLinearGradient(0, 0, 0, h);
    if (this.abs.roadCondition === 'asciutto') {
      roadGrad.addColorStop(0, '#1e293b');
      roadGrad.addColorStop(1, '#0f172a');
    } else if (this.abs.roadCondition === 'bagnato') {
      roadGrad.addColorStop(0, '#0c2238');
      roadGrad.addColorStop(1, '#081726');
    } else {
      roadGrad.addColorStop(0, '#2b394d');
      roadGrad.addColorStop(1, '#1e2c3d');
    }
    ctx.fillStyle = roadGrad;
    ctx.fillRect(0, 0, w, h);

    // Road borders
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(0, 45);
    ctx.lineTo(w, 45);
    ctx.moveTo(0, 255);
    ctx.lineTo(w, 255);
    ctx.stroke();

    // Center dashed lane separator (2 lanes: upper at y=105, lower at y=180)
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 3;
    ctx.setLineDash([25, 20]);
    // Moving dash offset to show vehicle motion!
    const dashOffset = (this.abs.phase === 'driving' ? -Date.now() * 0.12 : 0) % 45;
    ctx.lineDashOffset = dashOffset;
    ctx.beginPath();
    ctx.moveTo(0, 150);
    ctx.lineTo(w, 150);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.lineDashOffset = 0;

    // Lane labels
    ctx.fillStyle = 'rgba(255,255,255,0.2)';
    ctx.font = 'bold 12px Tahoma, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText('حارة التجاوز والتفادي (Corsia di sorpasso)', w - 20, 75);
    ctx.fillText('الحارة الأساسية (Corsia di marcia)', w - 20, 235);

    // Skid marks if without ABS
    if (this.abs.skidMarks.length > 0) {
      ctx.fillStyle = 'rgba(10, 10, 10, 0.8)';
      this.abs.skidMarks.forEach(sm => {
        ctx.fillRect(sm.x1, sm.y1, 8, 4);
        ctx.fillRect(sm.x2, sm.y2, 8, 4);
      });
    }

    // Draw Obstacle (at lower lane: x=680, y=180)
    ctx.save();
    ctx.translate(this.abs.obstacleX, this.abs.obstacleY);
    // Warning striped barrier
    ctx.fillStyle = '#dc2626';
    ctx.fillRect(-22, -26, 44, 52);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-18, -20, 36, 10);
    ctx.fillRect(-18, 10, 36, 10);
    // Flashing warning beacon
    ctx.beginPath();
    ctx.arc(0, -34, 8, 0, Math.PI * 2);
    ctx.fillStyle = (Math.floor(Date.now() / 200) % 2 === 0) ? '#f59e0b' : '#78350f';
    ctx.fill();
    ctx.restore();

    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 11px Tahoma, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('عائق فجائي 🛑', this.abs.obstacleX, this.abs.obstacleY + 44);

    // Braking Line Marker (at x=340)
    ctx.strokeStyle = 'rgba(245, 158, 11, 0.6)';
    ctx.lineWidth = 2;
    ctx.setLineDash([6, 6]);
    ctx.beginPath();
    ctx.moveTo(340, 45);
    ctx.lineTo(340, 255);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#fbbf24';
    ctx.font = '10px Tahoma, sans-serif';
    ctx.fillText('نقطة الفرملة الطارئة', 340, 38);

    // Draw Vehicle (top-down view)
    ctx.save();
    ctx.translate(this.abs.carX, this.abs.carY);
    ctx.rotate(this.abs.carAngle);

    // Vehicle Shadow
    ctx.fillStyle = 'rgba(0,0,0,0.45)';
    ctx.beginPath();
    ctx.roundRect(-36, -20, 72, 40, 8);
    ctx.fill();

    // Vehicle Body
    ctx.fillStyle = this.abs.enabled ? '#0284c7' : '#e11d48';
    ctx.beginPath();
    ctx.roundRect(-34, -18, 68, 36, 6);
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Windshield & Roof
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(-8, -14, 22, 28);
    ctx.fillStyle = '#38bdf8';
    ctx.fillRect(14, -13, 8, 26); // front windshield

    // Headlight Beams
    ctx.fillStyle = 'rgba(254, 240, 138, 0.28)';
    ctx.beginPath();
    ctx.moveTo(34, -12);
    ctx.lineTo(140, -36);
    ctx.lineTo(140, 36);
    ctx.lineTo(34, 12);
    ctx.closePath();
    ctx.fill();

    // 4 Wheels
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(16, -21, 14, 5); // Front left
    ctx.fillRect(16, 16, 14, 5);  // Front right
    ctx.fillRect(-26, -21, 14, 5); // Rear left
    ctx.fillRect(-26, 16, 14, 5);  // Rear right

    // If ABS active and braking: pulsating green halo on wheels
    if (this.abs.enabled && this.abs.phase === 'braking') {
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 2.5;
      ctx.strokeRect(14, -23, 18, 8);
      ctx.strokeRect(14, 14, 18, 8);
    }

    ctx.restore();

    // Crash flash effect
    if (this.abs.crashFlash > 0) {
      ctx.fillStyle = `rgba(239, 68, 68, ${this.abs.crashFlash * 0.45})`;
      ctx.fillRect(0, 0, w, h);
    }
  }

  renderAquaplaning() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    // Background: Dark workshop cutaway
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, w, h);

    // Road layer (Asphalt cross section)
    const roadY = 270;
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, roadY, w, h - roadY);

    // Water puddle layer on top of road
    const waterDepthPx = 25;
    const waterGrad = ctx.createLinearGradient(0, roadY - waterDepthPx, 0, roadY);
    waterGrad.addColorStop(0, 'rgba(56, 189, 248, 0.45)');
    waterGrad.addColorStop(1, 'rgba(14, 165, 233, 0.85)');
    ctx.fillStyle = waterGrad;
    ctx.fillRect(0, roadY - waterDepthPx, w, waterDepthPx);

    // Water surface waves & bubbles
    ctx.fillStyle = 'rgba(255,255,255,0.7)';
    this.aqua.bubbles.forEach(b => {
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.size, 0, Math.PI * 2);
      ctx.fill();
    });

    // Tire Cross Section
    ctx.save();
    const tireCenterX = w / 2;
    // Lift tire if aquaplaning occurs
    const tireCenterY = 160 - (this.aqua.liftAmount * 18);
    const tireRadius = 110;

    ctx.translate(tireCenterX, tireCenterY);

    // Tire outer rubber ring
    ctx.beginPath();
    ctx.arc(0, 0, tireRadius, 0, Math.PI * 2);
    ctx.fillStyle = '#1e2430';
    ctx.fill();
    ctx.lineWidth = 14;
    ctx.strokeStyle = '#0f172a';
    ctx.stroke();

    // Wheel Alloy Rim (Center)
    ctx.beginPath();
    ctx.arc(0, 0, 55, 0, Math.PI * 2);
    ctx.fillStyle = '#475569';
    ctx.fill();
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 4;
    ctx.stroke();

    // Rim spokes (rotating)
    ctx.save();
    ctx.rotate(this.aqua.tireRotation);
    for (let i = 0; i < 5; i++) {
      ctx.rotate((Math.PI * 2) / 5);
      ctx.fillStyle = '#cbd5e1';
      ctx.fillRect(-6, -50, 12, 45);
    }
    ctx.restore();

    // Tread Grooves (Madass) pattern around outer circumference
    ctx.save();
    ctx.rotate(this.aqua.tireRotation);
    const numGrooves = 24;
    const grooveDepth = (this.aqua.treadDepth / 8.0) * 12; // visual depth px

    for (let i = 0; i < numGrooves; i++) {
      ctx.rotate((Math.PI * 2) / numGrooves);
      if (grooveDepth > 1) {
        ctx.fillStyle = '#020617';
        ctx.fillRect(-3, tireRadius - grooveDepth, 6, grooveDepth);
      }
    }
    ctx.restore();

    ctx.restore();

    // Hydrodynamic Water Wedge (Cuneo d'acqua) in front of the tire
    ctx.save();
    const wedgeX = tireCenterX + 85;
    if (this.aqua.liftAmount > 0.1) {
      ctx.fillStyle = 'rgba(56, 189, 248, 0.75)';
      ctx.beginPath();
      ctx.moveTo(tireCenterX - 40, roadY - 4);
      ctx.lineTo(tireCenterX + 90, roadY - waterDepthPx - (this.aqua.liftAmount * 12));
      ctx.lineTo(tireCenterX + 120, roadY);
      ctx.closePath();
      ctx.fill();

      // Splashing water particles
      ctx.fillStyle = '#e0f2fe';
      for (let i = 0; i < 8; i++) {
        ctx.fillRect(wedgeX + (Math.random() * 20), roadY - 10 - (Math.random() * 25), 3, 3);
      }
    }
    ctx.restore();

    // Explanatory Overlays on Canvas
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 13px Tahoma, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(`عمق النقشة: ${this.aqua.treadDepth} مم`, w - 25, 40);
    ctx.fillText(`السرعة: ${this.aqua.speed} كم/ساعة`, w - 25, 65);
    ctx.fillText(`نسبة التلامس والتماسك (Aderenza): ${Math.round((1 - this.aqua.liftAmount) * 100)}%`, w - 25, 90);

    // Tread gauge visual indicator bar
    const barW = 160;
    const barH = 12;
    const barX = w - 185;
    const barY = 105;
    ctx.fillStyle = '#334155';
    ctx.fillRect(barX, barY, barW, barH);
    const fillW = (this.aqua.treadDepth / 8.0) * barW;
    ctx.fillStyle = this.aqua.treadDepth >= 1.6 ? '#10b981' : '#ef4444';
    ctx.fillRect(barX, barY, fillW, barH);
    ctx.strokeStyle = '#64748b';
    ctx.strokeRect(barX, barY, barW, barH);

    // Legal limit line (1.6mm)
    const limitX = barX + (1.6 / 8.0) * barW;
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(limitX, barY - 4);
    ctx.lineTo(limitX, barY + barH + 4);
    ctx.stroke();

    ctx.fillStyle = '#fde68a';
    ctx.font = '10px Tahoma, sans-serif';
    ctx.fillText('1.6mm الحد الأدنى الإلزامي', limitX + 45, barY + 24);
  }

  renderShocks() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    // Background
    ctx.fillStyle = '#0b1120';
    ctx.fillRect(0, 0, w, h);

    // Ground line
    const groundY = 260;
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(40, groundY);
    ctx.lineTo(w - 40, groundY);
    ctx.stroke();

    const carCenterX = w / 2;
    const isBraking = this.shocks.testType === 'braking';

    if (isBraking) {
      // Side Profile View (Pitching / Beccheggio)
      const carBaseY = 210;
      const pitchRad = (this.shocks.bodyPitch * Math.PI) / 180;

      // Wheels on ground
      ctx.fillStyle = '#1e293b';
      // Front wheel
      ctx.beginPath();
      ctx.arc(carCenterX - 110, groundY - 22, 22, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 4;
      ctx.stroke();
      // Rear wheel
      ctx.beginPath();
      ctx.arc(carCenterX + 110, groundY - 22, 22, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 4;
      ctx.stroke();

      // Car body tilting with pitch
      ctx.save();
      ctx.translate(carCenterX, carBaseY);
      ctx.rotate(-pitchRad); // tilt front down

      // Car Body Silhouette
      ctx.fillStyle = '#0284c7';
      ctx.beginPath();
      ctx.moveTo(-160, 10);
      ctx.lineTo(160, 10);
      ctx.lineTo(150, -25);
      ctx.lineTo(60, -30);
      ctx.lineTo(10, -75);
      ctx.lineTo(-90, -75);
      ctx.lineTo(-140, -30);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Windows
      ctx.fillStyle = '#0f172a';
      ctx.beginPath();
      ctx.moveTo(5, -70);
      ctx.lineTo(50, -30);
      ctx.lineTo(-20, -30);
      ctx.lineTo(-20, -70);
      ctx.closePath();
      ctx.fill();

      // Headlight Beam
      ctx.fillStyle = 'rgba(253, 224, 71, 0.35)';
      ctx.beginPath();
      ctx.moveTo(-155, -5);
      ctx.lineTo(-340, 20 + (this.shocks.bodyPitch * 8));
      ctx.lineTo(-340, 90 + (this.shocks.bodyPitch * 8));
      ctx.lineTo(-155, 10);
      ctx.closePath();
      ctx.fill();

      ctx.restore();

      // Text notes
      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 13px Tahoma, sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText('اختبار الفرملة الحادة: حركة الانغماس للأمام (Beccheggio)', w - 30, 40);
      ctx.fillStyle = this.shocks.condition === 'worn' ? '#f87171' : '#34d399';
      ctx.fillText(this.shocks.condition === 'worn' ? '⚠️ ممتص صدمات تالف: الواجهة تهبط بعنف وتنحرف الأضواء!' : '✅ ممتص صدمات سليم: ثبات فوري وإخماد تام', w - 30, 68);

    } else {
      // Rear Profile View (Rolling / Rollio)
      const carBaseY = 190;
      const rollRad = (this.shocks.bodyRoll * Math.PI) / 180;

      // Tires on road
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(carCenterX - 105, groundY - 40, 28, 40); // left tire
      ctx.fillRect(carCenterX + 77, groundY - 40, 28, 40);  // right tire

      // Body tilting with roll
      ctx.save();
      ctx.translate(carCenterX, carBaseY);
      ctx.rotate(rollRad);

      // Rear Body Silhouette
      ctx.fillStyle = '#0284c7';
      ctx.beginPath();
      ctx.roundRect(-100, -70, 200, 90, [15, 15, 6, 6]);
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Rear windshield
      ctx.fillStyle = '#0f172a';
      ctx.beginPath();
      ctx.roundRect(-75, -60, 150, 45, 8);
      ctx.fill();

      // Rear taillights
      ctx.fillStyle = '#ef4444';
      ctx.fillRect(-92, -10, 22, 14);
      ctx.fillRect(70, -10, 22, 14);

      // License plate
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(-28, 2, 56, 14);

      ctx.restore();

      // Text notes
      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 13px Tahoma, sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText('اختبار المنعطف الحاد: التأرجح والميلان الجانبي (Rollio)', w - 30, 40);
      ctx.fillStyle = this.shocks.condition === 'worn' ? '#f87171' : '#34d399';
      ctx.fillText(this.shocks.condition === 'worn' ? '⚠️ ممتص صدمات تالف: تأرجح جانبي حاد يهدد بفقدان السيطرة!' : '✅ ممتص سليم: المركبة تحافظ على مسارها الأفقي بثبات', w - 30, 68);
    }
  }
}

// Global initialization helper
window.initVehicleMechanicsStudio = function(containerId) {
  return new VehicleMechanicsStudio(containerId);
};

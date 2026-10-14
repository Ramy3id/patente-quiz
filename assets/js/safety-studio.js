/**
 * SAFETY STUDIO - STUDIO INTERATTIVO SICUREZZA STRADALE (CAPITOLO 19)
 * 60 FPS HTML5 Canvas Interactive Simulator
 * Modes:
 *   1. Crash Restraint Simulation (Cinture + Pretensionatore + Airbag in millisecondi)
 *   2. Child Restraint & ISOFIX Calculator (Regola 1,50 m e Disattivazione Airbag)
 *   3. Helmet & Motorcycle Gear Inspector (Casco ECE 22.06 e Abbigliamento Tecnico)
 */

(function () {
  'use strict';

  // Sound Engine using Web Audio API
  let audioCtx = null;
  function getAudioCtx() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  function playSound(type) {
    try {
      const ctx = getAudioCtx();
      if (!ctx) return;
      const now = ctx.currentTime;

      if (type === 'pyro') {
        // Pyrotechnic pop/snap
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(320, now);
        osc.frequency.exponentialRampToValueAtTime(60, now + 0.08);
        gain.gain.setValueAtTime(0.35, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.08);
      } else if (type === 'airbag') {
        // Airbag inflation whoosh / thud
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(140, now);
        osc.frequency.exponentialRampToValueAtTime(45, now + 0.16);
        gain.gain.setValueAtTime(0.4, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.16);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.16);
      } else if (type === 'click') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, now);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.04);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.04);
      } else if (type === 'danger') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(280, now);
        osc.frequency.setValueAtTime(220, now + 0.1);
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.25);
      } else if (type === 'success') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(523, now);
        osc.frequency.setValueAtTime(659, now + 0.08);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.2);
      }
    } catch (e) {
      // Audio fallback silent
    }
  }

  // State Management
  const state = {
    mode: 'crash', // 'crash' | 'isofix' | 'gear'
    
    // Mode 1: Crash
    crash: {
      speedKmH: 50,
      hasBelt: true,
      simulating: false,
      msElapsed: 0,
      maxMs: 140,
      lastTimestamp: 0,
      resultTextAr: 'اضغط على زر (بدء محاكاة الاصطدام) لمعاينة دورة عمل الأجهزة بالمللي ثانية.',
      resultTextIt: 'Premi "Avvia Simulazione Impatto" per osservare la sequenza in millisecondi.'
    },

    // Mode 2: ISOFIX & Child Seat
    child: {
      heightCm: 110,
      weightKg: 18,
      seatPosition: 'rear', // 'rear' | 'front'
      facing: 'forward',    // 'forward' | 'rearward'
      airbagActive: true,
      isDanger: false,
      statusAr: '',
      statusIt: ''
    },

    // Mode 3: Helmet & Gear
    gear: {
      helmetType: 'integrale', // 'integrale' | 'jet' | 'danneggiato'
      strapFastened: true,
      cleanVisor: true,
      hasGloves: true,
      hasBoots: true,
      hasJacket: true,
      score: 100,
      auditTextAr: '',
      auditTextIt: ''
    }
  };

  // DOM Elements
  let canvas, ctx;
  let animFrameId = null;

  function initStudio() {
    canvas = document.getElementById('safetyCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    // Setup high-DPI
    setupCanvasDPI();
    window.addEventListener('resize', () => {
      setupCanvasDPI();
      renderCurrentMode();
    });

    bindEvents();
    evaluateChildSafety();
    evaluateGearSafety();
    startAnimationLoop();
  }

  function setupCanvasDPI() {
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.resetTransform();
    ctx.scale(dpr, dpr);
  }

  function setMode(newMode) {
    state.mode = newMode;
    document.querySelectorAll('.safety-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === newMode);
    });

    document.querySelectorAll('.safety-panel-ctrl').forEach(p => {
      p.style.display = p.dataset.panel === newMode ? 'block' : 'none';
    });

    playSound('click');
    if (newMode === 'crash') {
      state.crash.simulating = false;
      state.crash.msElapsed = 0;
    }
    renderCurrentMode();
  }

  function bindEvents() {
    // Tab switching
    document.querySelectorAll('.safety-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        setMode(btn.dataset.mode);
      });
    });

    // --- Mode 1 Controls ---
    const speedSlider = document.getElementById('crashSpeedSlider');
    const speedVal = document.getElementById('crashSpeedVal');
    if (speedSlider) {
      speedSlider.addEventListener('input', (e) => {
        state.crash.speedKmH = parseInt(e.target.value, 10);
        if (speedVal) speedVal.textContent = state.crash.speedKmH + ' km/h';
      });
    }

    const beltCheck = document.getElementById('crashBeltCheck');
    if (beltCheck) {
      beltCheck.addEventListener('change', (e) => {
        state.crash.hasBelt = e.target.checked;
        playSound('click');
      });
    }

    const startBtn = document.getElementById('crashStartBtn');
    if (startBtn) {
      startBtn.addEventListener('click', () => {
        startCrashSimulation();
      });
    }

    // --- Mode 2 Controls ---
    const heightSlider = document.getElementById('childHeightSlider');
    const heightVal = document.getElementById('childHeightVal');
    if (heightSlider) {
      heightSlider.addEventListener('input', (e) => {
        state.child.heightCm = parseInt(e.target.value, 10);
        if (heightVal) heightVal.textContent = state.child.heightCm + ' cm';
        evaluateChildSafety();
      });
    }

    const seatPosSelect = document.getElementById('childSeatPos');
    if (seatPosSelect) {
      seatPosSelect.addEventListener('change', (e) => {
        state.child.seatPosition = e.target.value;
        evaluateChildSafety();
      });
    }

    const facingSelect = document.getElementById('childFacing');
    if (facingSelect) {
      facingSelect.addEventListener('change', (e) => {
        state.child.facing = e.target.value;
        evaluateChildSafety();
      });
    }

    const airbagToggle = document.getElementById('childAirbagToggle');
    if (airbagToggle) {
      airbagToggle.addEventListener('change', (e) => {
        state.child.airbagActive = e.target.checked;
        playSound('click');
        evaluateChildSafety();
      });
    }

    // --- Mode 3 Controls ---
    const helmetTypeSelect = document.getElementById('gearHelmetType');
    if (helmetTypeSelect) {
      helmetTypeSelect.addEventListener('change', (e) => {
        state.gear.helmetType = e.target.value;
        evaluateGearSafety();
      });
    }

    ['gearStrapCheck', 'gearVisorCheck', 'gearGlovesCheck', 'gearBootsCheck', 'gearJacketCheck'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('change', () => {
          if (id === 'gearStrapCheck') state.gear.strapFastened = el.checked;
          if (id === 'gearVisorCheck') state.gear.cleanVisor = el.checked;
          if (id === 'gearGlovesCheck') state.gear.hasGloves = el.checked;
          if (id === 'gearBootsCheck') state.gear.hasBoots = el.checked;
          if (id === 'gearJacketCheck') state.gear.hasJacket = el.checked;
          playSound('click');
          evaluateGearSafety();
        });
      }
    });
  }

  // --- Mode 1 Logic ---
  let soundPlayedPyro = false;
  let soundPlayedAirbag = false;

  function startCrashSimulation() {
    state.crash.simulating = true;
    state.crash.msElapsed = 0;
    state.crash.lastTimestamp = performance.now();
    soundPlayedPyro = false;
    soundPlayedAirbag = false;
    playSound('click');
  }

  function updateCrashTimeline(now) {
    if (!state.crash.simulating) return;

    const dt = now - state.crash.lastTimestamp;
    state.crash.lastTimestamp = now;

    // Simulation speed factor (1 ms sim = ~15 ms real time to make it visually trackable)
    state.crash.msElapsed += (dt * 0.08);

    // Audio cue triggers at precise simulated milliseconds
    if (state.crash.hasBelt && state.crash.msElapsed >= 15 && !soundPlayedPyro) {
      playSound('pyro');
      soundPlayedPyro = true;
    }
    if (state.crash.msElapsed >= 30 && !soundPlayedAirbag) {
      playSound('airbag');
      soundPlayedAirbag = true;
    }

    if (state.crash.msElapsed >= state.crash.maxMs) {
      state.crash.msElapsed = state.crash.maxMs;
      state.crash.simulating = false;
      updateCrashReport();
    }
  }

  function updateCrashReport() {
    const reportAr = document.getElementById('crashReportAr');
    const reportIt = document.getElementById('crashReportIt');
    const speed = state.crash.speedKmH;

    if (!state.crash.hasBelt) {
      const gForce = Math.round(speed * 0.95);
      const msgAr = `⚠️ خطر مميت: لعدم ربط حزام الأمان، اندفع الراكب للأمام بقوة تباطؤ هائلة (${gForce}G) وارتطم بالزجاج الأمامي وعجلة القيادة قبل انفتاح الوسادة الهوائية بكاملها، مما يحولها إلى أداة خطر بدل أن تحميه!`;
      const msgIt = `PERICOLO MORTALE: Senza cintura di sicurezza, il corpo viene proiettato in avanti subendo una decelerazione letale (${gForce}G) con impatto contro il parabrezza e volante!`;
      if (reportAr) reportAr.innerHTML = msgAr;
      if (reportIt) reportIt.innerHTML = msgIt;
      playSound('danger');
    } else {
      const gForce = Math.round(speed * 0.28);
      const msgAr = `✅ نجاة مؤكدة: اشتغل جهاز الشد المسبق (Pretensionatore) في أول 15 ms وسحب الحزام بإحكام مانعاً القذف. في 30 ms فتحت الوسادة الهوائية بسرعة 300 كم/س واستقبلت الصدمة، ثم تفرغت في 80 ms لتمكين التنفس. (قوة التباطؤ خُفضت إلى ${gForce}G الآمنة).`;
      const msgIt = `PROTEZIONE OTTIMALE: Il pretensionatore ha bloccato il gioco della cintura in 15 ms; l'airbag ha assorbito l'impatto a 30 ms sfiatando a 80 ms. Decelerazione ridotta a ${gForce}G.`;
      if (reportAr) reportAr.innerHTML = msgAr;
      if (reportIt) reportIt.innerHTML = msgIt;
      playSound('success');
    }
  }

  // --- Mode 2 Logic: Child Seat & Airbag Switch ---
  function evaluateChildSafety() {
    const h = state.child.heightCm;
    const isFront = state.child.seatPosition === 'front';
    const isRearward = state.child.facing === 'rearward';
    const airbagOn = state.child.airbagActive;

    let danger = false;
    let ar = '';
    let it = '';

    // Check mandatory child restraint (< 1.50 m)
    if (h < 150) {
      if (isFront && isRearward && airbagOn) {
        danger = true;
        ar = `🚨 فخ وزاري قاتل (PERICOLO GRAVISSIMO): تركيب مقعد الرضيع في المقعد الأمامي عكس اتجاه السير مع وسادة هوائية مفعلة (Airbag ATTIVO) ممنوع قانوناً قطيعاً! قوة انفجار الإيرباج تسحق المقعد على ظهر الكرسي وتسبب الوفاة فوراً.`;
        it = `VIETATO ASSOLUTAMENTE: Seggiolino contrario al senso di marcia sul sedile anteriore con AIRBAG ATTIVO! L'airbag DEVE essere obbligatoriamente disattivato.`;
      } else {
        const typeStr = h < 105 ? 'مقعد مخصص للرضع (Ovetto / Gruppo 0/0+)' : 'مقعد أطفال معتمد بنظام ISOFIX أو وسادة رافعة (Rialzo/Alzatina)';
        const typeStrIt = h < 105 ? 'Ovetto senso contrario (Gruppo 0/0+)' : 'Seggiolino con ancoraggi ISOFIX o alzatina';
        ar = `👶 الراكب أقل من 1.50 متراً (طوله ${h} سم): يلزم قانوناً استخدام ${typeStr}. استخدام حزام الأمان العادي وحده غير كافٍ ومخالف للمادة 172.`;
        it = `Statura inferiore a 1,50 m (${h} cm): Ritenuta per bambini obbligatoria (${typeStrIt}).`;
      }
    } else {
      ar = `🧑 الراكب أطول من 1.50 متراً (طوله ${h} سم): تجاوز عتبة الـ 1.50 متراً، وبالتالي يُسمح له باستخدام حزام الأمان العادي للبالغين بدون مقعد خاص.`;
      it = `Statura pari o superiore a 1,50 m (${h} cm): Può allacciare la normale cintura di sicurezza per adulti.`;
    }

    state.child.isDanger = danger;
    state.child.statusAr = ar;
    state.child.statusIt = it;

    const statArEl = document.getElementById('childStatusAr');
    const statItEl = document.getElementById('childStatusIt');
    const alertBox = document.getElementById('childAlertBox');

    if (statArEl) statArEl.innerHTML = ar;
    if (statItEl) statItEl.innerHTML = it;
    if (alertBox) {
      alertBox.className = danger ? 'safety-alert-box alert-danger' : 'safety-alert-box alert-safe';
    }

    if (danger) playSound('danger');
  }

  // --- Mode 3 Logic: Helmet & Gear Inspector ---
  function evaluateGearSafety() {
    let score = 100;
    const notesAr = [];
    const notesIt = [];

    if (state.gear.helmetType === 'danneggiato') {
      score -= 50;
      notesAr.push('❌ الخوذة تعرضت لصدمة سابقة: المادة الداخلية (Polistirolo espanso EPS) تفقد قدرتها على امتصاص الصدمات بعد أول ضربة قوية حتى لو كانت القشرة الخارجية تبدو سليمة تماماً! يجب استبدالها فوراً.');
      notesIt.push('Il casco ha subito un forte urto: la calotta interna in polistirolo si è deformata permanentemente. Va sostituito anche senza danni visibili!');
    } else if (state.gear.helmetType === 'jet') {
      score -= 10;
      notesAr.push('⚠️ خوذة مفتوحة بدون واقي فك (Demi-Jet): قانونية لكنها تفتقر لحماية الفك والوجه من الصدمات الأمامية.');
      notesIt.push('Casco jet: omologato ma privo di mentoniera protettiva (sigla J anziché P).');
    }

    if (!state.gear.strapFastened) {
      score -= 40;
      notesAr.push('❌ حزام الخوذة (Cinturino sottogola) غير مربوط أو مرتخٍ: مخالفة تسحب نقاط الرخصة وتحرم الراكب من الحماية لأن الخوذة ستتطاير عن الرأس في اللحظة الأولى للحادث!');
      notesIt.push('Cinturino non allacciato: sanzione, decurtazione punti e fermo amministrativo del veicolo!');
    }

    if (!state.gear.cleanVisor) {
      score -= 15;
      notesAr.push('⚠️ الواقية مخدوشة أو داكنة ليلاً: الخدوش تعكس أضواء السيارات المقابلة وتسبب عمى بصري مؤقت (Abbagliamento).');
      notesIt.push('Visiera graffiata o scura di notte: pericolo abbagliamento e visibilità distorta.');
    }

    if (!state.gear.hasGloves) {
      score -= 10;
      notesAr.push('🧤 غياب قفازات الموتوسيكل المعتمدة (EN 13594): يعرض كفوف اليدين للتسلخ والجروح عند السقوط على الأسفلت.');
      notesIt.push('Senza guanti tecnici EN 13594: rischio abrasioni da scivolamento.');
    }

    if (!state.gear.hasBoots) {
      score -= 10;
      notesAr.push('👢 غياب الأحذية المقواة (EN 13634): كاحل القدم (Malleolo) وعظمة الساق معرضة للكسور والحرارة من عادم المحرك.');
      notesIt.push('Senza stivali EN 13634: caviglie e malleoli esposti a fratture e calore.');
    }

    if (!state.gear.hasJacket) {
      score -= 10;
      notesAr.push('🧥 غياب الجاكيت الواقي وحامي الظهر (Paraschiena EN 1621-2): يزيد احتمالية إصابات العمود الفقري الخطيرة.');
      notesIt.push('Senza paraschiena EN 1621-2: elevato rischio di traumi vertebrali.');
    }

    state.gear.score = Math.max(0, score);
    state.gear.auditTextAr = notesAr.join('<br>');
    state.gear.auditTextIt = notesIt.join('<br>');

    const scoreVal = document.getElementById('gearScoreVal');
    const scoreBar = document.getElementById('gearScoreBar');
    const notesArEl = document.getElementById('gearNotesAr');
    const notesItEl = document.getElementById('gearNotesIt');

    if (scoreVal) scoreVal.textContent = state.gear.score + '%';
    if (scoreBar) {
      scoreBar.style.width = state.gear.score + '%';
      scoreBar.style.backgroundColor = state.gear.score > 80 ? '#10b981' : state.gear.score > 50 ? '#f59e0b' : '#ef4444';
    }
    if (notesArEl) notesArEl.innerHTML = state.gear.auditTextAr || '✅ تجهيزات أمان مكتملة ومطابقة لأعلى معايير كود السير!';
    if (notesItEl) notesItEl.innerHTML = state.gear.auditTextIt || 'Dotazione di sicurezza perfetta e conforme alle normative vigenti.';
  }

  // --- Canvas Rendering Loop ---
  function startAnimationLoop() {
    function loop(timestamp) {
      if (state.mode === 'crash') {
        updateCrashTimeline(timestamp);
      }
      renderCurrentMode();
      animFrameId = requestAnimationFrame(loop);
    }
    animFrameId = requestAnimationFrame(loop);
  }

  function renderCurrentMode() {
    if (!canvas || !ctx) return;
    const w = canvas.getBoundingClientRect().width;
    const h = canvas.getBoundingClientRect().height;

    ctx.clearRect(0, 0, w, h);

    if (state.mode === 'crash') {
      drawCrashScene(w, h);
    } else if (state.mode === 'isofix') {
      drawIsofixScene(w, h);
    } else if (state.mode === 'gear') {
      drawGearScene(w, h);
    }
  }

  // 1. Draw Crash Simulation Scene
  function drawCrashScene(w, h) {
    const ms = state.crash.msElapsed;
    const hasBelt = state.crash.hasBelt;

    // Background gradient
    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, '#0f172a');
    grad.addColorStop(1, '#1e293b');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // Car frame & windshield
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(w * 0.15, h * 0.15);
    ctx.lineTo(w * 0.45, h * 0.25);
    ctx.lineTo(w * 0.85, h * 0.85);
    ctx.stroke();

    // Car Seat
    ctx.fillStyle = '#334155';
    ctx.beginPath();
    ctx.moveTo(w * 0.70, h * 0.30);
    ctx.lineTo(w * 0.82, h * 0.30);
    ctx.lineTo(w * 0.78, h * 0.80);
    ctx.lineTo(w * 0.55, h * 0.82);
    ctx.lineTo(w * 0.58, h * 0.72);
    ctx.lineTo(w * 0.68, h * 0.70);
    ctx.closePath();
    ctx.fill();

    // Headrest
    ctx.fillStyle = '#475569';
    ctx.fillRect(w * 0.72, h * 0.18, w * 0.10, h * 0.10);

    // Steering wheel column & wheel
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 14;
    ctx.beginPath();
    ctx.moveTo(w * 0.35, h * 0.75);
    ctx.lineTo(w * 0.44, h * 0.55);
    ctx.stroke();

    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.ellipse(w * 0.44, h * 0.55, 30, 45, Math.PI / 6, 0, Math.PI * 2);
    ctx.stroke();

    // DUMMY PHYSICS KINEMATICS
    let headX = w * 0.68;
    let headY = h * 0.35;
    let torsoAngle = 0; // degrees leaning forward

    if (!hasBelt) {
      // Ejected forward violently
      const lean = Math.min(ms / 40, 1.0);
      headX -= lean * (w * 0.26);
      headY += lean * (h * 0.12);
      torsoAngle = lean * 42;
    } else {
      // Held by pretensioner & seatbelt
      // First 15 ms: pretensioner pulls back 2 cm!
      if (ms <= 15) {
        headX += (ms / 15) * 6;
      } else if (ms <= 45) {
        // Lean into airbag as load limiter yields
        const fwd = (ms - 15) / 30;
        headX -= fwd * 35;
        headY += fwd * 15;
      } else {
        // Rebound back into headrest
        const reb = (ms - 45) / 55;
        headX -= (1 - Math.min(reb, 1)) * 35;
        headY += (1 - Math.min(reb, 1)) * 15;
      }
    }

    // Draw Dummy Torso
    ctx.save();
    ctx.translate(w * 0.65, h * 0.68);
    ctx.rotate(-(torsoAngle * Math.PI) / 180);
    ctx.fillStyle = '#38bdf8';
    ctx.fillRect(-18, -90, 36, 90);
    ctx.restore();

    // Draw Dummy Head
    ctx.fillStyle = '#fde047';
    ctx.beginPath();
    ctx.arc(headX, headY, 26, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#1e293b';
    ctx.beginPath();
    ctx.arc(headX - 8, headY - 4, 4, 0, Math.PI * 2); // eye
    ctx.fill();

    // Seatbelt Webbing & Pretensioner Status
    if (hasBelt) {
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(w * 0.74, h * 0.25);
      ctx.lineTo(headX - 4, headY + 30);
      ctx.lineTo(w * 0.60, h * 0.76);
      ctx.stroke();

      // Pretensioner firing sparks at bottom anchor
      if (ms >= 10 && ms <= 28) {
        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(w * 0.74, h * 0.25, 14, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // AIRBAG DEPLOYMENT
    // Inflates at 25-35 ms, deflates after 70 ms
    let bagRadius = 0;
    if (ms >= 20 && ms <= 40) {
      bagRadius = ((ms - 20) / 20) * 55;
    } else if (ms > 40 && ms <= 75) {
      bagRadius = 55;
    } else if (ms > 75) {
      bagRadius = Math.max(15, 55 - ((ms - 75) / 50) * 35); // deflation
    }

    if (bagRadius > 0) {
      ctx.fillStyle = 'rgba(241, 245, 249, 0.9)';
      ctx.strokeStyle = '#cbd5e1';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(w * 0.47, h * 0.50, bagRadius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Exhaust vent gas lines
      if (ms >= 70) {
        ctx.strokeStyle = 'rgba(203, 213, 225, 0.6)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(w * 0.47, h * 0.42);
        ctx.lineTo(w * 0.42, h * 0.35);
        ctx.moveTo(w * 0.47, h * 0.58);
        ctx.lineTo(w * 0.42, h * 0.65);
        ctx.stroke();
      }
    }

    // Timeline Overlay Bar
    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
    ctx.fillRect(16, 16, w - 32, 54);
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 1;
    ctx.strokeRect(16, 16, w - 32, 54);

    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 15px Cairo, sans-serif';
    ctx.fillText(`⏱️ زمن الاصطدام: ${Math.round(ms)} ms (مللي ثانية) | السرعة: ${state.crash.speedKmH} كم/ساعة`, 28, 40);

    // Active device pill
    let activeDev = '0 ms: بدء الاستشعار';
    let devCol = '#94a3b8';
    if (ms >= 10 && ms < 25) {
      activeDev = '🔥 10-15 ms: اشتعال جهاز الشد المسبق (Pretensionatore)';
      devCol = '#f59e0b';
    } else if (ms >= 25 && ms < 65) {
      activeDev = '🎈 25-45 ms: انفجار الوسادة الهوائية (Airbag 300 km/h)';
      devCol = '#38bdf8';
    } else if (ms >= 65 && ms < 100) {
      activeDev = '💨 70-100 ms: تفرغ غاز الإيرباج (Sgonfiameno)';
      devCol = '#10b981';
    } else if (ms >= 100) {
      activeDev = '✅ نهاية التسلسل: حماية كاملة من الارتطام';
      devCol = '#10b981';
    }
    if (!hasBelt && ms > 30) {
      activeDev = '❌ خطر: ارتطام مباشر لعدم ربط الحزام!';
      devCol = '#ef4444';
    }

    ctx.fillStyle = devCol;
    ctx.font = 'bold 13px Cairo, sans-serif';
    ctx.fillText(activeDev, 28, 60);
  }

  // 2. Draw Child ISOFIX Scene
  function drawIsofixScene(w, h) {
    const isFront = state.child.seatPosition === 'front';
    const isRearward = state.child.facing === 'rearward';
    const isDanger = state.child.isDanger;
    const hChild = state.child.heightCm;

    // Background
    ctx.fillStyle = '#111827';
    ctx.fillRect(0, 0, w, h);

    // Car Seat base & back
    ctx.fillStyle = '#1f2937';
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.rect(w * 0.35, h * 0.20, w * 0.40, h * 0.65);
    ctx.fill();
    ctx.stroke();

    // Dashboard & front passenger indicator
    if (isFront) {
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(w * 0.05, h * 0.25, w * 0.25, h * 0.55);
      ctx.strokeStyle = '#475569';
      ctx.strokeRect(w * 0.05, h * 0.25, w * 0.25, h * 0.55);

      // Key switch indicator
      ctx.fillStyle = state.child.airbagActive ? '#22c55e' : '#ef4444';
      ctx.beginPath();
      ctx.arc(w * 0.18, h * 0.42, 22, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px Cairo, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(state.child.airbagActive ? 'AIRBAG ON' : 'AIRBAG OFF', w * 0.18, h * 0.45);
      ctx.textAlign = 'start';
    }

    // Child Seat or Booster Seat
    if (hChild < 150) {
      const seatX = w * 0.42;
      const seatY = h * 0.38;

      ctx.fillStyle = isDanger ? '#dc2626' : '#2563eb';
      ctx.strokeStyle = isDanger ? '#f87171' : '#60a5fa';
      ctx.lineWidth = 4;

      ctx.beginPath();
      ctx.roundRect(seatX, seatY, w * 0.28, h * 0.42, 16);
      ctx.fill();
      ctx.stroke();

      // ISOFIX Anchors visible at base
      ctx.fillStyle = '#f59e0b';
      ctx.fillRect(seatX - 15, seatY + h * 0.36, 20, 14);
      ctx.fillRect(seatX + w * 0.28 - 5, seatY + h * 0.36, 20, 14);

      // Child Silhouette
      ctx.fillStyle = '#fef08a';
      ctx.beginPath();
      // Facing forward vs rearward
      const eyeX = isRearward ? seatX + 35 : seatX + w * 0.28 - 35;
      ctx.arc(seatX + w * 0.14, seatY + 45, 24, 0, Math.PI * 2); // head
      ctx.fill();

      ctx.fillStyle = '#1e293b';
      ctx.beginPath();
      ctx.arc(eyeX, seatY + 42, 3, 0, Math.PI * 2); // pupil
      ctx.fill();

      // Danger Explosive Warning Sign if Airbag active on rearward
      if (isDanger) {
        ctx.fillStyle = 'rgba(239, 68, 68, 0.9)';
        ctx.beginPath();
        ctx.arc(w * 0.25, h * 0.45, 45, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(w * 0.25 - 25, h * 0.45 - 25);
        ctx.lineTo(w * 0.25 + 25, h * 0.45 + 25);
        ctx.moveTo(w * 0.25 + 25, h * 0.45 - 25);
        ctx.lineTo(w * 0.25 - 25, h * 0.45 + 25);
        ctx.stroke();
      }
    } else {
      // Adult sitting normally
      ctx.fillStyle = '#fde047';
      ctx.beginPath();
      ctx.arc(w * 0.55, h * 0.32, 28, 0, Math.PI * 2);
      ctx.fill();

      // Normal seatbelt across
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 7;
      ctx.beginPath();
      ctx.moveTo(w * 0.70, h * 0.22);
      ctx.lineTo(w * 0.45, h * 0.75);
      ctx.stroke();
    }

    // Top Banner
    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
    ctx.fillRect(16, 16, w - 32, 48);
    ctx.fillStyle = isDanger ? '#ef4444' : '#38bdf8';
    ctx.font = 'bold 15px Cairo, sans-serif';
    ctx.fillText(
      isDanger ? '🚨 خطر مميت: إلغاء تفعيل الإيرباج إلزامي مع مقعد الرضيع المعكوس!' : `👶 طول الطفل: ${hChild} سم | النظام: ${hChild < 150 ? 'مقعد خاص إلزامي' : 'حزام البالغين كافٍ'}`,
      28, 45
    );
  }

  // 3. Draw Motorcycle Gear Scene
  function drawGearScene(w, h) {
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, w, h);

    // Rider Dummy Silhouette with Gear Highlights
    const cx = w * 0.45;
    const cy = h * 0.50;

    // Head / Helmet
    const isDamaged = state.gear.helmetType === 'danneggiato';
    ctx.fillStyle = isDamaged ? '#7f1d1d' : '#1e3a8a';
    ctx.strokeStyle = isDamaged ? '#ef4444' : '#60a5fa';
    ctx.lineWidth = 3;

    ctx.beginPath();
    ctx.arc(cx, cy - 80, 42, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Visor
    ctx.fillStyle = state.gear.cleanVisor ? 'rgba(147, 197, 253, 0.7)' : 'rgba(75, 85, 99, 0.9)';
    ctx.beginPath();
    ctx.arc(cx - 15, cy - 80, 24, -Math.PI / 4, Math.PI / 4);
    ctx.fill();

    // Strap
    ctx.strokeStyle = state.gear.strapFastened ? '#22c55e' : '#ef4444';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(cx - 20, cy - 45);
    ctx.lineTo(cx, cy - 35);
    ctx.lineTo(cx + 20, cy - 45);
    ctx.stroke();

    // Jacket / Torso
    ctx.fillStyle = state.gear.hasJacket ? '#334155' : '#64748b';
    ctx.fillRect(cx - 45, cy - 30, 90, 110);

    // Back protector highlight
    if (state.gear.hasJacket) {
      ctx.fillStyle = '#f59e0b';
      ctx.fillRect(cx + 20, cy - 25, 20, 95);
    }

    // Gloves / Hands
    ctx.fillStyle = state.gear.hasGloves ? '#0284c7' : '#f87171';
    ctx.beginPath();
    ctx.arc(cx - 70, cy + 50, 16, 0, Math.PI * 2);
    ctx.arc(cx + 70, cy + 50, 16, 0, Math.PI * 2);
    ctx.fill();

    // Boots / Feet
    ctx.fillStyle = state.gear.hasBoots ? '#1e293b' : '#f87171';
    ctx.strokeStyle = state.gear.hasBoots ? '#10b981' : '#ef4444';
    ctx.lineWidth = 2;
    ctx.fillRect(cx - 40, cy + 130, 30, 40);
    ctx.strokeRect(cx - 40, cy + 130, 30, 40);
    ctx.fillRect(cx + 10, cy + 130, 30, 40);
    ctx.strokeRect(cx + 10, cy + 130, 30, 40);

    // Status Overlay
    ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
    ctx.fillRect(16, 16, w - 32, 54);
    ctx.fillStyle = state.gear.score > 80 ? '#10b981' : state.gear.score > 50 ? '#f59e0b' : '#ef4444';
    ctx.font = 'bold 15px Cairo, sans-serif';
    ctx.fillText(`🛡️ معدل الأمان والحماية: ${state.gear.score}% | معيار الخوذة: ECE 22.06`, 28, 42);
  }

  // Self Init on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStudio);
  } else {
    initStudio();
  }
})();

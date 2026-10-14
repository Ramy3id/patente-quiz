/**
 * MOTORWAY & TOWING STUDIO (CAPITOLO 17)
 * 60 FPS HTML5 Canvas Simulator with Web Audio API Integration
 * Modes:
 *   1. Motorway 3-Lane & 7-Meter Vehicle Filter (Regola dei 7 Metri in Corsia 3)
 *   2. Emergency Stop & Triangle Placement Lab (Distanze Triangolo e Giubbotto)
 *   3. Towing Physics & Hitch Safety Lab (Organi di Traino, Peso Sfera S e Caravan)
 */

(function () {
  'use strict';

  // Sound Engine
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

      if (type === 'click') {
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
        osc.frequency.setValueAtTime(320, now);
        osc.frequency.setValueAtTime(240, now + 0.1);
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
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.2);
      }
    } catch (e) {
      // Audio silent fallback
    }
  }

  // State Management
  const state = {
    mode: 'lanes', // 'lanes' | 'emergency' | 'towing'

    // Mode 1: Motorway Lanes & 7m Rule
    lanes: {
      vehicleLengthM: 8.5,
      selectedLane: 1, // 1 | 2 | 3
      isViolation: false,
      evalTextAr: '',
      evalTextIt: '',
      roadOffset: 0
    },

    // Mode 2: Emergency Stop & Triangle
    emergency: {
      roadType: 'autostrada', // 'autostrada' | 'extraurbana' | 'citta'
      triangleDistM: 100,
      hasVest: true,
      hasTriangle: true,
      isViolation: false,
      statusAr: '',
      statusIt: ''
    },

    // Mode 3: Towing & Towball
    towing: {
      ballLoadKg: 65, // vertical load S (50-75 kg optimal)
      hasSafetyCable: true,
      hasBreakawayChecked: true,
      attemptHighwayTow: false,
      statusAr: '',
      statusIt: '',
      isViolation: false
    }
  };

  let canvas, ctx;
  let animId = null;

  function initStudio() {
    canvas = document.getElementById('motorwayCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    setupCanvasDPI();
    window.addEventListener('resize', () => {
      setupCanvasDPI();
      renderCurrentMode();
    });

    bindEvents();
    evaluateLanes();
    evaluateEmergency();
    evaluateTowing();
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
    document.querySelectorAll('.motorway-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === newMode);
    });

    document.querySelectorAll('.motorway-panel-ctrl').forEach(p => {
      p.style.display = p.dataset.panel === newMode ? 'block' : 'none';
    });

    playSound('click');
    renderCurrentMode();
  }

  function bindEvents() {
    // Tab switching
    document.querySelectorAll('.motorway-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => setMode(btn.dataset.mode));
    });

    // --- Mode 1: Lanes Controls ---
    const lenSlider = document.getElementById('mwLengthSlider');
    const lenVal = document.getElementById('mwLengthVal');
    if (lenSlider) {
      lenSlider.addEventListener('input', (e) => {
        state.lanes.vehicleLengthM = parseFloat(e.target.value);
        if (lenVal) lenVal.textContent = state.lanes.vehicleLengthM.toFixed(1) + ' m';
        evaluateLanes();
      });
    }

    document.querySelectorAll('.mw-lane-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        state.lanes.selectedLane = parseInt(btn.dataset.lane, 10);
        document.querySelectorAll('.mw-lane-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        playSound('click');
        evaluateLanes();
      });
    });

    // --- Mode 2: Emergency Controls ---
    const roadSelect = document.getElementById('mwRoadTypeSelect');
    if (roadSelect) {
      roadSelect.addEventListener('change', (e) => {
        state.emergency.roadType = e.target.value;
        playSound('click');
        evaluateEmergency();
      });
    }

    const distSlider = document.getElementById('mwDistSlider');
    const distVal = document.getElementById('mwDistVal');
    if (distSlider) {
      distSlider.addEventListener('input', (e) => {
        state.emergency.triangleDistM = parseInt(e.target.value, 10);
        if (distVal) distVal.textContent = state.emergency.triangleDistM + ' m';
        evaluateEmergency();
      });
    }

    const vestCheck = document.getElementById('mwVestCheck');
    if (vestCheck) {
      vestCheck.addEventListener('change', (e) => {
        state.emergency.hasVest = e.target.checked;
        playSound('click');
        evaluateEmergency();
      });
    }

    // --- Mode 3: Towing Controls ---
    const ballSlider = document.getElementById('mwBallSlider');
    const ballVal = document.getElementById('mwBallVal');
    if (ballSlider) {
      ballSlider.addEventListener('input', (e) => {
        state.towing.ballLoadKg = parseInt(e.target.value, 10);
        if (ballVal) ballVal.textContent = state.towing.ballLoadKg + ' kg';
        evaluateTowing();
      });
    }

    const cableCheck = document.getElementById('mwCableCheck');
    if (cableCheck) {
      cableCheck.addEventListener('change', (e) => {
        state.towing.hasSafetyCable = e.target.checked;
        playSound('click');
        evaluateTowing();
      });
    }

    const towHwyBtn = document.getElementById('mwTowHighwayBtn');
    if (towHwyBtn) {
      towHwyBtn.addEventListener('click', () => {
        state.towing.attemptHighwayTow = !state.towing.attemptHighwayTow;
        towHwyBtn.classList.toggle('active', state.towing.attemptHighwayTow);
        evaluateTowing();
      });
    }
  }

  // --- Mode 1 Evaluation ---
  function evaluateLanes() {
    const len = state.lanes.vehicleLengthM;
    const lane = state.lanes.selectedLane;
    let violation = false;
    let ar = '';
    let it = '';

    if (len > 7.0 && lane === 3) {
      violation = true;
      ar = `🚨 مخالفة كود السير (قاعدة الـ 7 أمتار): طول المركبة (${len} متراً) يتجاوز 7 أمتار! يحظر عليها قطيعاً السير في الحارة الثالثة (أقصى اليسار)، ويسمح لها فقط بالحارة الأولى والثانية من اليمين.`;
      it = `VIOLAZIONE ART. 176: Veicolo di lunghezza ${len}m > 7m in 3ª corsia! Ammesso solo sulle prime due corsie di destra.`;
    } else if (lane === 1) {
      ar = `✅ الحارة 1 (أقصى اليمين): الحارة الإلزامية للسير العادي عندما تكون خالية لجميع المركبات والشاحنات.`;
      it = `Corsia 1: marcia normale obbligatoria su corsia libera a destra.`;
    } else if (lane === 2) {
      ar = `✅ الحارة 2 (الوسطى): مسموحة للتجاوز لجميع المركبات بما فيها التي يزيد طولها عن 7 أمتار (سيارة بمقطورة).`;
      it = `Corsia 2: primo sorpasso consentito anche ai complessi > 7 metri.`;
    } else {
      ar = `✅ الحارة 3 (أقصى اليسار): مسموحة للتجاوز السريع للسيارات التي لا يتجاوز طولها 7 أمتار فقط.`;
      it = `Corsia 3: consentita per ulteriore sorpasso a veicoli <= 7 metri.`;
    }

    state.lanes.isViolation = violation;
    state.lanes.evalTextAr = ar;
    state.lanes.evalTextIt = it;

    const repAr = document.getElementById('mwLaneReportAr');
    const repIt = document.getElementById('mwLaneReportIt');
    const alertBox = document.getElementById('mwLaneAlertBox');

    if (repAr) repAr.innerHTML = ar;
    if (repIt) repIt.innerHTML = it;
    if (alertBox) {
      alertBox.className = violation ? 'motorway-alert-box alert-danger' : 'motorway-alert-box alert-safe';
    }

    if (violation) playSound('danger');
  }

  // --- Mode 2 Evaluation ---
  function evaluateEmergency() {
    const road = state.emergency.roadType;
    const dist = state.emergency.triangleDistM;
    const hasVest = state.emergency.hasVest;
    let violation = false;
    let ar = '';
    let it = '';

    if (!hasVest && road !== 'citta') {
      violation = true;
      ar = '🚨 مخالفة جسيمة (المادة 162 مكرر): عدم ارتداء السترة العاكسة المعتمدة قبل النزول على الطريق ليلاً أو خارج المدن يعاقب عليه بغرامة وسحب نقاط!';
      it = 'VIOLAZIONE ART. 162-bis: Obbligo giubbotto alta visibilità prima di scendere sulla carreggiata!';
    } else if (road === 'autostrada') {
      if (dist < 100) {
        violation = true;
        ar = `⚠️ مسافة المثلث غير كافية في الأوتوستراد: المسافة الحالية (${dist} م) غير قانونية! يجب وضع المثلث على بعد 100 متر على الأقل خلف السيارة ليتسنى للسائقين القادمين بسرعة 130 كم/س تفاديه.`;
        it = `Distanza triangolo insufficiente in autostrada (${dist}m < 100m)! Obbligo almeno 100 metri.`;
      } else {
        ar = `✅ وضع قانوني مثالي: المثلث على بعد ${dist} م (الحد الأدنى 100م)، والسترة العاكسة مرتدية، والمثلث مرئي من مسافة 100م.`;
        it = `Conforme: triangolo a ${dist}m (min. 100m) e giubbotto indossato.`;
      }
    } else if (road === 'extraurbana') {
      if (dist < 50) {
        violation = true;
        ar = `⚠️ مسافة المثلث غير كافية على الطرق الخارجية: المسافة الحالية (${dist} م) أقل من الحد الأدنى القانوني وهو 50 متراً!`;
        it = `Distanza triangolo insufficiente su extraurbane (${dist}m < 50m)! Obbligo almeno 50 metri.`;
      } else {
        ar = `✅ وضع قانوني مثالي: المثلث على بعد ${dist} م (الحد الأدنى 50م) ومرئي من 100م والسترة مرتدية.`;
        it = `Conforme: triangolo a ${dist}m (min. 50m) e giubbotto indossato.`;
      }
    } else {
      ar = `ℹ️ داخل المدينة (Centro abitato): وضع المثلث غير إلزامي قانوناً، ولكن يجب إشعال الـ 4 فلاشات لتنبيه حركة المرور.`;
      it = `In centro abitato: esposizione del triangolo non obbligatoria; azionare le 4 frecce.`;
    }

    state.emergency.isViolation = violation;
    state.emergency.statusAr = ar;
    state.emergency.statusIt = it;

    const repAr = document.getElementById('mwEmergReportAr');
    const repIt = document.getElementById('mwEmergReportIt');
    const alertBox = document.getElementById('mwEmergAlertBox');

    if (repAr) repAr.innerHTML = ar;
    if (repIt) repIt.innerHTML = it;
    if (alertBox) {
      alertBox.className = violation ? 'motorway-alert-box alert-danger' : 'motorway-alert-box alert-safe';
    }

    if (violation) playSound('danger');
  }

  // --- Mode 3 Evaluation ---
  function evaluateTowing() {
    const s = state.towing.ballLoadKg;
    const cable = state.towing.hasSafetyCable;
    const hwyTow = state.towing.attemptHighwayTow;
    let violation = false;
    let ar = '';
    let it = '';

    if (hwyTow) {
      violation = true;
      ar = '🚨 محظور قطعياً (Art. 175 C.d.S.): يمنع منعاً باتاً سحب أي مركبة معطلة بين السيارات الخاصة على الأوتوستراد! يقتصر السحب على سيارات الإنقاذ المعتمدة (Soccorso Stradale).';
      it = 'VIETATO ASSOLUTAMENTE: Traino veicoli in avaria su autostrada riservato al Soccorso Stradale autorizzato!';
    } else if (!cable) {
      violation = true;
      ar = '⚠️ خطر انفصال المقطورة: كابل الفولاذ للأمان (Cavetto a strappo) غير موصول! في حال انفصال ذراع السحب ستتدحرج المقطورة دون فرامل مسببة كارثة.';
      it = 'PERICOLO SGANCIO: Cavetto di sicurezza assente! Non azionerebbe il freno d\'emergenza in caso di distacco.';
    } else if (s < 40) {
      violation = true;
      ar = `⚠️ حمل رأسي سالب أو خفيف جداً على الكرة (${s} كجم): يؤدي إلى ترنح المقطورة وانعدام ثباتها (Sbandamento e beccheggio) عند السرعات العالية والرياح!`;
      it = `Carico verticale S troppo basso (${s} kg): rischio sbandamento e alleggerimento asse posteriore motrice.`;
    } else if (s > 80) {
      violation = true;
      ar = `⚠️ حمل رأسي مفرط على كرة السحب (${s} كجم): يضغط بشدة على المساعدين الخلفيين ويرفع مقدمة السيارة، مما يضعف توجيه العجلات الأمامية وقوة الفرامل!`;
      it = `Carico verticale S eccessivo (${s} kg): schiaccia il retrotreno e alleggerisce l'avantreno riducendo la sterzata.`;
    } else {
      ar = `✅ توزيع وزن مثالي: الحمل الرأسي على الكرة (${s} كجم) ضمن النطاق الهندسي النموذجي (50 إلى 75 كجم) مع توصيل كابل الأمان.`;
      it = `Distribuzione peso ideale: carico S (${s} kg) nel range ottimale 50-75 kg con cavetto collegato.`;
    }

    state.towing.isViolation = violation;
    state.towing.statusAr = ar;
    state.towing.statusIt = it;

    const repAr = document.getElementById('mwTowReportAr');
    const repIt = document.getElementById('mwTowReportIt');
    const alertBox = document.getElementById('mwTowAlertBox');

    if (repAr) repAr.innerHTML = ar;
    if (repIt) repIt.innerHTML = it;
    if (alertBox) {
      alertBox.className = violation ? 'motorway-alert-box alert-danger' : 'motorway-alert-box alert-safe';
    }

    if (violation) playSound('danger');
  }

  // --- Animation Loop ---
  function startAnimationLoop() {
    function loop() {
      state.lanes.roadOffset = (state.lanes.roadOffset + 5) % 80;
      renderCurrentMode();
      animId = requestAnimationFrame(loop);
    }
    animId = requestAnimationFrame(loop);
  }

  function renderCurrentMode() {
    if (!canvas || !ctx) return;
    const w = canvas.getBoundingClientRect().width;
    const h = canvas.getBoundingClientRect().height;

    ctx.clearRect(0, 0, w, h);

    if (state.mode === 'lanes') {
      drawLanesScene(w, h);
    } else if (state.mode === 'emergency') {
      drawEmergencyScene(w, h);
    } else if (state.mode === 'towing') {
      drawTowingScene(w, h);
    }
  }

  // 1. Draw Lanes Scene
  function drawLanesScene(w, h) {
    const len = state.lanes.vehicleLengthM;
    const lane = state.lanes.selectedLane;
    const isViol = state.lanes.isViolation;

    // Road surface
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, w, h);

    // 3 Lanes divided by dashed lines
    const l1Y = h * 0.15;
    const l2Y = h * 0.45;
    const l3Y = h * 0.75;

    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 3;
    ctx.setLineDash([28, 22]);
    ctx.lineDashOffset = -state.lanes.roadOffset;

    ctx.beginPath();
    ctx.moveTo(0, l2Y);
    ctx.lineTo(w, l2Y);
    ctx.moveTo(0, l3Y);
    ctx.lineTo(w, l3Y);
    ctx.stroke();
    ctx.setLineDash([]); // reset

    // Continuous barrier line at top & bottom
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(0, l1Y);
    ctx.lineTo(w, l1Y);
    ctx.moveTo(0, h * 0.95);
    ctx.lineTo(w, h * 0.95);
    ctx.stroke();

    // Lane labels on left
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 12px Cairo, sans-serif';
    ctx.fillText('Corsia 3 (Sorpasso rapido)', 16, l1Y + 30);
    ctx.fillText('Corsia 2 (Primo sorpasso)', 16, l2Y + 30);
    ctx.fillText('Corsia 1 (Normale marcia)', 16, l3Y + 30);

    // Vehicle position based on selected lane
    // Lane 1 -> bottom, Lane 2 -> center, Lane 3 -> top
    const targetY = lane === 1 ? l3Y + 30 : lane === 2 ? l2Y + 30 : l1Y + 30;
    const vehW = Math.min(len * 22, w * 0.45);

    // Draw car
    ctx.fillStyle = isViol ? '#dc2626' : '#2563eb';
    ctx.strokeStyle = isViol ? '#ef4444' : '#60a5fa';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(w * 0.45, targetY, vehW, 36, 6);
    ctx.fill();
    ctx.stroke();

    // Wheels
    ctx.fillStyle = '#020617';
    ctx.fillRect(w * 0.45 + 10, targetY - 4, 18, 6);
    ctx.fillRect(w * 0.45 + 10, targetY + 34, 18, 6);
    ctx.fillRect(w * 0.45 + vehW - 28, targetY - 4, 18, 6);
    ctx.fillRect(w * 0.45 + vehW - 28, targetY + 34, 18, 6);

    // Text on vehicle
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 12px JetBrains Mono, monospace';
    ctx.fillText(`${len.toFixed(1)} m`, w * 0.45 + 15, targetY + 23);

    // If violation in Lane 3: Massive Red Cross
    if (isViol) {
      ctx.strokeStyle = 'rgba(239, 68, 68, 0.9)';
      ctx.lineWidth = 8;
      ctx.beginPath();
      ctx.moveTo(w * 0.40, l1Y + 10);
      ctx.lineTo(w * 0.70, l2Y - 10);
      ctx.moveTo(w * 0.70, l1Y + 10);
      ctx.lineTo(w * 0.40, l2Y - 10);
      ctx.stroke();
    }

    // Top status banner
    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
    ctx.fillRect(16, 16, w - 32, 44);
    ctx.strokeStyle = isViol ? '#ef4444' : '#38bdf8';
    ctx.lineWidth = 1;
    ctx.strokeRect(16, 16, w - 32, 44);

    ctx.fillStyle = isViol ? '#ef4444' : '#f8fafc';
    ctx.font = 'bold 15px Cairo, sans-serif';
    ctx.fillText(
      isViol ? `🚨 ممنوع السير بالحارة 3: طول المركبة ${len}م > 7 أمتار!` : `🚗 الحارة المختارة: ${lane} | الطول: ${len}م (مسموح بها)`,
      28, 44
    );
  }

  // 2. Draw Emergency Scene
  function drawEmergencyScene(w, h) {
    const road = state.emergency.roadType;
    const dist = state.emergency.triangleDistM;
    const hasVest = state.emergency.hasVest;
    const isViol = state.emergency.isViolation;

    // Road asphalt
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, w, h);

    // Broken vehicle on right
    const carX = w * 0.78;
    const carY = h * 0.45;
    ctx.fillStyle = '#475569';
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(carX, carY, 90, 48, 8);
    ctx.fill();
    ctx.stroke();

    // Hazard lights flashing
    ctx.fillStyle = '#f59e0b';
    ctx.beginPath();
    ctx.arc(carX + 6, carY + 8, 4, 0, Math.PI * 2);
    ctx.arc(carX + 6, carY + 40, 4, 0, Math.PI * 2);
    ctx.arc(carX + 84, carY + 8, 4, 0, Math.PI * 2);
    ctx.arc(carX + 84, carY + 40, 4, 0, Math.PI * 2);
    ctx.fill();

    // Driver with or without vest
    ctx.fillStyle = hasVest ? '#eab308' : '#3b82f6';
    ctx.beginPath();
    ctx.arc(carX + 45, carY + 75, 12, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#fef08a';
    ctx.beginPath();
    ctx.arc(carX + 45, carY + 60, 8, 0, Math.PI * 2);
    ctx.fill();

    // Triangle placed behind
    const scale = (w * 0.60) / 150;
    const triX = carX - (dist * scale);
    const triY = carY + 16;

    ctx.fillStyle = '#ef4444';
    ctx.beginPath();
    ctx.moveTo(triX, triY - 18);
    ctx.lineTo(triX - 14, triY + 14);
    ctx.lineTo(triX + 14, triY + 14);
    ctx.closePath();
    ctx.fill();

    // Distance line & label
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(triX, carY + 42);
    ctx.lineTo(carX, carY + 42);
    ctx.stroke();

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 13px JetBrains Mono, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(`${dist} METRI`, (triX + carX) / 2, carY + 36);
    ctx.textAlign = 'start';

    // Top status banner
    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
    ctx.fillRect(16, 16, w - 32, 44);
    ctx.strokeStyle = isViol ? '#ef4444' : '#10b981';
    ctx.lineWidth = 1;
    ctx.strokeRect(16, 16, w - 32, 44);

    ctx.fillStyle = isViol ? '#ef4444' : '#10b981';
    ctx.font = 'bold 15px Cairo, sans-serif';
    ctx.fillText(
      isViol ? '🚨 مسافة غير كافية أو غياب السترة العاكسة!' : `✅ مطابقة قانونية: المسافة ${dist}م على ${road.toUpperCase()}`,
      28, 44
    );
  }

  // 3. Draw Towing Scene
  function drawTowingScene(w, h) {
    const s = state.towing.ballLoadKg;
    const cable = state.towing.hasSafetyCable;
    const isViol = state.towing.isViolation;

    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, w, h);

    // Car on Left
    ctx.fillStyle = '#334155';
    ctx.fillRect(w * 0.15, h * 0.45, w * 0.25, 45);

    // Trailer on Right
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(w * 0.55, h * 0.40, w * 0.30, 55);

    // Towball & hitch connection
    ctx.fillStyle = '#94a3b8';
    ctx.beginPath();
    ctx.arc(w * 0.42, h * 0.55, 10, 0, Math.PI * 2);
    ctx.fill();

    // Towbar connecting
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(w * 0.40, h * 0.55);
    ctx.lineTo(w * 0.55, h * 0.55);
    ctx.stroke();

    // Red breakaway cable
    if (cable) {
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(w * 0.44, h * 0.60, 14, 0, Math.PI);
      ctx.stroke();
    }

    // Weight Arrow pointing down onto towball
    ctx.fillStyle = s > 80 || s < 40 ? '#ef4444' : '#10b981';
    ctx.font = 'bold 14px JetBrains Mono, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(`S = ${s} kg`, w * 0.42, h * 0.38);
    // Arrow
    ctx.strokeStyle = s > 80 || s < 40 ? '#ef4444' : '#10b981';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(w * 0.42, h * 0.41);
    ctx.lineTo(w * 0.42, h * 0.48);
    ctx.stroke();
    ctx.textAlign = 'start';

    // Top status banner
    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
    ctx.fillRect(16, 16, w - 32, 44);
    ctx.strokeStyle = isViol ? '#ef4444' : '#10b981';
    ctx.lineWidth = 1;
    ctx.strokeRect(16, 16, w - 32, 44);

    ctx.fillStyle = isViol ? '#ef4444' : '#10b981';
    ctx.font = 'bold 15px Cairo, sans-serif';
    ctx.fillText(
      isViol ? '🚨 خلل في توزيع وزن المقطورة أو كابل الأمان!' : `✅ وزن رأسي مثالي S = ${s} كجم (نطاق الأمان 50-75 كجم)`,
      28, 44
    );
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStudio);
  } else {
    initStudio();
  }
})();

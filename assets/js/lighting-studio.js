/**
 * LIGHTING & DASHBOARD STUDIO (CAPITOLO 18)
 * 60 FPS HTML5 Canvas Simulator with Web Audio API Integration
 * Modes:
 *   1. Road Beam & Glare Simulator (Fascio Anabbaglianti vs Abbaglianti e Abbagliamento)
 *   2. Dashboard Tell-tales Matrix (Quadro Spie Rosse, Gialle, Verdi e Blu)
 *   3. Reflectors & Cargo Overhang Lab (Catadiottri e Pannello Fig. 302)
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
      } else if (type === 'tictac') {
        // Turn signal relay click
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(1200, now);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.linearRampToValueAtTime(0.005, now + 0.03);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.03);
      } else if (type === 'danger') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(350, now);
        osc.frequency.setValueAtTime(260, now + 0.1);
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.25);
      } else if (type === 'horn') {
        // Two-tone car horn simulation
        [440, 554].forEach(freq => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(freq, now);
          gain.gain.setValueAtTime(0.2, now);
          gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now);
          osc.stop(now + 0.25);
        });
      } else if (type === 'spia') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(659, now);
        osc.frequency.setValueAtTime(880, now + 0.08);
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
    mode: 'beam', // 'beam' | 'spie' | 'cargo'

    // Mode 1: Road Beam Simulation
    beam: {
      condition: 'extraurbana_buia', // 'citta_notte' | 'extraurbana_buia' | 'incrocio_veicolo' | 'seguire_veicolo' | 'nebbia_fitta'
      lampMode: 'anabb',             // 'off' | 'pos' | 'anabb' | 'abbagl' | 'fendi'
      hazardActive: false,
      isGlaring: false,
      evalTextAr: '',
      evalTextIt: '',
      roadOffset: 0
    },

    // Mode 2: Dashboard Spie Diagnostic
    spie: {
      activeSpia: '697', // '697' | '698' | '696' | '699' | '704' | '705' | 'retronebbia' | 'abs'
      infoAr: '',
      infoIt: '',
      actionAr: '',
      trapAr: '',
      colorClass: 'danger'
    },

    // Mode 3: Cargo & Reflectors
    cargo: {
      vehicleType: 'rimorchio', // 'autovettura' | 'rimorchio'
      overhangPct: 20,          // 0 to 50 %
      hasPanel: true,
      frontOverhang: false,
      reflectorShape: 'triangolare', // 'triangolare' | 'non_triangolare'
      statusAr: '',
      statusIt: '',
      isViolation: false
    }
  };

  // Predefined SPIE Database
  const SPIE_DB = {
    '697': {
      code: 'Fig. 697',
      nameAr: 'لمبة ضغط زيت المحرك الحمراء',
      nameIt: 'Spia pressione olio motore',
      color: '#ef4444',
      badge: 'إيقاف فوري للمحرك',
      infoAr: 'تشير إلى انخفاض ضغط الزيت في دورة التزييت عن الحد الأدنى الآمن.',
      infoIt: 'Indica pressione insufficiente nel circuito di lubrificazione.',
      actionAr: 'أوقف المحرك فوراً وعلى الفور على جانب الطريق! استمرار السير لثوانٍ معدودة يؤدي إلى قفش المحرك (Grippaggio) وتلفه تماماً.',
      trapAr: 'فخ وزاري: اللمبة تقيس ضغط الزيت وليس مستوى الزيت فقط. قد يكون المستوى جيداً ولكن مضخة الزيت معطلة، لذلك التوقف إلزامي فوراً.'
    },
    '698': {
      code: 'Fig. 698',
      nameAr: 'لمبة حرارة سائل التبريد الحمراء',
      nameIt: 'Spia temperatura liquido raffreddamento',
      color: '#ef4444',
      badge: 'خطر سخونة المحرك',
      infoAr: 'تشير إلى غليان وسخونة مفرطة لسائل التبريد في الردياتير (تجاوز 100°C).',
      infoIt: 'Indica eccessivo surriscaldamento del liquido di raffreddamento.',
      actionAr: 'أوقف السيارة وأطفئ المحرك فوراً. تحذير قاتل: إياك أن تفتح غطاء قربة الردياتير والمحرك ساخن لأن البخار المضغوط سينفجر ويسبب حروقاً بالغة بالوجه واليدين!',
      trapAr: 'فخ وزاري: لا تفتح غطاء خزان التبريد قبل أن يبرد المحرك تماماً (حوالي 20 دقيقة).'
    },
    '696': {
      code: 'Fig. 696',
      nameAr: 'لمبة فرامل اليد ونظام الفرامل الحمراء',
      nameIt: 'Spia freno di stazionamento / impianto frenante',
      color: '#ef4444',
      badge: 'معنيان منفصلان',
      infoAr: 'تحمل معنيين دقيقين بحسب حالة حركة المركبة:',
      infoIt: 'Indica freno a mano inserito oppure livello liquido freni insufficiente.',
      actionAr: '1. فرامل اليد مرفوعة (تطفأ بإنزالها). 2. إذا ظلت مضاءة أثناء السير مع إنزال الفرامل، فهذا يعني نقصاً حاداً في زيت الفرامل أو تآكل أقمشة الفرامل.',
      trapAr: 'فخ وزاري: هذه اللمبة لا تعني أبداً عطل نظام ABS! نظام ABS له لمبة صفراء مستقلة مكتوب عليها حروف ABS.'
    },
    '699': {
      code: 'Fig. 699',
      nameAr: 'لمبة شحن البطارية والدينامو الحمراء',
      nameIt: 'Spia ricarica batteria / alternatore',
      color: '#ef4444',
      badge: 'عطل في المولد',
      infoAr: 'تشير إلى أن الدينامو (Alternatore) لا يشحن البطارية أثناء دوران المحرك.',
      infoIt: 'Indica che l\'alternatore non ricarica la batteria.',
      actionAr: 'السيارة تستهلك مخزون البطارية الكهربائي فقط وسيتوقف المحرك وتنطفئ الأنوار بعد قليل. توجه فوراً لأقرب ورشة صيانة قبل نفاد الشحنة.',
      trapAr: 'فخ وزاري: اللمبة لا تعني أن البطارية فارغة فقط، بل تعني أن نظام التوليد (الدينامو أو سيره) لا يغذي السيارة بالكهرباء.'
    },
    '704': {
      code: 'Fig. 704',
      nameAr: 'لمبة الضوء المنخفض الخضراء (Anabbaglianti)',
      nameIt: 'Spia proiettori anabbaglianti',
      color: '#22c55e',
      badge: 'إضاءة قياسية خضراء',
      infoAr: 'رمز كشاف ينبعث منه 5 أشعة مائلة للأسفل، تضيء باللون الأخضر.',
      infoIt: 'Fascio luminoso orientato verso il basso (luce verde).',
      actionAr: 'إلزامية ليلاً وفي الأنفاق وخارج المدن نهاراً، ولا تسبب أي إبهار بفضل تصميم الحزمة غير المتماثلة (Fascio asimmetrico).',
      trapAr: 'فخ وزاري: الضوء المنخفض إلزامي داخل الأنفاق حتى لو كانت مضاءة نهاراً.'
    },
    '705': {
      code: 'Fig. 705',
      nameAr: 'لمبة الضوء العالي الزرقاء (Abbaglianti)',
      nameIt: 'Spia proiettori di profondità (abbaglianti)',
      color: '#3b82f6',
      badge: 'اللمبة الزرقاء الوحيدة!',
      infoAr: 'اللمبة الوحيدة ذات اللون الأزرق في لوحة العدادات بالكامل! حزمتها أفقية متوازية تمتد لأكثر من 100 متر.',
      infoIt: 'L\'unica spia di colore BLU sul cruscotto! Fascio orizzontale profondo.',
      actionAr: 'ممنوعة داخل المدن، ويجب إطفاؤها فوراً والانتقال للمنخفض عند مقابلة سيارة أخرى أو عند السير خلف سيارة على مسافة قريبة تجنباً للإبهار.',
      trapAr: 'فخ وزاري حاسم: لون لمبة الضوء العالي هو الأزرق دائماً (BLU)، وكل سؤال يزعم أنها خضراء أو صفراء فهو FALSO قطيعاً.'
    },
    'retronebbia': {
      code: 'Retronebbia',
      nameAr: 'لمبة كشاف الضباب الخلفي الصفراء (Gialla Ambra)',
      nameIt: 'Spia luce posteriore per nebbia',
      color: '#f59e0b',
      badge: 'إلزامية عند الرؤية < 50م',
      infoAr: 'ضوء أحمر خلفي شديد التوهج يخترق الضباب. لمبته في التابلوه صفراء كهرمانية (Ambra).',
      infoIt: 'Spia di colore giallo ambra. Luce posteriore rossa ad alta intensità.',
      actionAr: 'يُسمح بتشغيله فقط عندما تقل الرؤية عن 50 متراً (ضباب كثيف أو أمطار غزيرة جداً). ويجب إطفاؤه فور انقشاع الضباب لتجنب إبهار السائقين بالخلف.',
      trapAr: 'فخ وزاري: لمبة كشاف الضباب الخلفي صفراء، بينما كشافات الضباب الأمامية لمبتها خضراء.'
    },
    'abs': {
      code: 'Spia ABS',
      nameAr: 'لمبة نظام منع انغلاق المكابح الصفراء (ABS)',
      nameIt: 'Spia anomalia sistema ABS',
      color: '#f59e0b',
      badge: 'عطل إلكتروني في ABS',
      infoAr: 'دائرة بداخلها كلمة ABS تضيء بلون كهرماني عند تعطل حساسات مانع الانغلاق.',
      infoIt: 'Indica anomalia al sistema antibloccaggio ruote ABS.',
      actionAr: 'نظام الفرامل الهيدروليكي العادي يظل يعمل بشكل طبيعي، ولكن تفقد السيارة ميزة منع انغلاق العجلات عند الفرملة الطارئة العنيفة.',
      trapAr: 'فخ وزاري: إضاءة لمبة ABS لا تعني توقف الفرامل كلياً، بل تعني أن الفرامل تعمل كنظام تقليدي بدون الحماية من الانزلاق.'
    }
  };

  // Canvas context
  let canvas, ctx;
  let animId = null;

  function initStudio() {
    canvas = document.getElementById('lightingCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    setupCanvasDPI();
    window.addEventListener('resize', () => {
      setupCanvasDPI();
      renderCurrentMode();
    });

    bindEvents();
    evaluateBeamSafety();
    selectSpia('697');
    evaluateCargoSafety();
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
    document.querySelectorAll('.lighting-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === newMode);
    });

    document.querySelectorAll('.lighting-panel-ctrl').forEach(p => {
      p.style.display = p.dataset.panel === newMode ? 'block' : 'none';
    });

    playSound('click');
    renderCurrentMode();
  }

  function bindEvents() {
    // Mode tabs
    document.querySelectorAll('.lighting-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => setMode(btn.dataset.mode));
    });

    // --- Mode 1: Beam Simulator Controls ---
    const condSelect = document.getElementById('beamConditionSelect');
    if (condSelect) {
      condSelect.addEventListener('change', (e) => {
        state.beam.condition = e.target.value;
        playSound('click');
        evaluateBeamSafety();
      });
    }

    const lampSelect = document.getElementById('beamLampSelect');
    if (lampSelect) {
      lampSelect.addEventListener('change', (e) => {
        state.beam.lampMode = e.target.value;
        playSound('click');
        evaluateBeamSafety();
      });
    }

    const hazardBtn = document.getElementById('beamHazardBtn');
    if (hazardBtn) {
      hazardBtn.addEventListener('click', () => {
        state.beam.hazardActive = !state.beam.hazardActive;
        hazardBtn.classList.toggle('active', state.beam.hazardActive);
        playSound(state.beam.hazardActive ? 'tictac' : 'click');
      });
    }

    const hornBtn = document.getElementById('beamHornBtn');
    if (hornBtn) {
      hornBtn.addEventListener('click', () => {
        playSound('horn');
        checkHornLegality();
      });
    }

    // --- Mode 2: Spie Selectors ---
    document.querySelectorAll('.spia-pill-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        selectSpia(btn.dataset.spia);
      });
    });

    // --- Mode 3: Cargo & Reflector Controls ---
    const vehSelect = document.getElementById('cargoVehicleSelect');
    if (vehSelect) {
      vehSelect.addEventListener('change', (e) => {
        state.cargo.vehicleType = e.target.value;
        playSound('click');
        evaluateCargoSafety();
      });
    }

    const overhangSlider = document.getElementById('cargoOverhangSlider');
    const overhangVal = document.getElementById('cargoOverhangVal');
    if (overhangSlider) {
      overhangSlider.addEventListener('input', (e) => {
        state.cargo.overhangPct = parseInt(e.target.value, 10);
        if (overhangVal) overhangVal.textContent = state.cargo.overhangPct + '%';
        evaluateCargoSafety();
      });
    }

    const panelCheck = document.getElementById('cargoPanelCheck');
    if (panelCheck) {
      panelCheck.addEventListener('change', (e) => {
        state.cargo.hasPanel = e.target.checked;
        playSound('click');
        evaluateCargoSafety();
      });
    }

    const frontCheck = document.getElementById('cargoFrontCheck');
    if (frontCheck) {
      frontCheck.addEventListener('change', (e) => {
        state.cargo.frontOverhang = e.target.checked;
        playSound('click');
        evaluateCargoSafety();
      });
    }

    const reflSelect = document.getElementById('cargoReflectorSelect');
    if (reflSelect) {
      reflSelect.addEventListener('change', (e) => {
        state.cargo.reflectorShape = e.target.value;
        playSound('click');
        evaluateCargoSafety();
      });
    }
  }

  // --- Mode 1 Logic ---
  function evaluateBeamSafety() {
    const cond = state.beam.condition;
    const lamp = state.beam.lampMode;
    let glaring = false;
    let ar = '';
    let it = '';

    if (lamp === 'off') {
      ar = '❌ الأنوار مطفأة: قيادة خطيرة ومخالفة صريحة لكود السير؛ القيادة ليلاً أو بالأنفاق تتطلب الضوء المنخفض حتماً.';
      it = 'Luci spente: circolazione vietata e pericolosa. Obbligo anabbaglianti di notte e in galleria.';
    } else if (lamp === 'pos') {
      ar = '⚠️ أنوار الموضع فقط (Luci di Posizione): غير كافية لإنارة الطريق أثناء السير! تستخدم فقط لإبراز وجود وحجم السيارة.';
      it = 'Solo luci di posizione: insufficienti durante la marcia, servono solo a rendere visibile il veicolo in sosta o all\'arresto.';
    } else if (lamp === 'abbagl') {
      if (cond === 'citta_notte') {
        glaring = true;
        ar = '🚨 إبهار محظور (ABBAGLIAMENTO): استخدام الضوء العالي داخل المدن المضاءة ممنوع ويعاقب عليه بغرامة وسحب نقاط!';
        it = 'VIETATO: Uso dei proiettori abbaglianti in centro abitato sufficientemente illuminato!';
      } else if (cond === 'incrocio_veicolo') {
        glaring = true;
        ar = '🚨 خطر إبهار السائق المقابل (ABBAGLIAMENTO): عند مقابلة سيارة قادمة في الاتجاه المعاكس يجب التحول فوراً إلى المنخفض!';
        it = 'PERICOLO GRAVISSIMO: Abbagliamento del conducente del veicolo incrociante! Passare subito agli anabbaglianti.';
      } else if (cond === 'seguire_veicolo') {
        glaring = true;
        ar = '🚨 إبهار عبر المرآة العاكسة: السير خلف مركبة أخرى بالضوء العالي يعمي سائقها عبر مرآة الرؤية الخلفية! تحول للمنخفض فوراً.';
        it = 'Abbagliamento dallo specchietto retrovisore del veicolo che precede a breve distanza!';
      } else if (cond === 'nebbia_fitta') {
        glaring = true;
        ar = '⚠️ جدار الضباب الأبيض: الضوء العالي في الضباب الكثيف يرتد على قطرات الماء ويعمي السائق نفسه (Muro bianco)!';
        it = 'Effetto muro bianco: gli abbaglianti nella nebbia creano riflessi che accecano il guidatore stesso.';
      } else {
        ar = '✅ استخدام صحيح للضوء العالي: طريق خارجي مظلم تماماً بدون حركة مرور مقابلة أو سيارات قريبة أمامك.';
        it = 'Uso corretto dei proiettori di profondità: strada extraurbana deserta e non illuminata.';
      }
    } else if (lamp === 'anabb') {
      if (cond === 'nebbia_fitta') {
        ar = '✅ وضع قياسي سليم: الضوء المنخفض يضيء أسفل طبقة الضباب دون ارتداد الحزمة على عينيك.';
        it = 'Anabbaglianti corretti con nebbia: fascio asimmetrico orientato verso l\'asfalto.';
      } else {
        ar = '✅ وضع قانوني مثالي: الضوء المنخفض (Anabbaglianti) يؤمن رؤية لمسافة 35-40 متراً بدون إبهار أي سائق.';
        it = 'Condizione ottimale: fascio anabbagliante asimmetrico conforme alle prescrizioni.';
      }
    } else if (lamp === 'fendi') {
      if (cond === 'nebbia_fitta') {
        ar = '🌟 أقصى كفاءة أمان في الضباب: الفندينيبيا الأمامية والريترونيبيا الخلفي يعملان لتأمين الرؤية وتنبيه القادمين من الخلف.';
        it = 'Configurazione ottimale per nebbia fitta: fendinebbia anteriori e retronebbia posteriore ad alta intensità.';
      } else {
        ar = '⚠️ كشاف الضباب الخلفي في ظروف عادية: إشعاله دون وجود ضباب كثيف (<50م) يبهر سائقي السيارات الخلفية بشدة ويعاقب عليه القانون.';
        it = 'Retronebbia superfluo: deve essere spento appena la visibilità torna superiore a 50 metri.';
      }
    }

    state.beam.isGlaring = glaring;
    state.beam.evalTextAr = ar;
    state.beam.evalTextIt = it;

    const repAr = document.getElementById('beamReportAr');
    const repIt = document.getElementById('beamReportIt');
    const alertBox = document.getElementById('beamAlertBox');

    if (repAr) repAr.innerHTML = ar;
    if (repIt) repIt.innerHTML = it;
    if (alertBox) {
      alertBox.className = glaring ? 'lighting-alert-box alert-danger' : 'lighting-alert-box alert-safe';
    }

    if (glaring) playSound('danger');
  }

  function checkHornLegality() {
    const cond = state.beam.condition;
    const repAr = document.getElementById('beamReportAr');
    if (cond === 'citta_notte') {
      if (repAr) repAr.innerHTML = '📢 صوت الكلاكس: <b>ممنوع قانوناً في المدينة ليلاً</b>، إلا في حالة نقل مصابين بحالة حرجة جداً أو لتفادي حادث وشيك. كان يجب استبداله بالوميض الخاطف للأضواء (Sfanalamento)!';
      playSound('danger');
    } else {
      if (repAr) repAr.innerHTML = '📢 صوت الكلاكس: استخدام مسموح خارج المدن للتنبيه قبل المنعطفات الضيقة أو للتحذير عند بدء التجاوز.';
    }
  }

  // --- Mode 2 Logic: Spie Matrix ---
  function selectSpia(code) {
    state.spie.activeSpia = code;
    const sp = SPIE_DB[code];
    if (!sp) return;

    playSound('spia');

    document.querySelectorAll('.spia-pill-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.spia === code);
    });

    const titleEl = document.getElementById('spiaTitle');
    const badgeEl = document.getElementById('spiaBadge');
    const infoArEl = document.getElementById('spiaInfoAr');
    const infoItEl = document.getElementById('spiaInfoIt');
    const actionEl = document.getElementById('spiaAction');
    const trapEl = document.getElementById('spiaTrap');

    if (titleEl) titleEl.textContent = `${sp.nameAr} (${sp.nameIt})`;
    if (badgeEl) {
      badgeEl.textContent = sp.badge;
      badgeEl.style.backgroundColor = sp.color;
    }
    if (infoArEl) infoArEl.textContent = sp.infoAr;
    if (infoItEl) infoItEl.textContent = sp.infoIt;
    if (actionEl) actionEl.innerHTML = `<b>الإجراء الفوري المطلوب:</b> ${sp.actionAr}`;
    if (trapEl) trapEl.innerHTML = `⚠️ <b>فخ الامتحان الوزاري:</b> ${sp.trapAr}`;
  }

  // --- Mode 3 Logic: Cargo & Reflectors ---
  function evaluateCargoSafety() {
    const isTrailer = state.cargo.vehicleType === 'rimorchio';
    const overhang = state.cargo.overhangPct;
    const hasPanel = state.cargo.hasPanel;
    const isFront = state.cargo.frontOverhang;
    const shape = state.cargo.reflectorShape;

    let violation = false;
    let ar = '';
    let it = '';

    // Check front overhang
    if (isFront && !isTrailer) {
      violation = true;
      ar = '🚨 مخالفة جسيمة: يمنع منعاً باتاً بروز أي حمولة من مقدمة السيارات الخاصة (Nessuna sporgenza anteriore)!';
      it = 'VIETATO: Il carico non può MAI sporgere longitudinalmente dalla parte anteriore dell\'autovettura!';
    } else if (overhang > 30) {
      violation = true;
      ar = `🚨 مخالفة كود السير (المادة 164): نسبة البروز الخلفي (${overhang}%) تتجاوز الحد الأقصى القانوني وهو 30% من طول المركبة!`;
      it = `VIOLAZIONE ART. 164: Sporgenza longitudinale posteriore superiore al 30% della lunghezza del veicolo!`;
    } else if (overhang > 0 && !hasPanel) {
      violation = true;
      ar = '⚠️ مخالفة إشارة الحمولة: وجود أي بروز خلفي يوجب تعليق اللوح المربع المعتمد ذي الخطوط الحمراء والبيضاء (Fig. 302)!';
      it = 'OBBLIGO PANNELLO: Qualsiasi carico sporgente posteriormente richiede il pannello quadrato Fig. 302 a strisce bianche e rosse.';
    } else if (!isTrailer && shape === 'triangolare') {
      violation = true;
      ar = '🚨 فخ وزاري قاطع: العواكس المثلثية الحمراء مخصصة حصرياً للمقطورات (Rimorchi)! يحظر تركيبها على السيارات منعاً للتضليل.';
      it = 'VIETATO ASSOLUTAMENTE: I catadiottri triangolari rossi sono riservati ESCLUSIVAMENTE ai rimorchi!';
    } else if (isTrailer && shape === 'non_triangolare') {
      violation = true;
      ar = '⚠️ مخالفة تجهيز المقطورة: يجب أن تزود خلفية أي مقطورة بعاكسين مثلثين باللون الأحمر مع توجيه الرأس للأعلى.';
      it = 'OBBLIGO RIMORCHI: I rimorchi DEVONO avere posteriormente due catadiottri TRIANGOLARI rossi.';
    } else {
      ar = `✅ الحمولة والتجهيزات مطابقة 100%: البروز (${overhang}%) ضمن نطاق الـ 30% المسموح، مع تثبيت اللوح العاكس، وشكل العواكس مطابق لنوع المركبة.`;
      it = `Configurazione perfettamente a norma: sporgenza max 30%, pannello Fig. 302 presente e catadiottri conformi.`;
    }

    state.cargo.isViolation = violation;
    state.cargo.statusAr = ar;
    state.cargo.statusIt = it;

    const statAr = document.getElementById('cargoStatusAr');
    const statIt = document.getElementById('cargoStatusIt');
    const alertBox = document.getElementById('cargoAlertBox');

    if (statAr) statAr.innerHTML = ar;
    if (statIt) statIt.innerHTML = it;
    if (alertBox) {
      alertBox.className = violation ? 'lighting-alert-box alert-danger' : 'lighting-alert-box alert-safe';
    }

    if (violation) playSound('danger');
  }

  // --- Animation Loop ---
  function startAnimationLoop() {
    function loop() {
      state.beam.roadOffset = (state.beam.roadOffset + 4) % 80;
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

    if (state.mode === 'beam') {
      drawBeamScene(w, h);
    } else if (state.mode === 'spie') {
      drawDashboardScene(w, h);
    } else if (state.mode === 'cargo') {
      drawCargoScene(w, h);
    }
  }

  // 1. Draw Road Beam Scene
  function drawBeamScene(w, h) {
    const cond = state.beam.condition;
    const lamp = state.beam.lampMode;
    const isFog = cond === 'nebbia_fitta';
    const isGlaring = state.beam.isGlaring;

    // Sky & Environment
    ctx.fillStyle = isFog ? '#2d3748' : '#090d16';
    ctx.fillRect(0, 0, w, h * 0.55);

    // Fog particles overlay if foggy
    if (isFog) {
      ctx.fillStyle = 'rgba(203, 213, 225, 0.25)';
      ctx.fillRect(0, 0, w, h * 0.55);
    }

    // Road asphalt in perspective
    ctx.fillStyle = '#1e2532';
    ctx.beginPath();
    ctx.moveTo(w * 0.35, h * 0.55);
    ctx.lineTo(w * 0.65, h * 0.55);
    ctx.lineTo(w * 0.95, h);
    ctx.lineTo(w * 0.05, h);
    ctx.closePath();
    ctx.fill();

    // Road dashed line in motion
    ctx.strokeStyle = '#f8fafc';
    ctx.lineWidth = 4;
    ctx.setLineDash([24, 20]);
    ctx.lineDashOffset = -state.beam.roadOffset;
    ctx.beginPath();
    ctx.moveTo(w * 0.50, h * 0.55);
    ctx.lineTo(w * 0.50, h);
    ctx.stroke();
    ctx.setLineDash([]); // reset

    // HEADLIGHT BEAM RAYS
    if (lamp !== 'off') {
      let beamColor = 'rgba(254, 240, 138, 0.45)';
      let beamReach = h * 0.25;

      if (lamp === 'pos') {
        beamColor = 'rgba(255, 255, 255, 0.15)';
        beamReach = h * 0.08;
      } else if (lamp === 'anabb') {
        beamColor = 'rgba(254, 240, 138, 0.55)';
        beamReach = h * 0.35;
      } else if (lamp === 'abbagl') {
        beamColor = 'rgba(255, 255, 255, 0.85)';
        beamReach = h * 0.50;
      } else if (lamp === 'fendi') {
        beamColor = 'rgba(253, 224, 71, 0.65)';
        beamReach = h * 0.28;
      }

      // Draw light trapezoid
      const carY = h * 0.90;
      ctx.fillStyle = beamColor;
      ctx.beginPath();
      if (lamp === 'anabb') {
        // Asymmetric beam: reaches further on right verge
        ctx.moveTo(w * 0.45, carY);
        ctx.lineTo(w * 0.35, carY - beamReach * 0.8);
        ctx.lineTo(w * 0.75, carY - beamReach * 1.2);
        ctx.lineTo(w * 0.55, carY);
      } else {
        ctx.moveTo(w * 0.42, carY);
        ctx.lineTo(w * 0.50 - (w * 0.35), carY - beamReach);
        ctx.lineTo(w * 0.50 + (w * 0.35), carY - beamReach);
        ctx.lineTo(w * 0.58, carY);
      }
      ctx.closePath();
      ctx.fill();
    }

    // Vehicle in front or oncoming car
    if (cond === 'incrocio_veicolo') {
      // Oncoming car in left lane
      ctx.fillStyle = '#334155';
      ctx.fillRect(w * 0.38, h * 0.60, 48, 30);
      // Headlights of oncoming car
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(w * 0.38 + 8, h * 0.60 + 18, 5, 0, Math.PI*2);
      ctx.arc(w * 0.38 + 40, h * 0.60 + 18, 5, 0, Math.PI*2);
      ctx.fill();
    } else if (cond === 'seguire_veicolo') {
      // Preceding vehicle ahead
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(w * 0.46, h * 0.65, 52, 34);
      // Red tail lights
      ctx.fillStyle = '#ef4444';
      ctx.beginPath();
      ctx.arc(w * 0.46 + 6, h * 0.65 + 20, 4, 0, Math.PI*2);
      ctx.arc(w * 0.46 + 46, h * 0.65 + 20, 4, 0, Math.PI*2);
      ctx.fill();
    }

    // GLARING FLASH EXPLOSION OVERLAY
    if (isGlaring) {
      ctx.fillStyle = 'rgba(239, 68, 68, 0.4)';
      ctx.fillRect(0, 0, w, h);
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(w * 0.50, h * 0.60, 70, 0, Math.PI * 2);
      ctx.fill();

      // Glare rays
      ctx.strokeStyle = '#fef08a';
      ctx.lineWidth = 4;
      for (let a = 0; a < 360; a += 30) {
        const rad = (a * Math.PI) / 180;
        ctx.beginPath();
        ctx.moveTo(w * 0.50, h * 0.60);
        ctx.lineTo(w * 0.50 + Math.cos(rad) * 110, h * 0.60 + Math.sin(rad) * 110);
        ctx.stroke();
      }
    }

    // Top status pill
    ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
    ctx.fillRect(16, 16, w - 32, 48);
    ctx.strokeStyle = isGlaring ? '#ef4444' : '#38bdf8';
    ctx.lineWidth = 1;
    ctx.strokeRect(16, 16, w - 32, 48);

    ctx.fillStyle = isGlaring ? '#ef4444' : '#f8fafc';
    ctx.font = 'bold 15px Cairo, sans-serif';
    ctx.fillText(
      isGlaring ? '🚨 خطر إبهار السائقين (ABBAGLIAMENTO) - انتقل للضوء المنخفض فوراً!' : `💡 وضع الإضاءة: ${lamp.toUpperCase()} | البيئة: ${cond}`,
      28, 45
    );
  }

  // 2. Draw Dashboard Cluster Scene
  function drawDashboardScene(w, h) {
    const cur = state.spie.activeSpia;
    const sp = SPIE_DB[cur] || SPIE_DB['697'];

    // Cluster background
    ctx.fillStyle = '#0a0f1d';
    ctx.fillRect(0, 0, w, h);

    // Dual Gauges
    const cx1 = w * 0.28;
    const cx2 = w * 0.72;
    const cy = h * 0.52;
    const rad = Math.min(w * 0.20, h * 0.38);

    // Gauge rings
    [cx1, cx2].forEach((cx, idx) => {
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 12;
      ctx.beginPath();
      ctx.arc(cx, cy, rad, Math.PI * 0.8, Math.PI * 2.2);
      ctx.stroke();

      // Needle
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      const angle = idx === 0 ? Math.PI * 1.3 : Math.PI * 1.5;
      ctx.lineTo(cx + Math.cos(angle) * (rad - 15), cy + Math.sin(angle) * (rad - 15));
      ctx.stroke();
    });

    // Center Display / Active Spia Illuminated Big
    ctx.fillStyle = '#111827';
    ctx.strokeStyle = sp.color;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.roundRect(w * 0.42, h * 0.22, w * 0.16, h * 0.42, 14);
    ctx.fill();
    ctx.stroke();

    // Spia Circle Icon
    ctx.fillStyle = sp.color;
    ctx.beginPath();
    ctx.arc(w * 0.50, h * 0.36, 26, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 16px JetBrains Mono, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(sp.code, w * 0.50, h * 0.55);
    ctx.textAlign = 'start';

    // Top Header Banner
    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
    ctx.fillRect(16, 16, w - 32, 48);
    ctx.fillStyle = sp.color;
    ctx.font = 'bold 15px Cairo, sans-serif';
    ctx.fillText(`🔍 تشخيص اللمبة النشطة: ${sp.nameAr} | اللون: ${sp.badge}`, 28, 45);
  }

  // 3. Draw Cargo & Reflector Scene
  function drawCargoScene(w, h) {
    const isTrailer = state.cargo.vehicleType === 'rimorchio';
    const overhang = state.cargo.overhangPct;
    const hasPanel = state.cargo.hasPanel;
    const isViolation = state.cargo.isViolation;
    const shape = state.cargo.reflectorShape;

    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, w, h);

    // Vehicle Silhouette on right
    ctx.fillStyle = '#334155';
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 3;

    if (isTrailer) {
      // Box trailer outline
      ctx.fillRect(w * 0.35, h * 0.35, w * 0.38, h * 0.42);
      ctx.strokeRect(w * 0.35, h * 0.35, w * 0.38, h * 0.42);
    } else {
      // Car outline
      ctx.fillRect(w * 0.35, h * 0.42, w * 0.42, h * 0.35);
      ctx.strokeRect(w * 0.35, h * 0.42, w * 0.42, h * 0.35);
    }

    // Wheels
    ctx.fillStyle = '#020617';
    ctx.beginPath();
    ctx.arc(w * 0.42, h * 0.78, 22, 0, Math.PI * 2);
    ctx.arc(w * 0.68, h * 0.78, 22, 0, Math.PI * 2);
    ctx.fill();

    // PROTRUDING CARGO (Sticking out to the left)
    if (overhang > 0) {
      const cargoWidth = (overhang / 100) * (w * 0.35);
      const cargoX = w * 0.35 - cargoWidth;

      ctx.fillStyle = isViolation ? '#dc2626' : '#2563eb';
      ctx.fillRect(cargoX, h * 0.46, cargoWidth, 24);

      // Panel Fig. 302 attached to end of cargo
      if (hasPanel) {
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 2;
        ctx.fillRect(cargoX - 8, h * 0.43, 26, 30);
        ctx.strokeRect(cargoX - 8, h * 0.43, 26, 30);
      }
    }

    // Catadiottri Reflectors on vehicle rear (Left edge of chassis)
    ctx.fillStyle = '#ef4444';
    if (shape === 'triangolare') {
      // Triangle
      ctx.beginPath();
      ctx.moveTo(w * 0.37, h * 0.68);
      ctx.lineTo(w * 0.35, h * 0.74);
      ctx.lineTo(w * 0.39, h * 0.74);
      ctx.closePath();
      ctx.fill();
    } else {
      // Circle
      ctx.beginPath();
      ctx.arc(w * 0.37, h * 0.71, 7, 0, Math.PI * 2);
      ctx.fill();
    }

    // Top status banner
    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
    ctx.fillRect(16, 16, w - 32, 48);
    ctx.fillStyle = isViolation ? '#ef4444' : '#10b981';
    ctx.font = 'bold 15px Cairo, sans-serif';
    ctx.fillText(
      isViolation ? '🚨 مخالفة لقواعد الحمولة والعواكس!' : `✅ وضعية سليمة: البروز الخلفي ${overhang}% (الحد الأقصى 30%)`,
      28, 45
    );
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStudio);
  } else {
    initStudio();
  }
})();

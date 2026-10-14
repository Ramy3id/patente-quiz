/**
 * Patente B Pro - Parking & Stopping Interactive Studio (Capitolo 16)
 * Real-time 60 FPS Telemetry Canvas & Interactive Legal Distance Radar
 * Compliant with Art. 157 & 158 Codice della Strada 2026
 */

(function () {
  'use strict';

  // Sound feedback integration
  function playClick() {
    if (window.soundEngine && typeof window.soundEngine.click === 'function') {
      window.soundEngine.click();
    }
  }

  // Distance Radar Scenario Data
  const SCENARIOS = {
    incrocio: {
      title: 'الوقوف بالقرب من تقاطعات الطرق (Incroci)',
      itTitle: 'Sosta in corrispondenza e in prossimità degli incroci',
      distance: 5,
      unit: 'أمتار (Metri)',
      limitRule: 'أقل من 5 أمتار = ممنوع منعاً باتاً (Vietata a meno di 5m)',
      status: 'VIETATA_SOSTA_FERMATA',
      statusText: 'ممنوع الوقوف والتوقف داخل النطاق',
      legalArticle: 'Art. 158 comma 1 lett. f CdS',
      urbanRule: 'داخل المدن: يمنع الوقوف والتوقف على مسافة تقل عن 5 أمتار من حافة التقاطع الأقرب.',
      extraUrbanRule: 'خارج المدن: يمنع الوقوف والتوقف في حرم التقاطع تماماً وعلى جوانب الطريق بالقرب منه.',
      trapWarning: '🚨 فخ امتحاني خطير: داخل المدن، يمنع الوقوف والتوقف على بعد أقل من 5 أمتار من التقاطع، ولا يجوز حتى للنزول المؤقت!',
      canvasType: 'intersection'
    },
    pedonale: {
      title: 'معابر المشاة والدراجات (Attraversamenti Pedonali e Ciclabili)',
      itTitle: 'Attraversamenti pedonali e passaggi ciclabili',
      distance: 5,
      unit: 'أمتار قبل المعبر (5m prima)',
      limitRule: 'ممنوع فوق المعبر تماماً، وممنوع الوقوف قبله بـ 5 أمتار',
      status: 'VIETATA_SOSTA_FERMATA',
      statusText: 'ممنوع فوق المعبر وممنوع الوقوف قبله بـ 5 أمتار',
      legalArticle: 'Art. 158 comma 1 lett. g CdS',
      urbanRule: 'يمنع التوقف والوقوف فوق خطوط عبور المشاة، ويمنع الوقوف على مسافة تقل عن 5 أمتار قبلها لحجب الرؤية.',
      extraUrbanRule: 'تطبق نفس المسافة خارج المدن لضمان رؤية المشاة قبل الشروع في العبور.',
      trapWarning: '⚠️ فخ الامتحان: يمنع الوقوف والتوقف "فوق" المعبر، لكن يمنع الوقوف على بعد 5 أمتار "قبله" (قبل المعبر وليس بعده)!',
      canvasType: 'pedestrian'
    },
    bus: {
      title: 'مواقف الحافلات ومركبات النقل العام (Fermata Autobus)',
      itTitle: 'Fermata dei veicoli in servizio pubblico di linea',
      distance: 15,
      unit: 'متراً (15 Metri)',
      limitRule: '15 متراً قبل وبعد اللافتة، أو كامل الخطوط الصفراء المتعرجة',
      status: 'SOSTA_VIETATA_FERMATA_OK',
      statusText: 'الوقوف ممنوع (Sosta Vietata) — التوقف المؤقت مسموح بشرط عدم التعطيل',
      legalArticle: 'Art. 158 comma 2 lett. d CdS',
      urbanRule: 'يمنع الوقوف (Sosta) على مسافة تقل عن 15 متراً من لوحة موقف الحافلات إذا لم تكن هناك خطوط صفراء، أو داخل المساحة المحددة بالخطوط المتعرجة.',
      extraUrbanRule: 'يسمح بالتوقف الوجيز (Fermata) لركوب أو نزول الركاب بشرط ألا يعيق وصول الحافلة أو حركتها.',
      trapWarning: '🎯 فخ الـ 15 متراً: في موقف الحافلات يمنع الوقوف (Sosta)، لكن يسمح بالتوقف المؤقت (Fermata) إذا لم يعطل الحافلة!',
      canvasType: 'bus_stop'
    },
    passaggio_livello: {
      title: 'مزلقانات القطارات والسكك الحديدية (Passaggi a Livello)',
      itTitle: 'Passaggi a livello e binari ferroviari / tranviari',
      distance: 15,
      unit: 'متراً (15 Metri)',
      limitRule: 'ممنوع فوق القضبان، وممنوع الوقوف على بعد يقل عن 15 متراً',
      status: 'VIETATA_SOSTA_FERMATA',
      statusText: 'ممنوع الوقوف والتوقف مطلقاً',
      legalArticle: 'Art. 158 comma 1 lett. d CdS',
      urbanRule: 'يمنع الوقوف والتوقف على قضبان السكك الحديدية أو الترام أو على مسافة تقل عن 15 متراً من المزلقان.',
      extraUrbanRule: 'الوقوف على مسافة تقل عن 15 متراً يوجب سحب المركبة بالونش وتحرير غرامة مشددة.',
      trapWarning: '🛑 فخ امتحاني: الوقوف بالقرب من مزلقان القطار ممنوع لمسافة 15 متراً كاملة وليس 5 أمتار فقط!',
      canvasType: 'railway'
    },
    passo_carrabile: {
      title: 'مخرج المرآب المصرح به (Passo Carrabile)',
      itTitle: 'Accesso carrabile con cartello autorizzato',
      distance: 0,
      unit: 'أمام البوابة (Altezza del passo)',
      limitRule: 'الوقوف ممنوع (Sosta Vietata) — التوقف اللحظي مسموح (Fermata Ammessa)',
      status: 'SOSTA_VIETATA_FERMATA_OK',
      statusText: 'ممنوع الوقوف والركن — مسموح التوقف اللحظي دون ترك السيارة',
      legalArticle: 'Art. 158 comma 2 lett. a CdS',
      urbanRule: 'يمنع الوقوف (Sosta) أمام مخرج الجراج النظامي المزود بلوحة ورقم ترخيص واسم البلدية. يترتب عليه سحب السيارة بالونش (Rimozione forzata).',
      extraUrbanRule: 'التوقف الوجيز (Fermata) لإنزال راكب مع بقاء السائق خلف المقود مستعداً للمغادرة مسموح به قانوناً!',
      trapWarning: '💡 فخ الامتحان الشهير: أمام Passo Carrabile يمنع الركن (Sosta)، لكن يجوز التوقف الوجيز (Fermata) إذا ظل السائق بالداخل!',
      canvasType: 'passo_carrabile'
    },
    senso_unico: {
      title: 'الوقوف في الشوارع ذات الاتجاه الواحد (Strade a Senso Unico)',
      itTitle: 'Sosta su strada a senso unico di circolazione',
      distance: 3,
      unit: 'أمتار متبقية (3 Metri di spazio)',
      limitRule: 'يسمح بالوقوف على اليسار أيضاً بشرط بقاء 3 أمتار لمرور السيارات',
      status: 'SOSTA_AMMESSA_CONDIZIONATA',
      statusText: 'مسموح على الجانبين بشرط ترك مساحة كافية (3m)',
      legalArticle: 'Art. 157 comma 2 CdS',
      urbanRule: 'في الشوارع ذات الاتجاه الواحد داخل المدن، يسمح بالوقوف على الجانب الأيسر أيضاً بشرط بقاء مساحة لا تقل عن 3 أمتار تكفي لمرور صف واحد من المركبات.',
      extraUrbanRule: 'في الطرق ذات الاتجاهين، يمنع الوقوف على الجانب الأيسر منعاً باتاً (يجب الوقوف دائماً في أقصى اليمين في اتجاه السير).',
      trapWarning: '⭐ قاعدة الـ 3 أمتار: الوقوف على الجانب الأيسر داخل المدن مباح فقط إذا كان الشارع باتجاه واحد وتركت مسافة 3 أمتار شاغرة!',
      canvasType: 'oneway'
    }
  };

  // Maneuver Matrix Data
  const MANEUVERS = {
    fermata: {
      title: 'التوقف المؤقت الإرادي (La Fermata)',
      icon: '⏱️',
      color: '#38bdf8',
      summary: 'تعليق السير لزمن وجيز جداً لتمكين الركاب من الصعود أو النزول، مع بقاء السائق خلف المقود وجاهزاً للتحرك فوراً.',
      conditions: [
        'بقاء السائق خلف عجلة القيادة مستعداً للتحرك في أي لحظة (Conducente a bordo e pronto a ripartire)',
        'استمرار دوران المحرك أو إيقافه مؤقتاً دون مغادرة السيارة',
        'مسموح أمام مداخل الجراجات (Passo carrabile) وفي مواقف الحافلات إذا لم يعق الحافلة',
        'مسموح في الصف الثاني (Seconda fila) حصرياً للدراجات النارية ذات العجلتين'
      ],
      prohibitions: [
        'ممنوع في المنحنيات والمرتفعات (Curve e dossi)',
        'ممنوع في الأنفاق والجسور والممرات السفلية (Gallerie, ponti, sottopassaggi)',
        'ممنوع في الأماكن التي تحجب رؤية الإشارات الضوئية أو شواخص المرور',
        'ممنوع عند وجود إشارة Divieto di Fermata (الصليب الأحمر X)'
      ],
      examTrap: 'فخ الامتحان: التوقف (Fermata) لا يتطلب وضع مثلث الخطر، ولا يعتبر وقوفاً ممتداً، ويسمح به أمام Passo carrabile!'
    },
    sosta: {
      title: 'الوقوف والركن الممتد (La Sosta)',
      icon: '🅿️',
      color: '#f59e0b',
      summary: 'إيقاف المركبة لفترة طويلة مع مغادرتها من جانب السائق، وتتطلب اتخاذ كافة إجراءات الأمان لمنع تدحرجها أو سرقتها.',
      conditions: [
        'إطفاء المحرك وتأمين السيارة بفرامل اليد (Freno di stazionamento)',
        'تعشيق السرعة الأولى (صعوداً) أو الخلفية (نزولاً)، وتوجيه العجلات نحو الرصيف',
        'إغلاق النوافذ وإحكام غلق الأبواب لمنع الاستخدام غير المصرح به',
        'استخدام قرص الوقوف (Disco orario) في المناطق المحددة بوقت، أو دفع التذكرة في Strisce Blu'
      ],
      prohibitions: [
        'ممنوع أمام Passo Carrabile (يستوجب سحب السيارة بالونش Rimozione)',
        'ممنوع في الصف الثاني إطلاقاً لكافة أنواع السيارات والمركبات',
        'ممنوع على مسافة تقل عن 5 أمتار من التقاطعات وممرات المشاة',
        'ممنوع في الأماكن المخصصة لذوي الاحتياجات الخاصة (Stalli invalidi)'
      ],
      examTrap: 'فخ الامتحان: تجديد قرص الوقوف (Disco orario) دون تحريك السيارة ممنوع ويترتب عليه تحرير مخالفة وسحب المركبة!'
    },
    arresto: {
      title: 'التوقف القسري لحركة المرور (L\'Arresto)',
      icon: '🛑',
      color: '#10b981',
      summary: 'التوقف الإجباري الناشئ عن مقتضيات حركة المرور (إشارة حمراء، شرطي، ازدحام، إعطاء أسبقية).',
      conditions: [
        'ناشئ عن متطلبات الطريق وقواعد المرور وليس رغبة السائق الشخصية',
        'لا تنطبق عليه قواعد أو لافتات منع الوقوف والتوقف (Divieto di sosta e fermata)',
        'يجب الحفاظ على مسافة أمان كافية مع المركبة التي في الأمام لمنع التراجع',
        'يجب عدم إغلاق التقاطعات أو المعابر عند تعطل حركة السير'
      ],
      prohibitions: [
        'لا يجوز استخدام فرامل اليد كبديل للسيطرة على السيارة أثناء التوقف القصير في الإشارات',
        'يمنع إيقاف المحرك في منتصف التقاطع'
      ],
      examTrap: 'فخ الامتحان: التوقف أمام الإشارة الضوئية الحمراء هو (Arresto) وليس (Fermata) ولا ينتهك إشارة منع التوقف!'
    },
    emergenza: {
      title: 'الوقوف الاضطراري للأعطال (Sosta di Emergenza)',
      icon: '🚨',
      color: '#f43f5e',
      summary: 'الوقوف الإجباري الناجم عن عطل فني في السيارة أو وعكة صحية مفاجئة للسائق أو أحد الركاب.',
      conditions: [
        'تشغيل أضواء الطوارئ الرباعية فوراً (Luce di pericolo / 4 frecce)',
        'ارتداء السترة العاكسة المعتمدة (Giubbotto riflettente) قبل النزول من السيارة ليلاً أو خارج المدن',
        'وضع مثلث الخطر (Segnale mobile di pericolo) على بعد 50 متراً على الأقل خلف السيارة',
        'على الأوتوستراد: إخلاء السيارة فوراً والانتظار خلف حاجز الأمان المعدني (Guard-rail)'
      ],
      prohibitions: [
        'على الأوتوستراد: يمنع تجاوز مدة 3 ساعات في حارة الطوارئ (Corsia di emergenza)',
        'يمنع إصلاح الأعطال الميكانيكية الكبرى على حارة الطوارئ (يجب استدعاء شاحنة السحب Soccorso stradale)'
      ],
      examTrap: 'فخ الامتحان: الحد الأقصى للوقوف في حارة الطوارئ بسبب العطل هو 3 ساعات فقط، وبعدها يتم سحب السيارة!'
    }
  };

  // State Management
  let currentScenarioKey = 'incrocio';
  let currentManeuverKey = 'fermata';
  let canvas, ctx;
  let animProgress = 0;
  let animId = null;

  function initStudio() {
    canvas = document.getElementById('parkingCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    setupEventListeners();
    updateScenarioDisplay();
    updateManeuverDisplay();
    startAnimation();
  }

  function resizeCanvas() {
    if (!canvas) return;
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width * (window.devicePixelRatio || 1);
    canvas.height = 360 * (window.devicePixelRatio || 1);
    ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
  }

  function setupEventListeners() {
    // Scenarios Buttons
    document.querySelectorAll('.pk-scenario-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        playClick();
        document.querySelectorAll('.pk-scenario-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        currentScenarioKey = this.dataset.scenario;
        updateScenarioDisplay();
      });
    });

    // Maneuver Tabs
    document.querySelectorAll('.pk-maneuver-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        playClick();
        document.querySelectorAll('.pk-maneuver-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        currentManeuverKey = this.dataset.maneuver;
        updateManeuverDisplay();
      });
    });
  }

  function updateScenarioDisplay() {
    const sc = SCENARIOS[currentScenarioKey];
    if (!sc) return;

    const titleEl = document.getElementById('pkScenarioTitle');
    const itTitleEl = document.getElementById('pkScenarioItTitle');
    const distEl = document.getElementById('pkScenarioDist');
    const limitEl = document.getElementById('pkScenarioLimit');
    const badgeEl = document.getElementById('pkScenarioBadge');
    const urbanEl = document.getElementById('pkScenarioUrban');
    const extraEl = document.getElementById('pkScenarioExtra');
    const trapEl = document.getElementById('pkScenarioTrap');
    const artEl = document.getElementById('pkScenarioArticle');

    if (titleEl) titleEl.textContent = sc.title;
    if (itTitleEl) itTitleEl.textContent = sc.itTitle;
    if (distEl) distEl.textContent = sc.distance > 0 ? `${sc.distance} ${sc.unit}` : sc.unit;
    if (limitEl) limitEl.textContent = sc.limitRule;
    if (artEl) artEl.textContent = sc.legalArticle;
    if (urbanEl) urbanEl.textContent = sc.urbanRule;
    if (extraEl) extraEl.textContent = sc.extraUrbanRule;
    if (trapEl) trapEl.innerHTML = sc.trapWarning;

    if (badgeEl) {
      badgeEl.textContent = sc.statusText;
      if (sc.status === 'VIETATA_SOSTA_FERMATA') {
        badgeEl.className = 'pk-status-badge badge-danger';
      } else if (sc.status === 'SOSTA_VIETATA_FERMATA_OK') {
        badgeEl.className = 'pk-status-badge badge-warning';
      } else {
        badgeEl.className = 'pk-status-badge badge-success';
      }
    }

    animProgress = 0;
  }

  function updateManeuverDisplay() {
    const mn = MANEUVERS[currentManeuverKey];
    if (!mn) return;

    const titleEl = document.getElementById('pkManTitle');
    const summaryEl = document.getElementById('pkManSummary');
    const condListEl = document.getElementById('pkManCondList');
    const prohibListEl = document.getElementById('pkManProhibList');
    const trapEl = document.getElementById('pkManTrap');

    if (titleEl) titleEl.innerHTML = `<span>${mn.icon}</span> <span>${mn.title}</span>`;
    if (summaryEl) summaryEl.textContent = mn.summary;

    if (condListEl) {
      condListEl.innerHTML = mn.conditions.map(c => `<li><span style="color:#10b981;">✓</span> <span>${c}</span></li>`).join('');
    }
    if (prohibListEl) {
      prohibListEl.innerHTML = mn.prohibitions.map(p => `<li><span style="color:#f43f5e;">✗</span> <span>${p}</span></li>`).join('');
    }
    if (trapEl) trapEl.innerHTML = `💡 <strong>التحليل الوزاري:</strong> ${mn.examTrap}`;
  }

  function startAnimation() {
    function loop() {
      renderCanvas();
      animProgress += 0.015;
      if (animProgress > 1) animProgress = 0;
      animId = requestAnimationFrame(loop);
    }
    if (animId) cancelAnimationFrame(animId);
    animId = requestAnimationFrame(loop);
  }

  function renderCanvas() {
    if (!ctx || !canvas) return;
    const w = canvas.parentElement.clientWidth;
    const h = 360;

    ctx.clearRect(0, 0, w, h);

    // Background road surface
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, w, h);

    // Grid lines for high-tech telemetry feel
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
    ctx.lineWidth = 1;
    for (let x = 0; x < w; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }

    // Render Scenario Specific Visuals
    const sc = SCENARIOS[currentScenarioKey];
    if (!sc) return;

    switch (sc.canvasType) {
      case 'intersection':
        drawIntersectionScenario(w, h);
        break;
      case 'pedestrian':
        drawPedestrianScenario(w, h);
        break;
      case 'bus_stop':
        drawBusStopScenario(w, h);
        break;
      case 'railway':
        drawRailwayScenario(w, h);
        break;
      case 'passo_carrabile':
        drawPassoCarrabileScenario(w, h);
        break;
      case 'oneway':
        drawOneWayScenario(w, h);
        break;
    }
  }

  function drawIntersectionScenario(w, h) {
    const midX = w / 2;
    const midY = h / 2;
    const roadWidth = 140;

    // Crossroad tarmac
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, midY - roadWidth / 2, w, roadWidth);
    ctx.fillRect(midX - roadWidth / 2, 0, roadWidth, h);

    // Curbs & Sidewalks
    ctx.fillStyle = '#334155';
    ctx.fillRect(0, midY - roadWidth / 2 - 20, midX - roadWidth / 2, 20);
    ctx.fillRect(midX + roadWidth / 2, midY - roadWidth / 2 - 20, w - (midX + roadWidth / 2), 20);
    ctx.fillRect(0, midY + roadWidth / 2, midX - roadWidth / 2, 20);
    ctx.fillRect(midX + roadWidth / 2, midY + roadWidth / 2, w - (midX + roadWidth / 2), 20);

    // 5 Meter Forbidden Buffer (Glowing Red Zones around corners)
    const bufLen = 90;
    const pulseAlpha = 0.25 + 0.15 * Math.sin(animProgress * Math.PI * 2);

    ctx.fillStyle = `rgba(244, 63, 94, ${pulseAlpha})`;
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 2;

    // Bottom-Right Corner Buffer
    ctx.fillRect(midX + roadWidth / 2, midY + roadWidth / 2, bufLen, 25);
    ctx.strokeRect(midX + roadWidth / 2, midY + roadWidth / 2, bufLen, 25);

    // Top-Right Corner Buffer
    ctx.fillRect(midX + roadWidth / 2, midY - roadWidth / 2 - 25, bufLen, 25);
    ctx.strokeRect(midX + roadWidth / 2, midY - roadWidth / 2 - 25, bufLen, 25);

    // Bottom-Left Corner Buffer
    ctx.fillRect(midX - roadWidth / 2 - bufLen, midY + roadWidth / 2, bufLen, 25);
    ctx.strokeRect(midX - roadWidth / 2 - bufLen, midY + roadWidth / 2, bufLen, 25);

    // Dimension Arrow & Labels
    ctx.fillStyle = '#f43f5e';
    ctx.font = 'bold 12px Cairo, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('⛔ مسافة 5 أمتار ممنوعة', midX + roadWidth / 2 + bufLen / 2, midY + roadWidth / 2 + 42);

    // Car parked safely outside the 5m zone
    const carX = midX + roadWidth / 2 + bufLen + 15;
    const carY = midY + roadWidth / 2 + 4;
    drawCarTopDown(carX, carY, 55, 26, '#10b981', '0°');

    ctx.fillStyle = '#10b981';
    ctx.font = 'bold 11px Cairo, sans-serif';
    ctx.fillText('وقوف قانوني (أكثر من 5m) ✓', carX + 28, carY + 40);
  }

  function drawPedestrianScenario(w, h) {
    const roadY = h / 2 - 50;
    const roadH = 100;

    // Roadway
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, roadY, w, roadH);

    // Zebra Crossing stripes
    const zebraX = w * 0.65;
    ctx.fillStyle = '#f8fafc';
    for (let y = roadY; y < roadY + roadH; y += 18) {
      ctx.fillRect(zebraX, y, 40, 10);
    }

    // 5 Meter Forbidden Buffer before crossing
    const bufLen = 100;
    const pulseAlpha = 0.25 + 0.15 * Math.sin(animProgress * Math.PI * 2);

    ctx.fillStyle = `rgba(244, 63, 94, ${pulseAlpha})`;
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 2;
    ctx.fillRect(zebraX - bufLen, roadY + roadH, bufLen, 25);
    ctx.strokeRect(zebraX - bufLen, roadY + roadH, bufLen, 25);

    // Label
    ctx.fillStyle = '#f43f5e';
    ctx.font = 'bold 12px Cairo, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('⛔ 5 أمتار قبل معبر المشاة (حظر حجب الرؤية)', zebraX - bufLen / 2, roadY + roadH + 42);

    // Car safely parked before 5m
    const carX = zebraX - bufLen - 75;
    const carY = roadY + roadH + 2;
    drawCarTopDown(carX, carY, 55, 24, '#10b981', '0°');

    ctx.fillStyle = '#10b981';
    ctx.font = 'bold 11px Cairo, sans-serif';
    ctx.fillText('وقوف نظامي ✓', carX + 28, carY + 40);
  }

  function drawBusStopScenario(w, h) {
    const roadY = h / 2 - 50;
    const roadH = 100;

    // Roadway
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, roadY, w, roadH);

    // Yellow zig-zag line zone (15m buffer)
    const busZoneX = w * 0.35;
    const busZoneW = 180;

    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 3;
    ctx.beginPath();
    let zig = true;
    for (let x = busZoneX; x < busZoneX + busZoneW; x += 15) {
      ctx.lineTo(x, roadY + roadH - (zig ? 20 : 0));
      zig = !zig;
    }
    ctx.stroke();

    // Stenciled BUS text on tarmac
    ctx.fillStyle = 'rgba(245, 158, 11, 0.4)';
    ctx.font = '900 24px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('BUS', busZoneX + busZoneW / 2, roadY + roadH - 35);

    // 15 Meter Dimension Label
    ctx.fillStyle = '#f59e0b';
    ctx.font = 'bold 12px Cairo, sans-serif';
    ctx.fillText('⚠️ مسافة 15 متراً لموقف الحافلات (Sosta Vietata / Fermata Ammessa)', busZoneX + busZoneW / 2, roadY + roadH + 35);

    // Bus Stop Shelter Pole
    ctx.fillStyle = '#38bdf8';
    ctx.beginPath();
    ctx.arc(busZoneX + busZoneW / 2, roadY - 15, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 10px Cairo, sans-serif';
    ctx.fillText('🚏 شاخصة الحافلة', busZoneX + busZoneW / 2, roadY - 30);
  }

  function drawRailwayScenario(w, h) {
    const roadY = h / 2 - 50;
    const roadH = 100;

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, roadY, w, roadH);

    // Railway tracks crossing diagonally
    const trackX = w * 0.6;
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 6;

    ctx.beginPath();
    ctx.moveTo(trackX - 30, 0);
    ctx.lineTo(trackX + 30, h);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(trackX - 10, 0);
    ctx.lineTo(trackX + 50, h);
    ctx.stroke();

    // 15 Meter Buffer Zone
    const bufLen = 140;
    const pulseAlpha = 0.25 + 0.15 * Math.sin(animProgress * Math.PI * 2);

    ctx.fillStyle = `rgba(244, 63, 94, ${pulseAlpha})`;
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 2;
    ctx.fillRect(trackX - 30 - bufLen, roadY + roadH, bufLen, 25);
    ctx.strokeRect(trackX - 30 - bufLen, roadY + roadH, bufLen, 25);

    ctx.fillStyle = '#f43f5e';
    ctx.font = 'bold 12px Cairo, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('⛔ 15 متراً قبل المزلقان (حظر الوقوف والتوقف)', trackX - 30 - bufLen / 2, roadY + roadH + 42);
  }

  function drawPassoCarrabileScenario(w, h) {
    const roadY = h / 2 - 40;
    const roadH = 90;

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, roadY, w, roadH);

    // Sidewalk & Garage Cutout
    ctx.fillStyle = '#334155';
    ctx.fillRect(0, roadY - 35, w, 35);

    const garageX = w * 0.45;
    const garageW = 80;

    // Garage Gate Cutout
    ctx.fillStyle = '#475569';
    ctx.fillRect(garageX, roadY - 35, garageW, 35);

    // Official Passo Carrabile Sign Plaque
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(garageX + garageW / 2 - 14, roadY - 50, 28, 14);
    ctx.strokeStyle = '#b91c1c';
    ctx.lineWidth = 1;
    ctx.strokeRect(garageX + garageW / 2 - 14, roadY - 50, 28, 14);

    // Car doing quick drop-off (Fermata) with driver inside
    const carX = garageX + 12;
    const carY = roadY + 8;
    drawCarTopDown(carX, carY, 55, 26, '#38bdf8', '0°');

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 11px Cairo, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('توقف مؤقت (Fermata) مسموح بشرط عدم التعطيل ✓', carX + 28, carY + 45);
    ctx.fillStyle = '#f43f5e';
    ctx.fillText('الركن وترك السيارة (Sosta) = سحب بالونش فوراً ✗', carX + 28, carY + 62);
  }

  function drawOneWayScenario(w, h) {
    const roadY = h / 2 - 60;
    const roadH = 120;

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, roadY, w, roadH);

    // Sidewalks
    ctx.fillStyle = '#334155';
    ctx.fillRect(0, roadY - 20, w, 20);
    ctx.fillRect(0, roadY + roadH, w, 20);

    // Cars parked on both left and right sides
    drawCarTopDown(w * 0.25, roadY + 4, 55, 24, '#10b981', '0°');
    drawCarTopDown(w * 0.25, roadY + roadH - 28, 55, 24, '#10b981', '0°');

    // Remaining Space (3 Meters Width)
    const midCorridorY = roadY + 30;
    const midCorridorH = roadH - 60;

    ctx.fillStyle = 'rgba(56, 189, 248, 0.15)';
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.strokeRect(w * 0.45, midCorridorY, 140, midCorridorH);
    ctx.setLineDash([]);

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 12px Cairo, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('↔ مساحة 3 أمتار شاغرة إجبارياً', w * 0.45 + 70, midCorridorY + midCorridorH / 2 + 4);
  }

  function drawCarTopDown(x, y, len, wid, color, rot) {
    ctx.save();
    ctx.translate(x + len / 2, y + wid / 2);

    // Chassis
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(-len / 2, -wid / 2, len, wid, 5);
    ctx.fill();

    // Windshields
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(-len * 0.2, -wid * 0.35, len * 0.3, wid * 0.7);

    // Headlights
    ctx.fillStyle = '#fef08a';
    ctx.fillRect(len * 0.42, -wid * 0.4, 3, 5);
    ctx.fillRect(len * 0.42, wid * 0.4 - 5, 3, 5);

    ctx.restore();
  }

  // Initialize on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStudio);
  } else {
    initStudio();
  }
})();

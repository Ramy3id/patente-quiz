/**
 * =======================================================================
 * Patente B Pro - Legal, RCA Insurance & Accident Studio (الباب 23)
 * =======================================================================
 * 60 FPS HTML5 Canvas Interactive Legal & Insurance Simulator:
 * 1. Bonus-Malus Dynamic Ladder & Premium Engine (حاسبة فئات المكافأة والجزاء CU 1-18)
 * 2. Accident Dynamics & Direct Compensation Flow (CAI & Fondo Vittime)
 * 3. Triple Liability Matrix (المسؤولية المدنية والجنائية والإدارية)
 * =======================================================================
 */

class InsuranceStudio {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;

    this.activeTab = 'bonusmalus'; // 'bonusmalus' | 'cai' | 'responsabilita'
    this.animationId = null;
    this.lastTime = 0;

    // Bonus-Malus State
    this.bm = {
      cu: 14, // default beginner entry class
      basePrice: 800, // base euro premium
      history: [14],
      multiplier: 1.0
    };

    // CAI & Accident Flow State
    this.cai = {
      scenario: 'cai_signed', // 'cai_signed' | 'cai_disputed' | 'hit_run' | 'uninsured'
      animProgress: 0,
      carAX: 180,
      carAY: 140,
      carBX: 320,
      carBY: 140,
      resolved: false
    };

    // Liability Matrix State
    this.resp = {
      scenario: 'cose', // 'cose' | 'lesioni' | 'omissione' | 'ebbrezza'
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

      if (type === 'bonus') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(659.25, now + 0.15);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.3);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
        osc.start(now);
        osc.stop(now + 0.38);
      } else if (type === 'malus') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.exponentialRampToValueAtTime(130, now + 0.25);
        gain.gain.setValueAtTime(0.09, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        osc.start(now);
        osc.stop(now + 0.3);
      } else if (type === 'toggle') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(520, now);
        osc.frequency.exponentialRampToValueAtTime(780, now + 0.08);
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
      <div class="ins-studio-card">
        <!-- Studio Header & Tab Switcher -->
        <div class="ins-studio-header">
          <div class="ins-title-group">
            <div class="ins-badge-tag">مختبر القانون والتأمين لكود السير 2026</div>
            <h3 class="ins-main-title">المحاكي التفاعلي: نظام Bonus-Malus وحوادث السير والمسؤوليات الثلاث</h3>
          </div>
          <div class="ins-tabs-nav">
            <button class="ins-tab-btn active" data-tab="bonusmalus">
              <span class="tab-icon">📈</span>
              <span class="tab-label">حاسبة فئات Bonus-Malus (CU 1-18)</span>
            </button>
            <button class="ins-tab-btn" data-tab="cai">
              <span class="tab-icon">🚗</span>
              <span class="tab-label">سيناريوهات الحوادث والتعويض (CAI & Fondo)</span>
            </button>
            <button class="ins-tab-btn" data-tab="responsabilita">
              <span class="tab-icon">⚖️</span>
              <span class="tab-label">مصفوفة المسؤوليات (مدنية، جنائية، إدارية)</span>
            </button>
          </div>
        </div>

        <!-- Canvas Container -->
        <div class="ins-canvas-wrapper">
          <canvas id="insCanvas" width="900" height="300"></canvas>
          
          <!-- Live Telemetry Overlays for Bonus-Malus -->
          <div class="ins-telemetry-hud" id="hudBm">
            <div class="ins-stat-box">
              <span class="ins-stat-label">الفئة الحالية</span>
              <span class="ins-stat-val" id="hudBmCu">CU 14 <small>(مبتدئ)</small></span>
            </div>
            <div class="ins-stat-box highlight-amber">
              <span class="ins-stat-label">معامل القسط</span>
              <span class="ins-stat-val" id="hudBmCoeff">1.00x</span>
            </div>
            <div class="ins-stat-box highlight-green" id="hudBmCostBox">
              <span class="ins-stat-label">القسط التقديري</span>
              <span class="ins-stat-val" id="hudBmCost">800 <small>€ / anno</small></span>
            </div>
            <div class="ins-stat-box">
              <span class="ins-stat-label">شهادة المخاطر (IVASS)</span>
              <span class="ins-stat-val" style="color:#38bdf8; font-size:0.95rem;">إلكترونية مسجلة</span>
            </div>
          </div>

          <!-- Live Telemetry Overlays for CAI Tab -->
          <div class="ins-telemetry-hud" id="hudCai" style="display:none;">
            <div class="ins-stat-box">
              <span class="ins-stat-label">نوع البلاغ</span>
              <span class="ins-stat-val" id="hudCaiType" style="font-size:0.95rem;">Modulo CAI الموقع</span>
            </div>
            <div class="ins-stat-box highlight-green">
              <span class="ins-stat-label">طريقة التعويض</span>
              <span class="ins-stat-val" id="hudCaiMethod" style="font-size:0.95rem;">تعويض مباشر (Risarcimento Diretto)</span>
            </div>
            <div class="ins-stat-box highlight-amber">
              <span class="ins-stat-label">الجهة الدافعة</span>
              <span class="ins-stat-val" id="hudCaiPayer" style="font-size:0.95rem;">شركة تأمينك الخاصة</span>
            </div>
          </div>

          <!-- Live Telemetry Overlays for Liability Tab -->
          <div class="ins-telemetry-hud" id="hudResp" style="display:none;">
            <div class="ins-stat-box" id="hudRespCiv">
              <span class="ins-stat-label">مدنية (Civile)</span>
              <span class="ins-stat-val" style="color:#10b981;">نعم (تعويض مالي)</span>
            </div>
            <div class="ins-stat-box" id="hudRespPen">
              <span class="ins-stat-label">جنائية (Penale)</span>
              <span class="ins-stat-val" style="color:#64748b;">لا (منعدمة)</span>
            </div>
            <div class="ins-stat-box" id="hudRespAmm">
              <span class="ins-stat-label">إدارية (Amm.)</span>
              <span class="ins-stat-val" style="color:#f59e0b;">نعم (غرامة ونقاط)</span>
            </div>
          </div>
        </div>

        <!-- Controls Toolbar: Bonus-Malus -->
        <div class="ins-controls-panel" id="panelBm">
          <div class="ctrl-group">
            <span class="ctrl-label">🏆 محاكاة سجل القيادة السنوي:</span>
            <div class="ctrl-btn-row">
              <button class="ins-btn-action" id="btnApplyBonus">
                <span>⭐</span> سنة بدون حوادث (Bonus: -1 درجة)
              </button>
              <button class="ins-btn-action malus" id="btnApplyMalus1">
                <span>💥</span> التسبب في حادث أول (Malus: +2 درجة)
              </button>
              <button class="ins-btn-action malus" id="btnApplyMalus2">
                <span>💥💥</span> التسبب في حادث إضافي (Malus: +3 درجات)
              </button>
              <button class="ins-btn-opt" id="btnResetCu">
                <span>🔄</span> إعادة تعيين الفئة (CU 14)
              </button>
            </div>
          </div>
          <div class="ins-explanation-pill">
            💡 <strong>قاعدة كود السير:</strong> نظام Bonus-Malus يمنحك (-1) درجة عند مرور سنة خالية من الحوادث؛ بينما الحادث الأول المخطئ فيه يعاقبك بـ (+2) درجة، وكل حادث إضافي في نفس السنة يعاقبك بـ (+3) درجات!
          </div>
        </div>

        <!-- Controls Toolbar: CAI & Accident Flow -->
        <div class="ins-controls-panel" id="panelCai" style="display:none;">
          <div class="ctrl-group">
            <span class="ctrl-label">📋 اختر سيناريو الحادث لمشاهدة مسار التعويض القانوني:</span>
            <div class="ctrl-btn-row">
              <button class="ins-btn-opt active" data-cai="cai_signed">1. نموذج CAI موقع من الطرفين (تعويض مباشر)</button>
              <button class="ins-btn-opt" data-cai="cai_disputed">2. خلاف وعدم توقيع مشترك (إجراءات عادية)</button>
              <button class="ins-btn-opt" data-cai="hit_run">3. سيارة هاربة مجهولة (تدخل صندوق الضمان)</button>
              <button class="ins-btn-opt" data-cai="uninsured">4. سيارة غير مؤمنة (حجز وتدخل الصندوق)</button>
            </div>
          </div>
        </div>

        <!-- Controls Toolbar: Liabilities Matrix -->
        <div class="ins-controls-panel" id="panelResp" style="display:none;">
          <div class="ctrl-group">
            <span class="ctrl-label">⚖️ اختر وقائع الحادث لفحص المسؤوليات الثلاث:</span>
            <div class="ctrl-btn-row">
              <button class="ins-btn-opt active" data-resp="cose">أضرار مادية بالمركبات فقط (Danni a cose)</button>
              <button class="ins-btn-opt" data-resp="lesioni">إصابات بدنية أو دهس مشاة (Lesioni personali)</button>
              <button class="ins-btn-opt" data-resp="omissione">هروب وعدم إسعاف المصابين (Omissione di soccorso)</button>
              <button class="ins-btn-opt" data-resp="ebbrezza">قيادة في حالة سكر بين (Guida in stato di ebbrezza)</button>
            </div>
          </div>
        </div>

        <!-- Educational Insight Banner -->
        <div class="ins-insight-bar" id="insInsightBar">
          <span class="insight-icon">⚖️</span>
          <span class="insight-text" id="insInsightText">
            <strong>المسؤولية المدنية والجنائية مستقلتان:</strong> المسؤولية المدنية تهدف لجبر الضرر والتعويض المالي؛ بينما الجنائية شخصية تنشأ فقط عند ارتكاب جريمة أو إحداث إصابات وقتلى.
          </span>
        </div>
      </div>
    `;
  }

  initCanvas() {
    this.canvas = document.getElementById('insCanvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
  }

  bindEvents() {
    // Tab switching
    const tabBtns = this.container.querySelectorAll('.ins-tab-btn');
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.dataset.tab;
        this.activeTab = target;
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Toggle HUDs
        document.getElementById('hudBm').style.display = target === 'bonusmalus' ? 'flex' : 'none';
        document.getElementById('hudCai').style.display = target === 'cai' ? 'flex' : 'none';
        document.getElementById('hudResp').style.display = target === 'responsabilita' ? 'flex' : 'none';

        // Toggle Panels
        document.getElementById('panelBm').style.display = target === 'bonusmalus' ? 'flex' : 'none';
        document.getElementById('panelCai').style.display = target === 'cai' ? 'flex' : 'none';
        document.getElementById('panelResp').style.display = target === 'responsabilita' ? 'flex' : 'none';

        this.playChime('toggle');
        this.updateInsight();
      });
    });

    // Bonus Malus buttons
    const btnBonus = document.getElementById('btnApplyBonus');
    if (btnBonus) {
      btnBonus.addEventListener('click', () => {
        if (this.bm.cu > 1) {
          this.bm.cu -= 1;
          this.playChime('bonus');
        }
        this.updateBmMetrics();
      });
    }

    const btnMalus1 = document.getElementById('btnApplyMalus1');
    if (btnMalus1) {
      btnMalus1.addEventListener('click', () => {
        this.bm.cu = Math.min(18, this.bm.cu + 2);
        this.playChime('malus');
        this.updateBmMetrics();
      });
    }

    const btnMalus2 = document.getElementById('btnApplyMalus2');
    if (btnMalus2) {
      btnMalus2.addEventListener('click', () => {
        this.bm.cu = Math.min(18, this.bm.cu + 3);
        this.playChime('malus');
        this.updateBmMetrics();
      });
    }

    const btnReset = document.getElementById('btnResetCu');
    if (btnReset) {
      btnReset.addEventListener('click', () => {
        this.bm.cu = 14;
        this.playChime('toggle');
        this.updateBmMetrics();
      });
    }

    // CAI Scenarios
    const caiBtns = this.container.querySelectorAll('[data-cai]');
    caiBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        caiBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.cai.scenario = btn.dataset.cai;
        this.cai.animProgress = 0;
        this.playChime('toggle');
        this.updateCaiMetrics();
      });
    });

    // Liability Scenarios
    const respBtns = this.container.querySelectorAll('[data-resp]');
    respBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        respBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.resp.scenario = btn.dataset.resp;
        this.playChime('toggle');
        this.updateRespMetrics();
      });
    });
  }

  updateBmMetrics() {
    // Multiplier calculation based on CU (CU 1 = 0.45, CU 14 = 1.0, CU 18 = 2.2)
    const cu = this.bm.cu;
    let coeff = 1.0;
    if (cu <= 14) {
      coeff = 0.45 + ((cu - 1) / 13) * 0.55;
    } else {
      coeff = 1.0 + ((cu - 14) / 4) * 1.2;
    }
    this.bm.multiplier = coeff;

    const price = Math.round(this.bm.basePrice * coeff);

    let tag = "(معتدل)";
    if (cu <= 4) tag = "(ممتاز جداً)";
    else if (cu <= 10) tag = "(جيد)";
    else if (cu === 14) tag = "(دخول المبتدئ)";
    else if (cu >= 17) tag = "(خطر شديد)";

    document.getElementById('hudBmCu').innerHTML = `CU ${cu} <small>${tag}</small>`;
    document.getElementById('hudBmCoeff').innerHTML = `${coeff.toFixed(2)}x`;
    document.getElementById('hudBmCost').innerHTML = `${price} <small>€ / anno</small>`;

    const costBox = document.getElementById('hudBmCostBox');
    if (cu <= 8) costBox.className = 'ins-stat-box highlight-green';
    else if (cu <= 14) costBox.className = 'ins-stat-box highlight-amber';
    else costBox.className = 'ins-stat-box highlight-rose';

    this.updateInsight();
  }

  updateCaiMetrics() {
    const sc = this.cai.scenario;
    const typeEl = document.getElementById('hudCaiType');
    const methEl = document.getElementById('hudCaiMethod');
    const payEl = document.getElementById('hudCaiPayer');

    if (sc === 'cai_signed') {
      typeEl.innerText = "نموذج CAI بتوقيع الطرفين";
      methEl.innerText = "تعويض مباشر (Risarcimento Diretto)";
      payEl.innerText = "شركة تأمينك الخاصة (سريع)";
    } else if (sc === 'cai_disputed') {
      typeEl.innerText = "خلاف أو توقيع طرف واحد";
      methEl.innerText = "المسطرة العادية (Procedura ordinaria)";
      payEl.innerText = "شركة تأمين الطرف المخطئ";
    } else if (sc === 'hit_run') {
      typeEl.innerText = "سيارة هاربة مجهولة (Auto Pirata)";
      methEl.innerText = "صندوق الضمان (Fondo di Garanzia)";
      payEl.innerText = "صندوق ضحايا الطرق (إصابات بدنية)";
    } else if (sc === 'uninsured') {
      typeEl.innerText = "سيارة بدون تأمين RCA إطلاقاً";
      methEl.innerText = "صندوق الضمان + حجز السيارة";
      payEl.innerText = "الصندوق ثم الرجوع على المتسبب (Rivalsa)";
    }
    this.updateInsight();
  }

  updateRespMetrics() {
    const sc = this.resp.scenario;
    const civ = document.getElementById('hudRespCiv');
    const pen = document.getElementById('hudRespPen');
    const amm = document.getElementById('hudRespAmm');

    if (sc === 'cose') {
      civ.innerHTML = '<span class="ins-stat-label">مدنية (Civile)</span><span class="ins-stat-val" style="color:#10b981;">نعم (تعويض مالي)</span>';
      pen.innerHTML = '<span class="ins-stat-label">جنائية (Penale)</span><span class="ins-stat-val" style="color:#64748b;">لا (منعدمة تماماً)</span>';
      amm.innerHTML = '<span class="ins-stat-label">إدارية (Amm.)</span><span class="ins-stat-val" style="color:#f59e0b;">نعم (مخالفة مرورية)</span>';
    } else if (sc === 'lesioni') {
      civ.innerHTML = '<span class="ins-stat-label">مدنية (Civile)</span><span class="ins-stat-val" style="color:#10b981;">نعم (تعويض مالي)</span>';
      pen.innerHTML = '<span class="ins-stat-label">جنائية (Penale)</span><span class="ins-stat-val" style="color:#ef4444;">نعم (إصابات خطأ)</span>';
      amm.innerHTML = '<span class="ins-stat-label">إدارية (Amm.)</span><span class="ins-stat-val" style="color:#f59e0b;">سحب رخصة ونقاط</span>';
    } else if (sc === 'omissione') {
      civ.innerHTML = '<span class="ins-stat-label">مدنية (Civile)</span><span class="ins-stat-val" style="color:#10b981;">نعم (تعويض)</span>';
      pen.innerHTML = '<span class="ins-stat-label">جنائية (Penale)</span><span class="ins-stat-val" style="color:#ef4444;">جناية (حبس فوري)</span>';
      amm.innerHTML = '<span class="ins-stat-label">إدارية (Amm.)</span><span class="ins-stat-val" style="color:#ef4444;">إلغاء وسحب الرخصة</span>';
    } else if (sc === 'ebbrezza') {
      civ.innerHTML = '<span class="ins-stat-label">مدنية (Civile)</span><span class="ins-stat-val" style="color:#10b981;">نعم (حق الرجوع)</span>';
      pen.innerHTML = '<span class="ins-stat-label">جنائية (Penale)</span><span class="ins-stat-val" style="color:#ef4444;">جنحة / جناية</span>';
      amm.innerHTML = '<span class="ins-stat-label">إدارية (Amm.)</span><span class="ins-stat-val" style="color:#ef4444;">مصادرة السيارة</span>';
    }
    this.updateInsight();
  }

  updateInsight() {
    const textEl = document.getElementById('insInsightText');
    if (!textEl) return;

    if (this.activeTab === 'bonusmalus') {
      textEl.innerHTML = `<strong>نظام Bonus-Malus:</strong> يبدأ المبتدئ في الفئة <strong>CU 14</strong>. كل سنة نظيفة تمنحه ترقية خطوة (-1)، بينما الحادث المخطئ فيه يعاقبه بخطوتين (+2)، والحادث الثاني بـ (+3) درجات! وتوثق هذه النتائج في شهادة المخاطر (Attestato di rischio).`;
    } else if (this.activeTab === 'cai') {
      if (this.cai.scenario === 'cai_signed') {
        textEl.innerHTML = `<strong>التعويض المباشر (Risarcimento Diretto):</strong> توقيع الطرفين على نموذج CAI الأزرق يُسرّع صرف التعويض خلال 30-60 يوماً من شركتك التأمينية مباشرة دون الحاجة لملاحقة شركة الطرف الآخر!`;
      } else if (this.cai.scenario === 'hit_run') {
        textEl.innerHTML = `<strong>صندوق ضمان الضحايا (Fondo di Garanzia):</strong> مخصص لتعويض الإصابات والأضرار البدنية الناتجة عن سيارة مجهولة هاربة أو غير مؤمنة إطلاقاً.`;
      } else {
        textEl.innerHTML = `<strong>السير بدون تأمين:</strong> جريمة تستوجب غرامة باهظة وحجز المركبة ومصادرتها (Confisca)؛ ولا يُعفي السائق من تعويض الضحايا من ماله الخاص!`;
      }
    } else if (this.activeTab === 'responsabilita') {
      textEl.innerHTML = `<strong>المسؤوليات الثلاث مستقلة تماماً:</strong> الأضرار المادية فقط (Danni a cose) لا تنشئ مسؤولية جنائية إطلاقاً (Nessuna responsabilità penale)، بل مدنية وإدارية فقط! المسؤولية الجنائية شخصية ولا تنقل للتأمين!`;
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
    if (this.activeTab === 'cai') {
      this.cai.animProgress = (this.cai.animProgress + dt * 0.8) % 3.0;
    }
  }

  draw() {
    this.ctx.clearRect(0, 0, 900, 300);

    if (this.activeTab === 'bonusmalus') {
      this.drawBonusMalusCanvas();
    } else if (this.activeTab === 'cai') {
      this.drawCaiCanvas();
    } else if (this.activeTab === 'responsabilita') {
      this.drawResponsabilitaCanvas();
    }
  }

  drawBonusMalusCanvas() {
    const ctx = this.ctx;

    // Dark sleek background
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, 900, 300);

    // Draw Bonus-Malus Universal Ladder (CU 1 to CU 18)
    const ladderX = 80;
    const ladderY = 220;
    const barWidth = 40;
    const maxBarH = 160;

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('سلم الفئات التأمينية المعيارية (Scala CU 1 - 18)', 40, 35);

    for (let c = 1; c <= 18; c++) {
      const bx = ladderX + (c - 1) * 41;
      const isCurrent = c === this.bm.cu;
      const barH = 30 + ((c - 1) / 17) * (maxBarH - 30);
      const by = ladderY - barH;

      // Color coding: 1-5 green, 6-13 sky, 14 amber, 15-18 red
      let fillCol = '#38bdf8';
      if (c <= 5) fillCol = '#10b981';
      else if (c === 14) fillCol = '#f59e0b';
      else if (c >= 15) fillCol = '#f43f5e';

      ctx.fillStyle = isCurrent ? fillCol : 'rgba(255, 255, 255, 0.08)';
      ctx.strokeStyle = isCurrent ? '#ffffff' : 'rgba(255, 255, 255, 0.15)';
      ctx.lineWidth = isCurrent ? 2 : 1;

      ctx.beginPath();
      ctx.roundRect(bx, by, 34, barH, 4);
      ctx.fill();
      ctx.stroke();

      // Number on bottom
      ctx.fillStyle = isCurrent ? '#ffffff' : '#64748b';
      ctx.font = isCurrent ? 'bold 11px monospace' : '10px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`CU${c}`, bx + 17, ladderY + 16);

      // Current marker pointer on top
      if (isCurrent) {
        ctx.fillStyle = fillCol;
        ctx.beginPath();
        ctx.moveTo(bx + 17, by - 12);
        ctx.lineTo(bx + 11, by - 22);
        ctx.lineTo(bx + 23, by - 22);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 11px sans-serif';
        ctx.fillText('أنت هنا', bx + 17, by - 26);
      }
    }

    // Legend & summary box (Right side)
    ctx.textAlign = 'left';
    ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(50, 250, 800, 36, 8);
    ctx.fill();
    ctx.stroke();

    ctx.font = '11px sans-serif';
    ctx.fillStyle = '#10b981';
    ctx.fillText('🟢 فئة 1 إلى 5: خصم ممتاز (Bonus)', 70, 272);
    ctx.fillStyle = '#f59e0b';
    ctx.fillText('🟡 فئة 14: فئة الانطلاق للمبتدئ (Ingresso)', 350, 272);
    ctx.fillStyle = '#f43f5e';
    ctx.fillText('🔴 فئة 15 إلى 18: عقوبة قصوى وغلاء القسط (Malus)', 600, 272);
  }

  drawCaiCanvas() {
    const ctx = this.ctx;

    // Dark road junction background
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, 900, 300);

    // Road junction layout
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(100, 100, 700, 100);

    // Road markings
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 2;
    ctx.setLineDash([20, 20]);
    ctx.beginPath();
    ctx.moveTo(100, 150);
    ctx.lineTo(800, 150);
    ctx.stroke();
    ctx.setLineDash([]);

    // Vehicles: Vehicle A (Blue) & Vehicle B (Orange)
    const sc = this.cai.scenario;

    // Vehicle A
    ctx.fillStyle = '#0284c7';
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(280, 125, 75, 40, 6);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('مركبة A (أنت)', 317, 149);

    // Vehicle B
    if (sc === 'hit_run') {
      // Fleeing car ghost/dash
      ctx.strokeStyle = 'rgba(244, 63, 94, 0.6)';
      ctx.setLineDash([6, 6]);
      ctx.lineWidth = 2;
      ctx.strokeRect(520, 125, 75, 40);
      ctx.setLineDash([]);
      ctx.fillStyle = '#f43f5e';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText('سيارة هاربة 💨', 557, 149);
    } else {
      ctx.fillStyle = sc === 'uninsured' ? '#7f1d1d' : '#d97706';
      ctx.strokeStyle = sc === 'uninsured' ? '#f43f5e' : '#f59e0b';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(420, 125, 75, 40, 6);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText(sc === 'uninsured' ? 'غير مؤمنة ⚠️' : 'مركبة B', 457, 149);
    }

    // Impact icon between cars
    if (sc !== 'hit_run') {
      ctx.fillStyle = '#ef4444';
      ctx.font = '16px sans-serif';
      ctx.fillText('💥', 385, 150);
    }

    // Direct compensation flow chart below
    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(80, 220, 740, 65, 8);
    ctx.fill();
    ctx.stroke();

    ctx.textAlign = 'left';
    ctx.font = 'bold 12px sans-serif';
    if (sc === 'cai_signed') {
      ctx.fillStyle = '#34d399';
      ctx.fillText('✅ مسار التعويض المباشر (Risarcimento Diretto):', 100, 245);
      ctx.font = '11px sans-serif';
      ctx.fillStyle = '#e2e8f0';
      ctx.fillText('تم توقيع نموذج CAI من الطرفين ➔ شركة تأمينك تتولى إصلاح أضرارك وصرف التعويض مباشرة ➔ تسوية سريعة خلال 30-60 يوماً.', 100, 268);
    } else if (sc === 'cai_disputed') {
      ctx.fillStyle = '#f59e0b';
      ctx.fillText('⚠️ مسار المسطرة العادية (Procedura Ordinaria):', 100, 245);
      ctx.font = '11px sans-serif';
      ctx.fillStyle = '#e2e8f0';
      ctx.fillText('خلاف في المسؤولية وتوقيع طرف واحد ➔ تقديم الطلب لشركة تأمين الطرف المخطئ ➔ فحص الخبراء واستدعاء الشهود.', 100, 268);
    } else if (sc === 'hit_run') {
      ctx.fillStyle = '#f43f5e';
      ctx.fillText('🏛️ مسار صندوق ضمان ضحايا الطرق (Fondo di Garanzia Vittime della Strada):', 100, 245);
      ctx.font = '11px sans-serif';
      ctx.fillStyle = '#e2e8f0';
      ctx.fillText('السيارة المتسببة مجهولة وهاربة ➔ الصندوق يتولى تعويض الأضرار البدنية والإصابات الخطرة للضحايا.', 100, 268);
    } else if (sc === 'uninsured') {
      ctx.fillStyle = '#f43f5e';
      ctx.fillText('🛑 سيارة غير مؤمنة إطلاقاً (Veicolo non assicurato):', 100, 245);
      ctx.font = '11px sans-serif';
      ctx.fillStyle = '#e2e8f0';
      ctx.fillText('حجز ومصادرة السيارة فورياً ➔ الصندوق يعوض الضحية ➔ الصندوق يرفع دعوى رجوع (Rivalsa) لتحصيل كل يورو من السائق المخطئ.', 100, 268);
    }
  }

  drawResponsabilitaCanvas() {
    const ctx = this.ctx;

    // Dark sleek matrix background
    ctx.fillStyle = '#090d16';
    ctx.fillRect(0, 0, 900, 300);

    const sc = this.resp.scenario;

    // 3 Major Columns: Civile, Penale, Amministrativa
    const cols = [
      {
        title: 'المسؤولية المدنية (Civile)',
        sub: 'جبر الأضرار والتعويض المالي',
        applies: true,
        consequence: 'التعويض المالي (Risarcimento)',
        who: 'شركة تأمين RCA بالتضامن',
        badgeColor: '#10b981'
      },
      {
        title: 'المسؤولية الجنائية (Penale)',
        sub: 'شخصية لا تنتقل للتأمين',
        applies: sc !== 'cose',
        consequence: sc === 'cose' ? 'منعدمة تماماً (لا جريمة)' : (sc === 'omissione' ? 'الحبس لجناية الهروب' : 'الحبس والغرامة الجنائية'),
        who: 'السائق المتسبب شخصياً (لا ينوب عنه التأمين)',
        badgeColor: sc === 'cose' ? '#64748b' : '#ef4444'
      },
      {
        title: 'المسؤولية الإدارية (Amministrativa)',
        sub: 'مخالفات ونقاط ورخصة السير',
        applies: true,
        consequence: sc === 'cose' ? 'غرامة مالية' : (sc === 'omissione' ? 'إلغاء الرخصة نهائياً' : 'سحب الرخصة ونقاط الجزاء'),
        who: 'السائق ومالك السيارة',
        badgeColor: '#f59e0b'
      }
    ];

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('مصفوفة المسؤوليات الثلاث المستقلة (Tipi di Responsabilità)', 40, 35);

    cols.forEach((col, idx) => {
      const cx = 50 + idx * 280;
      const cy = 60;
      const cw = 260;
      const ch = 215;

      ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
      ctx.strokeStyle = col.badgeColor;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.roundRect(cx, cy, cw, ch, 12);
      ctx.fill();
      ctx.stroke();

      // Column Header
      ctx.fillStyle = col.badgeColor;
      ctx.font = 'bold 13px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(col.title, cx + cw / 2, cy + 30);

      ctx.font = '11px sans-serif';
      ctx.fillStyle = '#94a3b8';
      ctx.fillText(col.sub, cx + cw / 2, cy + 50);

      // Status indicator
      ctx.fillStyle = col.applies ? 'rgba(16, 185, 129, 0.2)' : 'rgba(100, 116, 139, 0.2)';
      ctx.strokeStyle = col.badgeColor;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(cx + 20, cy + 70, cw - 40, 32, 6);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = col.badgeColor;
      ctx.font = 'bold 12px sans-serif';
      ctx.fillText(col.applies ? 'قائمة وتطبق حتماً' : 'منعدمة تماماً (غير مطبقة)', cx + cw / 2, cy + 91);

      // Body Details
      ctx.textAlign = 'left';
      ctx.font = '11px sans-serif';
      ctx.fillStyle = '#cbd5e1';
      ctx.fillText(`• الأثر: ${col.consequence}`, cx + 20, cy + 130);
      ctx.fillText(`• المتحمل: ${col.who}`, cx + 20, cy + 160);
    });
  }
}

// Global initialization
window.InsuranceStudio = InsuranceStudio;
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('insuranceStudioContainer')) {
    window.insStudio = new InsuranceStudio('insuranceStudioContainer');
  }
});

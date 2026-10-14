/**
 * Patente B - License & Penalties Studio (Chapter 20)
 * 60 FPS HTML5 Canvas Simulator with Web Audio API Integration
 * Topics: Patente a Punti, Categorie Patenti (AM, A1, A2, A, B, B96, BE), Ritiro, Sospensione, Revoca, Revisione
 */

(function () {
  'use strict';

  // Audio helper
  const playSfx = () => {
    if (window.soundEngine && typeof window.soundEngine.click === 'function') {
      window.soundEngine.click();
    }
  };

  class LicensePenaltiesStudio {
    constructor(containerId) {
      this.container = document.getElementById(containerId);
      if (!this.container) return;

      this.activeTab = 'punti'; // 'punti' | 'categorie' | 'sanzioni'

      // Punti simulator state
      this.currentPoints = 20;
      this.isNeopatentato = true;
      this.selectedInfractions = [];
      this.cleanYears = 0;

      // Categorie simulator state
      this.carWeight = 2000; // kg
      this.trailerWeight = 1200; // kg
      this.selectedCat = 'B';

      // Sanzioni state
      this.selectedSanzione = 'ritiro'; // 'ritiro' | 'sospensione' | 'revoca' | 'revisione'

      this.animFrame = null;
      this.animTime = 0;

      this.init();
    }

    init() {
      this.renderSkeleton();
      this.bindEvents();
      this.startLoop();
      this.updateUI();
    }

    renderSkeleton() {
      this.container.innerHTML = `
        <div class="lp-studio-card">
          <!-- Studio Header -->
          <div class="lp-studio-header">
            <div class="lp-studio-title-box">
              <div class="lp-studio-badge">
                <span class="lp-pulse-dot"></span>
                <span>المختبر التفاعلي المتقدم 60 FPS • الباب 20</span>
              </div>
              <h2 class="lp-studio-main-title">مختبر رخص القيادة، حاسبة خصم النقاط ومصفوفة العقوبات</h2>
              <p class="lp-studio-sub-title">محاكاة تفاعلية بالزمن الحقيقي لرصيد الـ 20 نقطة، مضاعفة السائقين الجدد، أوزان المقطورات B/B96/BE، والتمييز بين السحب والتعليق والإلغاء</p>
            </div>
            <!-- Mode Switcher Tabs -->
            <div class="lp-tab-group">
              <button class="lp-tab-btn active" data-tab="punti">
                <span class="lp-tab-icon">🔢</span>
                <span>حاسبة النقاط والخصم</span>
              </button>
              <button class="lp-tab-btn" data-tab="categorie">
                <span class="lp-tab-icon">🚛</span>
                <span>فئات الرخص والمقطورات</span>
              </button>
              <button class="lp-tab-btn" data-tab="sanzioni">
                <span class="lp-tab-icon">⚖️</span>
                <span>مصفوفة العقوبات الأربع</span>
              </button>
            </div>
          </div>

          <!-- Main Stage -->
          <div class="lp-stage-layout">
            <!-- Canvas Visualizer -->
            <div class="lp-canvas-wrapper">
              <canvas id="lpCanvas" width="860" height="420"></canvas>
            </div>

            <!-- Controls Panel -->
            <div class="lp-controls-panel" id="lpControlsPanel">
              <!-- Dynamically populated via updateUI() -->
            </div>
          </div>
        </div>
      `;
      this.canvas = document.getElementById('lpCanvas');
      this.ctx = this.canvas.getContext('2d');
    }

    bindEvents() {
      const tabs = this.container.querySelectorAll('.lp-tab-btn');
      tabs.forEach((tab) => {
        tab.addEventListener('click', (e) => {
          playSfx();
          tabs.forEach((t) => t.classList.remove('active'));
          const currentTab = e.currentTarget;
          currentTab.classList.add('active');
          this.activeTab = currentTab.getAttribute('data-tab');
          this.updateUI();
        });
      });
    }

    startLoop() {
      const loop = (timestamp) => {
        this.animTime = timestamp * 0.001;
        this.renderCanvas();
        this.animFrame = requestAnimationFrame(loop);
      };
      this.animFrame = requestAnimationFrame(loop);
    }

    updateUI() {
      const panel = document.getElementById('lpControlsPanel');
      if (!panel) return;

      if (this.activeTab === 'punti') {
        panel.innerHTML = this.renderPuntiControls();
        this.bindPuntiEvents();
      } else if (this.activeTab === 'categorie') {
        panel.innerHTML = this.renderCategorieControls();
        this.bindCategorieEvents();
      } else if (this.activeTab === 'sanzioni') {
        panel.innerHTML = this.renderSanzioniControls();
        this.bindSanzioniEvents();
      }
    }

    // -------------------------------------------------------------
    // TAB 1: PATENTE A PUNTI
    // -------------------------------------------------------------
    renderPuntiControls() {
      const infractionList = [
        { id: 'cinture', name: 'عدم ربط حزام الأمان / الهاتف', pts: 5 },
        { id: 'semaforo', name: 'قطع الإشارة الحمراء (Rosso)', pts: 6 },
        { id: 'precedenza', name: 'عدم إعطاء أسبقية المرور', pts: 5 },
        { id: 'velocita_40', name: 'تجاوز السرعة بين 40 و 60 كم/س', pts: 6 },
        { id: 'velocita_60', name: 'تجاوز السرعة بأكثر من 60 كم/س', pts: 10 },
        { id: 'contromano', name: 'السير عكس الاتجاه في منعطف', pts: 10 },
        { id: 'ebbrezza', name: 'قيادة تحت تأثير الكحول', pts: 10 }
      ];

      // Calculate total deductions
      let totalDeduction = 0;
      this.selectedInfractions.forEach((infId) => {
        const inf = infractionList.find((i) => i.id === infId);
        if (inf) {
          totalDeduction += this.isNeopatentato ? inf.pts * 2 : inf.pts;
        }
      });

      // Ministerial rule: Max deduction in single check without license suspension is 15 points
      const effectiveDeduction = Math.min(15, totalDeduction);
      const remainingPoints = Math.max(0, this.currentPoints - effectiveDeduction);

      let statusBadge = '';
      if (remainingPoints > 15) {
        statusBadge = `<div class="lp-legal-tag legal-safe">✅ رصيد ممتاز (${remainingPoints} نقطة)</div>`;
      } else if (remainingPoints > 0) {
        statusBadge = `<div class="lp-legal-tag legal-warn">⚠️ رصيد منخفض (${remainingPoints} نقطة) - يحتاج دورة استرداد</div>`;
      } else {
        statusBadge = `<div class="lp-legal-tag legal-danger">🚨 تصفير الرصيد (0 نقطة) - خضوع إلزامي للـ Revisione!</div>`;
      }

      return `
        <div class="lp-control-section">
          <div class="lp-control-title">حالة السائق ورصيد البداية:</div>
          <div class="lp-btn-toggle-row">
            <button class="lp-toggle-btn ${this.isNeopatentato ? 'active' : ''}" id="btnDriverNeo">
              سائق جديد (مضاعفة الخصم x2) ⚠️
            </button>
            <button class="lp-toggle-btn ${!this.isNeopatentato ? 'active' : ''}" id="btnDriverOrd">
              سائق معتاد (خصم قياسي x1)
            </button>
          </div>

          <div class="lp-control-title" style="margin-top:10px;">اختر المخالفات المرتكبة بالتزامن:</div>
          <div class="lp-infraction-grid">
            ${infractionList.map((inf) => {
              const isSelected = this.selectedInfractions.includes(inf.id);
              const ptsDisplay = this.isNeopatentato ? inf.pts * 2 : inf.pts;
              return `
                <button class="lp-inf-btn ${isSelected ? 'selected' : ''}" data-inf="${inf.id}">
                  <span>${inf.name}</span>
                  <span class="lp-inf-badge">-${ptsDisplay} pts</span>
                </button>
              `;
            }).join('')}
          </div>
        </div>

        <div class="lp-metrics-grid" style="margin-top:12px;">
          <div class="lp-metric-card">
            <span class="lp-metric-label">إجمالي نقاط المخالفات</span>
            <span class="lp-metric-val danger-val">-${totalDeduction}</span>
            <span class="lp-metric-sub">${totalDeduction > 15 ? 'يطبق سقف الـ 15 نقطة الأقصى' : 'خصم مباشر'}</span>
          </div>
          <div class="lp-metric-card">
            <span class="lp-metric-label">الخصم الفعلي المعتمد</span>
            <span class="lp-metric-val danger-val">-${effectiveDeduction}</span>
            <span class="lp-metric-sub">الحد الأقصى في الضبط الواحد 15 نقطة</span>
          </div>
          <div class="lp-metric-card">
            <span class="lp-metric-label">الرصيد المتبقي</span>
            <span class="lp-metric-val ${remainingPoints === 0 ? 'danger-val' : 'safe-val'}">${remainingPoints} / 20</span>
            <span class="lp-metric-sub">${remainingPoints === 0 ? 'إلزام بإعادة الامتحان' : 'صالح للسير'}</span>
          </div>
        </div>

        <div class="lp-summary-box" style="margin-top:12px;">
          ${statusBadge}
          <div class="lp-trap-box-interactive">
            <div class="lp-trap-header">⚠️ فخ الامتحان الوزاري لقواعد النقاط:</div>
            <p>
              1. <strong>السائق الجديد (Neopatentato):</strong> تضاعف نقاط الخصم خلال السنوات الـ 3 الأولى!<br>
              2. <strong>سقف الخصم اليومي:</strong> في حال ارتكاب عدة مخالفات معاً، لا يمكن خصم أكثر من <strong>15 نقطة</strong> كحد أقصى (ما لم تكن هناك مخالفة توجب سحب أو تعليق الرخصة).<br>
              3. <strong>بونص السائق الملتزم:</strong> تضاف <strong>نقطتان كل سنتين</strong> حتى حد أقصى <strong>30 نقطة</strong>.
            </p>
          </div>
        </div>
      `;
    }

    bindPuntiEvents() {
      const bNeo = document.getElementById('btnDriverNeo');
      const bOrd = document.getElementById('btnDriverOrd');
      if (bNeo && bOrd) {
        bNeo.addEventListener('click', () => {
          playSfx();
          this.isNeopatentato = true;
          this.updateUI();
        });
        bOrd.addEventListener('click', () => {
          playSfx();
          this.isNeopatentato = false;
          this.updateUI();
        });
      }

      const infBtns = this.container.querySelectorAll('[data-inf]');
      infBtns.forEach((btn) => {
        btn.addEventListener('click', (e) => {
          playSfx();
          const infId = e.currentTarget.getAttribute('data-inf');
          const idx = this.selectedInfractions.indexOf(infId);
          if (idx > -1) {
            this.selectedInfractions.splice(idx, 1);
          } else {
            this.selectedInfractions.push(infId);
          }
          this.updateUI();
        });
      });
    }

    // -------------------------------------------------------------
    // TAB 2: CATEGORIE & TRAILERS
    // -------------------------------------------------------------
    renderCategorieControls() {
      const totalWeight = this.carWeight + this.trailerWeight;
      let requiredLicense = '';
      let licenseColor = '';
      let licenseDesc = '';

      if (this.trailerWeight <= 750) {
        requiredLicense = 'Patente B (قياسية)';
        licenseColor = '#10b981';
        licenseDesc = 'المقطورة خفيفة (<= 750 كجم)؛ تكفي رخصة B العادية حتى لو تجاوز المجموع 3.500 كجم (حتى 4.250 كجم)!';
      } else if (totalWeight <= 3500) {
        requiredLicense = 'Patente B (قياسية)';
        licenseColor = '#10b981';
        licenseDesc = 'المقطورة غير خفيفة (> 750 كجم) ولكن الوزن الإجمالي للمجمع لا يتجاوز 3.500 كجم؛ تكفي رخصة B القياسية!';
      } else if (totalWeight <= 4250) {
        requiredLicense = 'Patente B con Codice 96 (B96)';
        licenseColor = '#f59e0b';
        licenseDesc = 'المجمع يتجاوز 3.500 كجم ولا يتعدى 4.250 كجم؛ يلزم كود 96 (اجتياز فحص عملي فقط دون امتحان نظري)!';
      } else {
        requiredLicense = 'Patente BE';
        licenseColor = '#ef4444';
        licenseDesc = 'المجمع يتجاوز 4.250 كجم مع مقطورة ثقيلة تصل حتى 3.500 كجم (المجموع حتى 7.000 كجم)؛ يلزم رخصة BE المتخصصة!';
      }

      return `
        <div class="lp-control-section">
          <div class="lp-control-title">حاسبة أوزان السيارة والمقطورة (Massa Complessiva):</div>

          <div class="lp-slider-box">
            <div class="lp-slider-labels">
              <span>وزن السيارة القاطرة (Motrice):</span>
              <span class="lp-slider-val">${this.carWeight} kg</span>
            </div>
            <input type="range" class="lp-slider" id="carSlider" min="1200" max="3500" step="50" value="${this.carWeight}">
            <div class="lp-slider-ticks">
              <span>1.200 kg</span>
              <span>2.000 kg</span>
              <span>2.800 kg</span>
              <span>3.500 kg</span>
            </div>
          </div>

          <div class="lp-slider-box">
            <div class="lp-slider-labels">
              <span>وزن المقطورة الإجمالي (Rimorchio):</span>
              <span class="lp-slider-val">${this.trailerWeight} kg</span>
            </div>
            <input type="range" class="lp-slider" id="trailerSlider" min="300" max="3500" step="50" value="${this.trailerWeight}">
            <div class="lp-slider-ticks">
              <span>300 kg (خفيف)</span>
              <span>750 kg (الحد الخفيف)</span>
              <span>1.500 kg</span>
              <span>3.500 kg (BE)</span>
            </div>
          </div>
        </div>

        <div class="lp-metrics-grid" style="margin-top:12px;">
          <div class="lp-metric-card">
            <span class="lp-metric-label">تصنيف المقطورة</span>
            <span class="lp-metric-val ${this.trailerWeight <= 750 ? 'safe-val' : 'danger-val'}">${this.trailerWeight <= 750 ? 'خفيفة (Leggero)' : 'ثقيلة (Non leggero)'}</span>
            <span class="lp-metric-sub">الحد الفاصل: 750 كجم</span>
          </div>
          <div class="lp-metric-card">
            <span class="lp-metric-label">الوزن الإجمالي للمجمع</span>
            <span class="lp-metric-val">${totalWeight} kg</span>
            <span class="lp-metric-sub">سيارة (${this.carWeight}) + مقطورة (${this.trailerWeight})</span>
          </div>
          <div class="lp-metric-card">
            <span class="lp-metric-label">الرخصة المطلوبة قانوناً</span>
            <span class="lp-metric-val" style="color:${licenseColor}; font-size:1.0rem;">${requiredLicense}</span>
            <span class="lp-metric-sub">حسب المادة 116 C.d.S.</span>
          </div>
        </div>

        <div class="lp-summary-box" style="margin-top:12px;">
          <div class="lp-legal-tag" style="background:rgba(2, 132, 199, 0.2); color:#38bdf8; border:1px solid #0284c7;">
            🔍 النتيجة: ${licenseDesc}
          </div>
          <div class="lp-trap-box-interactive">
            <div class="lp-trap-header">💡 قاعدة الامتحان الوزاري الإلزامية للمقطورات:</div>
            <p>
              • مقطورة خفيفة (<= 750 كجم): مسموحة <strong>دائماً</strong> مع رخصة B العادية حتى وزن إجمالي 4.250 كجم!<br>
              • مقطورة غير خفيفة (> 750 كجم): مسموحة برخصة B إذا كان المجموع <strong><= 3.500 كجم</strong>.<br>
              • كود 96 (B96): مطلوب حصراً إذا كان المجموع <strong>بين 3.500 كجم و 4.250 كجم</strong>.
            </p>
          </div>
        </div>
      `;
    }

    bindCategorieEvents() {
      const cSlide = document.getElementById('carSlider');
      const tSlide = document.getElementById('trailerSlider');

      if (cSlide) {
        cSlide.addEventListener('input', (e) => {
          this.carWeight = parseInt(e.target.value, 10);
          this.updateUI();
        });
      }
      if (tSlide) {
        tSlide.addEventListener('input', (e) => {
          this.trailerWeight = parseInt(e.target.value, 10);
          this.updateUI();
        });
      }
    }

    // -------------------------------------------------------------
    // TAB 3: SANZIONI (RITIRO, SOSPENSIONE, REVOCA, REVISIONE)
    // -------------------------------------------------------------
    renderSanzioniControls() {
      const sanzioniData = {
        ritiro: {
          title: '1. سحب الرخصة الميداني (Ritiro della Patente)',
          badge: 'إجراء مادي تحفظي فوري من الشرطة',
          reasons: `• انتهاء صلاحية الرخصة (Patente scaduta di validità).<br>• عدم وضع النظارات الطبية الإلزامية المسجلة بالكود 01.<br>• نقل حمولة بشكل غير آمن أو عدم توثيقها.<br>• القيادة تحت تأثير الكحول أو المخدرات بانتظار الفحص الطبي.`,
          solution: `تسلم الرخصة للمحافظ أو الشرطة، وتستعاد فور إزالة المخالفة وتجديد الفحص الطبي.`
        },
        sospensione: {
          title: '2. تعليق الرخصة المؤقت (Sospensione della Patente)',
          badge: 'عقوبة إدارية مانعة للقيادة لمدة محددة',
          reasons: `• تجاوز السرعة بأكثر من 40 كم/س (من شهر إلى 3 أشهر).<br>• السير عكس الاتجاه (Contromano) في المنعطفات والتلال.<br>• القيادة تحت تأثير الكحول (بين 0.5 و 1.5 جم/لتر).<br>• عدم مساعدة المصابين في حادث أو ارتكاب حوادث مع أضرار جسيمة.`,
          solution: `يصدر القرار من المحافظ (Prefetto) أو القاضي (Giudice) وتمنع القيادة طوال فترة التعليق.`
        },
        revoca: {
          title: '3. الإلغاء الدائم للرخصة (Revoca della Patente)',
          badge: 'إلغاء نهائي ومسح شامل لعنوان الرخصة',
          reasons: `• فقدان دائم للأهلية البدنية أو النفسية للقيادة.<br>• القيادة أثناء فترة تعليق الرخصة (Guida con patente sospesa).<br>• تكرار المخالفات الجنائية الخطيرة (Recidiva) أو تجاوز الكحول 1.5 جم/لتر للسائقين المهنيين.<br>• التحويل إلى رخصة أجنبية.`,
          solution: `إلغاء تام؛ لاستعادة حق القيادة يجب الانتظار 2 إلى 3 سنوات ثم إعادة الامتحان من الصفر!`
        },
        revisione: {
          title: '4. إعادة الفحص والتقييم (Revisione della Patente)',
          badge: 'شكوك في الأهلية الفنية أو الطبية',
          reasons: `• استنفاد وتصفير رصيد الـ 20 نقطة بالكامل (Azzeramento dei punti).<br>• ارتكاب مخالفة تسحب 5 نقاط يتبعها حادث خلال عامين.<br>• شكوك جدية لدى السلطات في اللياقة النفسية أو البصرية أو الفنية.`,
          solution: `إلزام السائق خلال 30 يوماً بإعادة الفحص الطبي أو إعادة امتحان النظري والعملي (Esame di idoneità). في حال عدم التقدم، تعلق الرخصة مؤقتاً لحين اجتيازه!`
        }
      };

      const curr = sanzioniData[this.selectedSanzione];

      return `
        <div class="lp-control-section">
          <div class="lp-control-title">اختر الإجراء العقابي لاستكشاف الفروق الامتحانية:</div>
          <div class="lp-btn-toggle-row">
            <button class="lp-toggle-btn ${this.selectedSanzione === 'ritiro' ? 'active' : ''}" data-sanz="ritiro">
              🛑 السحب (Ritiro)
            </button>
            <button class="lp-toggle-btn ${this.selectedSanzione === 'sospensione' ? 'active' : ''}" data-sanz="sospensione">
              ⛔ التعليق (Sospensione)
            </button>
            <button class="lp-toggle-btn ${this.selectedSanzione === 'revoca' ? 'active' : ''}" data-sanz="revoca">
              ❌ الإلغاء (Revoca)
            </button>
            <button class="lp-toggle-btn ${this.selectedSanzione === 'revisione' ? 'active' : ''}" data-sanz="revisione">
              🔍 إعادة التقييم (Revisione)
            </button>
          </div>
        </div>

        <div class="lp-summary-box" style="margin-top:12px;">
          <div class="lp-legal-tag legal-safe" style="font-size:0.95rem;">${curr.title}</div>
          <div style="font-size:0.8rem; color:#38bdf8; font-weight:700; margin-bottom:8px;">${curr.badge}</div>

          <div style="font-size:0.84rem; color:#cbd5e1; line-height:1.7;">
            <strong>الأسباب والحالات الموجبة:</strong><br>
            ${curr.reasons}
          </div>

          <div style="font-size:0.82rem; color:#f8fafc; background:rgba(15, 23, 42, 0.6); padding:8px 12px; border-radius:8px; margin-top:10px; border-right:3px solid #0284c7;">
            <strong>النتيجة القانونية:</strong> ${curr.solution}
          </div>
        </div>

        <div class="lp-trap-box-interactive" style="margin-top:12px;">
          <div class="lp-trap-header">⚠️ سر التمييز في الامتحان الوزاري:</div>
          <p>
            • رخصة منتهية أو بدون نظارة = <strong>RITIRO</strong> (سحب فوري).<br>
            • سرعة +40 كم/س أو كحول = <strong>SOSPENSIONE</strong> (تعليق لفترة).<br>
            • قيادة أثناء التعليق = <strong>REVOCA</strong> (إلغاء نهائي).<br>
            • تصفير الـ 20 نقطة = <strong>REVISIONE</strong> (إعادة فحص وإلزام بإعادة الامتحان)!
          </p>
        </div>
      `;
    }

    bindSanzioniEvents() {
      const sBtns = this.container.querySelectorAll('[data-sanz]');
      sBtns.forEach((b) => {
        b.addEventListener('click', (e) => {
          playSfx();
          this.selectedSanzione = e.currentTarget.getAttribute('data-sanz');
          this.updateUI();
        });
      });
    }

    // -------------------------------------------------------------
    // CANVAS ENGINE (60 FPS)
    // -------------------------------------------------------------
    renderCanvas() {
      const w = this.canvas.width;
      const h = this.canvas.height;
      const ctx = this.ctx;

      ctx.clearRect(0, 0, w, h);

      if (this.activeTab === 'punti') {
        this.drawPuntiScene(w, h, ctx);
      } else if (this.activeTab === 'categorie') {
        this.drawCategorieScene(w, h, ctx);
      } else if (this.activeTab === 'sanzioni') {
        this.drawSanzioniScene(w, h, ctx);
      }
    }

    drawPuntiScene(w, h, ctx) {
      // Dark High-tech Dashboard Background
      ctx.fillStyle = '#090d16';
      ctx.fillRect(0, 0, w, h);

      // Points Deduction Ladder Visual
      const ladderX = w * 0.1;
      const ladderY = 40;
      const ladderW = w * 0.8;
      const ladderH = 120;

      // Draw License Card Mockup
      const cardX = w * 0.5 - 180;
      const cardY = 180;
      const cardW = 360;
      const cardH = 210;

      // Plastic card gradient
      const cardGrad = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY + cardH);
      cardGrad.addColorStop(0, '#fbcfe8');
      cardGrad.addColorStop(0.5, '#f472b6');
      cardGrad.addColorStop(1, '#db2777');

      ctx.fillStyle = cardGrad;
      ctx.beginPath();
      ctx.roundRect(cardX, cardY, cardW, cardH, 14);
      ctx.fill();
      ctx.strokeStyle = '#fdf2f8';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Card Header
      ctx.fillStyle = '#831843';
      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText('REPUBBLICA ITALIANA - PATENTE DI GUIDA', cardX + 20, cardY + 30);

      // EU Flag in card corner
      ctx.fillStyle = '#1d4ed8';
      ctx.fillRect(cardX + cardW - 55, cardY + 15, 38, 24);
      ctx.fillStyle = '#fef08a';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('IT', cardX + cardW - 36, cardY + 31);

      // Photo Silhouette
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(cardX + 20, cardY + 50, 75, 95);
      ctx.fillStyle = '#9d174d';
      ctx.beginPath();
      ctx.arc(cardX + 57, cardY + 80, 18, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillRect(cardX + 35, cardY + 105, 45, 35);

      // Fields (1 to 5)
      ctx.fillStyle = '#4c0519';
      ctx.font = '10px Inter, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText('1. ROSSI', cardX + 110, cardY + 65);
      ctx.fillText('2. MARIO', cardX + 110, cardY + 82);
      ctx.fillText('3. 15/08/1998 ROMA', cardX + 110, cardY + 99);
      ctx.fillText('4a. 12/03/2026  4b. 12/03/2036', cardX + 110, cardY + 116);
      ctx.fillText('5. U1D883719X', cardX + 110, cardY + 133);

      // Category Stamp
      ctx.fillStyle = '#831843';
      ctx.font = 'bold 22px Inter, sans-serif';
      ctx.fillText('B', cardX + 110, cardY + 175);

      // Points Circle Indicator on Card
      let totalDeduction = 0;
      const infList = { cinture: 5, semaforo: 6, precedenza: 5, velocita_40: 6, velocita_60: 10, contromano: 10, ebbrezza: 10 };
      this.selectedInfractions.forEach((infId) => {
        const base = infList[infId] || 0;
        totalDeduction += this.isNeopatentato ? base * 2 : base;
      });
      const effectiveDeduction = Math.min(15, totalDeduction);
      const remainingPoints = Math.max(0, this.currentPoints - effectiveDeduction);

      const circleX = cardX + cardW - 70;
      const circleY = cardY + cardH - 55;

      ctx.beginPath();
      ctx.arc(circleX, circleY, 35, 0, Math.PI * 2);
      ctx.fillStyle = remainingPoints === 0 ? '#ef4444' : remainingPoints <= 10 ? '#f59e0b' : '#10b981';
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 3;
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 20px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`${remainingPoints}`, circleX, circleY + 7);

      ctx.font = '8px Inter, sans-serif';
      ctx.fillText('PUNTI', circleX, circleY + 20);

      // Top Points Progress Gauge
      ctx.fillStyle = 'rgba(30, 41, 59, 0.8)';
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.3)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(ladderX, ladderY, ladderW, ladderH, 12);
      ctx.fill();
      ctx.stroke();

      ctx.font = 'bold 14px Inter, sans-serif';
      ctx.fillStyle = '#38bdf8';
      ctx.textAlign = 'right';
      ctx.fillText(`رصيد النقاط الفعلي: ${remainingPoints} من أصل 20 نقطة`, ladderX + ladderW - 20, ladderY + 30);

      // Bar gauge
      const barW = ladderW - 40;
      const barH = 22;
      const barX = ladderX + 20;
      const barY = ladderY + 50;

      ctx.fillStyle = '#0f172a';
      ctx.fillRect(barX, barY, barW, barH);

      const fillW = (remainingPoints / 20) * barW;
      ctx.fillStyle = remainingPoints === 0 ? '#ef4444' : remainingPoints <= 10 ? '#f59e0b' : '#10b981';
      ctx.fillRect(barX, barY, fillW, barH);

      // Warning text in gauge
      ctx.font = '11px Inter, sans-serif';
      ctx.fillStyle = '#cbd5e1';
      ctx.textAlign = 'center';
      if (remainingPoints === 0) {
        ctx.fillStyle = '#f87171';
        ctx.fillText('🚨 استنفاد النقاط بالكامل! يجب الخضوع لامتحان تقييم الأهلية (Revisione) خلال 30 يوماً', ladderX + ladderW / 2, ladderY + 100);
      } else if (this.isNeopatentato && totalDeduction > 0) {
        ctx.fillText(`⚡ تم تطبيق مضاعفة السائق الجديد (x2): تم خصم ${totalDeduction} نقطة بدلاً من ${totalDeduction / 2}!`, ladderX + ladderW / 2, ladderY + 100);
      } else {
        ctx.fillText('كل سنتين بدون مخالفات تمنح السائق مكافأة نقطتين (+2) حتى سقف 30 نقطة', ladderX + ladderW / 2, ladderY + 100);
      }
    }

    drawCategorieScene(w, h, ctx) {
      // Vehicle + Trailer Geometry on Highway
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, w, h);

      // Road
      const roadY = h * 0.62;
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, roadY, w, 80);

      // Towing Car (Motrice)
      const carW = 160;
      const carH = 75;
      const carX = w * 0.22;
      const carY = roadY - carH;

      ctx.fillStyle = '#0284c7';
      ctx.beginPath();
      ctx.roundRect(carX, carY + 20, carW, carH - 20, 8);
      ctx.fill();
      // Cabin
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath();
      ctx.roundRect(carX + 35, carY, carW - 55, 35, 6);
      ctx.fill();

      // Car Wheels
      ctx.fillStyle = '#000000';
      ctx.beginPath();
      ctx.arc(carX + 35, roadY, 16, 0, Math.PI * 2);
      ctx.arc(carX + carW - 35, roadY, 16, 0, Math.PI * 2);
      ctx.fill();

      // Tow Hitch (Gancio di traino)
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(carX + carW, roadY - 15);
      ctx.lineTo(carX + carW + 40, roadY - 15);
      ctx.stroke();

      // Trailer (Rimorchio)
      const trailW = Math.max(100, Math.min(200, (this.trailerWeight / 3500) * 180 + 70));
      const trailH = Math.max(60, Math.min(105, (this.trailerWeight / 3500) * 80 + 50));
      const trailX = carX + carW + 40;
      const trailY = roadY - trailH;

      // Trailer Body
      ctx.fillStyle = this.trailerWeight <= 750 ? '#10b981' : '#f59e0b';
      ctx.beginPath();
      ctx.roundRect(trailX, trailY, trailW, trailH, 6);
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Trailer Wheel
      ctx.fillStyle = '#000000';
      ctx.beginPath();
      ctx.arc(trailX + trailW / 2, roadY, 15, 0, Math.PI * 2);
      ctx.fill();

      // Weight Badges on Vehicles
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`السيارة: ${this.carWeight} kg`, carX + carW / 2, carY + 45);
      ctx.fillText(`المقطورة: ${this.trailerWeight} kg`, trailX + trailW / 2, trailY + trailH / 2);

      // Top Diagnostic Box
      const totalWeight = this.carWeight + this.trailerWeight;
      const boxW = w * 0.85;
      const boxH = 95;
      const boxX = w * 0.075;
      const boxY = 25;

      ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
      ctx.strokeStyle = totalWeight > 4250 ? '#ef4444' : totalWeight > 3500 ? '#f59e0b' : '#10b981';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(boxX, boxY, boxW, boxH, 10);
      ctx.fill();
      ctx.stroke();

      ctx.font = 'bold 15px Inter, sans-serif';
      ctx.fillStyle = '#38bdf8';
      ctx.textAlign = 'center';
      ctx.fillText(`الوزن الإجمالي للمجمع: ${totalWeight} كجم`, w * 0.5, boxY + 30);

      ctx.font = '12px Inter, sans-serif';
      ctx.fillStyle = '#cbd5e1';
      if (this.trailerWeight <= 750) {
        ctx.fillText('✔ مقطورة خفيفة (Leggero <= 750 kg): مسموحة برخصة B القياسية حتى 4.250 كجم', w * 0.5, boxY + 60);
      } else if (totalWeight <= 3500) {
        ctx.fillText('✔ مقطورة ثقيلة لكن المجمع <= 3.500 كجم: تكفي رخصة B القياسية', w * 0.5, boxY + 60);
      } else if (totalWeight <= 4250) {
        ctx.fillStyle = '#fbbf24';
        ctx.fillText('⚠️ المجمع بين 3.500 و 4.250 كجم: يلزم رخصة B مع الكود المنسق 96 (B96)', w * 0.5, boxY + 60);
      } else {
        ctx.fillStyle = '#f87171';
        ctx.fillText('🚨 المجمع يتجاوز 4.250 كجم: يلزم رخصة قيادة المقطورات الثقيلة BE (حتى 7 طن)!', w * 0.5, boxY + 60);
      }
    }

    drawSanzioniScene(w, h, ctx) {
      // 4 Pillar Comparison Grid on Canvas
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, w, h);

      const cols = [
        { id: 'ritiro', name: 'RITIRO (سحب)', sub: 'إجراء فوري ومؤقت', color: '#f59e0b' },
        { id: 'sospensione', name: 'SOSPENSIONE (تعليق)', sub: 'عقوبة من شهر لسنتين', color: '#ef4444' },
        { id: 'revoca', name: 'REVOCA (إلغاء)', sub: 'إلغاء دائم ومسح للرخصة', color: '#991b1b' },
        { id: 'revisione', name: 'REVISIONE (مراجعة)', sub: 'إعادة فحص طبي أو نظري', color: '#0284c7' }
      ];

      const colW = (w - 70) / 4;
      const colH = 320;
      const startY = 50;

      cols.forEach((col, idx) => {
        const x = 20 + idx * (colW + 10);
        const isSelected = this.selectedSanzione === col.id;

        ctx.fillStyle = isSelected ? 'rgba(30, 41, 59, 0.95)' : 'rgba(15, 23, 42, 0.7)';
        ctx.strokeStyle = isSelected ? col.color : 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = isSelected ? 3 : 1;
        ctx.beginPath();
        ctx.roundRect(x, startY, colW, colH, 10);
        ctx.fill();
        ctx.stroke();

        // Top Header
        ctx.fillStyle = col.color;
        ctx.fillRect(x, startY, colW, 45);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 12px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(col.name, x + colW / 2, startY + 28);

        ctx.font = '10px Inter, sans-serif';
        ctx.fillStyle = '#cbd5e1';
        ctx.fillText(col.sub, x + colW / 2, startY + 70);

        // Content lines
        ctx.font = '10px Inter, sans-serif';
        ctx.fillStyle = '#94a3b8';
        ctx.textAlign = 'right';

        if (col.id === 'ritiro') {
          ctx.fillText('• رخصة منتهية الصلاحية', x + colW - 10, startY + 110);
          ctx.fillText('• عدم ارتداء النظارات', x + colW - 10, startY + 135);
          ctx.fillText('• حمولة غير مربوطة', x + colW - 10, startY + 160);
          ctx.fillText('• سحب مادي من الشرطة', x + colW - 10, startY + 185);
        } else if (col.id === 'sospensione') {
          ctx.fillText('• سرعة +40 إلى +60 كم/س', x + colW - 10, startY + 110);
          ctx.fillText('• سير عكس الاتجاه', x + colW - 10, startY + 135);
          ctx.fillText('• كحول بين 0.5 و 1.5', x + colW - 10, startY + 160);
          ctx.fillText('• قرار من المحافظ/القاضي', x + colW - 10, startY + 185);
        } else if (col.id === 'revoca') {
          ctx.fillText('• قيادة برخصة معلقة', x + colW - 10, startY + 110);
          ctx.fillText('• فقدان دائم للياقة', x + colW - 10, startY + 135);
          ctx.fillText('• كحول فوق 1.5 مكرر', x + colW - 10, startY + 160);
          ctx.fillText('• إعادة الامتحان من الصفر', x + colW - 10, startY + 185);
        } else if (col.id === 'revisione') {
          ctx.fillText('• تصفير الـ 20 نقطة', x + colW - 10, startY + 110);
          ctx.fillText('• حادث بعد خصم 5 نقاط', x + colW - 10, startY + 135);
          ctx.fillText('• مهلة 30 يوماً فقط', x + colW - 10, startY + 160);
          ctx.fillText('• فحص طبي أو نظري/عملي', x + colW - 10, startY + 185);
        }
      });
    }
  }

  // Initialize on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      new LicensePenaltiesStudio('licensePenaltiesStudioContainer');
    });
  } else {
    new LicensePenaltiesStudio('licensePenaltiesStudioContainer');
  }
})();

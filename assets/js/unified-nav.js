/**
 * =======================================================================
 * Patente B Pro - Unified Navigation, Header, Footer & Security Suite
 * =======================================================================
 * @author Patente B Pro Architecture & UX Team (2026)
 * @description
 * - توحيد شريط التنقل العلوي (Global Unified Header) لجميع صفحات المنصة
 * - توحيد قائمة الموبايل الاحترافية (Mobile Drawer with Backdrop Blur)
 * - توحيد الفوتر الذكي (Unified Footer with Scroll-to-Top & Hub Links)
 * - تعزيز الأمان: SafeStorage (حماية التخزين المحلي) و safeHtml (حماية DOM-XSS) و Link Hardening
 */

(function () {
  'use strict';

  // 1. ==================== أمان البيانات وحماية المدخلات ====================
  const sanitizeStr = function (str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  };
  window.safeHtml = window.safeHtml || sanitizeStr;
  window.escapeHtml = window.escapeHtml || sanitizeStr;

  window.SafeStorage = {
    _mem: {},
    get: function (key, defVal) {
      if (defVal === undefined) defVal = null;
      try {
        const item = localStorage.getItem(key);
        if (item === null) return defVal;
        try {
          return JSON.parse(item);
        } catch (_) {
          return item; // Fallback for raw string
        }
      } catch (err) {
        return this._mem[key] !== undefined ? this._mem[key] : defVal;
      }
    },
    set: function (key, val) {
      try {
        const strVal = typeof val === 'string' ? val : JSON.stringify(val);
        localStorage.setItem(key, strVal);
      } catch (err) {
        console.warn('[SafeStorage] Storage fallback to memory:', err);
        this._mem[key] = val;
      }
    },
    remove: function (key) {
      try {
        localStorage.removeItem(key);
      } catch (err) {
        delete this._mem[key];
      }
    }
  };

  // 2. ==================== تحديد مسارات الروابط تلقائياً ====================
  function getPathContext() {
    const rawPath = (window.location.pathname || '').replace(/\\/g, '/');
    const parts = rawPath.split('/').filter(Boolean);
    const currentFile = parts.length > 0 ? parts[parts.length - 1] : 'index.html';

    // هل نحن داخل مجلد فرعي داخل Capitoli_Divisi (مثل Capitolo_01_definizioni_generali)؟
    if (/\/Capitoli_Divisi\/Capitolo_[^\/]+/i.test(rawPath)) {
      return {
        root: '../../',
        interactive: '../../interactive_pages/',
        capitoli: '../',
        currentFile: currentFile,
        fullPath: rawPath
      };
    }
    // هل نحن في Capitoli_Divisi مباشرة؟
    if (/\/Capitoli_Divisi/i.test(rawPath)) {
      return {
        root: '../',
        interactive: '../interactive_pages/',
        capitoli: './',
        currentFile: currentFile,
        fullPath: rawPath
      };
    }
    // هل نحن في interactive_pages؟
    if (/\/interactive_pages/i.test(rawPath)) {
      return {
        root: '../',
        interactive: './',
        capitoli: '../Capitoli_Divisi/',
        currentFile: currentFile,
        fullPath: rawPath
      };
    }
    // في الجذر (Root)
    return {
      root: './',
      interactive: './interactive_pages/',
      capitoli: './Capitoli_Divisi/',
      currentFile: currentFile,
      fullPath: rawPath
    };
  }

  // 3. ==================== بيانات الأبواب الـ 25 للتنقل السريع ====================
  const CHAPTERS_DATA = [
    { num: 1, title: 'المفاهيم العامة وواجبات الطريق', folder: 'Capitolo_01_definizioni_generali_doveri_strada', guide: 'دليل_الباب_01_المفاهيم_العامة_وواجبات_مستخدمي_الطريق.html' },
    { num: 2, title: 'إشارات الخطر (Pericolo)', folder: 'Capitolo_02_segnali_pericolo', guide: 'دليل_الباب_02_إشارات_الخطر.html' },
    { num: 3, title: 'إشارات المنع (Divieto)', folder: 'Capitolo_03_segnali_divieto', guide: 'دليل_الباب_03_إشارات_المنع.html' },
    { num: 4, title: 'إشارات الإلزام (Obbligo)', folder: 'Capitolo_04_segnali_obbligo', guide: 'دليل_الباب_04_إشارات_الإلزام.html' },
    { num: 5, title: 'إشارات الأسبقية (Precedenza)', folder: 'Capitolo_05_segnali_precedenza', guide: 'دليل_الباب_05_إشارات_الأسبقية.html' },
    { num: 6, title: 'العلامات الأرضية والمطبات', folder: 'Capitolo_06_segnaletica_orizzontale_ostacoli', guide: 'دليل_الباب_06_العلامات_الأرضية_والإشارات_الأفقية.html' },
    { num: 7, title: 'إشارات المرور الضوئية والشرطي', folder: 'Capitolo_07_semafori_vigili', guide: 'دليل_الباب_07_إشارات_المرور_الضوئية_ورجال_الشرطة.html' },
    { num: 8, title: 'إشارات الإرشاد والمعلومات والخدمات', folder: 'Capitolo_08_segnali_indicazione', guide: 'دليل_الباب_08_إشارات_الإرشاد_والمعلومات.html' },
    { num: 9, title: 'إشارات الورش والتحويلات المؤقتة', folder: 'Capitolo_09_segnali_complementari_cantiere', guide: 'دليل_الباب_09_الإشارات_التكميلية_وورش_العمل.html' },
    { num: 10, title: 'اللوحات الإضافية الملحقة بالإشارات', folder: 'Capitolo_10_pannelli_integrativi', guide: 'دليل_الباب_10_اللوحات_الإضافية_الملحقة_بالإشارات.html' },
    { num: 11, title: 'حدود السرعة ومخاطرها', folder: 'Capitolo_11_limiti_di_velocita', guide: 'دليل_الباب_11_حدود_السرعة_ومخاطرها.html' },
    { num: 12, title: 'مسافة الأمان والعوامل المؤثرة', folder: 'Capitolo_12_distanza_di_sicurezza', guide: 'دليل_الباب_12_مسافة_الأمان_والعوامل_المؤثرة.html' },
    { num: 13, title: 'قواعد السير وتنظيم الحارات والمسارات', folder: 'Capitolo_13_norme_di_circolazione', guide: 'دليل_الباب_13_قواعد_السير_والمسارات.html' },
    { num: 14, title: 'أسبقية المرور وفك التقاطعات المعقدة', folder: 'Capitolo_14_precedenza_incroci', guide: 'دليل_الباب_14_أسبقية_المرور_وفك_التقاطعات.html' },
    { num: 15, title: 'مناورة التجاوز والتخطي (Sorpasso)', folder: 'Capitolo_15_sorpasso', guide: 'دليل_الباب_15_مناورة_التجاوز_والتخطي.html' },
    { num: 16, title: 'الوقوف والتوقف والركن (Sosta e Fermata)', folder: 'Capitolo_16_fermata_sosta_arresto', guide: 'دليل_الباب_16_الوقوف_والتوقف_والركن.html' },
    { num: 17, title: 'الأوتوستراد وسحب المقطورات والحمولة', folder: 'Capitolo_17_norme_varie_autostrade_pannelli', guide: 'دليل_الباب_17_الأوتوستراد_والحمولة_وسحب_المقطورات.html' },
    { num: 18, title: 'استخدام الأضواء ولمبات التابلوه', folder: 'Capitolo_18_luci_dispositivi_acustici', guide: 'دليل_الباب_18_استخدام_الأضواء_ولمبات_التابلوه_والعواكس.html' },
    { num: 19, title: 'أحزمة الأمان والخوذة ومقاعد الأطفال', folder: 'Capitolo_19_cinture_casco_sicurezza', guide: 'دليل_الباب_19_أحزمة_الأمان_والخوذة_ومقاعد_الأطفال.html' },
    { num: 20, title: 'رخص القيادة والنقاط والعقوبات الرسمية', folder: 'Capitolo_20_patente_punti_documenti', guide: 'دليل_الباب_20_رخص_القيادة_والنقاط_والعقوبات.html' },
    { num: 21, title: 'حوادث السير وظروف الطقس الصعبة', folder: 'Capitolo_21_incidenti_stradali_comportamenti', guide: 'دليل_الباب_21_حوادث_السير_وظروف_الطقس_الصعبة.html' },
    { num: 22, title: 'الكحول والمخدرات والإسعافات الأولية', folder: 'Capitolo_22_alcool_droga_primo_soccorso', guide: 'دليل_الباب_22_الكحول_والمخدرات_والإسعافات_الأولية.html' },
    { num: 23, title: 'المسؤولية المدنية والجنائية والتأمين RCA', folder: 'Capitolo_23_responsabilita_civile_penale_e_assicurazione', guide: 'دليل_الباب_23_المسؤولية_والتأمين.html' },
    { num: 24, title: 'استهلاك الوقود وحماية البيئة والتلوث', folder: 'Capitolo_24_consumi_ambiente_inquinamento', guide: 'دليل_الباب_24_استهلاك_الوقود_وحماية_البيئة.html' },
    { num: 25, title: 'الميكانيكا وصيانة المركبة وأجهزة الأمان', folder: 'Capitolo_25_elementi_veicolo_manutenzione_comportamenti', guide: 'دليل_الباب_25_الميكانيكا_وصيانة_المركبة_وأجهزة_الأمان.html' }
  ];

  // 4. ==================== بناء الهيدر الموحد ====================
  function renderGlobalHeader(ctx) {
    const cur = ctx.currentFile.toLowerCase();
    const full = (ctx.fullPath || '').toLowerCase();

    const isGuide = (full.includes('interactive_pages') && (cur.includes('index') || cur === '' || cur === 'interactive_pages')) || 
                    cur.includes('دليل') || 
                    cur.includes('guida');
    const isHub = (full.includes('capitoli_divisi') && cur.includes('index')) || 
                  (!full.includes('interactive_pages') && cur.includes('index') && !isGuide);
    const isPiano = cur.includes('piano-studio');
    const isParole = cur.includes('parole-spia');
    const isIncroci = cur.includes('decodificatore-incroci');
    const isTrucchi = cur.includes('trucchi-esame');
    const isNumeri = cur.includes('laboratorio-numeri');
    const isSoccorso = cur.includes('primo-soccorso');
    const isScheda = cur.includes('scheda-esame');
    const isCards = cur.includes('flashcards');
    const isDash = cur.includes('dashboard');
    const isTraps = cur.includes('traps_and_games');
    const isAllenamento = cur.includes('allenamento-capitolo');

    const navItems = [
      { id: 'guide', label: 'شرح الأبواب (1-25)', icon: '📖', href: ctx.interactive + 'index.html', active: isGuide },
      { id: 'hub', label: 'بنك أسئلة الأبواب', icon: '📝', href: ctx.capitoli + 'index.html', active: isHub },
      { id: 'piano', label: 'خطة الدراسة', icon: '📅', href: ctx.interactive + 'piano-studio.html', active: isPiano },
      { id: 'parole', label: 'رادار الكلمات', icon: '🎯', href: ctx.interactive + 'parole-spia.html', active: isParole },
      { id: 'incroci', label: 'مفكك التقاطعات', icon: '🔄', href: ctx.interactive + 'decodificatore-incroci.html', active: isIncroci },
      { id: 'trucchi', label: 'خزينة التريكات', icon: '💎', href: ctx.interactive + 'trucchi-esame.html', active: isTrucchi },
      { id: 'numeri', label: 'معمل الأرقام', icon: '📏', href: ctx.interactive + 'laboratorio-numeri.html', active: isNumeri },
      { id: 'soccorso', label: 'الإسعافات', icon: '🚑', href: ctx.interactive + 'primo-soccorso.html', active: isSoccorso },
      { id: 'scheda', label: 'محاكي الامتحان', icon: '⏱️', href: ctx.interactive + 'scheda-esame.html', active: isScheda },
      { id: 'flashcards', label: 'فلاش كاردز', icon: '🗂️', href: ctx.interactive + 'flashcards.html', active: isCards },
      { id: 'dashboard', label: 'لوحة التقدم', icon: '📊', href: ctx.interactive + 'dashboard.html', active: isDash },
      { id: 'traps', label: 'بنك الفخاخ', icon: '🎮', href: ctx.interactive + 'traps_and_games.html', active: isTraps }
    ];

    if (isAllenamento) {
      navItems.unshift({ id: 'allenamento', label: 'تدريب الباب', icon: '⚡', href: '#', active: true });
    }

    const desktopTabsHtml = navItems.map(item => `
      <a href="${item.href}" class="nav-tab-desktop ${item.active ? 'active' : ''}">
        <span class="nav-tab-icon">${item.icon}</span>
        <span>${item.label}</span>
      </a>
    `).join('');

    const drawerItemsHtml = navItems.map(item => `
      <a href="${item.href}" class="mobile-drawer-link ${item.active ? 'active' : ''}">
        <span class="drawer-link-icon">${item.icon}</span>
        <span class="drawer-link-text">${item.label}</span>
        ${item.active ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
      </a>
    `).join('');

    const chaptersListHtml = CHAPTERS_DATA.map(ch => {
      const chPad = ch.num < 10 ? '0' + ch.num : String(ch.num);
      const isCur = cur.includes(`capitolo_${chPad}`) || 
                    cur.includes(`الباب_${chPad}`) ||
                    cur.includes(`الباب_${ch.num}`);
      return `
        <div class="mobile-drawer-chapter-row ${isCur ? 'active' : ''}">
          <div class="drawer-ch-header">
            <span class="drawer-ch-badge">الباب ${chPad}</span>
            <span class="drawer-ch-name" title="${ch.title}">${ch.title}</span>
          </div>
          <div class="drawer-ch-pills">
            <a href="${ctx.capitoli}${ch.folder}/index.html" class="drawer-ch-pill quiz" title="كويز وبنك أسئلة">
              <span>📝 أسئلة</span>
            </a>
            <a href="${ctx.interactive}${ch.guide}" class="drawer-ch-pill guide" title="الشرح والقاموس">
              <span>📖 شرح</span>
            </a>
          </div>
        </div>
      `;
    }).join('');

    return `
      <header class="unified-portal-nav" id="globalPortalNav">
        <div class="nav-brand-group" style="display:flex; align-items:center; gap:10px;">
          <a href="${ctx.capitoli}index.html" class="nav-brand" title="الرئيسية — Patente B Pro">
            <span style="font-size:1.35rem; line-height:1;">🚦</span>
            <span>Patente B Pro</span>
            <span class="badge-tag">2026</span>
          </a>
        </div>

        <nav class="nav-desktop-tabs" id="globalDesktopTabs">
          ${desktopTabsHtml}
        </nav>

        <div class="nav-desktop-actions" id="globalDesktopActions" style="display:flex; align-items:center; gap:8px;">
          <button class="nav-theme-btn" onclick="window.toggleTheme && window.toggleTheme()" title="تبديل الوضع (نهاري / ليلي) [Alt + T]">
            <span class="theme-icon-span">☀️</span>
            <span class="theme-label-span">الوضع</span>
          </button>
        </div>

        <!-- أزرار الموبايل المستقلة (خارج nav-desktop-actions لضمان الظهور 100% على كافة الشاشات) -->
        <div class="nav-mobile-controls" id="globalMobileControls">
          <button class="nav-theme-btn nav-mobile-theme-btn" onclick="window.toggleTheme && window.toggleTheme()" title="تبديل الوضع" aria-label="تبديل الوضع">
            <span class="theme-icon-span">☀️</span>
          </button>

          <button class="nav-hamburger-btn nav-mobile-hamburger" id="btnToggleMobileDrawer" aria-label="فتح قائمة التنقل وتصفح الأبواب" aria-expanded="false">
            <div class="hamburger-box">
              <span class="hamburger-line line-top"></span>
              <span class="hamburger-line line-mid"></span>
              <span class="hamburger-line line-bot"></span>
            </div>
          </button>
        </div>
      </header>

      <!-- قائمة الموبايل السلسة (Mobile Drawer) -->
      <div class="mobile-drawer-backdrop" id="mobileDrawerBackdrop">
        <aside class="mobile-drawer-pane" id="mobileDrawerPane">
          <div class="mobile-drawer-header">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:1.35rem;">🚦</span>
              <div>
                <strong style="font-size:1.02rem; color:var(--text-primary, #FFF); display:block; line-height:1.2;">Patente B Pro</strong>
                <span style="font-size:0.75rem; color:#94A3B8;">القائمة الموحدة وتصفح الأبواب</span>
              </div>
            </div>
            <button class="mobile-drawer-close" id="btnCloseMobileDrawer" aria-label="إغلاق القائمة">✕</button>
          </div>

          <div class="mobile-drawer-links-wrap">
            <div class="mobile-drawer-section-label">🏛️ الأقسام والأدوات الرئيسية</div>
            ${drawerItemsHtml}

            <div class="mobile-drawer-divider"></div>

            <div class="mobile-drawer-accordion-btn" id="btnToggleChaptersAccordion" role="button" tabindex="0">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:1.15rem;">📚</span>
                <span style="font-weight:800; color:var(--text-primary, #FFF);">تصفح الأبواب المقسمة (1 - 25)</span>
              </div>
              <span class="accordion-arrow" id="chaptersAccordionArrow" style="transition:transform 0.25s ease; font-size:0.9rem;">▾</span>
            </div>

            <div class="mobile-drawer-chapters-container" id="mobileChaptersContainer">
              ${chaptersListHtml}
            </div>
          </div>

          <div class="mobile-drawer-footer">
            <button class="mobile-control-btn" onclick="window.toggleTheme && window.toggleTheme()">
              <span class="theme-icon-span">☀️</span>
              <span class="theme-label-span">تبديل الوضع النهاري / الليلي</span>
            </button>
          </div>
        </aside>
      </div>
    `;
  }

  // 4. ==================== بناء الفوتر الموحد (Developer Signature Footer) ====================
  function renderGlobalFooter(ctx) {
    return `
      <footer class="unified-portal-footer" id="globalPortalFooter">
        <div class="footer-inner-container">
          <div class="dev-footer-card">
            <div class="dev-info-left">
              <div class="dev-avatar-wrap">
                <span class="dev-avatar-icon">👨‍💻</span>
              </div>
              <div class="dev-text-details">
                <div class="dev-name-row">
                  <span class="dev-name">Eng. Ramy Eid Saad Fahmy</span>
                  <span class="dev-badge">Ingegnere Informatico</span>
                </div>
                <p class="dev-sub-desc">
                  Full Stack & Automation Developer • Brindisi, Italia
                </p>
              </div>
            </div>

            <div class="dev-links-right">
              <a href="https://portfolio-taupe-eight-84.vercel.app/" target="_blank" rel="noopener noreferrer" class="dev-pill-btn" title="Portfolio Personale">
                <span>🌐</span>
                <span>Portfolio</span>
              </a>
              <a href="https://github.com/Ramy3id" target="_blank" rel="noopener noreferrer" class="dev-pill-btn" title="GitHub Profile">
                <span>💻</span>
                <span>GitHub</span>
              </a>
              <a href="mailto:ramyeid.dev@gmail.com" class="dev-pill-btn" title="Email: ramyeid.dev@gmail.com">
                <span>✉️</span>
                <span>Email</span>
              </a>
              <a href="https://wa.me/393447044605" target="_blank" rel="noopener noreferrer" class="dev-pill-btn" title="WhatsApp: (+39) 3447044605">
                <span>💬</span>
                <span>WhatsApp</span>
              </a>
              <button class="footer-btn-scrolltop" onclick="window.scrollTo({top:0, behavior:'smooth'})" title="العودة لأعلى الصفحة (Scroll to top)">
                <span>⬆️</span>
              </button>
            </div>
          </div>

          <div class="dev-copyright-row">
            <span>Patente B Pro &copy; 2026 • Progettato e sviluppato da <strong>Eng. Ramy Eid Saad Fahmy</strong></span>
            <span class="dev-status-pill">⚡ Offline PWA Ready</span>
          </div>
        </div>
      </footer>
    `;
  }

  // 5. ==================== التنسيقات المتكاملة ====================
  function injectStyles() {
    if (document.getElementById('unifiedNavCustomStyles')) return;
    const style = document.createElement('style');
    style.id = 'unifiedNavCustomStyles';
    style.textContent = `
      /* الهيدر الموحد */
      .unified-portal-nav {
        position: sticky;
        top: 0;
        z-index: 9999;
        min-height: 56px;
        background: rgba(11, 15, 25, 0.92);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 18px;
        gap: 12px;
        box-sizing: border-box;
      }
      html.light .unified-portal-nav {
        background: rgba(255, 255, 255, 0.95);
        border-bottom: 1px solid rgba(15, 23, 42, 0.09);
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
      }

      /* الشعار والوسم */
      .nav-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.02rem;
        font-weight: 800;
        color: #FFFFFF;
        text-decoration: none;
        white-space: nowrap;
        flex-shrink: 0;
      }
      html.light .nav-brand {
        color: #0F172A;
      }
      .nav-brand .badge-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        padding: 2px 7px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38BDF8;
        border-radius: 6px;
        font-weight: 700;
      }
      html.light .nav-brand .badge-tag {
        background: rgba(2, 132, 199, 0.08);
        border-color: rgba(2, 132, 199, 0.25);
        color: #0284C7;
      }

      /* ألسنة التبويب للديسكتوب */
      .nav-desktop-tabs {
        display: flex;
        align-items: center;
        gap: 4px;
        overflow-x: auto;
        scrollbar-width: none;
        flex: 1;
        justify-content: center;
        padding: 0 10px;
      }
      .nav-desktop-tabs::-webkit-scrollbar {
        display: none;
      }
      .nav-tab-desktop {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 11px;
        border-radius: 8px;
        color: #94A3B8;
        text-decoration: none;
        font-size: 0.82rem;
        font-weight: 700;
        transition: all 0.15s ease;
        white-space: nowrap;
        background: transparent;
        border: 1px solid transparent;
      }
      .nav-tab-desktop:hover {
        color: #FFFFFF;
        background: rgba(255, 255, 255, 0.06);
      }
      .nav-tab-desktop.active {
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.12);
        border-color: rgba(56, 189, 248, 0.25);
      }
      html.light .nav-tab-desktop {
        color: #334155;
      }
      html.light .nav-tab-desktop:hover {
        color: #0F172A;
        background: rgba(15, 23, 42, 0.05);
      }
      html.light .nav-tab-desktop.active {
        color: #0284C7;
        background: rgba(2, 132, 199, 0.1);
        border-color: rgba(2, 132, 199, 0.28);
      }

      /* عناصر التحكم للموبايل والهمبرغر */
      .nav-mobile-controls {
        display: none;
      }
      .nav-mobile-hamburger, .nav-hamburger-btn {
        display: none;
        width: 42px;
        height: 42px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #FFF;
        border-radius: 12px;
        cursor: pointer;
        align-items: center;
        justify-content: center;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        padding: 0;
        flex-shrink: 0;
      }
      html.light .nav-mobile-hamburger,
      html.light .nav-hamburger-btn {
        background: rgba(15, 23, 42, 0.05);
        border-color: rgba(15, 23, 42, 0.12);
        color: #0F172A;
      }
      .nav-mobile-hamburger:hover, .nav-hamburger-btn:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: rgba(56, 189, 248, 0.3);
        color: #38BDF8;
      }
      .nav-mobile-hamburger:active, .nav-hamburger-btn:active {
        transform: scale(0.92);
      }
      .hamburger-box {
        width: 20px;
        height: 14px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        pointer-events: none;
      }
      .hamburger-line {
        display: block;
        width: 100%;
        height: 2px;
        background-color: currentColor;
        border-radius: 2px;
        transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s, background-color 0.2s;
      }
      .nav-hamburger-btn.is-active .line-top,
      .nav-mobile-hamburger.is-active .line-top {
        transform: translateY(6px) rotate(45deg);
        background-color: #38BDF8;
      }
      .nav-hamburger-btn.is-active .line-mid,
      .nav-mobile-hamburger.is-active .line-mid {
        opacity: 0;
        transform: scaleX(0);
      }
      .nav-hamburger-btn.is-active .line-bot,
      .nav-mobile-hamburger.is-active .line-bot {
        transform: translateY(-6px) rotate(-45deg);
        background-color: #38BDF8;
      }
      .nav-mobile-theme-btn {
        width: 42px;
        height: 42px;
        padding: 0;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #FFF;
        font-size: 1.15rem;
        cursor: pointer;
      }
      html.light .nav-mobile-theme-btn {
        background: rgba(15, 23, 42, 0.05);
        border-color: rgba(15, 23, 42, 0.1);
        color: #0F172A;
      }
      @media (max-width: 992px) {
        .nav-desktop-tabs { display: none !important; }
        .nav-desktop-actions { display: none !important; }
        .nav-mobile-controls {
          display: flex !important;
          align-items: center;
          gap: 8px;
        }
        .nav-mobile-hamburger, .nav-hamburger-btn {
          display: inline-flex !important;
        }
      }

      /* القوائم المنسدلة الذكية */
      .nav-dropdown-wrapper {
        position: relative;
        display: inline-flex;
        align-items: center;
      }
      .nav-dropdown-btn {
        height: 34px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 8px;
        color: #e4e4e7;
        font-size: 0.82rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s ease;
        font-family: inherit;
        white-space: nowrap;
      }
      html.light .nav-dropdown-btn {
        background: rgba(15, 23, 42, 0.05);
        border-color: rgba(15, 23, 42, 0.15);
        color: #0f172a;
      }
      .nav-dropdown-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(56, 189, 248, 0.3);
      }
      html.light .nav-dropdown-btn:hover {
        background: rgba(15, 23, 42, 0.08);
        border-color: rgba(2, 132, 199, 0.35);
      }
      .nav-dropdown-menu {
        position: absolute;
        top: calc(100% + 8px);
        left: 0;
        width: 290px;
        max-height: 480px;
        overflow-y: auto;
        background: #18181b;
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 12px;
        padding: 8px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
        display: none;
        z-index: 10001;
      }
      html.light .nav-dropdown-menu {
        background: #ffffff;
        border-color: rgba(15, 23, 42, 0.12);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.15);
      }
      .nav-dropdown-menu.show { display: block; }
      .nav-dropdown-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        border-radius: 8px;
        color: #d4d4d8;
        text-decoration: none;
        font-size: 0.84rem;
        font-weight: 600;
        transition: all 0.15s ease;
      }
      html.light .nav-dropdown-item {
        color: #334155;
      }
      .nav-dropdown-item:hover, .nav-dropdown-item.active {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
      }
      html.light .nav-dropdown-item:hover, html.light .nav-dropdown-item.active {
        background: rgba(217, 119, 6, 0.12);
        color: #d97706;
      }

      /* قائمة الموبايل Drawer */
      .mobile-drawer-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.65);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        z-index: 99999;
        display: none;
        opacity: 0;
        transition: opacity 0.25s ease;
      }
      .mobile-drawer-backdrop.open {
        display: block;
        opacity: 1;
      }
      .mobile-drawer-pane {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        width: 85%;
        max-width: 340px;
        background: #0F172A;
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: -8px 0 28px rgba(0, 0, 0, 0.4);
        padding: 20px;
        box-sizing: border-box;
      }
      html.light .mobile-drawer-pane {
        background: #FFFFFF;
        border-left: 1px solid rgba(15, 23, 42, 0.12);
        box-shadow: -8px 0 28px rgba(15, 23, 42, 0.15);
      }
      .mobile-drawer-backdrop.open .mobile-drawer-pane {
        transform: translateX(0);
      }
      .mobile-drawer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 16px;
      }
      html.light .mobile-drawer-header {
        border-bottom-color: rgba(15, 23, 42, 0.08);
      }
      .mobile-drawer-close {
        background: transparent;
        border: none;
        color: #94A3B8;
        font-size: 1.3rem;
        cursor: pointer;
        padding: 4px;
      }
      .mobile-drawer-links-wrap {
        flex: 1;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      .mobile-drawer-link {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 12px;
        text-decoration: none;
        color: #94A3B8;
        font-weight: 700;
        font-size: 0.92rem;
        transition: all 0.15s;
      }
      html.light .mobile-drawer-link {
        color: #334155;
      }
      .mobile-drawer-link:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #FFF;
      }
      html.light .mobile-drawer-link:hover {
        background: rgba(15, 23, 42, 0.05);
        color: #0F172A;
      }
      .mobile-drawer-link.active {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
      }
      html.light .mobile-drawer-link.active {
        background: rgba(2, 132, 199, 0.1);
        color: #0284C7;
        border-color: rgba(2, 132, 199, 0.28);
      }
      .drawer-link-badge {
        margin-right: auto;
        font-size: 0.7rem;
        padding: 2px 6px;
        border-radius: 6px;
        background: #38BDF8;
        color: #0B0F19;
        font-weight: 800;
      }

      /* تنسيقات أقسام وتفريعات قائمة الموبايل والأبواب الـ 25 */
      .mobile-drawer-section-label {
        font-size: 0.76rem;
        font-weight: 800;
        text-transform: uppercase;
        color: #71717A;
        letter-spacing: 0.05em;
        margin: 10px 4px 6px;
      }
      html.light .mobile-drawer-section-label {
        color: #64748B;
      }
      .mobile-drawer-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
        margin: 14px 0;
      }
      html.light .mobile-drawer-divider {
        background: rgba(15, 23, 42, 0.08);
      }
      .mobile-drawer-accordion-btn {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 11px 14px;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.22);
        border-radius: 12px;
        cursor: pointer;
        font-size: 0.88rem;
        margin-bottom: 8px;
        transition: all 0.2s ease;
      }
      .mobile-drawer-accordion-btn:hover {
        background: rgba(56, 189, 248, 0.15);
      }
      html.light .mobile-drawer-accordion-btn {
        background: rgba(2, 132, 199, 0.08);
        border-color: rgba(2, 132, 199, 0.2);
      }
      .mobile-drawer-chapters-container {
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding-top: 4px;
      }
      .mobile-drawer-chapter-row {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 8px 10px;
        display: flex;
        flex-direction: column;
        gap: 6px;
        transition: all 0.15s;
      }
      html.light .mobile-drawer-chapter-row {
        background: rgba(15, 23, 42, 0.03);
        border-color: rgba(15, 23, 42, 0.08);
      }
      .mobile-drawer-chapter-row.active {
        border-color: rgba(56, 189, 248, 0.35);
        background: rgba(56, 189, 248, 0.08);
      }
      .drawer-ch-header {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .drawer-ch-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 800;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        padding: 2px 6px;
        border-radius: 5px;
      }
      .drawer-ch-name {
        font-size: 0.82rem;
        font-weight: 700;
        color: #E4E4E7;
        flex: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      html.light .drawer-ch-name {
        color: #1E293B;
      }
      .drawer-ch-pills {
        display: flex;
        gap: 6px;
      }
      .drawer-ch-pill {
        flex: 1;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        padding: 5px 8px;
        border-radius: 6px;
        font-size: 0.74rem;
        font-weight: 700;
        text-decoration: none;
        transition: all 0.15s;
      }
      .drawer-ch-pill.quiz {
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.25);
      }
      .drawer-ch-pill.quiz:hover {
        background: rgba(16, 185, 129, 0.25);
      }
      .drawer-ch-pill.guide {
        background: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.25);
      }
      .drawer-ch-pill.guide:hover {
        background: rgba(56, 189, 248, 0.25);
      }

      /* الفوتر الموحد - توقيع المطور (Developer Signature Footer) */
      .unified-portal-footer {
        margin-top: 50px;
        background: rgba(11, 15, 25, 0.95);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px 20px 20px;
        color: #94A3B8;
        box-sizing: border-box;
      }
      html.light .unified-portal-footer {
        background: #FFFFFF;
        border-top: 1px solid rgba(15, 23, 42, 0.09);
        color: #475569;
      }
      .footer-inner-container {
        max-width: 1100px;
        margin: 0 auto;
      }
      .dev-footer-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
        padding-bottom: 18px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      }
      html.light .dev-footer-card {
        border-bottom-color: rgba(15, 23, 42, 0.06);
      }
      .dev-info-left {
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .dev-avatar-wrap {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.35rem;
        flex-shrink: 0;
      }
      html.light .dev-avatar-wrap {
        background: rgba(2, 132, 199, 0.08);
        border-color: rgba(2, 132, 199, 0.2);
      }
      .dev-text-details {
        display: flex;
        flex-direction: column;
        gap: 2px;
      }
      .dev-name-row {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }
      .dev-name {
        font-size: 1.02rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.2px;
      }
      html.light .dev-name {
        color: #0F172A;
      }
      .dev-badge {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 6px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
      }
      html.light .dev-badge {
        background: rgba(5, 150, 105, 0.1);
        border-color: rgba(5, 150, 105, 0.25);
        color: #059669;
      }
      .dev-sub-desc {
        font-size: 0.82rem;
        color: #94A3B8;
        margin: 0;
      }
      html.light .dev-sub-desc {
        color: #64748B;
      }
      .dev-links-right {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }
      .dev-pill-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 12px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #94A3B8;
        text-decoration: none;
        font-size: 0.82rem;
        font-weight: 700;
        transition: all 0.2s ease;
      }
      html.light .dev-pill-btn {
        background: rgba(15, 23, 42, 0.04);
        border-color: rgba(15, 23, 42, 0.09);
        color: #334155;
      }
      .dev-pill-btn:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: rgba(56, 189, 248, 0.35);
        color: #38BDF8;
        transform: translateY(-2px);
      }
      html.light .dev-pill-btn:hover {
        background: rgba(2, 132, 199, 0.1);
        border-color: rgba(2, 132, 199, 0.3);
        color: #0284C7;
      }
      .footer-btn-scrolltop {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #38BDF8;
        padding: 7px 12px;
        border-radius: 10px;
        font-family: inherit;
        font-size: 0.88rem;
        font-weight: 800;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
      }
      html.light .footer-btn-scrolltop {
        background: rgba(15, 23, 42, 0.04);
        border-color: rgba(15, 23, 42, 0.1);
        color: #0284C7;
      }
      .footer-btn-scrolltop:hover {
        background: rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
      }
      .dev-copyright-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        padding-top: 14px;
        font-size: 0.8rem;
        color: #64748B;
        direction: ltr;
      }
      html.light .dev-copyright-row {
        color: #64748B;
      }
      .dev-status-pill {
        font-size: 0.72rem;
        font-weight: 700;
        color: #34D399;
        direction: ltr;
      }
      @media (max-width: 768px) {
        .dev-footer-card {
          flex-direction: column;
          align-items: flex-start;
        }
        .dev-links-right {
          width: 100%;
          justify-content: flex-start;
        }
      }
    `;
    document.head.appendChild(style);
  }

  // 6. ==================== تفعيل أحداث الموبايل والأمان ====================
  function setupDrawerEvents() {
    const btnOpen = document.getElementById('btnToggleMobileDrawer') || document.querySelector('.nav-hamburger-btn');
    const btnClose = document.getElementById('btnCloseMobileDrawer');
    const backdrop = document.getElementById('mobileDrawerBackdrop');
    const allHamburgerBtns = document.querySelectorAll('.nav-hamburger-btn, .nav-mobile-hamburger');

    function openDrawer() {
      if (backdrop) backdrop.classList.add('open');
      allHamburgerBtns.forEach(btn => {
        btn.classList.add('is-active');
        btn.setAttribute('aria-expanded', 'true');
      });
      document.body.style.overflow = 'hidden';
      if (window.soundEngine && typeof window.soundEngine.click === 'function') {
        try { window.soundEngine.click(); } catch (_) {}
      }
    }

    function closeDrawer() {
      if (backdrop) backdrop.classList.remove('open');
      allHamburgerBtns.forEach(btn => {
        btn.classList.remove('is-active');
        btn.setAttribute('aria-expanded', 'false');
      });
      document.body.style.overflow = '';
    }

    if (btnOpen) {
      btnOpen.addEventListener('click', function (e) {
        e.stopPropagation();
        if (backdrop && backdrop.classList.contains('open')) {
          closeDrawer();
        } else {
          openDrawer();
        }
      });
    }

    if (btnClose) {
      btnClose.addEventListener('click', function (e) {
        e.stopPropagation();
        closeDrawer();
      });
    }

    if (backdrop) {
      backdrop.addEventListener('click', function (e) {
        if (e.target === backdrop) closeDrawer();
      });
    }

    // إغلاق بـ Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && backdrop && backdrop.classList.contains('open')) {
        closeDrawer();
      }
    });

    // إغلاق القائمة عند النقر على أي رابط داخلها
    document.querySelectorAll('.mobile-drawer-link, .drawer-ch-pill').forEach(function (link) {
      link.addEventListener('click', function () {
        closeDrawer();
      });
    });

    // الأكورديون الذكي لقائمة الأبواب الـ 25
    const btnAcc = document.getElementById('btnToggleChaptersAccordion');
    const containerAcc = document.getElementById('mobileChaptersContainer');
    const arrowAcc = document.getElementById('chaptersAccordionArrow');
    if (btnAcc && containerAcc) {
      btnAcc.addEventListener('click', function (e) {
        e.stopPropagation();
        const isClosed = containerAcc.style.display === 'none';
        containerAcc.style.display = isClosed ? 'flex' : 'none';
        if (arrowAcc) arrowAcc.style.transform = isClosed ? 'rotate(0deg)' : 'rotate(180deg)';
      });
    }

    // دعم استدعاءات الجافاسكريبت القديمة (Backward Compatibility)
    window.toggleMobileNav = function () {
      if (backdrop && backdrop.classList.contains('open')) {
        closeDrawer();
      } else {
        openDrawer();
      }
    };
    window.closeMobileNav = closeDrawer;

    // تأمين الروابط الخارجية (Link Hardening)
    document.querySelectorAll('a[href^="http"]').forEach(function (link) {
      if (!link.href.includes(window.location.hostname)) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
      }
    });

    // تفعيل القوائم المنسدلة الذكية (مثل تصفح الأبواب في الديسكتوب)
    document.addEventListener('click', function (e) {
      const dropdownBtn = e.target.closest('.nav-dropdown-btn');
      const allMenus = document.querySelectorAll('.nav-dropdown-menu');
      if (dropdownBtn) {
        e.stopPropagation();
        if (window.soundEngine && typeof window.soundEngine.click === 'function') {
          try { window.soundEngine.click(); } catch (_) {}
        }
        const parent = dropdownBtn.closest('.nav-dropdown-wrapper');
        const menu = parent ? parent.querySelector('.nav-dropdown-menu') : null;
        allMenus.forEach(function (m) { if (m !== menu) m.classList.remove('show'); });
        if (menu) menu.classList.toggle('show');
      } else {
        allMenus.forEach(function (m) { m.classList.remove('show'); });
      }
    });

    // مزامنة حالة الثيم مع الزرار
    if (window.updateThemeButtons) {
      const isLight = document.documentElement.classList.contains('light');
      window.updateThemeButtons(isLight ? 'light' : 'dark');
    }
  }

  // 7. ==================== البدء التلقائي والتركيب ====================
  function initUnifiedPortalUI() {
    injectStyles();
    const ctx = getPathContext();

    // إزالة أي لوحات دروة أو أوفرلاي قديمة من الـ HTML الساكن لتفادي التكرار
    const oldDrawerPanel = document.getElementById('mobile-drawer-panel') || document.querySelector('.mobile-drawer-panel');
    const oldDrawerOverlay = document.getElementById('mobile-drawer-overlay') || document.querySelector('.mobile-drawer-overlay');
    if (oldDrawerPanel) oldDrawerPanel.remove();
    if (oldDrawerOverlay) oldDrawerOverlay.remove();

    // 1. فحص هل يوجد هيدر موحد مسبقاً
    let globalNav = document.getElementById('globalPortalNav');
    if (!globalNav) {
      // هل يوجد هيدر قديم لاستبداله؟
      let oldNav = document.querySelector('.unified-portal-nav') || 
                     document.querySelector('.inc-navbar') || 
                     document.querySelector('.tr-navbar');
      
      const wrapper = document.createElement('div');
      wrapper.innerHTML = renderGlobalHeader(ctx);
      const newHeaderEl = wrapper.firstElementChild;
      const drawerEl = wrapper.lastElementChild;

      if (oldNav) {
        // الحفاظ على قائمة تصفح الأبواب المنسدلة إن وجدت في الهيدر القديم ونقلها بسلاسة للديسكتوب
        const existingDropdown = oldNav.querySelector('.nav-dropdown-wrapper');
        if (existingDropdown) {
          const actionsContainer = newHeaderEl.querySelector('.nav-desktop-actions');
          if (actionsContainer) {
            actionsContainer.insertBefore(existingDropdown, actionsContainer.firstElementChild);
          }
        }
        oldNav.remove();
      }
      const headerContainer = document.getElementById('unified-header') || document.getElementById('app-header');
      if (headerContainer) {
        headerContainer.innerHTML = '';
        headerContainer.appendChild(newHeaderEl);
      } else {
        document.body.insertAdjacentElement('afterbegin', newHeaderEl);
      }
      document.body.appendChild(drawerEl);

      // إزالة أي أزرار رجوع قديمة مكررة تسبق الهيدر
      document.querySelectorAll('.action-btn.home-btn').forEach(btn => btn.remove());
    }

    // 2. فحص الفوتر
    let globalFooter = document.getElementById('globalPortalFooter');
    if (!globalFooter) {
      const footerContainer = document.getElementById('unified-footer') || document.getElementById('app-footer');
      if (footerContainer) {
        footerContainer.innerHTML = renderGlobalFooter(ctx);
      } else {
        document.body.insertAdjacentHTML('beforeend', renderGlobalFooter(ctx));
      }
    }

    setupDrawerEvents();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUnifiedPortalUI);
  } else {
    initUnifiedPortalUI();
  }

})();

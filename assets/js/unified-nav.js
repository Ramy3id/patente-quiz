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

  // 3. ==================== بناء الهيدر الموحد ====================
  function renderGlobalHeader(ctx) {
    const cur = ctx.currentFile.toLowerCase();
    const full = (ctx.fullPath || '').toLowerCase();

    const isHub = (full.includes('capitoli_divisi') && cur.includes('index')) || (!full.includes('interactive_pages') && cur.includes('index'));
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
      { id: 'hub', label: 'الأبواب وبنك الأسئلة', icon: '📚', href: ctx.capitoli + 'index.html', active: isHub },
      { id: 'piano', label: 'خطة الدراسة', icon: '📅', href: ctx.interactive + 'piano-studio.html', active: isPiano },
      { id: 'parole', label: 'رادار الكلمات', icon: '🎯', href: ctx.interactive + 'parole-spia.html', active: isParole },
      { id: 'incroci', label: 'مفكك التقاطعات', icon: '🔄', href: ctx.interactive + 'decodificatore-incroci.html', active: isIncroci },
      { id: 'trucchi', label: 'خزينة التريكات', icon: '💎', href: ctx.interactive + 'trucchi-esame.html', active: isTrucchi },
      { id: 'numeri', label: 'معمل الأرقام', icon: '📏', href: ctx.interactive + 'laboratorio-numeri.html', active: isNumeri },
      { id: 'soccorso', label: 'الإسعافات', icon: '🚑', href: ctx.interactive + 'primo-soccorso.html', active: isSoccorso },
      { id: 'scheda', label: 'محاكي الامتحان', icon: '📝', href: ctx.interactive + 'scheda-esame.html', active: isScheda },
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

    return `
      <header class="unified-portal-nav" id="globalPortalNav">
        <div style="display:flex; align-items:center; gap:10px;">
          <a href="${ctx.capitoli}index.html" class="nav-brand" title="الرئيسية — Patente B Pro">
            <span style="font-size:1.35rem; line-height:1;">🚦</span>
            <span>Patente B Pro</span>
            <span class="badge-tag">2026</span>
          </a>
        </div>

        <nav class="nav-desktop-tabs" id="globalDesktopTabs">
          ${desktopTabsHtml}
        </nav>

        <div class="nav-desktop-actions" style="display:flex; align-items:center; gap:8px;">
          <button class="nav-theme-btn" onclick="window.toggleTheme && window.toggleTheme()" title="تبديل الوضع (نهاري / ليلي) [Alt + T]">
            <span class="theme-icon-span">☀️</span>
            <span class="theme-label-span">الوضع</span>
          </button>

          <button class="nav-mobile-hamburger" id="btnToggleMobileDrawer" aria-label="فتح قائمة الأدوات">
            <span>☰</span>
          </button>
        </div>
      </header>

      <!-- قائمة الموبايل السلسة (Mobile Drawer) -->
      <div class="mobile-drawer-backdrop" id="mobileDrawerBackdrop">
        <aside class="mobile-drawer-pane" id="mobileDrawerPane">
          <div class="mobile-drawer-header">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:1.3rem;">🚦</span>
              <strong style="font-size:1.05rem; color:var(--text-primary, #FFF);">أدوات Patente B Pro</strong>
            </div>
            <button class="mobile-drawer-close" id="btnCloseMobileDrawer" aria-label="إغلاق القائمة">✕</button>
          </div>

          <div class="mobile-drawer-links-wrap">
            ${drawerItemsHtml}
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

  // 4. ==================== بناء الفوتر الموحد ====================
  function renderGlobalFooter(ctx) {
    return `
      <footer class="unified-portal-footer" id="globalPortalFooter">
        <div class="footer-inner-container">
          <div class="footer-top-row">
            <div class="footer-brand-wrap">
              <div style="display:flex; align-items:center; gap:8px; font-weight:900; font-size:1.15rem; color:var(--text-primary, #FFF);">
                <span>🚦</span>
                <span>Patente B Pro</span>
                <span class="badge-tag">Official Hub</span>
              </div>
              <p class="footer-tagline">
                المنظومة الهندسية المتكاملة لحسم رخصة القيادة الإيطالية باللغة العربية عبر المنطق الرياضي والتريكات الوزارية المعتمدة.
              </p>
            </div>

            <div class="footer-actions-wrap">
              <button class="footer-btn-scrolltop" onclick="window.scrollTo({top:0, behavior:'smooth'})" title="العودة لأعلى الصفحة">
                <span>⬆️</span>
                <span>إلى الأعلى</span>
              </button>
            </div>
          </div>

          <div class="footer-pills-row">
            <a href="${ctx.capitoli}index.html" class="footer-pill-link">📚 بنك أسئلة الأبواب</a>
            <a href="${ctx.interactive}parole-spia.html" class="footer-pill-link">🎯 رادار الكلمات السحرية</a>
            <a href="${ctx.interactive}decodificatore-incroci.html" class="footer-pill-link">🔄 مفكك التقاطعات</a>
            <a href="${ctx.interactive}trucchi-esame.html" class="footer-pill-link">💎 خزينة التريكات</a>
            <a href="${ctx.interactive}laboratorio-numeri.html" class="footer-pill-link">📏 معمل الأرقام والمقاييس</a>
            <a href="${ctx.interactive}primo-soccorso.html" class="footer-pill-link">🚑 كبسولة الإسعافات</a>
            <a href="${ctx.interactive}piano-studio.html" class="footer-pill-link">📅 خطة الدراسة</a>
            <a href="${ctx.interactive}scheda-esame.html" class="footer-pill-link">📝 محاكي الامتحان الوزاري</a>
            <a href="${ctx.interactive}flashcards.html" class="footer-pill-link">🗂️ بطاقات التكرار المتباعد</a>
            <a href="${ctx.interactive}dashboard.html" class="footer-pill-link">📊 لوحة تقدم الطالب</a>
            <a href="${ctx.interactive}traps_and_games.html" class="footer-pill-link">🎮 بنك الفخاخ والألعاب</a>
          </div>

          <div class="footer-bottom-row">
            <div style="display:flex; align-items:center; gap:8px; font-size:0.84rem; color:var(--text-muted, #94A3B8);">
              <span>⚡</span>
              <span>تطبيق ويب تقدمي يعمل بالكامل دون الحاجة لاتصال بالإنترنت (Offline PWA Ready)</span>
            </div>
            <div style="font-size:0.82rem; color:var(--text-muted, #94A3B8); direction:ltr;">
              Patente B Pro &copy; 2026. Made with precision for future drivers.
            </div>
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

      /* زر الموبايل همبرغر */
      .nav-mobile-hamburger {
        display: none;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #FFF;
        font-size: 1.25rem;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        cursor: pointer;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
      }
      html.light .nav-mobile-hamburger {
        background: rgba(15, 23, 42, 0.05);
        border-color: rgba(15, 23, 42, 0.1);
        color: #0F172A;
      }
      .nav-mobile-hamburger:hover {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
      }
      @media (max-width: 992px) {
        .nav-desktop-tabs { display: none !important; }
        .nav-mobile-hamburger { display: flex !important; }
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

      /* الفوتر الموحد */
      .unified-portal-footer {
        margin-top: 60px;
        background: rgba(15, 23, 42, 0.9);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding: 40px 20px 24px;
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
      .footer-top-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 24px;
      }
      .footer-brand-wrap {
        max-width: 600px;
      }
      .footer-tagline {
        font-size: 0.88rem;
        line-height: 1.6;
        margin-top: 8px;
        color: #64748B;
      }
      .footer-btn-scrolltop {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #38BDF8;
        padding: 10px 18px;
        border-radius: 12px;
        font-family: inherit;
        font-size: 0.88rem;
        font-weight: 800;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s;
      }
      html.light .footer-btn-scrolltop {
        background: rgba(15, 23, 42, 0.05);
        border-color: rgba(15, 23, 42, 0.1);
        color: #0284C7;
      }
      .footer-btn-scrolltop:hover {
        background: rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
      }
      .footer-pills-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        padding: 16px 0;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
      }
      html.light .footer-pills-row {
        border-top-color: rgba(15, 23, 42, 0.06);
        border-bottom-color: rgba(15, 23, 42, 0.06);
      }
      .footer-pill-link {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 6px 14px;
        border-radius: 999px;
        color: #94A3B8;
        text-decoration: none;
        font-size: 0.82rem;
        font-weight: 700;
        transition: all 0.2s;
      }
      html.light .footer-pill-link {
        background: rgba(15, 23, 42, 0.04);
        border-color: rgba(15, 23, 42, 0.08);
        color: #475569;
      }
      .footer-pill-link:hover {
        color: #38BDF8;
        border-color: rgba(56, 189, 248, 0.3);
      }
      html.light .footer-pill-link:hover {
        color: #0284C7;
        border-color: rgba(2, 132, 199, 0.3);
      }
      .footer-bottom-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
      }
    `;
    document.head.appendChild(style);
  }

  // 6. ==================== تفعيل أحداث الموبايل والأمان ====================
  function setupDrawerEvents() {
    const btnOpen = document.getElementById('btnToggleMobileDrawer');
    const btnClose = document.getElementById('btnCloseMobileDrawer');
    const backdrop = document.getElementById('mobileDrawerBackdrop');

    if (btnOpen && backdrop) {
      btnOpen.addEventListener('click', function () {
        backdrop.classList.add('open');
      });
    }
    if (btnClose && backdrop) {
      btnClose.addEventListener('click', function () {
        backdrop.classList.remove('open');
      });
    }
    if (backdrop) {
      backdrop.addEventListener('click', function (e) {
        if (e.target === backdrop) backdrop.classList.remove('open');
      });
    }

    // إغلاق بـ Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && backdrop && backdrop.classList.contains('open')) {
        backdrop.classList.remove('open');
      }
    });

    // تأمين الروابط الخارجية (Link Hardening)
    document.querySelectorAll('a[href^="http"]').forEach(function (link) {
      if (!link.href.includes(window.location.hostname)) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
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

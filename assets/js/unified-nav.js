/**
 * =======================================================================
 * Patente B Pro - Unified Navigation, Header, Footer & Security Suite
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description 
 * - توحيد شريط التنقل العلوي (Global Unified Header)
 * - توحيد قائمة الموبايل السلسة (Mobile Drawer with Backdrop Blur)
 * - توحيد الفوتر الذكي (Unified Footer with Scroll-to-Top & PWA Status)
 * - تعزيز الأمان: SafeStorage (حماية LocalStorage) و SafeHtml (حماية XSS) و Link Hardening
 */

(function () {
  'use strict';

  // 1. ==================== أمان البيانات وحماية المدخلات ====================
  window.safeHtml = function (str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  };

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
          return item; // Fallback for raw strings
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
        console.warn('[SafeStorage] LocalStorage quota/blocked, using memory fallback:', err);
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
    const p = (window.location.pathname || '').replace(/\\/g, '/');
    
    // هل نحن داخل مجلد فرعي داخل Capitoli_Divisi (مثل Capitolo_01)؟
    if (/\/Capitoli_Divisi\/Capitolo_[^\/]+\//i.test(p)) {
      return {
        root: '../../',
        interactive: '../../interactive_pages/',
        capitoli: '../',
        currentFile: p.split('/').pop() || 'index.html'
      };
    }
    // هل نحن في Capitoli_Divisi مباشرة؟
    if (/\/Capitoli_Divisi\//i.test(p)) {
      return {
        root: '../',
        interactive: '../interactive_pages/',
        capitoli: './',
        currentFile: p.split('/').pop() || 'index.html'
      };
    }
    // هل نحن في interactive_pages؟
    if (/\/interactive_pages\//i.test(p)) {
      return {
        root: '../',
        interactive: './',
        capitoli: '../Capitoli_Divisi/',
        currentFile: p.split('/').pop() || 'index.html'
      };
    }
    // في الجذر (Root)
    return {
      root: './',
      interactive: './interactive_pages/',
      capitoli: './Capitoli_Divisi/',
      currentFile: p.split('/').pop() || 'index.html'
    };
  }

  // 3. ==================== بناء الهيدر الموحد ====================
  function renderGlobalHeader(ctx) {
    const current = ctx.currentFile.toLowerCase();

    // قائمة الروابط الأساسية
    const navItems = [
      { id: 'hub', label: 'الأبواب وبنك الأسئلة', icon: '📚', href: ctx.capitoli + 'index.html', active: current.includes('capitoli') && !current.includes('parole-spia') },
      { id: 'piano', label: 'خطة الدراسة', icon: '📅', href: ctx.interactive + 'piano-studio.html', active: current.includes('piano-studio') },
      { id: 'parole', label: 'رادار الكلمات', icon: '🎯', href: ctx.interactive + 'parole-spia.html', active: current.includes('parole-spia') },
      { id: 'incroci', label: 'مفكك التقاطعات', icon: '🔄', href: ctx.interactive + 'decodificatore-incroci.html', active: current.includes('decodificatore-incroci') },
      { id: 'trucchi', label: 'خزينة التريكات', icon: '💎', href: ctx.interactive + 'trucchi-esame.html', active: current.includes('trucchi-esame') },
      { id: 'numeri', label: 'معمل الأرقام', icon: '📏', href: ctx.interactive + 'laboratorio-numeri.html', active: current.includes('laboratorio-numeri') },
      { id: 'soccorso', label: 'الإسعافات', icon: '🚑', href: ctx.interactive + 'primo-soccorso.html', active: current.includes('primo-soccorso') },
      { id: 'scheda', label: 'محاكي الامتحان', icon: '📝', href: ctx.interactive + 'scheda-esame.html', active: current.includes('scheda-esame') },
      { id: 'flashcards', label: 'فلاش كاردز', icon: '🗂️', href: ctx.interactive + 'flashcards.html', active: current.includes('flashcards') },
      { id: 'dashboard', label: 'لوحة التقدم', icon: '📊', href: ctx.interactive + 'dashboard.html', active: current.includes('dashboard') },
      { id: 'traps', label: 'بنك الفخاخ', icon: '🎮', href: ctx.interactive + 'traps_and_games.html', active: current.includes('traps_and_games') }
    ];

    const desktopTabsHtml = navItems.map(item => `
      <a href="${item.href}" class="nav-tab-desktop ${item.active ? 'active' : ''}">
        <span>${item.icon}</span>
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
        <div style="display:flex; align-items:center; gap:12px;">
          <a href="${ctx.capitoli}index.html" class="nav-brand">
            <span style="font-size:1.35rem;">🚦</span>
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
            <span class="theme-label-span" style="display:none;">الوضع</span>
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
              <strong style="font-size:1.05rem; color:var(--text-primary);">أدوات Patente B Pro</strong>
            </div>
            <button class="mobile-drawer-close" id="btnCloseMobileDrawer">✕</button>
          </div>

          <div class="mobile-drawer-links-wrap">
            ${drawerItemsHtml}
          </div>

          <div class="mobile-drawer-footer">
            <button class="mobile-control-btn" onclick="window.toggleTheme && window.toggleTheme()">
              <span class="theme-icon-span">☀️</span>
              <span>تبديل الوضع النهاري / الليلي</span>
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
              <div style="display:flex; align-items:center; gap:8px; font-weight:900; font-size:1.15rem; color:var(--text-primary);">
                <span>🚦</span>
                <span>Patente B Pro</span>
                <span class="badge-tag">Official Hub</span>
              </div>
              <p class="footer-tagline">
                المنصة الهندسية المتكاملة لحسم رخصة القيادة الإيطالية باللغة العربية عبر المنطق الرياضي والتريكات الوزارية.
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
            <a href="${ctx.interactive}parole-spia.html" class="footer-pill-link">🎯 رادار الكلمات</a>
            <a href="${ctx.interactive}decodificatore-incroci.html" class="footer-pill-link">🔄 مفكك التقاطعات</a>
            <a href="${ctx.interactive}trucchi-esame.html" class="footer-pill-link">💎 خزينة التريكات</a>
            <a href="${ctx.interactive}laboratorio-numeri.html" class="footer-pill-link">📏 معمل الأرقام</a>
            <a href="${ctx.interactive}primo-soccorso.html" class="footer-pill-link">🚑 كبسولة الإسعافات</a>
            <a href="${ctx.interactive}piano-studio.html" class="footer-pill-link">📅 خطة الدراسة</a>
            <a href="${ctx.interactive}scheda-esame.html" class="footer-pill-link">📝 محاكي الامتحان</a>
          </div>

          <div class="footer-bottom-row">
            <div style="display:flex; align-items:center; gap:6px; font-size:0.82rem; color:var(--text-muted);">
              <span>⚡</span>
              <span>تطبيق ويب تقدمي يعمل بالكامل دون اتصال بالإنترنت (Offline PWA Ready)</span>
            </div>
            <div style="font-size:0.82rem; color:var(--text-muted); direction:ltr;">
              Patente B Pro &copy; 2026. Made with precision for future drivers.
            </div>
          </div>
        </div>
      </footer>
    `;
  }

  // 5. ==================== تنسيق وإدراج المكونات ====================
  function injectStyles() {
    if (document.getElementById('unifiedNavCustomStyles')) return;
    const style = document.createElement('style');
    style.id = 'unifiedNavCustomStyles';
    style.textContent = `
      /* زر الموبايل همبرغر */
      .nav-mobile-hamburger {
        display: none;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: var(--text-primary, #FFF);
        font-size: 1.25rem;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        cursor: pointer;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
      }
      .nav-mobile-hamburger:hover {
        background: rgba(56, 189, 248, 0.15);
        color: var(--cyan-primary, #38BDF8);
      }
      @media (max-width: 900px) {
        .nav-mobile-hamburger { display: flex; }
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
        background: var(--bg-surface, #0F172A);
        border-left: 1px solid var(--border-subtle, rgba(255,255,255,0.1));
        display: flex;
        flex-direction: column;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: -8px 0 28px rgba(0,0,0,0.4);
        padding: 20px;
        box-sizing: border-box;
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
      .mobile-drawer-close {
        background: transparent;
        border: none;
        color: var(--text-muted, #94A3B8);
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
        color: var(--text-secondary, #94A3B8);
        font-weight: 700;
        font-size: 0.92rem;
        transition: all 0.15s;
      }
      .mobile-drawer-link:hover {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-primary, #FFF);
      }
      .mobile-drawer-link.active {
        background: rgba(56, 189, 248, 0.15);
        color: var(--cyan-primary, #38BDF8);
        border: 1px solid rgba(56, 189, 248, 0.3);
      }
      .drawer-link-badge {
        margin-right: auto;
        font-size: 0.7rem;
        padding: 2px 6px;
        border-radius: 6px;
        background: var(--cyan-primary, #38BDF8);
        color: #0B0F19;
        font-weight: 800;
      }

      /* الفوتر الموحد */
      .unified-portal-footer {
        margin-top: 60px;
        background: var(--bg-surface, rgba(15, 23, 42, 0.85));
        border-top: 1px solid var(--border-subtle, rgba(255,255,255,0.08));
        padding: 40px 20px 24px;
        color: var(--text-secondary, #94A3B8);
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
        color: var(--text-muted, #64748B);
      }
      .footer-btn-scrolltop {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border-subtle, rgba(255,255,255,0.1));
        color: var(--cyan-primary, #38BDF8);
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
      .footer-pill-link {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--border-subtle, rgba(255,255,255,0.08));
        padding: 6px 14px;
        border-radius: 999px;
        color: var(--text-secondary, #94A3B8);
        text-decoration: none;
        font-size: 0.82rem;
        font-weight: 700;
        transition: all 0.2s;
      }
      .footer-pill-link:hover {
        color: var(--cyan-primary, #38BDF8);
        border-color: rgba(56, 189, 248, 0.3);
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
  }

  // 7. ==================== البدء التلقائي والتركيب ====================
  function initUnifiedPortalUI() {
    injectStyles();
    const ctx = getPathContext();

    // 1. فحص هل يوجد هيدر موحد مسبقاً
    let globalNav = document.getElementById('globalPortalNav');
    if (!globalNav) {
      // هل يوجد هيدر قديم لاستبداله؟
      let oldNav = document.querySelector('.unified-portal-nav') || document.querySelector('.inc-navbar') || document.querySelector('.tr-navbar');
      
      const wrapper = document.createElement('div');
      wrapper.innerHTML = renderGlobalHeader(ctx);
      const newHeaderEl = wrapper.firstElementChild;
      const drawerEl = wrapper.lastElementChild;

      if (oldNav) {
        oldNav.replaceWith(newHeaderEl);
        document.body.appendChild(drawerEl);
      } else {
        const headerContainer = document.getElementById('unified-header') || document.getElementById('app-header');
        if (headerContainer) {
          headerContainer.innerHTML = '';
          headerContainer.appendChild(newHeaderEl);
          document.body.appendChild(drawerEl);
        } else {
          document.body.insertAdjacentElement('afterbegin', newHeaderEl);
          document.body.appendChild(drawerEl);
        }
      }

      // إخفاء أي أزرار رجوع مكررة تسبق الهيدر
      document.querySelectorAll('.action-btn.home-btn').forEach(btn => btn.style.display = 'none');
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

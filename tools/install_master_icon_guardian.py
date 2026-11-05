import sys

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# Comprehensive Master Icon Guardian
guardian_code = """  // ==========================================================================
  // UNIVERSAL SVG ICON GUARDIAN (Platform-Wide Auto-Hydration)
  // Replaces all arbitrary UI emojis across ALL pages automatically
  // ==========================================================================
  function hydratePlatformIcons() {
    try {
      const emojiMap = {
        '⚡': SVG_ICONS.zap,
        '🔍': SVG_ICONS.search,
        '📅': SVG_ICONS.calendar,
        '⏱️': SVG_ICONS.timer,
        '⏱': SVG_ICONS.timer,
        '🎯': SVG_ICONS.crosshair,
        '🔄': SVG_ICONS.repeat,
        '📐': SVG_ICONS.ruler,
        '📏': SVG_ICONS.ruler,
        '📖': SVG_ICONS.book,
        '📚': SVG_ICONS.book,
        '🎮': SVG_ICONS.gamepad,
        '🧩': SVG_ICONS.cards,
        '🗂️': SVG_ICONS.cards,
        '🗂': SVG_ICONS.cards,
        '💎': SVG_ICONS.gem,
        '🚑': SVG_ICONS.ambulance,
        '⚠️': SVG_ICONS.shieldAlert,
        '⚠': SVG_ICONS.shieldAlert,
        '🔤': SVG_ICONS.notes,
        '📝': SVG_ICONS.notes,
        '🖼️': SVG_ICONS.image,
        '🖼': SVG_ICONS.image,
        '📊': SVG_ICONS.chart,
        '👤': SVG_ICONS.user,
        '⚖️': SVG_ICONS.shieldCheck,
        '⚖': SVG_ICONS.shieldCheck,
        '🔒': SVG_ICONS.lock,
        '🔊': SVG_ICONS.soundOn,
        '🔇': SVG_ICONS.soundOff,
        '☀️': SVG_ICONS.sun,
        '🌙': SVG_ICONS.moon,
        '💡': SVG_ICONS.lightbulb,
        '✅': SVG_ICONS.checkCircle,
        '🏠': SVG_ICONS.home
      };

      // 1. استبدال الأيقونات في الحاويات المخصصة للأيقونات
      const selectors = [
        '.bento-icon-box', '.stat-ico', '.meta-icon', '.card-icon', '.tool-icon',
        '.btn-ico', '.bento-spark-badge', '.cat-item-icon', '.drawer-link-icon',
        '.search-icon', '.tab-icon', '.chapter-gated-badge', '.stat-pill',
        '.portal-badge-live', '.hero-badge', '.badge-tag', '.nav-tab-desktop',
        '.nav-dropdown-item', '.result-badge', '.pill-icon', '.nav-mobile-btn span'
      ];

      document.querySelectorAll(selectors.join(',')).forEach(el => {
        if (el.querySelector('svg') || el.querySelector('img')) return;
        const text = el.textContent.trim();
        if (emojiMap[text]) {
          el.innerHTML = emojiMap[text];
          el.classList.add('hydrated-svg');
        }
      });

      // 2. فحص أزرار بدء المذاكرة
      document.querySelectorAll('.btn-action-study, .btn-study, .study-btn').forEach(btn => {
        if (btn.querySelector('svg')) return;
        if (btn.textContent.includes('بدء المذاكرة') || btn.textContent.includes('🎯')) {
          btn.innerHTML = '<span>' + SVG_ICONS.play + ' ' + btn.textContent.replace('🎯', '').trim() + '</span>';
        }
      });

      // 3. تطهير علامات المرور 🚦 من شريط اللوجو واستبداله بشعار المنصة
      document.querySelectorAll('.nav-brand, .brand-wrapper, .footer-brand-header').forEach(b => {
        const spanEmoji = Array.from(b.querySelectorAll('span')).find(s => s.textContent.includes('🚦'));
        if (spanEmoji) {
          const ctx = (typeof getPathContext === 'function') ? getPathContext() : { root: '../' };
          spanEmoji.outerHTML = `<img src="${ctx.root}assets/brand/brand_logo_steering_trans.png" alt="Patente B Pro" class="footer-brand-logo" width="28" height="28" style="width:28px;height:28px;object-fit:contain;border-radius:50%;vertical-align:middle;">`;
        }
      });

      // 4. استبدال الإيموجيز داخل النصوص في العناوين والبادجات
      const textTargets = document.querySelectorAll('h1, h2, h3, h4, .stat-pill, .bento-main-heading, .portal-badge-live, .chapter-gated-badge');
      textTargets.forEach(el => {
        if (el.dataset.emojiHydrated) return;
        let html = el.innerHTML;
        let changed = false;
        for (const [em, svg] of Object.entries(emojiMap)) {
          if (html.includes(em)) {
            html = html.split(em).join('<span class="inline-ui-svg" style="display:inline-flex;vertical-align:middle;margin:0 3px;">' + svg + '</span>');
            changed = true;
          }
        }
        if (changed) {
          el.innerHTML = html;
          el.dataset.emojiHydrated = 'true';
        }
      });

    } catch(err) {
      console.warn('[IconHydrator] Non-fatal hydration note:', err);
    }
  }

  // Run automatically on DOM ready and after dynamic contents
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydratePlatformIcons);
  } else {
    hydratePlatformIcons();
  }
  window.addEventListener('load', hydratePlatformIcons);

  // مراقب ديناميكي لتطهير أي نتائج بحث أو محتويات يتم حقنها لاحقاً
  if (window.MutationObserver) {
    const observer = new MutationObserver((mutations) => {
      let shouldHydrate = false;
      for (const m of mutations) {
        if (m.addedNodes.length > 0) {
          shouldHydrate = true;
          break;
        }
      }
      if (shouldHydrate) {
        hydratePlatformIcons();
      }
    });
    observer.observe(document.body || document.documentElement, { childList: true, subtree: true });
  }"""

# Find start of old hydrator
idx_start = nav.find('  // ==========================================================================\n  // UNIVERSAL SVG ICON GUARDIAN')
idx_end = nav.find('  function initUnifiedPortalUI() {')

if idx_start != -1 and idx_end != -1:
    nav = nav[:idx_start] + guardian_code + "\n\n" + nav[idx_end:]
    with open(nav_path, 'w', encoding='utf-8') as f:
        f.write(nav)
    print('SUCCESS: Master Icon Guardian with MutationObserver installed into unified-nav.js')
else:
    print('ERROR: Anchors not found for Master Icon Guardian.')

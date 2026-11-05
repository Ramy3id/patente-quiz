import sys

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

old_hydrator = """  // ==========================================================================
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
        '🔇': SVG_ICONS.soundOff
      };

      // Target elements that typically host UI icons
      const selectors = [
        '.bento-icon-box', '.stat-ico', '.meta-icon', '.card-icon', '.tool-icon',
        '.btn-ico', '.bento-spark-badge', '.cat-item-icon', '.drawer-link-icon',
        '.search-icon', '.tab-icon', '.chapter-gated-badge'
      ];

      document.querySelectorAll(selectors.join(',')).forEach(el => {
        if (el.querySelector('svg')) return; // Already has SVG
        const text = el.textContent.trim();
        if (emojiMap[text]) {
          el.innerHTML = emojiMap[text];
        }
      });

      // Chapter study CTA buttons: '🎯 بدء المذاكرة التفاعلية'
      document.querySelectorAll('.btn-action-study, .btn-study, .study-btn').forEach(btn => {
        if (btn.querySelector('svg')) return;
        if (btn.textContent.includes('بدء المذاكرة') || btn.textContent.includes('🎯')) {
          btn.innerHTML = '<span>' + SVG_ICONS.play + ' ' + btn.textContent.replace('🎯', '').trim() + '</span>';
        }
      });
    } catch(err) {
      console.warn('[IconHydrator] Non-fatal note:', err);
    }
  }"""

new_hydrator = """  // ==========================================================================
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
        '🔇': SVG_ICONS.soundOff
      };

      // 1. Selector-based targets
      const selectors = [
        '.bento-icon-box', '.stat-ico', '.meta-icon', '.card-icon', '.tool-icon',
        '.btn-ico', '.bento-spark-badge', '.cat-item-icon', '.drawer-link-icon',
        '.search-icon', '.tab-icon', '.chapter-gated-badge', '.badge-icon'
      ];

      document.querySelectorAll(selectors.join(',')).forEach(el => {
        if (el.querySelector('svg')) return;
        const text = el.textContent.trim();
        if (emojiMap[text]) {
          el.innerHTML = emojiMap[text];
        }
      });

      // 2. Headings, buttons, cards, links containing UI emojis across all pages
      const textContainers = document.querySelectorAll(
        'h1, h2, h3, h4, h5, h6, button, a, .btn, .card-title, .tool-card-title, ' +
        '.portal-badge-live, .gate-free-badge, .section-title, .badge, .pill'
      );

      textContainers.forEach(container => {
        // Do not touch script, style or inputs
        if (['SCRIPT', 'STYLE', 'INPUT', 'TEXTAREA'].includes(container.tagName)) return;
        // Check if container contains any of our known UI emojis
        for (const [em, svg] of Object.entries(emojiMap)) {
          if (container.textContent && container.textContent.includes(em)) {
            // Traverse child text nodes safely
            const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null, false);
            const textNodes = [];
            let node;
            while ((node = walker.nextNode())) {
              if (node.nodeValue && node.nodeValue.includes(em)) {
                textNodes.push(node);
              }
            }
            textNodes.forEach(tn => {
              const span = document.createElement('span');
              span.className = 'inline-ui-svg';
              span.innerHTML = svg;
              const parts = tn.nodeValue.split(em);
              const parent = tn.parentNode;
              for (let i = 0; i < parts.length; i++) {
                if (parts[i]) parent.insertBefore(document.createTextNode(parts[i]), tn);
                if (i < parts.length - 1) parent.insertBefore(span.cloneNode(true), tn);
              }
              parent.removeChild(tn);
            });
          }
        }
      });
    } catch(err) {
      console.warn('[IconHydrator] Non-fatal note:', err);
    }
  }"""

nav_norm = nav.replace('\r\n', '\n')
old_hydrator_norm = old_hydrator.replace('\r\n', '\n')
new_hydrator_norm = new_hydrator.replace('\r\n', '\n')

if old_hydrator_norm in nav_norm:
    nav_norm = nav_norm.replace(old_hydrator_norm, new_hydrator_norm, 1)
    with open(nav_path, 'w', encoding='utf-8') as f:
        f.write(nav_norm)
    print("SUCCESS: Upgraded hydratePlatformIcons in unified-nav.js to recursive text walker!")
else:
    print("WARNING: old_hydrator not found in unified-nav.js!")

# Add .inline-ui-svg styling to theme-modes.css
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

inline_svg_css = """
.inline-ui-svg {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  vertical-align: middle !important;
  margin: 0 4px !important;
}

.inline-ui-svg .ui-svg {
  width: 1.15em !important;
  height: 1.15em !important;
  stroke-width: 2.2 !important;
  vertical-align: -0.15em !important;
}
"""

if '.inline-ui-svg' not in tm:
    tm += '\n' + inline_svg_css
    with open(tm_path, 'w', encoding='utf-8') as f:
        f.write(tm)
    print("SUCCESS: Added .inline-ui-svg CSS to theme-modes.css")

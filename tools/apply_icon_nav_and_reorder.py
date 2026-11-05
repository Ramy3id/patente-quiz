import re

CSS_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css"
JS_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js"

# =========================================================================
# 1. UPDATE ASSETS/JS/UNIFIED-NAV.JS (MARKUP AND STYLES)
# =========================================================================
with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the HTML markup of nav-desktop-actions in renderGlobalHeader
old_actions_markup = """        <!-- 3. أدوات الديسكتوب السريعة: بحث + إنجاز + حساب + مظهر -->
        <div class="nav-desktop-actions" id="globalDesktopActions">
          <!-- زر البحث الفوري (Spotlight Search Button) -->
          <button class="nav-search-trigger" id="btnOpenGlobalSearch" title="بحث فوري في الأبواب والمصطلحات والأسئلة [Ctrl + K]">
            <span class="search-icon">${SVG_ICONS.search}</span>
            <span class="search-text">بحث سريع...</span>
            <kbd class="search-kbd">Ctrl K</kbd>
          </button>

          <!-- شريط الإنجاز السريع المطور (Clean Horizontal Layout) -->
          <a href="${ctx.interactive}dashboard.html" class="nav-progress-pill" id="globalProgressPill" title="إنجازك العام: حللت ${globalStats.answered} من ${globalStats.total} سؤالاً (اضغط لفتح لوحة الإنجاز)">
            <span class="prog-pill-icon">${SVG_ICONS.crosshair}</span>
            <span class="prog-pill-label">إنجازك</span>
            <strong class="prog-pill-val" id="globalProgressPctVal">${globalStats.pct}%</strong>
            <div class="prog-pill-bar-track">
              <div class="prog-pill-bar-fill" id="globalProgressMiniFill" style="width:${globalStats.pct}%;"></div>
            </div>
          </a>

          <!-- كبسولة حساب المستخدم (Desktop Auth Pill) -->
          <div style="position:relative; display:inline-flex; align-items:center;">
            <button class="nav-auth-pill guest" id="globalAuthPill" title="تسجيل الدخول أو إنشاء حساب لحفظ تقدمك الدراسي">
              <span>${SVG_ICONS.user}</span>
              <span>حسابي / دخول</span>
            </button>
          </div>

          <!-- زر تبديل الوضع النهاري / الليلي -->
          <button class="nav-theme-btn" onclick="window.toggleTheme && window.toggleTheme()" title="تبديل المظهر (نهاري / ليلي) [Alt + T]">
            <span class="theme-icon-span">${SVG_ICONS.sun}</span>
            <span class="theme-label-span">المظهر</span>
          </button>
        </div>"""

new_actions_markup = """        <!-- 3. أدوات الديسكتوب السريعة: أيقونات فقط لتوفير المساحة وتسهيل الوصول -->
        <div class="nav-desktop-actions" id="globalDesktopActions">
          <!-- زر البحث الفوري (Spotlight Search Icon) -->
          <button class="nav-search-trigger" id="btnOpenGlobalSearch" title="بحث فوري في الأبواب والمصطلحات والأسئلة [Ctrl + K]" aria-label="بحث فوري">
            <span class="search-icon">${SVG_ICONS.search}</span>
          </button>

          <!-- زر لوحة الإنجاز كأيقونة معبرة (Expressive Progress Icon) -->
          <a href="${ctx.interactive}dashboard.html" class="nav-progress-pill" id="globalProgressPill" title="إنجازك العام: حللت ${globalStats.answered} من ${globalStats.total} سؤالاً (${globalStats.pct}%)" aria-label="إنجازك">
            <span class="prog-pill-icon">${SVG_ICONS.chart}</span>
          </a>

          <!-- زر حساب المستخدم كأيقونة (Desktop Auth Icon) -->
          <div style="position:relative; display:inline-flex; align-items:center;">
            <button class="nav-auth-pill guest" id="globalAuthPill" title="تسجيل الدخول أو بيانات الحساب" aria-label="بيانات الدخول">
              <span>${SVG_ICONS.user}</span>
            </button>
          </div>

          <!-- زر تبديل المظهر النهاري / الليلي كأيقونة -->
          <button class="nav-theme-btn" onclick="window.toggleTheme && window.toggleTheme()" title="تبديل المظهر (نهاري / ليلي) [Alt + T]" aria-label="تبديل المظهر">
            <span class="theme-icon-span">${SVG_ICONS.sun}</span>
            <span class="theme-label-span" style="display:none;">المظهر</span>
          </button>
        </div>"""

if old_actions_markup in js:
    js = js.replace(old_actions_markup, new_actions_markup)
    print("Replaced actions markup in unified-nav.js")
else:
    # Try regex match for actions block
    pat = r'<div class="nav-desktop-actions" id="globalDesktopActions">[\s\S]*?<\/div>\s*<!-- 4\.'
    replacement = new_actions_markup + "\n\n        <!-- 4."
    if re.search(pat, js):
        js = re.sub(pat, replacement, js)
        print("Replaced actions markup via regex in unified-nav.js")
    else:
        print("Warning: Could not match nav-desktop-actions markup")

# Update injectStyles desktop floating block in unified-nav.js
js_desktop_rule = """
      @media (min-width: 993px) {
        #globalPortalNav {
          max-width: 1200px !important;
          width: calc(100% - 36px) !important;
          margin: 12px auto 0 auto !important;
          top: 12px !important;
          border-radius: 16px !important;
          padding: 0 20px !important;
          border: 1px solid rgba(255, 255, 255, 0.12) !important;
          box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28), 0 2px 8px rgba(0, 0, 0, 0.18) !important;
          background: rgba(15, 23, 42, 0.88) !important;
          display: flex !important;
          justify-content: space-between !important;
          align-items: center !important;
          direction: rtl !important;
        }
        html.light #globalPortalNav {
          border: 1px solid rgba(15, 23, 42, 0.12) !important;
          box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08), 0 2px 6px rgba(15, 23, 42, 0.04) !important;
          background: rgba(255, 255, 255, 0.92) !important;
        }

        /* 1. Actions on EXTREME RIGHT (Order 1 in RTL) */
        #globalPortalNav .nav-desktop-actions {
          order: 1 !important;
          margin: 0 !important;
          display: flex !important;
          align-items: center !important;
          gap: 8px !important;
        }

        /* 2. Tabs in CENTER (Order 2 in RTL) */
        #globalPortalNav .nav-desktop-tabs {
          order: 2 !important;
          margin: 0 auto !important;
        }

        /* 3. Logo and Chapters on EXTREME LEFT (Order 3 in RTL) */
        #globalPortalNav .nav-brand-group {
          order: 3 !important;
          margin: 0 !important;
          display: flex !important;
          flex-direction: row-reverse !important;
          align-items: center !important;
          gap: 10px !important;
        }

        /* Megamenu opens inwards to the right from left position */
        .nav-chapters-megamenu {
          left: 0 !important;
          right: auto !important;
        }

        /* Action Buttons -> Icon Only (38x38px) */
        .nav-desktop-actions .nav-search-trigger,
        .nav-desktop-actions .nav-progress-pill,
        .nav-desktop-actions .nav-auth-pill,
        .nav-desktop-actions .nav-theme-btn {
          width: 38px !important;
          min-width: 38px !important;
          max-width: 38px !important;
          height: 38px !important;
          min-height: 38px !important;
          max-height: 38px !important;
          padding: 0 !important;
          border-radius: 10px !important;
          display: inline-flex !important;
          align-items: center !important;
          justify-content: center !important;
          box-sizing: border-box !important;
          cursor: pointer !important;
          background: rgba(255, 255, 255, 0.05) !important;
          border: 1px solid rgba(255, 255, 255, 0.1) !important;
          color: #94a3b8 !important;
          transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }

        html.light .nav-desktop-actions .nav-search-trigger,
        html.light .nav-desktop-actions .nav-progress-pill,
        html.light .nav-desktop-actions .nav-auth-pill,
        html.light .nav-desktop-actions .nav-theme-btn {
          background: rgba(15, 23, 42, 0.04) !important;
          border: 1px solid rgba(15, 23, 42, 0.1) !important;
          color: #475569 !important;
        }

        .nav-desktop-actions .nav-search-trigger:hover,
        .nav-desktop-actions .nav-progress-pill:hover,
        .nav-desktop-actions .nav-auth-pill:hover,
        .nav-desktop-actions .nav-theme-btn:hover {
          background: rgba(255, 255, 255, 0.12) !important;
          border-color: rgba(56, 189, 248, 0.45) !important;
          color: #38bdf8 !important;
          transform: translateY(-1px) !important;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        }

        html.light .nav-desktop-actions .nav-search-trigger:hover,
        html.light .nav-desktop-actions .nav-progress-pill:hover,
        html.light .nav-desktop-actions .nav-auth-pill:hover,
        html.light .nav-desktop-actions .nav-theme-btn:hover {
          background: rgba(15, 23, 42, 0.08) !important;
          border-color: rgba(2, 132, 199, 0.35) !important;
          color: #0284c7 !important;
          transform: translateY(-1px) !important;
          box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
        }

        .nav-desktop-actions svg.ui-svg {
          width: 18px !important;
          height: 18px !important;
          stroke-width: 2 !important;
          margin: 0 !important;
        }
      }
"""

# Replace existing @media (min-width: 993px) block in injectStyles
old_media_min = re.search(r'@media \(min-width: 993px\) \{[\s\S]*?html\.light #globalPortalNav \{[\s\S]*?\}\s*\}', js)
if old_media_min:
    js = js[:old_media_min.start()] + js_desktop_rule.strip() + js[old_media_min.end():]
    print("Updated injectStyles @media (min-width: 993px) in unified-nav.js")

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

# =========================================================================
# 2. UPDATE ASSETS/CSS/THEME-MODES.CSS
# =========================================================================
with open(CSS_PATH, 'r', encoding='utf-8') as f:
    css = f.read()

css_desktop_rule = """/* ==========================================================================
   DESKTOP FLOATING ISLAND CAPSULE SPECIFICATION (Apple VisionOS / Raycast)
   Preserves mobile edge-to-edge 100% while floating on 1200px desktop grid
   ========================================================================== */
@media (min-width: 993px) {
  #globalPortalNav,
  .unified-portal-nav {
    max-width: 1200px !important;
    width: calc(100% - 36px) !important;
    margin: 12px auto 0 auto !important;
    top: 12px !important;
    border-radius: 16px !important;
    padding: 0 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28), 0 2px 8px rgba(0, 0, 0, 0.18) !important;
    background: rgba(15, 23, 42, 0.88) !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    direction: rtl !important;
  }

  html.light #globalPortalNav,
  html.light .unified-portal-nav {
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08), 0 2px 6px rgba(15, 23, 42, 0.04) !important;
    background: rgba(255, 255, 255, 0.92) !important;
  }

  /* 1. Actions on EXTREME RIGHT (Order 1 in RTL) */
  #globalPortalNav .nav-desktop-actions {
    order: 1 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
  }

  /* 2. Tabs in CENTER (Order 2 in RTL) */
  #globalPortalNav .nav-desktop-tabs {
    order: 2 !important;
    margin: 0 auto !important;
  }

  /* 3. Logo and Chapters on EXTREME LEFT (Order 3 in RTL) */
  #globalPortalNav .nav-brand-group {
    order: 3 !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: row-reverse !important;
    align-items: center !important;
    gap: 10px !important;
  }

  /* Megamenu opens inwards to the right from left position */
  .nav-chapters-megamenu {
    left: 0 !important;
    right: auto !important;
  }

  /* Luxury Icon-Only Action Buttons */
  .nav-desktop-actions .nav-search-trigger,
  .nav-desktop-actions .nav-progress-pill,
  .nav-desktop-actions .nav-auth-pill,
  .nav-desktop-actions .nav-theme-btn {
    width: 38px !important;
    min-width: 38px !important;
    max-width: 38px !important;
    height: 38px !important;
    min-height: 38px !important;
    max-height: 38px !important;
    padding: 0 !important;
    border-radius: 10px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    cursor: pointer !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #94a3b8 !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }

  html.light .nav-desktop-actions .nav-search-trigger,
  html.light .nav-desktop-actions .nav-progress-pill,
  html.light .nav-desktop-actions .nav-auth-pill,
  html.light .nav-desktop-actions .nav-theme-btn {
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.1) !important;
    color: #475569 !important;
  }

  .nav-desktop-actions .nav-search-trigger:hover,
  .nav-desktop-actions .nav-progress-pill:hover,
  .nav-desktop-actions .nav-auth-pill:hover,
  .nav-desktop-actions .nav-theme-btn:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    border-color: rgba(56, 189, 248, 0.45) !important;
    color: #38bdf8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
  }

  html.light .nav-desktop-actions .nav-search-trigger:hover,
  html.light .nav-desktop-actions .nav-progress-pill:hover,
  html.light .nav-desktop-actions .nav-auth-pill:hover,
  html.light .nav-desktop-actions .nav-theme-btn:hover {
    background: rgba(15, 23, 42, 0.08) !important;
    border-color: rgba(2, 132, 199, 0.35) !important;
    color: #0284c7 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
  }

  .nav-desktop-actions svg.ui-svg {
    width: 18px !important;
    height: 18px !important;
    stroke-width: 2 !important;
    margin: 0 !important;
  }
}"""

old_css_block = re.search(r'\/\* =+ *\r?\n *DESKTOP FLOATING ISLAND CAPSULE SPECIFICATION[\s\S]*?@media \(min-width: 993px\) \{[\s\S]*?html\.light \.unified-portal-nav \{[\s\S]*?\}\s*\}', css)
if old_css_block:
    css = css[:old_css_block.start()] + css_desktop_rule.strip() + css[old_css_block.end():]
    print("Updated theme-modes.css desktop floating island block")
else:
    print("Warning: Could not match CSS desktop floating block")

with open(CSS_PATH, 'w', encoding='utf-8') as f:
    f.write(css)

print("All updates applied cleanly!")

import re

JS_NAV_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js"
CSS_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css"
INDEX_PATH = r"R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html"

# =========================================================================
# 1. UPDATE ASSETS/JS/UNIFIED-NAV.JS
# =========================================================================
with open(JS_NAV_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# Update actions block in renderGlobalHeader
old_actions_pat = r'<div class="nav-desktop-actions" id="globalDesktopActions">[\s\S]*?<\/div>\s*<!-- 4\.'

new_actions_block = """<div class="nav-desktop-actions" id="globalDesktopActions">
          <!-- 1. حساب المستخدم (أقصى اليمين - الحافة الخارجية) -->
          <div class="nav-auth-wrapper" style="position:relative; display:inline-flex; align-items:center;">
            <button class="nav-auth-pill guest" id="globalAuthPill" title="تسجيل الدخول أو بيانات الحساب" aria-label="بيانات الدخول">
              <span class="auth-icon-wrap" style="display:inline-flex;align-items:center;justify-content:center;">${SVG_ICONS.user}</span>
            </button>
          </div>

          <!-- 2. تبديل المظهر النهاري / الليلي -->
          <button class="nav-theme-btn" onclick="window.toggleTheme && window.toggleTheme()" title="تبديل المظهر (نهاري / ليلي) [Alt + T]" aria-label="تبديل المظهر">
            <span class="theme-icon-span">${SVG_ICONS.sun}</span>
            <span class="theme-label-span" style="display:none;">المظهر</span>
          </button>

          <!-- 3. لوحة الإنجاز ونسبة التقدم الحية (Circular Progress Gauge) -->
          <a href="${ctx.interactive}dashboard.html" class="nav-progress-pill" id="globalProgressPill" title="إنجازك العام: حللت ${globalStats.answered} من ${globalStats.total} سؤالاً (${globalStats.pct}%)" aria-label="إنجازك">
            <div class="prog-circular-wrap" style="position:relative; width:28px; height:28px; display:inline-flex; align-items:center; justify-content:center;">
              <svg viewBox="0 0 36 36" style="width:28px; height:28px; transform:rotate(-90deg);">
                <circle cx="18" cy="18" r="14" fill="none" stroke="currentColor" stroke-width="3" opacity="0.15"></circle>
                <circle id="globalProgressCircleStroke" cx="18" cy="18" r="14" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="88" stroke-dashoffset="${88 - (88 * globalStats.pct / 100)}" stroke-linecap="round"></circle>
              </svg>
              <span id="globalProgressPctVal" style="position:absolute; font-size:10px; font-weight:800; font-family:'Cairo',sans-serif; color:inherit; direction:ltr;">${globalStats.pct}%</span>
            </div>
          </a>

          <!-- 4. البحث الفوري (الأقرب للتبويبات والمناهج) -->
          <button class="nav-search-trigger" id="btnOpenGlobalSearch" title="بحث فوري في الأبواب والمصطلحات والأسئلة [Ctrl + K]" aria-label="بحث فوري">
            <span class="search-icon">${SVG_ICONS.search}</span>
          </button>
        </div>

        <!-- 4."""

if re.search(old_actions_pat, js):
    js = re.sub(old_actions_pat, new_actions_block, js)
    print("Updated desktop actions markup in unified-nav.js")
else:
    print("Warning: old actions markup pattern not found")

# Update updateAllProgressBadges in unified-nav.js to handle circle stroke
old_update_fn = """  function updateAllProgressBadges() {
    const stats = getGlobalProgressStats();
    // Desktop Pill
    const pctVal = document.getElementById('globalProgressPctVal');
    const fill = document.getElementById('globalProgressMiniFill');
    const pill = document.getElementById('globalProgressPill');
    if (pctVal) pctVal.textContent = `${stats.pct}%`;
    if (fill) fill.style.width = `${stats.pct}%`;
    if (pill) pill.setAttribute('title', `إنجازك العام: حللت ${stats.answered} من ${stats.total} سؤالاً (${stats.pct}%)`);"""

new_update_fn = """  function updateAllProgressBadges() {
    const stats = getGlobalProgressStats();
    // Desktop Circular Pill
    const pctVal = document.getElementById('globalProgressPctVal');
    const circleStroke = document.getElementById('globalProgressCircleStroke');
    const fill = document.getElementById('globalProgressMiniFill');
    const pill = document.getElementById('globalProgressPill');
    if (pctVal) pctVal.textContent = `${stats.pct}%`;
    if (circleStroke) {
      const offset = 88 - (88 * stats.pct / 100);
      circleStroke.style.strokeDashoffset = offset;
    }
    if (fill) fill.style.width = `${stats.pct}%`;
    if (pill) pill.setAttribute('title', `إنجازك العام: حللت ${stats.answered} من ${stats.total} سؤالاً (${stats.pct}%)`);"""

if old_update_fn in js:
    js = js.replace(old_update_fn, new_update_fn)
    print("Updated updateAllProgressBadges in unified-nav.js")
else:
    # Regex fallback
    js = re.sub(r'function updateAllProgressBadges\(\)\s*\{[\s\S]*?if \(pill\) pill\.setAttribute[\s\S]*?\);', new_update_fn, js)
    print("Regex updated updateAllProgressBadges in unified-nav.js")

# Update injectStyles in unified-nav.js
js_desktop_spec = """
      @media (min-width: 1200px) {
        #globalPortalNav {
          position: fixed !important;
          top: 14px !important;
          left: calc((100% - 1164px) / 2) !important;
          right: calc((100% - 1164px) / 2) !important;
          width: 1164px !important;
          max-width: 1164px !important;
          height: 64px !important;
          min-height: 64px !important;
          max-height: 64px !important;
          border-radius: 18px !important;
          padding: 0 16px !important;
          margin: 0 !important;
          z-index: 10000 !important;
          box-sizing: border-box !important;
          display: flex !important;
          justify-content: space-between !important;
          align-items: center !important;
          direction: rtl !important;
          background: rgba(15, 23, 42, 0.88) !important;
          border: 1px solid rgba(255, 255, 255, 0.12) !important;
          box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.18) !important;
          backdrop-filter: blur(20px) !important;
          -webkit-backdrop-filter: blur(20px) !important;
        }
      }
      @media (max-width: 1199px) and (min-width: 993px) {
        #globalPortalNav {
          position: fixed !important;
          top: 14px !important;
          left: 18px !important;
          right: 18px !important;
          width: calc(100% - 36px) !important;
          max-width: calc(100% - 36px) !important;
          height: 64px !important;
          min-height: 64px !important;
          max-height: 64px !important;
          border-radius: 18px !important;
          padding: 0 16px !important;
          margin: 0 !important;
          z-index: 10000 !important;
          box-sizing: border-box !important;
          display: flex !important;
          justify-content: space-between !important;
          align-items: center !important;
          direction: rtl !important;
          background: rgba(15, 23, 42, 0.88) !important;
          border: 1px solid rgba(255, 255, 255, 0.12) !important;
          box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.18) !important;
          backdrop-filter: blur(20px) !important;
          -webkit-backdrop-filter: blur(20px) !important;
        }
      }
      @media (min-width: 993px) {
        body {
          padding-top: 92px !important;
        }
        html.light #globalPortalNav {
          background: rgba(255, 255, 255, 0.94) !important;
          border: 1px solid rgba(15, 23, 42, 0.12) !important;
          box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08), 0 2px 8px rgba(15, 23, 42, 0.04) !important;
        }

        /* 1. Actions on FAR RIGHT (Order 1 in RTL) */
        #globalPortalNav .nav-desktop-actions {
          order: 1 !important;
          margin: 0 !important;
          display: flex !important;
          align-items: center !important;
          gap: 8px !important;
          flex-shrink: 0 !important;
          direction: rtl !important;
        }

        /* Order inside Actions (Rightmost to Leftmost):
           1: Auth (Profile)
           2: Theme Toggle
           3: Progress Ring %
           4: Search
        */
        .nav-desktop-actions .nav-auth-wrapper { order: 1 !important; }
        .nav-desktop-actions .nav-theme-btn { order: 2 !important; }
        .nav-desktop-actions .nav-progress-pill { order: 3 !important; }
        .nav-desktop-actions .nav-search-trigger { order: 4 !important; }

        /* 2. Tabs in CENTER (Equalized 40px Height for ALL tabs) */
        #globalPortalNav .nav-desktop-tabs {
          order: 2 !important;
          margin: 0 auto !important;
          display: flex !important;
          align-items: center !important;
          gap: 4px !important;
        }
        .nav-desktop-tabs .nav-dropdown-tab,
        .nav-desktop-tabs .nav-direct-tab {
          height: 40px !important;
          min-height: 40px !important;
          max-height: 40px !important;
          display: inline-flex !important;
          align-items: center !important;
          justify-content: center !important;
          box-sizing: border-box !important;
          border-radius: 10px !important;
          font-size: 0.86rem !important;
          font-weight: 700 !important;
          padding: 0 14px !important;
        }

        /* 3. Logo and Chapters on FAR LEFT */
        #globalPortalNav .nav-brand-group {
          order: 3 !important;
          margin: 0 !important;
          display: flex !important;
          flex-direction: row-reverse !important;
          align-items: center !important;
          gap: 8px !important;
          flex-shrink: 0 !important;
        }

        /* Chapters button compact */
        .nav-chapters-btn {
          height: 40px !important;
          padding: 0 10px !important;
          gap: 5px !important;
          font-size: 0.82rem !important;
          border-radius: 10px !important;
        }

        /* Megamenu opens inwards to the right from left position */
        .nav-chapters-megamenu {
          left: 0 !important;
          right: auto !important;
        }

        /* Action Buttons -> Strictly 40x40 Icon Only */
        .nav-desktop-actions .nav-search-trigger,
        .nav-desktop-actions .nav-progress-pill,
        .nav-desktop-actions .nav-auth-pill,
        .nav-desktop-actions .nav-theme-btn {
          width: 40px !important;
          min-width: 40px !important;
          max-width: 40px !important;
          height: 40px !important;
          min-height: 40px !important;
          max-height: 40px !important;
          padding: 0 !important;
          border-radius: 10px !important;
          display: inline-flex !important;
          align-items: center !important;
          justify-content: center !important;
          box-sizing: border-box !important;
          cursor: pointer !important;
          overflow: hidden !important;
          background: rgba(255, 255, 255, 0.05) !important;
          border: 1px solid rgba(255, 255, 255, 0.1) !important;
          color: #94a3b8 !important;
          transform: none !important;
          transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease, box-shadow 0.18s ease !important;
        }

        html.light .nav-desktop-actions .nav-search-trigger,
        html.light .nav-desktop-actions .nav-progress-pill,
        html.light .nav-desktop-actions .nav-auth-pill,
        html.light .nav-desktop-actions .nav-theme-btn {
          background: rgba(15, 23, 42, 0.04) !important;
          border: 1px solid rgba(15, 23, 42, 0.1) !important;
          color: #475569 !important;
        }

        /* Smooth, stable hover WITHOUT any jitter / jump */
        .nav-desktop-actions .nav-search-trigger:hover,
        .nav-desktop-actions .nav-progress-pill:hover,
        .nav-desktop-actions .nav-auth-pill:hover,
        .nav-desktop-actions .nav-theme-btn:hover {
          background: rgba(255, 255, 255, 0.12) !important;
          border-color: rgba(56, 189, 248, 0.45) !important;
          color: #38bdf8 !important;
          transform: none !important;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        }

        html.light .nav-desktop-actions .nav-search-trigger:hover,
        html.light .nav-desktop-actions .nav-progress-pill:hover,
        html.light .nav-desktop-actions .nav-auth-pill:hover,
        html.light .nav-desktop-actions .nav-theme-btn:hover {
          background: rgba(15, 23, 42, 0.08) !important;
          border-color: rgba(2, 132, 199, 0.35) !important;
          color: #0284c7 !important;
          transform: none !important;
          box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
        }

        /* Hide any injected text */
        .nav-desktop-actions .nav-search-trigger .search-text,
        .nav-desktop-actions .nav-search-trigger .search-kbd,
        .nav-desktop-actions .nav-progress-pill .prog-pill-label,
        .nav-desktop-actions .nav-progress-pill .prog-pill-val,
        .nav-desktop-actions .nav-progress-pill .prog-pill-bar-track,
        .nav-desktop-actions .nav-auth-pill span:not(.auth-icon-wrap):not(.auth-online-dot),
        .nav-desktop-actions .nav-theme-btn .theme-label-span {
          display: none !important;
        }

        .nav-desktop-actions svg.ui-svg {
          width: 19px !important;
          height: 19px !important;
          stroke-width: 2 !important;
          margin: 0 !important;
        }
      }
"""

js = re.sub(r'@media \(min-width: 1200px\) \{[\s\S]*?\.nav-desktop-actions svg\.ui-svg \{[\s\S]*?\}\s*\}', js_desktop_spec.strip(), js)

with open(JS_NAV_PATH, 'w', encoding='utf-8') as f:
    f.write(js)
print("Saved updated unified-nav.js")


# =========================================================================
# 2. UPDATE ASSETS/CSS/THEME-MODES.CSS
# =========================================================================
with open(CSS_PATH, 'r', encoding='utf-8') as f:
    css = f.read()

css_desktop_spec = """/* ==========================================================================
   DESKTOP FLOATING ISLAND CAPSULE SPECIFICATION (Apple VisionOS / Raycast)
   Preserves mobile edge-to-edge 100% while floating with exact 1164px grid match
   ========================================================================== */
@media (min-width: 1200px) {
  #globalPortalNav,
  .unified-portal-nav {
    position: fixed !important;
    top: 14px !important;
    left: calc((100% - 1164px) / 2) !important;
    right: calc((100% - 1164px) / 2) !important;
    width: 1164px !important;
    max-width: 1164px !important;
    height: 64px !important;
    min-height: 64px !important;
    max-height: 64px !important;
    border-radius: 18px !important;
    padding: 0 16px !important;
    margin: 0 !important;
    z-index: 10000 !important;
    box-sizing: border-box !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    direction: rtl !important;
    background: rgba(15, 23, 42, 0.88) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.18) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
  }
}
@media (max-width: 1199px) and (min-width: 993px) {
  #globalPortalNav,
  .unified-portal-nav {
    position: fixed !important;
    top: 14px !important;
    left: 18px !important;
    right: 18px !important;
    width: calc(100% - 36px) !important;
    max-width: calc(100% - 36px) !important;
    height: 64px !important;
    min-height: 64px !important;
    max-height: 64px !important;
    border-radius: 18px !important;
    padding: 0 16px !important;
    margin: 0 !important;
    z-index: 10000 !important;
    box-sizing: border-box !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    direction: rtl !important;
    background: rgba(15, 23, 42, 0.88) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.18) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
  }
}
@media (min-width: 993px) {
  body {
    padding-top: 92px !important;
  }
  html.light #globalPortalNav,
  html.light .unified-portal-nav {
    background: rgba(255, 255, 255, 0.94) !important;
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08), 0 2px 8px rgba(15, 23, 42, 0.04) !important;
  }

  /* 1. Actions on FAR RIGHT (Order 1 in RTL) */
  #globalPortalNav .nav-desktop-actions {
    order: 1 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    flex-shrink: 0 !important;
    direction: rtl !important;
  }

  /* Order inside Actions (Rightmost to Leftmost):
     1: Auth (Profile)
     2: Theme Toggle
     3: Progress Ring %
     4: Search
  */
  .nav-desktop-actions .nav-auth-wrapper { order: 1 !important; }
  .nav-desktop-actions .nav-theme-btn { order: 2 !important; }
  .nav-desktop-actions .nav-progress-pill { order: 3 !important; }
  .nav-desktop-actions .nav-search-trigger { order: 4 !important; }

  /* 2. Tabs in CENTER (Equalized 40px Height for ALL tabs) */
  #globalPortalNav .nav-desktop-tabs {
    order: 2 !important;
    margin: 0 auto !important;
    display: flex !important;
    align-items: center !important;
    gap: 4px !important;
  }
  .nav-desktop-tabs .nav-dropdown-tab,
  .nav-desktop-tabs .nav-direct-tab {
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    border-radius: 10px !important;
    font-size: 0.86rem !important;
    font-weight: 700 !important;
    padding: 0 14px !important;
  }

  /* 3. Logo and Chapters on FAR LEFT */
  #globalPortalNav .nav-brand-group {
    order: 3 !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: row-reverse !important;
    align-items: center !important;
    gap: 8px !important;
    flex-shrink: 0 !important;
  }

  /* Chapters button compact */
  .nav-chapters-btn {
    height: 40px !important;
    padding: 0 10px !important;
    gap: 5px !important;
    font-size: 0.82rem !important;
    border-radius: 10px !important;
  }

  /* Megamenu opens inwards to the right from left position */
  .nav-chapters-megamenu {
    left: 0 !important;
    right: auto !important;
  }

  /* Action Buttons -> Strictly 40x40 Icon Only */
  .nav-desktop-actions .nav-search-trigger,
  .nav-desktop-actions .nav-progress-pill,
  .nav-desktop-actions .nav-auth-pill,
  .nav-desktop-actions .nav-theme-btn {
    width: 40px !important;
    min-width: 40px !important;
    max-width: 40px !important;
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    padding: 0 !important;
    border-radius: 10px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    cursor: pointer !important;
    overflow: hidden !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #94a3b8 !important;
    transform: none !important;
    transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease, box-shadow 0.18s ease !important;
  }

  html.light .nav-desktop-actions .nav-search-trigger,
  html.light .nav-desktop-actions .nav-progress-pill,
  html.light .nav-desktop-actions .nav-auth-pill,
  html.light .nav-desktop-actions .nav-theme-btn {
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.1) !important;
    color: #475569 !important;
  }

  /* Smooth, stable hover WITHOUT any jitter / jump */
  .nav-desktop-actions .nav-search-trigger:hover,
  .nav-desktop-actions .nav-progress-pill:hover,
  .nav-desktop-actions .nav-auth-pill:hover,
  .nav-desktop-actions .nav-theme-btn:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    border-color: rgba(56, 189, 248, 0.45) !important;
    color: #38bdf8 !important;
    transform: none !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
  }

  html.light .nav-desktop-actions .nav-search-trigger:hover,
  html.light .nav-desktop-actions .nav-progress-pill:hover,
  html.light .nav-desktop-actions .nav-auth-pill:hover,
  html.light .nav-desktop-actions .nav-theme-btn:hover {
    background: rgba(15, 23, 42, 0.08) !important;
    border-color: rgba(2, 132, 199, 0.35) !important;
    color: #0284c7 !important;
    transform: none !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
  }

  /* Hide any injected text */
  .nav-desktop-actions .nav-search-trigger .search-text,
  .nav-desktop-actions .nav-search-trigger .search-kbd,
  .nav-desktop-actions .nav-progress-pill .prog-pill-label,
  .nav-desktop-actions .nav-progress-pill .prog-pill-val,
  .nav-desktop-actions .nav-progress-pill .prog-pill-bar-track,
  .nav-desktop-actions .nav-auth-pill span:not(.auth-icon-wrap):not(.auth-online-dot),
  .nav-desktop-actions .nav-theme-btn .theme-label-span {
    display: none !important;
  }

  .nav-desktop-actions svg.ui-svg {
    width: 19px !important;
    height: 19px !important;
    stroke-width: 2 !important;
    margin: 0 !important;
  }
}"""

css = re.sub(r'\/\* =+ *\r?\n *DESKTOP FLOATING ISLAND CAPSULE SPECIFICATION[\s\S]*?\.nav-desktop-actions svg\.ui-svg \{[\s\S]*?\}\s*\}', css_desktop_spec.strip(), css)

with open(CSS_PATH, 'w', encoding='utf-8') as f:
    f.write(css)
print("Saved updated theme-modes.css")

# =========================================================================
# 3. BUMP CACHE BUSTER IN CAPITOLI_DIVISI/INDEX.HTML
# =========================================================================
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    idx = f.read()

idx = re.sub(r'theme-modes\.css\?v=[^"\'\s>]+', 'theme-modes.css?v=2026.11.05.FINAL_PERFECT', idx)
idx = re.sub(r'unified-nav\.js\?v=[^"\'\s>]+', 'unified-nav.js?v=2026.11.05.FINAL_PERFECT', idx)

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(idx)
print("Bumped query string in Capitoli_Divisi/index.html to FINAL_PERFECT")

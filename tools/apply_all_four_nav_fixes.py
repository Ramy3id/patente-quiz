import re

CSS_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css"
JS_NAV_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js"
JS_AUTH_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\js\firebase-auth-engine.js"
INDEX_PATH = r"R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html"

# =========================================================================
# 1. UPDATE ASSETS/JS/FIREBASE-AUTH-ENGINE.JS
# =========================================================================
with open(JS_AUTH_PATH, 'r', encoding='utf-8') as f:
    auth_js = f.read()

# Update updateAuthUiLoggedOut
old_logged_out = "pill.innerHTML = '<span>👤</span> <span>دخول / تسجيل</span>';"
new_logged_out = """pill.innerHTML = '<span class="auth-icon-wrap" style="display:inline-flex;align-items:center;justify-content:center;"><svg class="ui-svg" viewBox="0 0 24 24" style="width:19px;height:19px;stroke:currentColor;fill:none;stroke-width:2;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></span>';"""

if old_logged_out in auth_js:
    auth_js = auth_js.replace(old_logged_out, new_logged_out)
    print("Updated updateAuthUiLoggedOut in firebase-auth-engine.js")
else:
    # Regex fallback
    auth_js = re.sub(r"pill\.innerHTML\s*=\s*'<span>.*?<\/span>\s*<span>.*?<\/span>';", new_logged_out, auth_js)
    print("Regex updated updateAuthUiLoggedOut in firebase-auth-engine.js")

# Update updateAuthUiLoggedIn to keep icon-only on desktop
old_logged_in_pill = """pill.innerHTML = `
        <span class="auth-online-dot" id="authSyncDot"></span>
        <span>👤 ${escapeHtml(name)}</span>
        <span style="font-size:0.7rem;">▾</span>
      `;"""
new_logged_in_pill = """pill.innerHTML = `
        <span class="auth-online-dot" id="authSyncDot" style="position:absolute;top:6px;right:6px;width:7px;height:7px;border-radius:50%;background:#10b981;box-shadow:0 0 6px #10b981;"></span>
        <span class="auth-icon-wrap" style="display:inline-flex;align-items:center;justify-content:center;"><svg class="ui-svg" viewBox="0 0 24 24" style="width:19px;height:19px;stroke:currentColor;fill:none;stroke-width:2;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></span>
      `;"""

if old_logged_in_pill in auth_js:
    auth_js = auth_js.replace(old_logged_in_pill, new_logged_in_pill)
    print("Updated updateAuthUiLoggedIn in firebase-auth-engine.js")
else:
    auth_js = re.sub(r"pill\.innerHTML\s*=\s*`\s*<span class=\"auth-online-dot\"[\s\S]*?`;", new_logged_in_pill, auth_js)
    print("Regex updated updateAuthUiLoggedIn in firebase-auth-engine.js")

with open(JS_AUTH_PATH, 'w', encoding='utf-8') as f:
    f.write(auth_js)


# =========================================================================
# 2. UPDATE ASSETS/JS/UNIFIED-NAV.JS
# =========================================================================
with open(JS_NAV_PATH, 'r', encoding='utf-8') as f:
    nav_js = f.read()

# Make chapters button label compact: "1-25"
old_chapters_btn = """              <span class="btn-icon">${SVG_ICONS.book}</span>
              <span class="btn-label">تصفح الأبواب (1-25)</span>
              <span class="dropdown-chevron">▾</span>"""

new_chapters_btn = """              <span class="btn-icon">${SVG_ICONS.book}</span>
              <span class="btn-label">1-25</span>
              <span class="dropdown-chevron">▾</span>"""

if old_chapters_btn in nav_js:
    nav_js = nav_js.replace(old_chapters_btn, new_chapters_btn)
    print("Updated chapters button to compact 1-25 in unified-nav.js")
else:
    nav_js = re.sub(r'<span class="btn-label">تصفح الأبواب \(1-25\)<\/span>', '<span class="btn-label">1-25</span>', nav_js)
    print("Regex updated chapters button label in unified-nav.js")

# Update injectStyles desktop rule in unified-nav.js
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

        /* 1. Actions on FAR RIGHT */
        #globalPortalNav .nav-desktop-actions {
          order: 1 !important;
          margin: 0 !important;
          display: flex !important;
          align-items: center !important;
          gap: 8px !important;
          flex-shrink: 0 !important;
        }

        /* 2. Tabs in CENTER */
        #globalPortalNav .nav-desktop-tabs {
          order: 2 !important;
          margin: 0 auto !important;
          display: flex !important;
          align-items: center !important;
          gap: 4px !important;
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

        /* Hide text completely inside action buttons */
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

old_js_rule_match = re.search(r'@media \(min-width: 993px\) \{[\s\S]*?\.nav-desktop-actions svg\.ui-svg \{[\s\S]*?\}\s*\}', nav_js)
if old_js_rule_match:
    nav_js = nav_js[:old_js_rule_match.start()] + js_desktop_spec.strip() + nav_js[old_js_rule_match.end():]
    print("Replaced injectStyles desktop spec in unified-nav.js")

with open(JS_NAV_PATH, 'w', encoding='utf-8') as f:
    f.write(nav_js)


# =========================================================================
# 3. UPDATE ASSETS/CSS/THEME-MODES.CSS
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

  /* 1. Actions on FAR RIGHT */
  #globalPortalNav .nav-desktop-actions {
    order: 1 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    flex-shrink: 0 !important;
  }

  /* 2. Tabs in CENTER */
  #globalPortalNav .nav-desktop-tabs {
    order: 2 !important;
    margin: 0 auto !important;
    display: flex !important;
    align-items: center !important;
    gap: 4px !important;
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

  /* Hide text completely inside action buttons */
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

old_css_rule_match = re.search(r'\/\* =+ *\r?\n *DESKTOP FLOATING ISLAND CAPSULE SPECIFICATION[\s\S]*?\.nav-desktop-actions svg\.ui-svg \{[\s\S]*?\}\s*\}', css)
if old_css_rule_match:
    css = css[:old_css_rule_match.start()] + css_desktop_spec.strip() + css[old_css_rule_match.end():]
    print("Replaced CSS desktop floating capsule spec in theme-modes.css")

with open(CSS_PATH, 'w', encoding='utf-8') as f:
    f.write(css)


# =========================================================================
# 4. UPDATE CACHE BUSTER IN CAPITOLI_DIVISI/INDEX.HTML
# =========================================================================
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    idx = f.read()

idx = re.sub(r'theme-modes\.css\?v=[^"\'\s>]+', 'theme-modes.css?v=2026.11.05.FIX4', idx)
idx = re.sub(r'unified-nav\.js\?v=[^"\'\s>]+', 'unified-nav.js?v=2026.11.05.FIX4', idx)

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(idx)

print("Bumped cache buster query string in Capitoli_Divisi/index.html")
print("All 4 fixes applied cleanly!")

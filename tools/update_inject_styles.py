import sys

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# Replace the injectStyles block for native-bottom-dock
start_str = "      /* =========================================================\n         Native Bottom Dock - 5 Pillars (Apple HIG & Material 3)\n         ========================================================= */"
end_str = "      #patenteScrollTopBtn {\n        bottom: calc(76px + env(safe-area-inset-bottom, 0px)) !important;\n      }"

# Let's normalize crlf
nav_norm = nav.replace('\r\n', '\n')

replacement_css = """      /* =========================================================
         Hybrid Floating Island Dock + Center Hero (Apple HIG & Material 3)
         ========================================================= */
      .native-bottom-dock {
        position: fixed !important;
        bottom: calc(12px + env(safe-area-inset-bottom, 0px)) !important;
        left: 12px !important;
        right: 12px !important;
        max-width: 440px !important;
        margin: 0 auto !important;
        height: 64px !important;
        border-radius: 28px !important;
        background: rgba(15, 23, 42, 0.88) !important;
        backdrop-filter: blur(28px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(28px) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        box-shadow: 0 14px 36px -4px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(255, 255, 255, 0.05) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-around !important;
        padding: 0 4px !important;
        z-index: 9998 !important;
        direction: rtl !important;
        user-select: none !important;
        -webkit-user-select: none !important;
      }
      html.light .native-bottom-dock {
        background: rgba(255, 255, 255, 0.92) !important;
        border-color: rgba(15, 23, 42, 0.12) !important;
        box-shadow: 0 14px 36px -4px rgba(15, 23, 42, 0.12), 0 0 0 1px rgba(15, 23, 42, 0.04) !important;
      }
      @media (min-width: 993px) {
        .native-bottom-dock {
          display: none !important;
        }
      }
      @media (max-width: 992px) {
        body {
          padding-bottom: calc(96px + env(safe-area-inset-bottom, 0px)) !important;
        }
      }
      .dock-tab {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 3px !important;
        padding: 6px 4px !important;
        border-radius: 16px !important;
        color: #94A3B8 !important;
        text-decoration: none !important;
        min-width: 52px !important;
        position: relative !important;
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        -webkit-tap-highlight-color: transparent !important;
      }
      html.light .dock-tab {
        color: #64748B !important;
      }
      .dock-tab:active {
        transform: scale(0.92) !important;
      }
      .dock-tab.active {
        color: #38BDF8 !important;
        background: rgba(56, 189, 248, 0.12) !important;
      }
      html.light .dock-tab.active {
        color: #0284C7 !important;
        background: rgba(2, 132, 199, 0.1) !important;
      }
      .dock-tab.active::after {
        content: '' !important;
        position: absolute !important;
        bottom: 2px !important;
        width: 14px !important;
        height: 3px !important;
        background: #38BDF8 !important;
        border-radius: 99px !important;
        box-shadow: 0 0 8px #38BDF8 !important;
      }
      html.light .dock-tab.active::after {
        background: #0284C7 !important;
        box-shadow: 0 0 8px rgba(2, 132, 199, 0.6) !important;
      }
      .dock-svg {
        width: 20px !important;
        height: 20px !important;
        stroke-width: 2.2 !important;
        stroke: currentColor !important;
        fill: none !important;
        stroke-linecap: round !important;
        stroke-linejoin: round !important;
        transition: transform 0.2s ease !important;
      }
      .dock-tab.active .dock-svg {
        transform: translateY(-1px) !important;
      }
      .dock-label {
        font-family: 'Cairo', system-ui, sans-serif !important;
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        line-height: 1 !important;
      }
      /* Center Hero Elevated FAB */
      .hero-center-tab {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-decoration: none !important;
        margin-top: -24px !important;
        position: relative !important;
        z-index: 10 !important;
        gap: 3px !important;
        transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        -webkit-tap-highlight-color: transparent !important;
      }
      .hero-center-tab:active {
        transform: scale(0.92) !important;
      }
      .hero-fab {
        width: 52px !important;
        height: 52px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #075985 100%) !important;
        border: 3.5px solid #090D16 !important;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.55), inset 0 1px 2px rgba(255, 255, 255, 0.35) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #FFFFFF !important;
        position: relative !important;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
      }
      html.light .hero-fab {
        border-color: #E2E8F0 !important;
        background: linear-gradient(135deg, #0284C7 0%, #0284C7 100%) !important;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
      }
      .hero-fab::after {
        content: '' !important;
        position: absolute !important;
        inset: -3.5px !important;
        border-radius: 50% !important;
        background: conic-gradient(from 0deg, #009246 0deg 120deg, #FFFFFF 120deg 240deg, #CE2B37 240deg 360deg) !important;
        z-index: -1 !important;
        opacity: 0.65 !important;
      }
      .hero-fab-svg {
        width: 25px !important;
        height: 25px !important;
        stroke-width: 2.2 !important;
        stroke: currentColor !important;
        fill: none !important;
        stroke-linecap: round !important;
        stroke-linejoin: round !important;
      }
      .hero-label {
        font-family: 'Cairo', system-ui, sans-serif !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        color: #38BDF8 !important;
        line-height: 1 !important;
      }
      html.light .hero-label {
        color: #0284C7 !important;
      }
      .dock-badge {
        position: absolute !important;
        top: -3px !important;
        left: -8px !important;
        background: #EF4444 !important;
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.58rem !important;
        font-weight: 800 !important;
        padding: 0 5px !important;
        height: 15px !important;
        border-radius: 99px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 2px 6px rgba(239, 68, 68, 0.6) !important;
        border: 1.5px solid #0F172A !important;
        z-index: 5 !important;
      }
      html.light .dock-badge {
        border-color: #FFFFFF !important;
      }
      #patenteScrollTopBtn {
        bottom: calc(90px + env(safe-area-inset-bottom, 0px)) !important;
      }"""

idx_start = nav_norm.find(start_str)
idx_end = nav_norm.find(end_str)

if idx_start != -1 and idx_end != -1:
    idx_end += len(end_str)
    nav_norm = nav_norm[:idx_start] + replacement_css + nav_norm[idx_end:]
    with open(nav_path, 'w', encoding='utf-8') as f:
        f.write(nav_norm)
    print("SUCCESS: Updated injectStyles in unified-nav.js")
else:
    print(f"FAILED to find target: start={idx_start}, end={idx_end}")

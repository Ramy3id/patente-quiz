import re

JS_PATH = r"R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js"

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js_content = f.read()

target = """      #globalPortalNav .nav-mobile-controls {
        direction: rtl !important;
        display: none !important;
        align-items: center !important;
        gap: 8px !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        order: 1 !important;
      }"""

replacement = """      #globalPortalNav .nav-mobile-controls {
        direction: rtl !important;
        display: none !important;
        align-items: center !important;
        gap: 8px !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        order: 1 !important;
      }
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
        }
        html.light #globalPortalNav {
          border: 1px solid rgba(15, 23, 42, 0.12) !important;
          box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08), 0 2px 6px rgba(15, 23, 42, 0.04) !important;
          background: rgba(255, 255, 255, 0.92) !important;
        }
      }"""

if target in js_content:
    js_content = js_content.replace(target, replacement, 1)
    with open(JS_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("Cleanly updated unified-nav.js!")
else:
    print("Target not found in unified-nav.js")

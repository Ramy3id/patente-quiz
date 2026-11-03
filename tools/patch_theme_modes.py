import sys

with open('R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

overflow_guard = """
/* ==========================================================================
   PLATFORM-WIDE ZERO HORIZONTAL OVERFLOW GUARD (Apple HIG & Material 3)
   Guarantees 100% responsive viewport fit on all mobile screens (320px - 430px)
   ========================================================================== */
html {
  overflow-x: hidden !important;
  max-width: 100vw !important;
  width: 100% !important;
  box-sizing: border-box !important;
  -webkit-text-size-adjust: 100% !important;
}

body {
  overflow-x: hidden !important;
  max-width: 100vw !important;
  width: 100% !important;
  position: relative !important;
  box-sizing: border-box !important;
}

*, *::before, *::after {
  box-sizing: border-box !important;
}
"""

if "PLATFORM-WIDE ZERO HORIZONTAL OVERFLOW GUARD" not in content_norm:
    # Insert right at the top of the file after the first comments
    idx = content_norm.find('/* 1. Touch Targets Standard')
    if idx != -1:
        new_content = content_norm[:idx] + overflow_guard + "\n" + content_norm[idx:]
        with open('R:/Ramy/PATENTE_PRO_APP/assets/css/theme-modes.css', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("SUCCESS: added global overflow guard to theme-modes.css")
    else:
        print("Could not find insertion point in theme-modes.css")
else:
    print("ALREADY EXISTS in theme-modes.css")

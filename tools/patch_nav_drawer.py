import sys

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = """      .mobile-drawer-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        z-index: 99999;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1),
                    visibility 0.3s ease;
      }
      .mobile-drawer-backdrop.open {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
      }"""

replacement = """      .mobile-drawer-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        z-index: 99999;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        overflow: hidden !important;
        transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1),
                    visibility 0.3s ease;
      }
      .mobile-drawer-backdrop:not(.open) {
        visibility: hidden !important;
        pointer-events: none !important;
      }
      .mobile-drawer-backdrop:not(.open) .mobile-drawer-pane {
        display: none !important;
      }
      .mobile-drawer-backdrop.open {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
      }"""

# Normalise CRLF vs LF
content_norm = content.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')
replacement_norm = replacement.replace('\r\n', '\n')

if target_norm in content_norm:
    new_content = content_norm.replace(target_norm, replacement_norm, 1)
    with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: patched unified-nav.js drawer")
else:
    print("ERROR: target not found in unified-nav.js")

import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(file_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# 1. Fix nav-mobile-controls rule that forced display: flex !important everywhere
old_rule = '''#globalPortalNav .nav-mobile-controls {
        direction: rtl !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        margin-right: auto !important;
        margin-left: 0 !important;
      }'''

new_rule = '''#globalPortalNav .nav-mobile-controls {
        direction: rtl !important;
        display: none !important;
        align-items: center !important;
        gap: 8px !important;
        margin-right: auto !important;
        margin-left: 0 !important;
      }
      @media (max-width: 992px) {
        #globalPortalNav .nav-mobile-controls {
          display: flex !important;
        }
      }'''

if old_rule in nav:
    nav = nav.replace(old_rule, new_rule, 1)
    print("Fixed #globalPortalNav .nav-mobile-controls rule.")
else:
    print("WARNING: old_rule not found!")

# 2. Fix .native-bottom-dock to HIDE on desktop (min-width: 993px)
# Find the dock media queries in nav
old_dock_mq = '''@media (min-width: 641px) {
        .native-bottom-dock {
          max-width: 480px !important;
          left: 50% !important;
          right: auto !important;
          transform: translateX(-50%) !important;
          bottom: 12px !important;
          border-radius: 22px !important;
          border: 1px solid rgba(255, 255, 255, 0.12) !important;
          padding: 6px 14px !important;
        }
        html.light .native-bottom-dock {
          border: 1px solid rgba(15, 23, 42, 0.1) !important;
        }
      }
      body {
        padding-bottom: calc(76px + env(safe-area-inset-bottom, 0px)) !important;
      }'''

new_dock_mq = '''@media (min-width: 641px) and (max-width: 992px) {
        .native-bottom-dock {
          max-width: 480px !important;
          left: 50% !important;
          right: auto !important;
          transform: translateX(-50%) !important;
          bottom: 12px !important;
          border-radius: 22px !important;
          border: 1px solid rgba(255, 255, 255, 0.12) !important;
          padding: 6px 14px !important;
        }
        html.light .native-bottom-dock {
          border: 1px solid rgba(15, 23, 42, 0.1) !important;
        }
      }
      @media (min-width: 993px) {
        .native-bottom-dock {
          display: none !important;
        }
      }
      @media (max-width: 992px) {
        body {
          padding-bottom: calc(76px + env(safe-area-inset-bottom, 0px)) !important;
        }
      }'''

if old_dock_mq in nav:
    nav = nav.replace(old_dock_mq, new_dock_mq, 1)
    print("Fixed .native-bottom-dock to be hidden on desktop.")
else:
    print("WARNING: old_dock_mq not found!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(nav)

print("Updated unified-nav.js successfully.")

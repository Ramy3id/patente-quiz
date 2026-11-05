import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update unified-nav.js
nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# Replace inline style on footer-bottom-compact
nav = nav.replace('class="footer-bottom-compact" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);"', 'class="footer-bottom-compact"')

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)
print("Updated unified-nav.js.")

# 2. Update theme-modes.css
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

# Replace padding: 48px 24px 120px !important; on .unified-portal-footer
tm = tm.replace('padding: 48px 24px 120px !important;', 'padding: 36px 20px 24px !important;')

# Replace .footer-bottom-compact rules
old_bottom_compact = '''.footer-bottom-compact {
  text-align: center !important;
  padding: 16px 12px 24px !important;
  border-top: none !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 6px !important;
}'''

new_bottom_compact = '''.footer-bottom-compact {
  text-align: center !important;
  padding: 24px 12px 6px !important;
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-bottom: none !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 4px !important;
  margin-top: 24px !important;
  margin-bottom: 0 !important;
}'''

if old_bottom_compact in tm:
    tm = tm.replace(old_bottom_compact, new_bottom_compact, 1)
    print("Replaced old_bottom_compact.")

old_bottom_light = '''.footer-bottom-compact {
  border-top: none !important;
}'''

new_bottom_light = '''.footer-bottom-compact {
  border-top: 1px solid rgba(15, 23, 42, 0.08) !important;
  border-bottom: none !important;
}'''

if old_bottom_light in tm:
    tm = tm.replace(old_bottom_light, new_bottom_light, 1)
    print("Replaced old_bottom_light.")

# Replace .footer-dev-card-compact rules
old_dev_compact = '''.footer-dev-card-compact {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 24px 14px 16px !important;
  background: transparent !important;
  border: none !important;
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 0 !important;
  margin: 28px auto 0 !important;
  gap: 12px !important;
  box-shadow: none !important;
  width: 100% !important;
  max-width: 680px !important;
  box-sizing: border-box !important;
}'''

new_dev_compact = '''.footer-dev-card-compact {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  border-top: none !important;
  border-radius: 0 !important;
  margin: 10px auto 0 !important;
  gap: 10px !important;
  box-shadow: none !important;
  width: 100% !important;
  max-width: 680px !important;
  box-sizing: border-box !important;
}'''

if old_dev_compact in tm:
    tm = tm.replace(old_dev_compact, new_dev_compact, 1)
    print("Replaced old_dev_compact.")

old_dev_light = '''.footer-dev-card-compact {
  background: transparent !important;
  border-color: transparent !important;
  border-top: 1px solid rgba(15, 23, 42, 0.08) !important;
  box-shadow: none !important;
}'''

new_dev_light = '''.footer-dev-card-compact {
  background: transparent !important;
  border-color: transparent !important;
  border-top: none !important;
  box-shadow: none !important;
}'''

if old_dev_light in tm:
    tm = tm.replace(old_dev_light, new_dev_light, 1)
    print("Replaced old_dev_light.")

with open(tm_path, 'w', encoding='utf-8') as f:
    f.write(tm)

print("Updated theme-modes.css.")

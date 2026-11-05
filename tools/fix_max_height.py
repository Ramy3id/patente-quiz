import sys
sys.stdout.reconfigure(encoding='utf-8')

target_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_box_style = """    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      width: 100% !important;
      max-width: 100% !important;
      min-height: 100% !important;
      margin: 0 !important;
      padding: 72px 14px 180px 14px !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      background: transparent !important;
      overflow: visible !important;
    }"""

new_box_style = """    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      width: 100% !important;
      max-width: 100% !important;
      min-height: 100% !important;
      height: auto !important;
      max-height: none !important;
      margin: 0 !important;
      padding: 72px 14px 140px 14px !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      background: transparent !important;
      overflow: visible !important;
    }
    .sp-modal-backdrop#planSetupModal .sp-modal-actions-bar {
      margin-top: 30px !important;
      margin-bottom: 80px !important;
    }"""

if old_box_style in content:
    content = content.replace(old_box_style, new_box_style)
    print("Replaced with max-height: none !important.")
else:
    print("old_box_style not found verbatim.")

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated piano-studio.html successfully.")

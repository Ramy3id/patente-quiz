import sys
sys.stdout.reconfigure(encoding='utf-8')

target_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_padding = """    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding: 72px 14px 100px 14px !important;
    }
    .sp-modal-actions-bar {
      margin-top: 26px !important;
      margin-bottom: 50px !important;
    }"""

new_padding = """    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding: 72px 14px 220px 14px !important;
    }
    .sp-modal-actions-bar {
      margin-top: 30px !important;
      margin-bottom: 100px !important;
    }"""

if old_padding in content:
    content = content.replace(old_padding, new_padding)
    print("Increased bottom padding and margin for safe dock clearance.")
else:
    print("Warning: old_padding not found.")

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated piano-studio.html successfully.")

import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''.sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding: 68px 14px 24px 14px !important;
    }
    .sp-modal-actions-bar {
      margin-top: 20px !important;
      margin-bottom: 24px !important;
    }'''

replacement = '''.sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding: 68px 14px 80px 14px !important;
    }
    .sp-modal-actions-bar {
      margin-top: 20px !important;
      margin-bottom: 16px !important;
    }'''

if target in content:
    content = content.replace(target, replacement, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated clearance padding to 80px!")
else:
    print("Target not found!")

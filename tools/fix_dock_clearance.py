import sys
sys.stdout.reconfigure(encoding='utf-8')

target_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_css = """    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding: 72px 14px 220px 14px !important;
    }
    .sp-modal-actions-bar {
      margin-top: 30px !important;
      margin-bottom: 100px !important;
    }"""

new_css = """    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding: 72px 14px 180px 14px !important;
    }
    .sp-modal-actions-bar {
      margin-top: 30px !important;
      margin-bottom: 120px !important;
    }"""

if old_css in content:
    content = content.replace(old_css, new_css)
    print("Updated clearance.")
else:
    print("Warning: old_css not found verbatim, appending override.")
    override = """
  @media (max-width: 768px) {
    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding-bottom: 220px !important;
    }
    .sp-modal-actions-bar {
      margin-bottom: 140px !important;
    }
  }
"""
    content = content.replace('</style>', override + '\n  </style>')

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated piano-studio.html successfully.")

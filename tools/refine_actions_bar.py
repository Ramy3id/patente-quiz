import sys
sys.stdout.reconfigure(encoding='utf-8')

target_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Refine CSS for sp-modal-actions-bar to be in normal flow with generous bottom clearance
old_actions_css = """  /* Bottom Actions Bar on Mobile (Floating Above Bottom Navigation Dock) */
  .sp-modal-actions-bar {
    display: flex !important;
    gap: 10px !important;
    margin-top: 24px !important;
  }
  @media (max-width: 768px) {
    .sp-modal-actions-bar {
      position: fixed !important;
      bottom: 56px !important; /* right above the 56px native bottom dock */
      left: 0 !important;
      right: 0 !important;
      width: 100% !important;
      background: rgba(255, 255, 255, 0.96) !important;
      backdrop-filter: blur(16px) !important;
      -webkit-backdrop-filter: blur(16px) !important;
      border-top: 1px solid #E2E8F0 !important;
      padding: 10px 14px !important;
      z-index: 6000 !important;
      box-shadow: 0 -4px 20px rgba(15, 23, 42, 0.08) !important;
      margin: 0 !important;
    }
    html.dark .sp-modal-actions-bar {
      background: rgba(11, 15, 25, 0.96) !important;
      border-top-color: rgba(255, 255, 255, 0.1) !important;
      box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.4) !important;
    }
  }
  .sp-btn-save-plan {
    flex: 2 !important;
    min-height: 48px !important;
    font-size: 0.92rem !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    justify-content: center !important;
    background: linear-gradient(135deg, #0284C7, #0369A1) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25) !important;
    border: none !important;
  }
  .sp-btn-cancel-plan {
    flex: 1 !important;
    min-height: 48px !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    justify-content: center !important;
  }"""

new_actions_css = """  /* Bottom Actions Bar (Generous Clearance Above Bottom Dock) */
  .sp-modal-actions-bar {
    display: flex !important;
    gap: 12px !important;
    margin-top: 28px !important;
    margin-bottom: 40px !important;
    width: 100% !important;
    position: relative !important;
  }
  @media (max-width: 768px) {
    .sp-modal-backdrop#planSetupModal .sp-modal-box {
      padding: 72px 14px 100px 14px !important;
    }
    .sp-modal-actions-bar {
      margin-top: 26px !important;
      margin-bottom: 50px !important;
    }
  }
  .sp-btn-save-plan {
    flex: 2 !important;
    min-height: 50px !important;
    font-size: 0.94rem !important;
    font-weight: 800 !important;
    border-radius: 14px !important;
    justify-content: center !important;
    background: linear-gradient(135deg, #0284C7, #0369A1) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 16px rgba(2, 132, 199, 0.28) !important;
    border: none !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
  }
  .sp-btn-cancel-plan {
    flex: 1 !important;
    min-height: 50px !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    justify-content: center !important;
    border: 1px solid #CBD5E1 !important;
    background: #FFFFFF !important;
    color: #475569 !important;
    cursor: pointer !important;
  }
  html.dark .sp-btn-cancel-plan {
    background: rgba(255, 255, 255, 0.05) !important;
    border-color: rgba(255, 255, 255, 0.12) !important;
    color: #CBD5E1 !important;
  }"""

if old_actions_css in content:
    content = content.replace(old_actions_css, new_actions_css)
    print("Updated sp-modal-actions-bar to normal flow with generous clearance.")
else:
    print("Warning: old_actions_css not found verbatim.")

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated piano-studio.html successfully.")

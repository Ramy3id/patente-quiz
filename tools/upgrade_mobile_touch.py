path = r'R:\Ramy\PATENTE\Simulatore_Esame.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''  @media (max-width: 768px) {
    .q-grid-nav { grid-template-columns: repeat(10, 1fr); }
  }'''

replacement = '''  @media (max-width: 768px) {
    .q-grid-nav { grid-template-columns: repeat(10, 1fr); }
  }
  @media (max-width: 480px) {
    .q-grid-nav {
      grid-template-columns: repeat(6, 1fr) !important;
      gap: 8px !important;
      padding: 10px !important;
    }
    .q-pill {
      height: 44px !important;
      font-size: 0.92rem !important;
      border-radius: 9px !important;
    }
    .btn-choice {
      padding: 16px 20px !important;
      font-size: 1.1rem !important;
    }
  }
  .btn-stage-nav, .btn-submit-exam, .btn-subtle-back {
    min-height: 44px;
  }'''

if target in content:
    content = content.replace(target, replacement, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Simulatore_Esame.html mobile touch targets upgraded to Apple HIG 44px standard!")
else:
    print("Target media query not found!")

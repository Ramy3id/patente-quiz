path = r'R:\Ramy\PATENTE\assets\css\theme-modes.css'

with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

depth_css = '''
/* ==========================================================================
   Enhanced Multi-Layered Elevation & Depth (Light Mode WCAG AAA)
   ========================================================================== */
html.light .chapter-card,
html.light .q-stage-card,
html.light .legal-card,
html.light .hero-main-card,
html.light .hero-side-card {
  background: #ffffff !important;
  border: 1px solid rgba(15, 23, 42, 0.12) !important;
  box-shadow: 
    0 1px 3px 0 rgba(15, 23, 42, 0.05),
    0 10px 25px -5px rgba(15, 23, 42, 0.06) !important;
}

html.light .chapter-card:hover {
  border-color: #0284c7 !important;
  box-shadow: 
    0 4px 6px -1px rgba(15, 23, 42, 0.07),
    0 16px 32px -4px rgba(2, 132, 199, 0.12) !important;
  transform: translateY(-2px);
}

html.light .btn-action-study {
  background: #f1f5f9 !important;
  color: #0f172a !important;
  border: 1px solid rgba(15, 23, 42, 0.12) !important;
}

html.light .btn-action-study:hover {
  background: #059669 !important;
  color: #ffffff !important;
  border-color: #047857 !important;
}
'''

if 'Enhanced Multi-Layered Elevation & Depth' not in css:
    css += '\n' + depth_css
    with open(path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Light Mode multi-layered depth CSS added to theme-modes.css!")
else:
    print("Depth CSS already exists in theme-modes.css")

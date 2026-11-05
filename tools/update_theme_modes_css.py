import sys

sys.stdout.reconfigure(encoding='utf-8')

css_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

extra_css = """
/* ==========================================================================
   PLATFORM-WIDE UNIFIED SVG ICONS & BRAND STYLING (2026 Apple HIG Standard)
   ========================================================================== */

.inline-ui-svg {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  vertical-align: middle !important;
  line-height: 1 !important;
}

.inline-ui-svg svg,
.hydrated-svg svg,
.btn-svg-wrap svg {
  width: 1.15em !important;
  height: 1.15em !important;
  fill: none !important;
  stroke: currentColor !important;
  stroke-width: 2 !important;
  stroke-linecap: round !important;
  stroke-linejoin: round !important;
}

.footer-brand-header {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  gap: 12px !important;
  margin-bottom: 12px !important;
  direction: rtl !important;
}

.footer-brand-logo {
  width: 32px !important;
  height: 32px !important;
  min-width: 32px !important;
  min-height: 32px !important;
  border-radius: 50% !important;
  object-fit: contain !important;
  flex-shrink: 0 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
}

.footer-brand-year {
  order: 1 !important;
  font-size: 0.75rem !important;
  font-weight: 800 !important;
  background: rgba(56, 189, 248, 0.14) !important;
  border: 1px solid rgba(56, 189, 248, 0.3) !important;
  color: #38BDF8 !important;
  padding: 2px 8px !important;
  border-radius: 6px !important;
  font-family: 'JetBrains Mono', monospace !important;
  white-space: nowrap !important;
}

html.light .footer-brand-year {
  background: rgba(2, 132, 199, 0.08) !important;
  border-color: rgba(2, 132, 199, 0.25) !important;
  color: #0284C7 !important;
}

.footer-brand-title {
  order: 2 !important;
  font-size: 1.25rem !important;
  font-weight: 900 !important;
  color: #F8FAFC !important;
  letter-spacing: -0.3px !important;
}

html.light .footer-brand-title {
  color: #0F172A !important;
}

.footer-brand-logo {
  order: 3 !important;
}

.badge-dot-live {
  display: inline-block !important;
  width: 8px !important;
  height: 8px !important;
  border-radius: 50% !important;
  background: #10B981 !important;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.6) !important;
  margin-left: 6px !important;
  vertical-align: middle !important;
}
"""

if 'PLATFORM-WIDE UNIFIED SVG ICONS' not in css:
    css += extra_css
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print('SUCCESS: Added unified SVG icons and brand styling CSS.')
else:
    print('NOTE: Styles already present in theme-modes.css')

file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'

with open(file_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .footer-dev-card-compact and light mode rules
old_target = '''.footer-dev-card-compact {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 16px 14px !important;
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 18px !important;
  margin: 22px 0 14px !important;
  gap: 12px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
  max-width: 440px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  box-sizing: border-box !important;
}
html.light .footer-dev-card-compact {
  background: #ffffff !important;
  border-color: #E2E8F0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
}'''

new_replacement = '''/* Integrated Seamless Signature Band (Executive Minimalist 10/10) */
.footer-dev-card-compact {
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
}
html.light .footer-dev-card-compact {
  background: transparent !important;
  border-color: transparent !important;
  border-top: 1px solid rgba(15, 23, 42, 0.08) !important;
  box-shadow: none !important;
}'''

if old_target in css:
    css = css.replace(old_target, new_replacement)
    print("Replaced exact target in theme-modes.css")
else:
    import re
    css = re.sub(
        r'\.footer-dev-card-compact\s*\{[\s\S]*?html\.light\s*\.footer-dev-card-compact\s*\{[^}]*\}',
        new_replacement,
        css,
        count=1
    )
    print("Replaced via regex in theme-modes.css")

# Also update .footer-bottom-compact to remove border-top so it seamlessly blends with the signature band
css = css.replace(
    'border-top: 1px solid rgba(255, 255, 255, 0.06) !important;',
    'border-top: none !important;'
)
css = css.replace(
    'border-top-color: #E2E8F0 !important;',
    'border-top: none !important;'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated theme-modes.css successfully!")

css_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(css_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """#patenteScrollTopBtn {
  bottom: calc(76px + env(safe-area-inset-bottom, 0px)) !important;
}"""

replacement = """#patenteScrollTopBtn {
  bottom: calc(76px + env(safe-area-inset-bottom, 0px)) !important;
  width: 48px !important;
  height: 48px !important;
  min-width: 48px !important;
  min-height: 48px !important;
  max-width: 48px !important;
  max-height: 48px !important;
  border-radius: 50% !important;
  aspect-ratio: 1 / 1 !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-sizing: border-box !important;
}

/* Strict 1:1 Perfect Circular Shapes for All Modal Close and Floating Round Buttons */
.auth-close-btn,
#btnGateClose,
#btnAuthClose,
.modal-close-btn,
.round-close-btn {
  width: 36px !important;
  height: 36px !important;
  min-width: 36px !important;
  min-height: 36px !important;
  max-width: 36px !important;
  max-height: 36px !important;
  border-radius: 50% !important;
  aspect-ratio: 1 / 1 !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
  box-sizing: border-box !important;
}"""

target_crlf = target.replace('\n', '\r\n')
replacement_crlf = replacement.replace('\n', '\r\n')

if target_crlf in text:
    text = text.replace(target_crlf, replacement_crlf)
    print("Updated theme-modes.css (CRLF)")
elif target in text:
    text = text.replace(target, replacement)
    print("Updated theme-modes.css (LF)")
else:
    print("Target not found in theme-modes.css")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(text)

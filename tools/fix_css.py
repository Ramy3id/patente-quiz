path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace display: flex !important in .global-search-backdrop
old_part = """.global-search-backdrop {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(11, 15, 25, 0.78) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  z-index: 999999 !important;
  display: flex !important;
  align-items: flex-start !important;
  justify-content: center !important;
  padding: 40px 16px 20px !important;
  box-sizing: border-box !important;
  direction: rtl !important;
}"""

new_part = """.global-search-backdrop[style*="display: none"],
.global-search-backdrop[style*="display:none"] {
  display: none !important;
}

.global-search-backdrop {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(11, 15, 25, 0.78) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  z-index: 999999 !important;
  align-items: flex-start !important;
  justify-content: center !important;
  padding: 40px 16px 20px !important;
  box-sizing: border-box !important;
  direction: rtl !important;
}"""

# Normalize crlf
c_norm = c.replace('\r\n', '\n')
old_norm = old_part.replace('\r\n', '\n')
new_norm = new_part.replace('\r\n', '\n')

if old_norm in c_norm:
    c_norm = c_norm.replace(old_norm, new_norm)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c_norm)
    print("Success: theme-modes.css updated!")
else:
    print("Target not found in theme-modes.css")

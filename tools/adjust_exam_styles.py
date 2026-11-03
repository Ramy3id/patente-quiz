file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove #btnQuickSubmit from hub-primary-row
text = text.replace("""          <!-- زر التسليم السريع -->
          <button type="button" class="btn-quick-submit" id="btnQuickSubmit" title="تسليم بطاقة الامتحان وتصحيح النتيجة">
            <span>تسليم 📋</span>
          </button>""", "")

# 2. Perfect vertical alignment for exam-nav-steps
old_nav_steps_css = """.exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
      height: 38px;
    }"""

new_nav_steps_css = """.exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 6px;
      height: 42px;
    }
    .btn-submit-pill {
      height: 42px !important;
      padding: 0 16px !important;
      border-radius: 12px !important;
      background: linear-gradient(135deg, #10B981, #059669) !important;
      border: none !important;
      color: #FFFFFF !important;
      font-weight: 800 !important;
      font-size: 0.86rem !important;
      cursor: pointer !important;
      white-space: nowrap !important;
      box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3) !important;
      font-family: inherit !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    .btn-nav-step {
      height: 42px !important;
      min-height: 42px !important;
      max-height: 42px !important;
      font-size: 0.88rem !important;
      padding: 0 12px !important;
      border-radius: 12px !important;
      background: rgba(255, 255, 255, 0.06) !important;
      border: 1px solid rgba(255, 255, 255, 0.1) !important;
      color: var(--text-secondary) !important;
      cursor: pointer !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }"""

if old_nav_steps_css in text:
    text = text.replace(old_nav_steps_css, new_nav_steps_css)
    print("Updated nav steps CSS")
elif old_nav_steps_css.replace('\n', '\r\n') in text:
    text = text.replace(old_nav_steps_css.replace('\n', '\r\n'), new_nav_steps_css.replace('\n', '\r\n'))
    print("Updated nav steps CSS (CRLF)")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Adjustments saved.")

import sys

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# Replace footer bottom structure in unified-nav.js
old_snippet = '''          <!-- الجزء 2: شريط الحقوق والأمان الفاخر -->
          <div class="footer-bottom-compact">
            <div class="footer-copy-line">Patente B Pro © 2026 • مبادرة تعليمية</div>
            <div class="footer-meta-line" style="margin-top: 4px;">
              <span>Vanilla JS</span> • <span>WCAG 2.1 AA</span> • <span>Safe Storage</span>
            </div>
          </div>

          <!-- الجزء 3: كارت المهندس والمطور (في أسفل الفوتر تماماً تحت سطر الحقوق) -->
          <div class="footer-dev-card-compact">'''

new_snippet = '''          <!-- الجزء 2 و 3 الموحد: شريط الحقوق + بطاقة المطور مدمجين مع خط فاصل علوي أنيق -->
          <div class="footer-bottom-unified-wrap">
            <div class="footer-bottom-compact">
              <div class="footer-copy-line">Patente B Pro © 2026 • مبادرة تعليمية</div>
              <div class="footer-meta-line" style="margin-top: 4px;">
                <span>Vanilla JS</span> • <span>WCAG 2.1 AA</span> • <span>Safe Storage</span>
              </div>
            </div>

            <!-- كارت المهندس والمطور مدمج تحت سطر الحقوق بمسافة متناسقة -->
            <div class="footer-dev-card-compact">'''

if old_snippet in nav:
    nav = nav.replace(old_snippet, new_snippet, 1)
    # Add closing </div> for footer-bottom-unified-wrap before </div>\n      </footer>
    # Let's find the closing of footer-dev-card-compact
    idx_dev_close = nav.find('</div>\n          </div>\n        </div>\n      </footer>')
    if idx_dev_close != -1:
        nav = nav[:idx_dev_close] + '</div>\n            </div>\n          </div>\n        </div>\n      </footer>' + nav[idx_dev_close + len('</div>\n          </div>\n        </div>\n      </footer>'):]
    print("Replaced footer HTML in unified-nav.js.")
else:
    print("WARNING: old_snippet not found in unified-nav.js")

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

# Update theme-modes.css
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

# Add styles for footer-bottom-unified-wrap and streamline bottom-compact & dev-compact
footer_wrap_css = '''
/* Unified Footer Bottom Architecture with Master Divider */
.footer-bottom-unified-wrap {
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
  padding-top: 20px !important;
  padding-bottom: 4px !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  gap: 12px !important;
  width: 100% !important;
  margin: 0 auto !important;
}

html.light .footer-bottom-unified-wrap {
  border-top: 1px solid rgba(15, 23, 42, 0.08) !important;
}

.footer-bottom-compact {
  text-align: center !important;
  padding: 0 !important;
  margin: 0 !important;
  border: none !important;
  border-top: none !important;
  border-bottom: none !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 4px !important;
}

html.light .footer-bottom-compact {
  border: none !important;
  border-top: none !important;
  border-bottom: none !important;
}

.footer-dev-card-compact {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  margin: 0 !important;
  background: transparent !important;
  border: none !important;
  border-top: none !important;
  border-radius: 0 !important;
  gap: 10px !important;
  box-shadow: none !important;
  width: 100% !important;
  max-width: 680px !important;
  box-sizing: border-box !important;
}

html.light .footer-dev-card-compact {
  background: transparent !important;
  border: none !important;
  border-top: none !important;
  box-shadow: none !important;
}
'''

# Append before the last few lines or add to theme-modes.css
tm += '\n' + footer_wrap_css

with open(tm_path, 'w', encoding='utf-8') as f:
    f.write(tm)

print("Updated theme-modes.css with unified bottom wrap CSS.")

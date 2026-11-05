import sys, re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update unified-nav.js
nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# --- A. Reorder mobile controls in HTML: Hamburger first (Right), Auth second, Search third ---
old_mobile_controls = '''<!-- 4. عناصر تحكم الموبايل (<= 992px) - مظهر أنيق وموحد مع أيقونة الحساب -->
        <div class="nav-mobile-controls" id="globalMobileControls">
          <!-- زر البحث الفوري السريع -->
          <button class="nav-mobile-btn" id="btnOpenMobileSearch" title="بحث فوري [Ctrl + K]" aria-label="بحث سريع">
            <span style="font-size:1.15rem;">🔍</span>
          </button>

          <!-- زر الحساب والمصادقة الموحد للموبايل -->
          <button class="nav-mobile-btn" id="btnOpenMobileAuth" title="تسجيل الدخول أو عرض الملف الشخصي" aria-label="حساب المستخدم">
            <span style="font-size:1.15rem;">👤</span>
          </button>

          <!-- زر تبديل الوضع النهاري والليلي -->
          <button class="nav-mobile-btn nav-mobile-theme-btn" onclick="window.toggleTheme && window.toggleTheme()" title="تبديل الوضع" aria-label="تبديل الوضع">
            <span class="theme-icon-span">☀️</span>
          </button>

          <!-- زر الهمبرغر المتطور لفتح القائمة الشاملة -->
          <button class="nav-hamburger-btn nav-mobile-hamburger" id="btnToggleMobileDrawer" aria-label="فتح قائمة التنقل وتصفح الأبواب" aria-expanded="false">
            <div class="hamburger-box">
              <span class="hamburger-line line-top"></span>
              <span class="hamburger-line line-mid"></span>
              <span class="hamburger-line line-bot"></span>
            </div>
          </button>
        </div>'''

new_mobile_controls = '''<!-- 4. عناصر تحكم الموبايل (<= 992px) - الأيقونات على اليمين بالترتيب: همبرغر، حساب، بحث -->
        <div class="nav-mobile-controls" id="globalMobileControls">
          <!-- زر الهمبرغر المربع لفتح القائمة الشاملة -->
          <button class="nav-hamburger-btn nav-mobile-hamburger" id="btnToggleMobileDrawer" aria-label="فتح قائمة التنقل وتصفح الأبواب" aria-expanded="false">
            <div class="hamburger-box">
              <span class="hamburger-line line-top"></span>
              <span class="hamburger-line line-mid"></span>
              <span class="hamburger-line line-bot"></span>
            </div>
          </button>

          <!-- زر الحساب والمصادقة الموحد للموبايل -->
          <button class="nav-mobile-btn" id="btnOpenMobileAuth" title="تسجيل الدخول أو عرض الملف الشخصي" aria-label="حساب المستخدم">
            <span style="font-size:1.15rem;">👤</span>
          </button>

          <!-- زر البحث الفوري السريع -->
          <button class="nav-mobile-btn" id="btnOpenMobileSearch" title="بحث فوري [Ctrl + K]" aria-label="بحث سريع">
            <span style="font-size:1.15rem;">🔍</span>
          </button>
        </div>'''

if old_mobile_controls in nav:
    nav = nav.replace(old_mobile_controls, new_mobile_controls, 1)
    print("Reordered mobile controls in HTML successfully.")
else:
    print("WARNING: old_mobile_controls not matched exactly, checking pattern...")

# --- B. Update Footer in unified-nav.js: put user info BELOW copyright & remove 'غير ربحية' ---
# Find developer card and bottom bar
dev_card_pattern = r'<!-- الجزء 2: كارت المطور[\s\S]*?</div>\s*</div>\s*<!-- الجزء 3: شريط الحقوق[\s\S]*?</div>\s*</div>'

new_footer_bottom = '''<!-- الجزء 2: شريط الحقوق والأمان الفاخر -->
          <div class="footer-bottom-compact" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
            <div class="footer-copy-line">Patente B Pro © 2026 • مبادرة تعليمية</div>
            <div class="footer-meta-line" style="margin-top: 4px;">
              <span>Vanilla JS</span> • <span>WCAG 2.1 AA</span> • <span>Safe Storage</span>
            </div>
          </div>

          <!-- الجزء 3: كارت المهندس والمطور (في أسفل الفوتر تماماً تحت سطر الحقوق) -->
          <div class="footer-dev-card-compact">
            <div class="footer-dev-info-row">
              <div class="footer-dev-meta">
                <div class="footer-dev-name">Eng. Ramy Fahmy</div>
                <div class="footer-dev-title">Software Architecture Engineer • Brindisi, IT</div>
              </div>
            </div>

            <!-- شريط الأيقونات الـ 5 المعتمد طبقاً لـ Apple HIG -->
            <div class="footer-dev-icons-bar">
              <a href="https://github.com/Ramy3id" target="_blank" rel="noopener noreferrer" class="dev-icon-btn" title="GitHub" aria-label="GitHub">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
              </a>
              <a href="https://portfolio-taupe-eight-84.vercel.app/" target="_blank" rel="noopener noreferrer" class="dev-icon-btn" title="Portfolio" aria-label="Portfolio">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
              </a>
              <a href="https://wa.me/393278788484" target="_blank" rel="noopener noreferrer" class="dev-icon-btn" title="WhatsApp" aria-label="WhatsApp">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/></svg>
              </a>
              <a href="mailto:ramy.eid.fahmy@gmail.com" class="dev-icon-btn" title="Email" aria-label="Email">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              </a>
              <a href="https://linkedin.com/in/ramy-eid-fahmy" target="_blank" rel="noopener noreferrer" class="dev-icon-btn" title="LinkedIn" aria-label="LinkedIn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
              </a>
            </div>
          </div>'''

# Search around 'footer-dev-card-compact'
idx_dev = nav.find('footer-dev-card-compact')
idx_bottom_end = nav.find('</footer>', idx_dev)
if idx_dev != -1 and idx_bottom_end != -1:
    # Find start of comment before dev card
    idx_dev_comment = nav.rfind('<!--', 0, idx_dev)
    nav = nav[:idx_dev_comment] + new_footer_bottom + '\n        </div>\n      ' + nav[idx_bottom_end:]
    print("Reordered footer successfully (developer info below copyright, removed 'غير ربحية').")

# --- C. Update Header CSS in unified-nav.js ---
# Swap Logo (Left) and Icons (Right) on mobile, make hamburger and mobile buttons perfect squares
header_css_updates = '''
      /* Header RTL Layout: Icons on Right, Logo on Left */
      @media (max-width: 992px) {
        .unified-portal-nav {
          display: flex !important;
          flex-direction: row !important;
          justify-content: space-between !important;
          align-items: center !important;
          padding: 0 12px !important;
        }
        #globalPortalNav .nav-mobile-controls {
          order: 1 !important; /* Right side in RTL */
          display: flex !important;
          align-items: center !important;
          gap: 6px !important;
          margin: 0 !important;
        }
        #globalPortalNav .nav-brand-group {
          order: 2 !important; /* Left side in RTL */
          display: flex !important;
          align-items: center !important;
          margin: 0 !important;
        }
        .nav-mobile-btn,
        .nav-mobile-hamburger,
        .nav-hamburger-btn {
          width: 38px !important;
          min-width: 38px !important;
          max-width: 38px !important;
          height: 38px !important;
          min-height: 38px !important;
          max-height: 38px !important;
          border-radius: 10px !important;
          padding: 0 !important;
          box-sizing: border-box !important;
          display: inline-flex !important;
          align-items: center !important;
          justify-content: center !important;
          flex-shrink: 0 !important;
        }
      }
'''

# Add this CSS before </style> in unified-nav.js
idx_style_end = nav.find('</style>')
if idx_style_end != -1:
    nav = nav[:idx_style_end] + header_css_updates + nav[idx_style_end:]
    print("Appended header layout & square hamburger CSS.")

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

# 2. Update theme-modes.css to make .nav-hamburger-btn square
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

# Replace min-height 44px on nav-hamburger-btn
old_tm_snippet = '''.nav-mobile-btn,
  .tools-sheet-close {
    min-width: 44px !important;
    min-height: 44px !important;
    padding: 10px;
  }'''

new_tm_snippet = '''.nav-mobile-btn,
  .nav-hamburger-btn,
  .nav-mobile-hamburger,
  .tools-sheet-close {
    width: 38px !important;
    min-width: 38px !important;
    max-width: 38px !important;
    height: 38px !important;
    min-height: 38px !important;
    max-height: 38px !important;
    border-radius: 10px !important;
    padding: 0 !important;
  }'''

if old_tm_snippet in tm:
    tm = tm.replace(old_tm_snippet, new_tm_snippet, 1)
    print("Updated theme-modes.css for square hamburger buttons.")
    with open(tm_path, 'w', encoding='utf-8') as f:
        f.write(tm)

print("Applied all changes successfully!")

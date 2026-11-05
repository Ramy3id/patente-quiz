import sys

sys.stdout.reconfigure(encoding='utf-8')
nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'

with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# Swap header in drawer
target = '''          <div class="mobile-drawer-header">
            <div class="drawer-header-brand">
              <span style="font-size:1.4rem;">🚦</span>
              <div>
                <strong class="drawer-app-title">Patente B Pro</strong>
                <span class="drawer-app-subtitle">القائمة الموحدة وتصفح الأبواب</span>
              </div>
            </div>
            <button class="mobile-drawer-close" id="btnCloseMobileDrawer" aria-label="إغلاق القائمة">✕</button>
          </div>'''

replacement = '''          <div class="mobile-drawer-header">
            <!-- زر الإغلاق على اليمين في نفس موضع زر الهمبرغر لتسهيل التحكم بالإبهام -->
            <button class="mobile-drawer-close" id="btnCloseMobileDrawer" aria-label="إغلاق القائمة" title="إغلاق القائمة">✕</button>

            <!-- الشعار والاسم على اليسار ليتطابق مع هيدر التطبيق الرئيسي -->
            <div class="drawer-header-brand">
              <div>
                <strong class="drawer-app-title">Patente B Pro</strong>
                <span class="drawer-app-subtitle">القائمة الموحدة وتصفح الأبواب</span>
              </div>
              <span style="font-size:1.4rem;">🚦</span>
            </div>
          </div>'''

if target in nav:
    nav = nav.replace(target, replacement, 1)
    print("Replaced mobile-drawer-header successfully.")
else:
    print("Target not found!")

# Also improve .mobile-drawer-close styling
old_close_css = '''.mobile-drawer-close {
        background: transparent;
        border: none;
        color: #94A3B8;
        font-size: 1.3rem;
        cursor: pointer;
        padding: 4px;
      }'''

new_close_css = '''.mobile-drawer-close {
        width: 36px;
        height: 36px;
        min-width: 36px;
        min-height: 36px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #94A3B8;
        font-size: 1.15rem;
        cursor: pointer;
        padding: 0;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
      }
      .mobile-drawer-close:hover {
        background: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border-color: rgba(239, 68, 68, 0.3);
      }
      html.light .mobile-drawer-close {
        background: rgba(15, 23, 42, 0.05);
        border-color: rgba(15, 23, 42, 0.1);
        color: #64748B;
      }
      html.light .mobile-drawer-close:hover {
        background: rgba(239, 68, 68, 0.1);
        color: #EF4444;
      }'''

if old_close_css in nav:
    nav = nav.replace(old_close_css, new_close_css, 1)
    print("Updated mobile-drawer-close CSS successfully.")

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

print("Saved unified-nav.js.")

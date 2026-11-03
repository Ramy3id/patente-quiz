file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update Modern Skin switcher markup to use sync classes
old_modern_switcher = '''          <!-- تبديل الوضع (Pill Switcher) -->
          <div class="exam-skin-switcher-mini">
            <button type="button" class="skin-btn-mini active" id="btnSkinModern" title="الوضع العصري الفاخر">
              <span>🌟 عصري</span>
            </button>
            <button type="button" class="skin-btn-mini" id="btnSkinMoto" title="شاشة كمبيوتر المرور">
              <span>🖥️ رسمي</span>
            </button>
          </div>'''

new_modern_switcher = '''          <!-- تبديل الوضع كبسولة ON / OFF (Segmented Switch) -->
          <div class="exam-skin-switcher-mini">
            <button type="button" class="skin-btn-mini active btn-skin-modern-sync" id="btnSkinModern" title="الوضع العصري الفاخر">
              <span>🌟 عصري</span>
            </button>
            <button type="button" class="skin-btn-mini btn-skin-moto-sync" id="btnSkinMoto" title="شاشة كمبيوتر المرور">
              <span>🖥️ رسمي</span>
            </button>
          </div>'''

if old_modern_switcher in c:
    c = c.replace(old_modern_switcher, new_modern_switcher)
    print('1. Modern switcher markup updated with sync classes')
else:
    print('1. old_modern_switcher not found')

# 2. Update Motorizzazione Header markup to use the EXACT SAME switcher
old_moto_actions = '''        <div class="moto-header-actions">
          <button type="button" class="btn-moto-switch-modern" id="btnMotoReturnModern" title="العودة للوضع العصري">
            <span>🌟 عصري</span>
          </button>
          <div class="moto-timer-badge" id="motoTimerBadge">⏱️ 20:00</div>
        </div>'''

new_moto_actions = '''        <div class="moto-header-actions">
          <!-- نفس زر التقليب ON / OFF كبسولة موحدة في الوضع الرسمي -->
          <div class="exam-skin-switcher-mini" id="motoSkinSwitcher">
            <button type="button" class="skin-btn-mini btn-skin-modern-sync" id="btnSkinModernMoto" title="الوضع العصري الفاخر">
              <span>🌟 عصري</span>
            </button>
            <button type="button" class="skin-btn-mini active btn-skin-moto-sync" id="btnSkinMotoMoto" title="شاشة كمبيوتر المرور">
              <span>🖥️ رسمي</span>
            </button>
          </div>
          <div class="moto-timer-badge" id="motoTimerBadge">⏱️ 20:00</div>
        </div>'''

if old_moto_actions in c:
    c = c.replace(old_moto_actions, new_moto_actions)
    print('2. Motorizzazione header updated with identical ON / OFF toggle switch')
else:
    print('2. old_moto_actions not found')

# 3. Update setSkin and click listeners in JS
old_set_skin = '''      // تبديل المظهر Skin
      function setSkin(skin) {
        currentSkin = skin;
        localStorage.setItem('patente_exam_skin', skin);
        document.body.classList.toggle('skin-moto', skin === 'motorizzazione');
        document.getElementById('btnSkinModern').classList.toggle('active', skin === 'modern');
        document.getElementById('btnSkinMoto').classList.toggle('active', skin === 'motorizzazione');
        renderActiveQuestion();
        renderPills();
      }

      document.getElementById('btnSkinModern').addEventListener('click', () => setSkin('modern'));
      document.getElementById('btnSkinMoto').addEventListener('click', () => setSkin('motorizzazione'));
      document.getElementById('btnMotoReturnModern')?.addEventListener('click', () => setSkin('modern'));'''

new_set_skin = '''      // تبديل المظهر Skin بمزامنة زر ON / OFF في كلا الوضعين
      function setSkin(skin) {
        currentSkin = skin;
        localStorage.setItem('patente_exam_skin', skin);
        document.body.classList.toggle('skin-moto', skin === 'motorizzazione');
        
        document.querySelectorAll('.btn-skin-modern-sync').forEach(b => {
          b.classList.toggle('active', skin === 'modern');
        });
        document.querySelectorAll('.btn-skin-moto-sync').forEach(b => {
          b.classList.toggle('active', skin === 'motorizzazione');
        });
        
        renderActiveQuestion();
        renderPills();
      }

      document.querySelectorAll('.btn-skin-modern-sync').forEach(b => {
        b.addEventListener('click', () => setSkin('modern'));
      });
      document.querySelectorAll('.btn-skin-moto-sync').forEach(b => {
        b.addEventListener('click', () => setSkin('motorizzazione'));
      });'''

if old_set_skin in c:
    c = c.replace(old_set_skin, new_set_skin)
    print('3. JS setSkin and event listeners updated for all sync buttons')
else:
    print('3. old_set_skin not found')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Toggle switch synchronization applied successfully.')

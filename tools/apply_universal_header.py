import re

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML structure: lift exam-control-hub OUTSIDE modernScreenWrap
old_html_pattern = re.compile(
    r'<div class="exam-portal-container">\s*'
    r'<!-- =+\s*1\. واجهة الوضع العصري.*?-->\s*'
    r'<div class="modern-screen-wrap" id="modernScreenWrap">\s*'
    r'<!-- شريط التحكم العلوي المدمج.*?-->\s*'
    r'<div class="exam-control-hub">[\s\S]*?</div>\s*'
    r'<!-- شريط أرقام الأسئلة الـ 30 الفوري -->\s*'
    r'<div class="exam-nav-pills" id="examPillsGrid"></div>\s*'
    r'</div>\s*'
    r'<!-- بطاقة السؤال النشط',
    re.DOTALL
)

# Let's inspect the exact lines between <div class="exam-portal-container"> and <div class="exam-question-card"
start_str = '<div class="exam-portal-container">'
end_str = '<div class="exam-question-card" id="questionCardStage">'

s_idx = content.find(start_str)
e_idx = content.find(end_str)

print("Found start:", s_idx, "end:", e_idx)

replacement_html = '''<div class="exam-portal-container">
    <!-- =========================================================
         0. شريط التحكم العلوي الموحد والثابت 100% بين جميع الأوضاع
         (Universal Master Exam Header - Zero Layout Shift Switcher)
         ========================================================= -->
    <div class="exam-control-hub" id="examMasterControlHub">
      <div class="hub-primary-row">
        <!-- زر التبديل العصري والرسمي (مكان ثابت 100% لا يتحرك مليمتر واحد أبداً) -->
        <div class="exam-skin-switcher-mini" id="masterSkinSwitcher">
          <button type="button" class="skin-btn-mini active btn-skin-modern-sync" id="btnSkinModern" title="الوضع العصري الفاخر">
            <span>🌟 عصري</span>
          </button>
          <button type="button" class="skin-btn-mini btn-skin-moto-sync" id="btnSkinMoto" title="شاشة كمبيوتر المرور">
            <span>🖥️ رسمي</span>
          </button>
        </div>

        <!-- عداد الإنجاز الموحد -->
        <div class="hub-progress-badge">
          <span>تمت:</span>
          <strong id="answeredCounter">0</strong>
          <span>/ 30</span>
        </div>

        <!-- المؤقت التنازلي الموحد -->
        <div class="exam-timer-box-mini" id="examTimerDisplay">⏱️ 20:00</div>
      </div>
    </div>

    <!-- =========================================================
         1. واجهة الوضع العصري (Modern Skin)
         ========================================================= -->
    <div class="modern-screen-wrap" id="modernScreenWrap">
      <!-- شريط أرقام الأسئلة الـ 30 الفوري للوضع العصري -->
      <div class="exam-nav-pills-row">
        <div class="exam-nav-pills" id="examPillsGrid"></div>
      </div>

      '''

content = content[:s_idx] + replacement_html + content[e_idx:]

# 2. In moto-top-header, remove the duplicate switcher and make it a clean authentic ministerial banner
moto_header_pattern = re.compile(
    r'<div class="moto-top-header">[\s\S]*?</div>\s*<div class="moto-main-terminal">',
    re.DOTALL
)

replacement_moto_header = '''<div class="moto-top-header">
        <div class="moto-flag-brand">
          <div class="moto-flag-tricolore">
            <div class="flag-green"></div>
            <div class="flag-white"></div>
            <div class="flag-red"></div>
          </div>
          <div class="moto-titles-text">
            <strong>REPUBBLICA ITALIANA • MINISTERO DEI TRASPORTI</strong>
            <small>DIPARTIMENTO PER I TRASPORTI TERRESTRI • ESAME PATENTE B</small>
          </div>
        </div>
        <div class="moto-timer-badge" id="motoTimerBadge">⏱️ 20:00</div>
      </div>

      <div class="moto-main-terminal">'''

content = moto_header_pattern.sub(replacement_moto_header, content, count=1)

# 3. Refine CSS for moto-top-header, moto-sign-panel, moto-text-italian and exam-nav-pills-row
moto_css_updates = '''
    .exam-nav-pills-row {
      margin-bottom: 8px;
    }
    .moto-top-header {
      background: #0F172A;
      border-bottom: 2px solid #38BDF8;
      padding: 8px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #FFFFFF;
      min-height: 44px;
      box-sizing: border-box;
    }
    html.light .moto-top-header {
      background: #F1F5F9;
      border-bottom-color: #0284C7;
      color: #0F172A;
    }
    .moto-titles-text strong {
      display: block;
      font-size: 0.78rem;
      letter-spacing: 0.5px;
      color: #38BDF8;
      line-height: 1.2;
    }
    html.light .moto-titles-text strong {
      color: #0284C7;
    }
    .moto-titles-text small {
      display: block;
      font-size: 0.65rem;
      color: #94A3B8;
      line-height: 1.2;
    }
    html.light .moto-titles-text small {
      color: #64748B;
    }
    .moto-sign-panel {
      background: #0F172A;
      border: 2px solid #334155;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 4px;
      height: 140px;
      min-height: 140px;
      max-height: 140px;
      box-sizing: border-box;
    }
    .moto-sign-img {
      max-height: 130px;
      max-width: 260px;
      object-fit: contain;
    }
    .moto-text-italian {
      height: 130px;
      min-height: 130px;
      max-height: 130px;
      overflow-y: hidden;
      scrollbar-width: none;
      -ms-overflow-style: none;
      font-size: 1.02rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.36;
      margin-bottom: 8px;
      direction: ltr;
      text-align: left;
      padding: 2px 4px;
      box-sizing: border-box;
    }
'''

content = content.replace('.moto-top-header {', moto_css_updates + '\n    .moto-top-header-legacy {')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Applied unified header and moto refinements successfully!')

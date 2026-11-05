import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# 1. Update renderGlobalFooter in unified-nav.js
old_footer_func = """  function renderGlobalFooter(ctx) {
    return `
      <footer class="unified-portal-footer" id="globalPortalFooter" role="contentinfo" dir="rtl">
        <div class="footer-container">
          
          <!-- الجزء 1: شبكة الأقسام المنظمة (Desktop & Mobile 2026) -->
          <div class="footer-top-grid">
            
            <!-- العمود 1: الشعار ورؤية المنصة -->
            <div class="footer-col footer-col-brand">
              <div class="footer-brand-header">
                <span class="footer-brand-year">2026</span>
                <span class="footer-brand-title">Patente B Pro</span>
                <img src="${ctx.root}assets/brand/brand_logo_steering_trans.png" alt="Patente B Pro" class="footer-brand-logo" width="30" height="30" style="width:30px; height:30px; object-fit:contain; border-radius:50%; flex-shrink:0;">
              </div>
              <p class="footer-brand-desc">
                المنظومة الرقمية الشاملة والمعتمدة لتدريب وتأهيل طلاب رخصة القيادة الإيطالية باللغتين العربية والإيطالية، مع كشف الفخاخ الوزارية والمحاكاة الرسمية.
              </p>
              <div class="footer-brand-stats">
                <span class="footer-stat-badge">📚 25 باباً رسمياً</span>
                <span class="footer-stat-badge">📝 7,139 سؤالاً معتمداً</span>
                <span class="footer-stat-badge">⚡ PWA جاهز أوفلاين</span>
              </div>
            </div>

            <!-- العمود 2: روابط المناهج والأبواب -->
            <div class="footer-col">
              <h4 class="footer-col-title">📖 المناهج والأبواب</h4>
              <ul class="footer-nav-list">
                <li><a href="${ctx.capitoli}index.html" class="footer-nav-link"><span>فهرس بنك الأسئلة الـ 25</span></a></li>
                <li><a href="${ctx.interactive}index.html" class="footer-nav-link"><span>مكتبة أدلة وشروحات الأبواب</span></a></li>
                <li><a href="${ctx.capitoli}dizionario-sinonimi.html" class="footer-nav-link"><span>معجم المترادفات والبدائل</span></a></li>
                <li><a href="${ctx.capitoli}parole-quiz.html" class="footer-nav-link"><span>بنك كلماتي ومستكشف الفخاخ</span></a></li>
              </ul>
            </div>

            <!-- العمود 3: المعامل والأدوات التفاعلية -->
            <div class="footer-col">
              <h4 class="footer-col-title">🔬 المعامل الذكية</h4>
              <ul class="footer-nav-list">
                <li><a href="${ctx.interactive}scheda-esame.html" class="footer-nav-link"><span>محاكي الامتحان الوزاري (30 سؤال)</span></a></li>
                <li><a href="${ctx.interactive}parole-spia.html" class="footer-nav-link"><span>رادار الكلمات السحرية (Parole Spia)</span></a></li>
                <li><a href="${ctx.interactive}decodificatore-incroci.html" class="footer-nav-link"><span>مفكك شفرة التقاطعات (Incroci)</span></a></li>
                <li><a href="${ctx.interactive}laboratorio-numeri.html" class="footer-nav-link"><span>معمل الأرقام والمقاييس والسرعات</span></a></li>
                <li><a href="${ctx.interactive}trucchi-esame.html" class="footer-nav-link"><span>خزينة التريكات ودستور الأبواب</span></a></li>
              </ul>
            </div>

            <!-- العمود 4: أدوات المتابعة والإنجاز -->
            <div class="footer-col">
              <h4 class="footer-col-title">📊 الإنجاز والمتابعة</h4>
              <ul class="footer-nav-list">
                <li><a href="${ctx.interactive}dashboard.html" class="footer-nav-link"><span>لوحة الجاهزية وبنك الأخطاء</span></a></li>
                <li><a href="${ctx.interactive}zero-mistake.html" class="footer-nav-link"><span>تحدي الـ 0 أخطاء (وضع البقاء)</span></a></li>
                <li><a href="${ctx.interactive}piano-studio.html" class="footer-nav-link"><span>خطة المذاكرة الذكية (30 يوماً)</span></a></li>
                <li><a href="${ctx.interactive}cerca-quiz.html" class="footer-nav-link"><span>محرك البحث الوزاري الفوري</span></a></li>
              </ul>
            </div>
          </div>"""

new_footer_func = """  function renderGlobalFooter(ctx) {
    return `
      <footer class="unified-portal-footer" id="globalPortalFooter" role="contentinfo" dir="rtl">
        <div class="footer-container">
          
          <!-- الجزء 1: شبكة الأقسام المنظمة والمختصرة (Desktop & Mobile 2026) -->
          <div class="footer-top-grid">
            
            <!-- العمود 1: الشعار ورؤية المنصة والإحصائيات والمعايير -->
            <div class="footer-col footer-col-brand">
              <div class="footer-brand-header">
                <span class="footer-brand-year">2026</span>
                <span class="footer-brand-title">Patente B Pro</span>
                <img src="${ctx.root}assets/brand/brand_logo_steering_trans.png" alt="Patente B Pro" class="footer-brand-logo" width="30" height="30" style="width:30px; height:30px; object-fit:contain; border-radius:50%; flex-shrink:0;">
              </div>
              <p class="footer-brand-desc">
                المنظومة الرقمية الشاملة لتأهيل الطلاب لاجتياز رخصة القيادة الإيطالية باللغتين العربية والإيطالية، مع كشف الفخاخ الوزارية والمحاكاة الرسمية للاختبارات وفق كود المرور الإيطالي (Codice della Strada).
              </p>
              
              <!-- إحصائيات باهتة بدون إطارات ولا خلفيات بجانب بعض -->
              <div class="footer-brand-stats-inline">
                <span>25 باباً رسمياً</span> • <span>7,139 سؤالاً معتمداً</span> • <span>متوافق مع الهواتف وPWA</span>
              </div>

              <!-- قسم المعايير والخصوصية الأوروبية -->
              <div class="footer-standards-block">
                <div class="footer-standards-title">المعايير والخصوصية</div>
                <p class="footer-standards-desc">
                  حماية البيانات مطابقة للائحة الأوروبية EU 2016/679 (GDPR). يتم حفظ التقدم في متصفحك محلياً بشكل آمن دون تتبع إعلاني خارجي.
                </p>
                <div class="footer-official-badge">Ministero delle Infrastrutture e dei Trasporti</div>
              </div>
            </div>

            <!-- العمود 2: المناهج والأبواب -->
            <div class="footer-col">
              <h4 class="footer-col-title">📖 المناهج الرسمية</h4>
              <ul class="footer-nav-list">
                <li><a href="${ctx.capitoli}index.html" class="footer-nav-link"><span>فهرس بنك الأسئلة الـ 25</span></a></li>
                <li><a href="${ctx.interactive}index.html" class="footer-nav-link"><span>مكتبة أدلة وشروحات الأبواب</span></a></li>
                <li><a href="${ctx.capitoli}dizionario-sinonimi.html" class="footer-nav-link"><span>معجم المترادفات والبدائل</span></a></li>
                <li><a href="${ctx.capitoli}parole-quiz.html" class="footer-nav-link"><span>بنك كلماتي ومستكشف الفخاخ</span></a></li>
              </ul>
            </div>

            <!-- العمود 3: المعامل والامتحانات -->
            <div class="footer-col">
              <h4 class="footer-col-title">🔬 المعامل والتدريب</h4>
              <ul class="footer-nav-list">
                <li><a href="${ctx.interactive}scheda-esame.html" class="footer-nav-link"><span>محاكي الامتحان الوزاري</span></a></li>
                <li><a href="${ctx.interactive}parole-spia.html" class="footer-nav-link"><span>رادار الكلمات السحرية (Parole Spia)</span></a></li>
                <li><a href="${ctx.interactive}dashboard.html" class="footer-nav-link"><span>لوحة الجاهزية وبنك الأخطاء</span></a></li>
                <li><a href="${ctx.interactive}piano-studio.html" class="footer-nav-link"><span>خطة المذاكرة الذكية (30 يوماً)</span></a></li>
              </ul>
            </div>
          </div>"""

# Normalize crlf
nav_norm = nav.replace('\r\n', '\n')
old_footer_norm = old_footer_func.replace('\r\n', '\n')
new_footer_norm = new_footer_func.replace('\r\n', '\n')

if old_footer_norm in nav_norm:
    nav_norm = nav_norm.replace(old_footer_norm, new_footer_norm, 1)
    print("SUCCESS: Updated renderGlobalFooter in unified-nav.js")
else:
    print("WARNING: old_footer_func not found!")

# 2. Update renderNativeBottomDock with Hybrid Dock (SVG icons + Elevated Center Hero FAB)
old_dock_html = """    dock.innerHTML = `
      <a href="${ctx.capitoli}index.html" class="dock-tab ${isHome ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="فهرس الأبواب (الرئيسية)">
        <span class="dock-icon">🏠</span>
        <span class="dock-label">الرئيسية</span>
      </a>
      <a href="${ctx.interactive}scheda-esame.html" class="dock-tab ${isExam ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="محاكي الامتحان الوزاري">
        <span class="dock-icon">⏱️</span>
        <span class="dock-label">الامتحان</span>
      </a>
      <a href="${ctx.interactive}parole-spia.html" class="dock-tab ${isRadar ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="رادار الكلمات السحرية">
        <span class="dock-icon">🎯</span>
        <span class="dock-label">الرادار</span>
      </a>
      <a href="${ctx.interactive}dashboard.html" class="dock-tab ${isMistakes ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="بنك الأخطاء والإنجاز">
        <span class="dock-icon-wrapper">
          <span class="dock-icon">⚠️</span>
          ${badgeHtml}
        </span>
        <span class="dock-label">أخطائي</span>
      </a>
      <a href="${ctx.capitoli}dizionario-sinonimi.html" class="dock-tab ${isVocab ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="معجم المترادفات والبدائل">
        <span class="dock-icon">📖</span>
        <span class="dock-label">المعجم</span>
      </a>
    `;"""

new_dock_html = """    dock.innerHTML = `
      <!-- 1. الرئيسية -->
      <a href="${ctx.capitoli}index.html" class="dock-tab ${isHome ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="الرئيسية">
        <svg class="dock-svg" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        <span class="dock-label">الرئيسية</span>
      </a>

      <!-- 2. الرادار -->
      <a href="${ctx.interactive}parole-spia.html" class="dock-tab ${isRadar ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="رادار الكلمات السحرية">
        <svg class="dock-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><line x1="12" y1="3" x2="12" y2="7"/><line x1="12" y1="17" x2="12" y2="21"/><line x1="3" y1="12" x2="7" y2="12"/><line x1="17" y1="12" x2="21" y2="12"/></svg>
        <span class="dock-label">الرادار</span>
      </a>

      <!-- 3. قمرة القيادة المركزية: محاكي الامتحان الوزاري -->
      <a href="${ctx.interactive}scheda-esame.html" class="hero-center-tab ${isExam ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="محاكي الامتحان الوزاري">
        <div class="hero-fab">
          <svg class="hero-fab-svg" viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5"/><path d="M10 2h4"/></svg>
        </div>
        <span class="hero-label">الامتحان</span>
      </a>

      <!-- 4. أخطائي -->
      <a href="${ctx.interactive}dashboard.html" class="dock-tab ${isMistakes ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="بنك الأخطاء والإنجاز">
        <span class="dock-icon-wrapper" style="position:relative; display:inline-flex;">
          <svg class="dock-svg" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          ${badgeHtml}
        </span>
        <span class="dock-label">أخطائي</span>
      </a>

      <!-- 5. المعجم -->
      <a href="${ctx.capitoli}dizionario-sinonimi.html" class="dock-tab ${isVocab ? 'active' : ''}" onclick="if(window.soundEngine)soundEngine.click()" title="معجم المترادفات والبدائل">
        <svg class="dock-svg" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
        <span class="dock-label">المعجم</span>
      </a>
    `;"""

old_dock_norm = old_dock_html.replace('\r\n', '\n')
new_dock_norm = new_dock_html.replace('\r\n', '\n')

if old_dock_norm in nav_norm:
    nav_norm = nav_norm.replace(old_dock_norm, new_dock_norm, 1)
    print("SUCCESS: Updated renderNativeBottomDock in unified-nav.js")
else:
    print("WARNING: old_dock_html not found!")

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav_norm)

# 3. Add CSS rules in theme-modes.css for the Hybrid Dock & Streamlined Footer
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

hybrid_css = """
/* ==========================================================================
   HYBRID FLOATING ISLAND DOCK + STREAMLINED FOOTER OVERHAUL
   ========================================================================== */

/* Body Bottom Clearance for Floating Island Dock */
body {
  padding-bottom: calc(96px + env(safe-area-inset-bottom, 0px)) !important;
}

/* Floating Glass Island Dock (Mobile & Desktop) */
.native-bottom-dock {
  position: fixed !important;
  bottom: calc(12px + env(safe-area-inset-bottom, 0px)) !important;
  left: 12px !important;
  right: 12px !important;
  max-width: 440px !important;
  margin: 0 auto !important;
  height: 64px !important;
  border-radius: 28px !important;
  background: rgba(15, 23, 42, 0.88) !important;
  backdrop-filter: blur(28px) saturate(190%) !important;
  -webkit-backdrop-filter: blur(28px) !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  box-shadow: 0 14px 36px -4px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(255, 255, 255, 0.05) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-around !important;
  padding: 0 4px !important;
  z-index: 9998 !important;
  direction: rtl !important;
  user-select: none !important;
  -webkit-user-select: none !important;
}

html.light .native-bottom-dock {
  background: rgba(255, 255, 255, 0.92) !important;
  border-color: rgba(15, 23, 42, 0.12) !important;
  box-shadow: 0 14px 36px -4px rgba(15, 23, 42, 0.12), 0 0 0 1px rgba(15, 23, 42, 0.04) !important;
}

/* Standard Tabs */
.dock-tab {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 3px !important;
  padding: 6px 4px !important;
  border-radius: 16px !important;
  color: #94A3B8 !important;
  text-decoration: none !important;
  min-width: 52px !important;
  position: relative !important;
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  -webkit-tap-highlight-color: transparent !important;
}

html.light .dock-tab {
  color: #64748B !important;
}

.dock-tab:active {
  transform: scale(0.92) !important;
}

.dock-tab.active {
  color: #38BDF8 !important;
  background: rgba(56, 189, 248, 0.12) !important;
}

html.light .dock-tab.active {
  color: #0284C7 !important;
  background: rgba(2, 132, 199, 0.1) !important;
}

.dock-tab.active::after {
  content: '' !important;
  position: absolute !important;
  bottom: 2px !important;
  width: 14px !important;
  height: 3px !important;
  background: #38BDF8 !important;
  border-radius: 99px !important;
  box-shadow: 0 0 8px #38BDF8 !important;
}

html.light .dock-tab.active::after {
  background: #0284C7 !important;
  box-shadow: 0 0 8px rgba(2, 132, 199, 0.6) !important;
}

.dock-svg {
  width: 20px !important;
  height: 20px !important;
  stroke-width: 2.2 !important;
  stroke: currentColor !important;
  fill: none !important;
  stroke-linecap: round !important;
  stroke-linejoin: round !important;
  transition: transform 0.2s ease !important;
}

.dock-tab.active .dock-svg {
  transform: translateY(-1px) !important;
}

.dock-label {
  font-family: 'Cairo', system-ui, sans-serif !important;
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  line-height: 1 !important;
}

/* Center Hero Elevated FAB (Speedometer / Exam) */
.hero-center-tab {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-decoration: none !important;
  margin-top: -24px !important;
  position: relative !important;
  z-index: 10 !important;
  gap: 3px !important;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  -webkit-tap-highlight-color: transparent !important;
}

.hero-center-tab:active {
  transform: scale(0.92) !important;
}

.hero-fab {
  width: 52px !important;
  height: 52px !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #075985 100%) !important;
  border: 3.5px solid #090D16 !important;
  box-shadow: 0 8px 24px rgba(2, 132, 199, 0.55), inset 0 1px 2px rgba(255, 255, 255, 0.35) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  color: #FFFFFF !important;
  position: relative !important;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}

html.light .hero-fab {
  border-color: #E2E8F0 !important;
  background: linear-gradient(135deg, #0284C7 0%, #0284C7 100%) !important;
  box-shadow: 0 8px 24px rgba(2, 132, 199, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
}

.hero-fab::after {
  content: '' !important;
  position: absolute !important;
  inset: -3.5px !important;
  border-radius: 50% !important;
  background: conic-gradient(from 0deg, #009246 0deg 120deg, #FFFFFF 120deg 240deg, #CE2B37 240deg 360deg) !important;
  z-index: -1 !important;
  opacity: 0.65 !important;
}

.hero-fab-svg {
  width: 25px !important;
  height: 25px !important;
  stroke-width: 2.2 !important;
  stroke: currentColor !important;
  fill: none !important;
  stroke-linecap: round !important;
  stroke-linejoin: round !important;
}

.hero-label {
  font-family: 'Cairo', system-ui, sans-serif !important;
  font-size: 0.68rem !important;
  font-weight: 800 !important;
  color: #38BDF8 !important;
  line-height: 1 !important;
}

html.light .hero-label {
  color: #0284C7 !important;
}

/* Red Error Badge */
.dock-badge {
  position: absolute !important;
  top: -3px !important;
  left: -8px !important;
  background: #EF4444 !important;
  color: #FFFFFF !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.58rem !important;
  font-weight: 800 !important;
  padding: 0 5px !important;
  height: 15px !important;
  border-radius: 99px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.6) !important;
  border: 1.5px solid #0F172A !important;
  z-index: 5 !important;
}

html.light .dock-badge {
  border-color: #FFFFFF !important;
}

/* ==========================================================================
   STREAMLINED FOOTER & STANDARDS / PRIVACY STYLES
   ========================================================================== */
.footer-brand-stats-inline {
  display: flex !important;
  align-items: center !important;
  flex-wrap: wrap !important;
  gap: 8px !important;
  font-size: 0.82rem !important;
  color: #94A3B8 !important;
  margin-top: 10px !important;
  margin-bottom: 14px !important;
  line-height: 1.6 !important;
}

html.light .footer-brand-stats-inline {
  color: #64748B !important;
}

.footer-standards-block {
  margin-top: 12px !important;
  padding-top: 12px !important;
  border-top: 1px dashed rgba(255, 255, 255, 0.1) !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 5px !important;
}

html.light .footer-standards-block {
  border-top-color: rgba(15, 23, 42, 0.1) !important;
}

.footer-standards-title {
  font-size: 0.84rem !important;
  font-weight: 800 !important;
  color: #38BDF8 !important;
}

html.light .footer-standards-title {
  color: #0284C7 !important;
}

.footer-standards-desc {
  font-size: 0.74rem !important;
  color: #94A3B8 !important;
  line-height: 1.5 !important;
  margin: 0 !important;
}

html.light .footer-standards-desc {
  color: #64748B !important;
}

.footer-official-badge {
  font-family: 'JetBrains Mono', system-ui, sans-serif !important;
  font-size: 0.72rem !important;
  color: #64748B !important;
  letter-spacing: 0.2px !important;
  margin-top: 2px !important;
}

html.light .footer-official-badge {
  color: #475569 !important;
}
"""

tm += '\n' + hybrid_css

with open(tm_path, 'w', encoding='utf-8') as f:
    f.write(tm)

print("SUCCESS: Applied Hybrid Dock and Footer CSS to theme-modes.css")

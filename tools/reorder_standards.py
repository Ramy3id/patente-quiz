import sys

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

old_block = """            <!-- العمود 1: الشعار ورؤية المنصة والإحصائيات والمعايير -->
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
            </div>"""

new_block = """            <!-- العمود 1: الشعار ورؤية المنصة والإحصائيات -->
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

            <!-- العمود 4: المعايير والخصوصية (بعد المعامل والتدريب) -->
            <div class="footer-col footer-col-standards">
              <h4 class="footer-col-title">⚖️ المعايير والخصوصية</h4>
              <p class="footer-standards-desc">
                حماية البيانات مطابقة للائحة الأوروبية EU 2016/679 (GDPR). يتم حفظ التقدم في متصفحك محلياً بشكل آمن دون تتبع إعلاني خارجي.
              </p>
              <div class="footer-official-badge">Ministero delle Infrastrutture e dei Trasporti</div>
            </div>"""

nav_norm = nav.replace('\r\n', '\n')
old_block_norm = old_block.replace('\r\n', '\n')
new_block_norm = new_block.replace('\r\n', '\n')

if old_block_norm in nav_norm:
    nav_norm = nav_norm.replace(old_block_norm, new_block_norm, 1)
    with open(nav_path, 'w', encoding='utf-8') as f:
        f.write(nav_norm)
    print("SUCCESS: Moved Standards & Privacy after Labs & Training in unified-nav.js")
else:
    print("WARNING: old_block not found!")

# Update theme-modes.css for footer-col-standards
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

standards_css = """
.footer-col-standards .footer-standards-desc {
  font-size: 0.78rem !important;
  color: #94A3B8 !important;
  line-height: 1.6 !important;
  margin: 0 0 10px 0 !important;
}

html.light .footer-col-standards .footer-standards-desc {
  color: #64748B !important;
}

.footer-col-standards .footer-official-badge {
  font-family: 'JetBrains Mono', system-ui, sans-serif !important;
  font-size: 0.74rem !important;
  font-weight: 700 !important;
  color: #38BDF8 !important;
  letter-spacing: 0.2px !important;
}

html.light .footer-col-standards .footer-official-badge {
  color: #0284C7 !important;
}
"""

tm += '\n' + standards_css

with open(tm_path, 'w', encoding='utf-8') as f:
    f.write(tm)

print("SUCCESS: Updated theme-modes.css with footer-col-standards rules")

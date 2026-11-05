import sys
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# 1. Replace mobile header buttons 👤 and 🔍 with SVG_ICONS
nav = nav.replace(
    '<button class="nav-mobile-btn" id="btnOpenMobileAuth" title="تسجيل الدخول أو عرض الملف الشخصي" aria-label="حساب المستخدم">\n            <span style="font-size:1.15rem;">👤</span>\n          </button>',
    '<button class="nav-mobile-btn" id="btnOpenMobileAuth" title="تسجيل الدخول أو عرض الملف الشخصي" aria-label="حساب المستخدم">\n            <span class="btn-svg-wrap" style="display:inline-flex;align-items:center;justify-content:center;">${SVG_ICONS.user}</span>\n          </button>'
)

nav = nav.replace(
    '<button class="nav-mobile-btn" id="btnOpenMobileSearch" title="بحث فوري [Ctrl + K]" aria-label="بحث سريع">\n            <span style="font-size:1.15rem;">🔍</span>\n          </button>',
    '<button class="nav-mobile-btn" id="btnOpenMobileSearch" title="بحث فوري [Ctrl + K]" aria-label="بحث سريع">\n            <span class="btn-svg-wrap" style="display:inline-flex;align-items:center;justify-content:center;">${SVG_ICONS.search}</span>\n          </button>'
)

# 2. Fix search category labels
nav = nav.replace("categoryLabel: '📚 الأبواب الرسمية'", "categoryLabel: 'الأبواب الرسمية'")
nav = nav.replace("categoryLabel: '🔬 المعامل والأدوات'", "categoryLabel: 'المعامل والأدوات'")
nav = nav.replace("categoryLabel: '🔤 مصطلحات وفخاخ هامة'", "categoryLabel: 'المصطلحات والفخاخ'")

# 3. Fix tool icons in buildSearchDatabase
tool_icon_map = {
    "icon: '⚠️'": "icon: SVG_ICONS.shieldAlert",
    "icon: '⏱️'": "icon: SVG_ICONS.timer",
    "icon: '🔄'": "icon: SVG_ICONS.repeat",
    "icon: '🎯'": "icon: SVG_ICONS.crosshair",
    "icon: '📏'": "icon: SVG_ICONS.ruler",
    "icon: '🗂️'": "icon: SVG_ICONS.cards",
    "icon: '🎮'": "icon: SVG_ICONS.gamepad",
    "icon: '💎'": "icon: SVG_ICONS.gem",
    "icon: '🚑'": "icon: SVG_ICONS.ambulance",
    "icon: '📅'": "icon: SVG_ICONS.calendar",
    "icon: '📊'": "icon: SVG_ICONS.chart",
    "icon: '⚡'": "icon: SVG_ICONS.zap",
    "icon: '📖'": "icon: SVG_ICONS.book"
}
for old_i, new_i in tool_icon_map.items():
    nav = nav.replace(old_i, new_i)

# 4. In renderSearchResults: replace search empty state 🔍 and fallback
nav = nav.replace(
    '<span style="font-size:2rem; display:block; margin-bottom:8px;">🔍</span>',
    '<span style="font-size:1.8rem; display:inline-flex; justify-content:center; margin-bottom:8px;">${SVG_ICONS.search}</span>'
)

nav = nav.replace(
    "${item.type === 'chapter' ? item.badge.replace('Cap. ', '') : (item.icon || '🔬')}",
    "${item.type === 'chapter' ? item.badge.replace('Cap. ', '') : (item.icon || SVG_ICONS.flask)}"
)

# 5. Fix BiDi text wrap and typography in footer
nav = nav.replace(
    'وفق كود المرور الإيطالي (Codice della Strada).',
    'وفق كود المرور الإيطالي <bdi dir="ltr">(Codice della Strada)</bdi>.'
)

nav = nav.replace(
    '<span>25 باباً رسمياً</span> • <span>7,139 سؤالاً معتمداً</span> • <span>متوافق مع الهواتف وPWA</span>',
    '<span>25 باباً معتمداً</span> • <span>7,139 سؤالاً رسمياً</span> • <span>تطبيق ويب تقدمي (PWA) أوفلاين</span>'
)

nav = nav.replace(
    'حماية البيانات مطابقة للائحة الأوروبية EU 2016/679 (GDPR). يتم حفظ التقدم في متصفحك محلياً بشكل آمن دون تتبع إعلاني خارجي.',
    'حماية البيانات مطابقة للائحة الأوروبية <bdi dir="ltr">EU 2016/679 (GDPR)</bdi>. يتم حفظ التقدم في متصفحك محلياً بشكل آمن دون تتبع إعلاني خارجي.'
)

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

print('SUCCESS: Updated unified-nav.js with clean SVGs, BiDi fix, and search icons.')

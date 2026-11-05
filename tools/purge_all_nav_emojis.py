import sys

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# Add missing SVG icons to SVG_ICONS object if not present
missing_svgs = """    sun: '<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>',
    moon: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>',
    checkCircle: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
    lightbulb: '<svg class="ui-svg" viewBox="0 0 24 24"><line x1="9" y1="18" x2="15" y2="18"></line><line x1="10" y1="22" x2="14" y2="22"></line><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"></path></svg>',"""

if 'sun:' not in nav:
    nav = nav.replace("    soundOff:", missing_svgs + "\n    soundOff:")

# Replacements in templates
replacements = [
    # Top desktop tabs
    ('<span class="tab-icon">📖</span>', '<span class="tab-icon">${SVG_ICONS.book}</span>'),
    ('<span class="tab-icon">🔬</span>', '<span class="tab-icon">${SVG_ICONS.flask}</span>'),
    ('<span class="tab-icon">🎮</span>', '<span class="tab-icon">${SVG_ICONS.gamepad}</span>'),
    ('<span class="tab-icon">📊</span>', '<span class="tab-icon">${SVG_ICONS.chart}</span>'),
    ('<span class="btn-icon">📚</span>', '<span class="btn-icon">${SVG_ICONS.book}</span>'),
    
    # Megamenu and search
    ('<span class="input-search-icon">🔍</span>', '<span class="input-search-icon">${SVG_ICONS.search}</span>'),
    ('<span class="bottombar-hint">💡', '<span class="bottombar-hint">${SVG_ICONS.lightbulb}'),
    ('📊 عرض لوحة الإنجاز العامة', '${SVG_ICONS.chart} عرض لوحة الإنجاز العامة'),
    
    # Question / Guide pills
    ('<span>📝 أسئلة</span>', '<span>${SVG_ICONS.notes} أسئلة</span>'),
    ('<span>📖 شرح</span>', '<span>${SVG_ICONS.book} شرح</span>'),
    ('✅ 100%', '${SVG_ICONS.checkCircle} 100%'),
    ('✅ مكتمل', '${SVG_ICONS.checkCircle} مكتمل'),
    
    # Theme icons
    ('<span class="theme-icon-span">☀️</span>', '<span class="theme-icon-span">${SVG_ICONS.sun}</span>'),
    
    # Drawer shortcuts
    ('<span>🎯</span>', '<span>${SVG_ICONS.crosshair}</span>'),
    ('<span>🔍</span>', '<span>${SVG_ICONS.search}</span>'),
    ('<span style="font-size:1.15rem;">📚</span>', '<span style="display:inline-flex;">${SVG_ICONS.book}</span>'),
    
    # Badges
    ("badge: '💡'", "badge: 'مهم'"),
]

for old_s, new_s in replacements:
    nav = nav.replace(old_s, new_s)

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

print('SUCCESS: Purged all emojis from unified-nav.js templates.')

import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update Capitoli_Divisi/index.html
index_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace hero & bento badges
html = html.replace('<span class="portal-badge-live">🟢 بنك الأسئلة المعتمد 2026</span>', '<span class="portal-badge-live"><span class="badge-dot-live"></span> بنك الأسئلة المعتمد 2026</span>')
html = html.replace('<span class="btn-ico">⏱️</span>', '<span class="btn-ico"><svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"></circle><path d="M12 9v4l2.5 2.5"></path><path d="M10 2h4"></path></svg></span>')
html = html.replace('<span class="bento-spark-badge">⚡</span>', '<span class="bento-spark-badge"><svg class="ui-svg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg></span>')

# Replace the 13 Bento Tool Icons with clean Lucide SVGs
bento_replacements = [
    ('>📅</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg></div>'),
    ('>⏱️</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"></circle><path d="M12 9v4l2.5 2.5"></path><path d="M10 2h4"></path></svg></div>'),
    ('>🎯</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="3" x2="12" y2="7"></line><line x1="12" y1="17" x2="12" y2="21"></line><line x1="3" y1="12" x2="7" y2="12"></line><line x1="17" y1="12" x2="21" y2="12"></line></svg></div>'),
    ('>🔄</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path></svg></div>'),
    ('>📐</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><path d="M2 12l10-10 10 10-10 10z"></path><line x1="6" y1="8" x2="8" y2="6"></line><line x1="10" y1="12" x2="12" y2="10"></line><line x1="14" y1="16" x2="16" y2="14"></line></svg></div>'),
    ('>📖</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg></div>'),
    ('>🎮</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="6"></rect><line x1="6" y1="12" x2="10" y2="12"></line><line x1="8" y1="10" x2="8" y2="14"></line><line x1="15" y1="13" x2="15.01" y2="13"></line><line x1="18" y1="11" x2="18.01" y2="11"></line></svg></div>'),
    ('>🧩</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><rect x="2" y="7" width="16" height="13" rx="2"></rect><path d="M6 3h14a2 2 0 0 1 2 2v12"></path></svg></div>'),
    ('>💎</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><path d="M6 3h12l4 6-10 13L2 9z"></path><path d="M11 3L8 9l4 13 4-13-3-6"></path><line x1="2" y1="9" x2="22" y2="9"></line></svg></div>'),
    ('>🚑</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><rect x="1" y="3" width="15" height="13" rx="2"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle><line x1="8.5" y1="7" x2="8.5" y2="12"></line><line x1="6" y1="9.5" x2="11" y2="9.5"></line></svg></div>'),
    ('>🔍</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></div>'),
    ('>⚠️</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg></div>'),
    ('>🔤</div>', '><svg class="ui-svg" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg></div>'),
]

for old_b, new_b in bento_replacements:
    html = html.replace(old_b, new_b)

# Replace search input icon
html = html.replace('<span class="search-icon">🔍</span>', '<span class="search-icon"><svg class="ui-svg" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></span>')

# Replace chapter cards stats and badges
html = html.replace('<span class="stat-ico">📝</span>', '<span class="stat-ico"><svg class="ui-svg" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg></span>')
html = html.replace('<span class="stat-ico">🖼️</span>', '<span class="stat-ico"><svg class="ui-svg" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg></span>')
html = html.replace('<span>🎯 بدء المذاكرة التفاعلية</span>', '<span><svg class="ui-svg" viewBox="0 0 24 24" style="width:13px;height:13px;stroke-width:2.5;margin-left:4px;"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>بدء المذاكرة التفاعلية</span>')
html = html.replace('<span class="gate-free-badge">🟢 مفتوح مجاناً</span>', '<span class="gate-free-badge"><span class="badge-dot-live"></span> مفتوح مجاناً</span>')
html = html.replace('<span class="chapter-gated-badge">🔒 عينة 5 أسئلة</span>', '<span class="chapter-gated-badge"><svg class="ui-svg" viewBox="0 0 24 24" style="width:12px;height:12px;margin-left:4px;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>عينة 5 أسئلة</span>')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("SUCCESS: Capitoli_Divisi/index.html updated cleanly!")

# 2. Add Universal SVG Hydrator to assets/js/unified-nav.js
nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

# Add image, play, lock to SVG_ICONS if not present
if "image: '<svg class=\"ui-svg\"" not in nav:
    nav = nav.replace(
        "chevronDown: '<svg class=\"ui-svg chevron-svg\" viewBox=\"0 0 24 24\" style=\"width:12px;height:12px;\"><polyline points=\"6 9 12 15 18 9\"></polyline></svg>'",
        "chevronDown: '<svg class=\"ui-svg chevron-svg\" viewBox=\"0 0 24 24\" style=\"width:12px;height:12px;\"><polyline points=\"6 9 12 15 18 9\"></polyline></svg>',\n"
        "    image: '<svg class=\"ui-svg\" viewBox=\"0 0 24 24\"><rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\" ry=\"2\"></rect><circle cx=\"8.5\" cy=\"8.5\" r=\"1.5\"></circle><polyline points=\"21 15 16 10 5 21\"></polyline></svg>',\n"
        "    play: '<svg class=\"ui-svg\" viewBox=\"0 0 24 24\"><polygon points=\"5 3 19 12 5 21 5 3\"></polygon></svg>',\n"
        "    lock: '<svg class=\"ui-svg\" viewBox=\"0 0 24 24\"><rect x=\"3\" y=\"11\" width=\"18\" height=\"11\" rx=\"2\" ry=\"2\"></rect><path d=\"M7 11V7a5 5 0 0 1 10 0v4\"></path></svg>',\n"
        "    soundOn: '<svg class=\"ui-svg\" viewBox=\"0 0 24 24\"><polygon points=\"11 5 6 9 2 9 2 15 6 15 11 19 11 5\"></polygon><path d=\"M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07\"></path></svg>',\n"
        "    soundOff: '<svg class=\"ui-svg\" viewBox=\"0 0 24 24\"><polygon points=\"11 5 6 9 2 9 2 15 6 15 11 19 11 5\"></polygon><line x1=\"23\" y1=\"9\" x2=\"17\" y2=\"15\"></line><line x1=\"17\" y1=\"9\" x2=\"23\" y2=\"15\"></line></svg>'"
    )

# Universal Icon Hydrator function
hydrator_code = """
  // ==========================================================================
  // UNIVERSAL SVG ICON GUARDIAN (Platform-Wide Auto-Hydration)
  // Replaces all arbitrary UI emojis across ALL pages automatically
  // ==========================================================================
  function hydratePlatformIcons() {
    try {
      const emojiMap = {
        '⚡': SVG_ICONS.zap,
        '🔍': SVG_ICONS.search,
        '📅': SVG_ICONS.calendar,
        '⏱️': SVG_ICONS.timer,
        '⏱': SVG_ICONS.timer,
        '🎯': SVG_ICONS.crosshair,
        '🔄': SVG_ICONS.repeat,
        '📐': SVG_ICONS.ruler,
        '📏': SVG_ICONS.ruler,
        '📖': SVG_ICONS.book,
        '📚': SVG_ICONS.book,
        '🎮': SVG_ICONS.gamepad,
        '🧩': SVG_ICONS.cards,
        '🗂️': SVG_ICONS.cards,
        '🗂': SVG_ICONS.cards,
        '💎': SVG_ICONS.gem,
        '🚑': SVG_ICONS.ambulance,
        '⚠️': SVG_ICONS.shieldAlert,
        '⚠': SVG_ICONS.shieldAlert,
        '🔤': SVG_ICONS.notes,
        '📝': SVG_ICONS.notes,
        '🖼️': SVG_ICONS.image,
        '🖼': SVG_ICONS.image,
        '📊': SVG_ICONS.chart,
        '👤': SVG_ICONS.user,
        '⚖️': SVG_ICONS.shieldCheck,
        '⚖': SVG_ICONS.shieldCheck,
        '🔒': SVG_ICONS.lock,
        '🔊': SVG_ICONS.soundOn,
        '🔇': SVG_ICONS.soundOff
      };

      // Target elements that typically host UI icons
      const selectors = [
        '.bento-icon-box', '.stat-ico', '.meta-icon', '.card-icon', '.tool-icon',
        '.btn-ico', '.bento-spark-badge', '.cat-item-icon', '.drawer-link-icon',
        '.search-icon', '.tab-icon', '.chapter-gated-badge'
      ];

      document.querySelectorAll(selectors.join(',')).forEach(el => {
        if (el.querySelector('svg')) return; // Already has SVG
        const text = el.textContent.trim();
        if (emojiMap[text]) {
          el.innerHTML = emojiMap[text];
        }
      });

      // Chapter study CTA buttons: '🎯 بدء المذاكرة التفاعلية'
      document.querySelectorAll('.btn-action-study, .btn-study, .study-btn').forEach(btn => {
        if (btn.querySelector('svg')) return;
        if (btn.textContent.includes('بدء المذاكرة') || btn.textContent.includes('🎯')) {
          btn.innerHTML = '<span>' + SVG_ICONS.play + ' ' + btn.textContent.replace('🎯', '').trim() + '</span>';
        }
      });
    } catch(err) {
      console.warn('[IconHydrator] Non-fatal hydration note:', err);
    }
  }

  // Run automatically on DOM ready and after dynamic contents
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydratePlatformIcons);
  } else {
    hydratePlatformIcons();
  }
  window.addEventListener('load', hydratePlatformIcons);
"""

anchor_init = "  function initUnifiedPortalUI() {"
if anchor_init in nav:
    nav = nav.replace(anchor_init, hydrator_code + "\n  function initUnifiedPortalUI() {", 1)
    print("SUCCESS: Injected hydratePlatformIcons into unified-nav.js")
else:
    print("WARNING: initUnifiedPortalUI anchor not found")

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav)

# 3. Add supporting CSS in assets/css/theme-modes.css
tm_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(tm_path, 'r', encoding='utf-8') as f:
    tm = f.read()

card_icons_css = """
/* Chapter Cards and Bento Tools Precision SVG Styling */
.bento-icon-box .ui-svg {
  width: 22px !important;
  height: 22px !important;
  stroke-width: 2.2 !important;
}

.stat-ico {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin-left: 3px !important;
}

.stat-ico .ui-svg {
  width: 14px !important;
  height: 14px !important;
  stroke-width: 2.2 !important;
  vertical-align: middle !important;
  color: #38BDF8 !important;
}

html.light .stat-ico .ui-svg {
  color: #0284C7 !important;
}

.btn-action-study .ui-svg {
  width: 13px !important;
  height: 13px !important;
  stroke-width: 2.5 !important;
  vertical-align: middle !important;
  margin-left: 4px !important;
}

.bento-spark-badge .ui-svg {
  width: 14px !important;
  height: 14px !important;
  stroke-width: 2.5 !important;
  color: #F59E0B !important;
}

.badge-dot-live {
  width: 7px !important;
  height: 7px !important;
  border-radius: 50% !important;
  background: #10B981 !important;
  display: inline-block !important;
  margin-left: 6px !important;
  box-shadow: 0 0 8px #10B981 !important;
}
"""

tm += '\n' + card_icons_css

with open(tm_path, 'w', encoding='utf-8') as f:
    f.write(tm)

print("SUCCESS: theme-modes.css updated with card and bento SVG rules!")

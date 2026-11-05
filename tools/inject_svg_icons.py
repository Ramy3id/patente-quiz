import sys

sys.stdout.reconfigure(encoding='utf-8')

nav_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(nav_path, 'r', encoding='utf-8') as f:
    nav = f.read()

svg_icons_def = '''  // ==========================================================================
  // UNIFIED VECTOR SVG ICON SYSTEM (Zero Emojis - 100% Consistent Lucide/SF Style)
  // ==========================================================================
  const SVG_ICONS = {
    home: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
    book: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>',
    notes: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>',
    calendar: '<svg class="ui-svg" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>',
    search: '<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
    flask: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M10 2v7.31L4.1 20.3A1 1 0 0 0 5 22h14a1 1 0 0 0 .9-1.7L14 9.31V2"></path><line x1="8.5" y1="2" x2="15.5" y2="2"></line></svg>',
    crosshair: '<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="3" x2="12" y2="7"></line><line x1="12" y1="17" x2="12" y2="21"></line><line x1="3" y1="12" x2="7" y2="12"></line><line x1="17" y1="12" x2="21" y2="12"></line></svg>',
    repeat: '<svg class="ui-svg" viewBox="0 0 24 24"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path></svg>',
    ruler: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M2 12l10-10 10 10-10 10z"></path><line x1="6" y1="8" x2="8" y2="6"></line><line x1="10" y1="12" x2="12" y2="10"></line><line x1="14" y1="16" x2="16" y2="14"></line></svg>',
    ambulance: '<svg class="ui-svg" viewBox="0 0 24 24"><rect x="1" y="3" width="15" height="13" rx="2"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle><line x1="8.5" y1="7" x2="8.5" y2="12"></line><line x1="6" y1="9.5" x2="11" y2="9.5"></line></svg>',
    timer: '<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"></circle><path d="M12 9v4l2.5 2.5"></path><path d="M10 2h4"></path></svg>',
    cards: '<svg class="ui-svg" viewBox="0 0 24 24"><rect x="2" y="7" width="16" height="13" rx="2"></rect><path d="M6 3h14a2 2 0 0 1 2 2v12"></path></svg>',
    gamepad: '<svg class="ui-svg" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="6"></rect><line x1="6" y1="12" x2="10" y2="12"></line><line x1="8" y1="10" x2="8" y2="14"></line><line x1="15" y1="13" x2="15.01" y2="13"></line><line x1="18" y1="11" x2="18.01" y2="11"></line></svg>',
    gem: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M6 3h12l4 6-10 13L2 9z"></path><path d="M11 3L8 9l4 13 4-13-3-6"></path><line x1="2" y1="9" x2="22" y2="9"></line></svg>',
    shieldAlert: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
    chart: '<svg class="ui-svg" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line><line x1="2" y1="20" x2="22" y2="20"></line></svg>',
    shieldCheck: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><polyline points="9 12 11 14 15 10"></polyline></svg>',
    user: '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>',
    zap: '<svg class="ui-svg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>',
    chevronDown: '<svg class="ui-svg chevron-svg" viewBox="0 0 24 24" style="width:12px;height:12px;"><polyline points="6 9 12 15 18 9"></polyline></svg>'
  };
'''

target = "(function () {\n  'use strict';"
replacement = target + "\n\n" + svg_icons_def

nav_norm = nav.replace('\r\n', '\n')
if target in nav_norm:
    nav_norm = nav_norm.replace(target, replacement, 1)
    with open(nav_path, 'w', encoding='utf-8') as f:
        f.write(nav_norm)
    print("SUCCESS: Injected SVG_ICONS at top of unified-nav.js")
else:
    print("Target not found")

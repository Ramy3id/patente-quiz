import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

root = r'R:\Ramy\PATENTE_PRO_APP'

# Mapping of emojis to clean vector icons / elements
replacements = [
    # Traffic light brand emoji
    ('<span style="font-size:1.25rem;">🚦</span>', '<img src="../../assets/brand/brand_logo_steering_trans.png" alt="Patente B Pro" width="26" height="26" style="width:26px;height:26px;object-fit:contain;border-radius:50%;vertical-align:middle;">'),
    ('<span>🚦</span>', '<img src="../../assets/brand/brand_logo_steering_trans.png" alt="Patente B Pro" width="26" height="26" style="width:26px;height:26px;object-fit:contain;border-radius:50%;vertical-align:middle;">'),
    
    # Old static tabs
    ('🏛️ أدلة وقواميس الشرح', 'أدلة وقواميس الشرح'),
    ('📚 بنك أسئلة الأبواب', 'بنك أسئلة الأبواب'),
    ('📖 معجم المترادفات والبدائل', 'معجم المترادفات والبدائل'),
    ('🔤 بنك كلماتي والأسئلة', 'بنك كلماتي والأسئلة'),
    ('⏱️ محاكي الامتحان', 'محاكي الامتحان'),
    ('<span>📖</span> <span>الباب', '<span>الباب'),
    
    # Chapter card badges
    ('🟢 مفتوح مجاناً', '<span class="badge-dot-live"></span> مفتوح مجاناً'),
    ('🔒 عينة 5 أسئلة', '<svg class="ui-svg" viewBox="0 0 24 24" style="width:12px;height:12px;margin-left:4px;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>عينة 5 أسئلة'),
    
    # Stats
    ('<span class="stat-ico">📝</span>', '<span class="stat-ico"><svg class="ui-svg" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg></span>'),
    ('<span class="stat-ico">🖼️</span>', '<span class="stat-ico"><svg class="ui-svg" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg></span>'),
    
    # Study buttons
    ('<span>🎯 بدء المذاكرة التفاعلية</span>', '<span><svg class="ui-svg" viewBox="0 0 24 24" style="width:13px;height:13px;stroke-width:2.5;margin-left:4px;"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>بدء المذاكرة التفاعلية</span>'),
    ('🎯 بدء المذاكرة التفاعلية', '<svg class="ui-svg" viewBox="0 0 24 24" style="width:13px;height:13px;stroke-width:2.5;margin-left:4px;"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>بدء المذاكرة التفاعلية'),
    
    # Spark badge
    ('<span class="bento-spark-badge">⚡</span>', '<span class="bento-spark-badge"><svg class="ui-svg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg></span>'),
    
    # Hero badges in index
    ('<span class="portal-badge-live">🟢 بنك الأسئلة المعتمد 2026</span>', '<span class="portal-badge-live"><span class="badge-dot-live"></span> بنك الأسئلة المعتمد 2026</span>'),
    ('<span class="btn-ico">⏱️</span>', '<span class="btn-ico"><svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"></circle><path d="M12 9v4l2.5 2.5"></path><path d="M10 2h4"></path></svg></span>')
]

count = 0
for dirpath, dirnames, filenames in os.walk(root):
    if '.git' in dirpath:
        continue
    for f in filenames:
        if f.endswith('.html'):
            p = os.path.join(dirpath, f)
            try:
                with open(p, 'r', encoding='utf-8') as file:
                    content = file.read()
                original = content
                for old_val, new_val in replacements:
                    if old_val in content:
                        content = content.replace(old_val, new_val)
                if content != original:
                    with open(p, 'w', encoding='utf-8') as file:
                        file.write(content)
                    count += 1
            except Exception as e:
                print(f'Error processing {p}: {e}')

print(f'SUCCESS: Cleaned and unified {count} HTML files across platform.')

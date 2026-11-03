import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

# 1. Fix line 962-965
old_c1 = """      /* =========================================================
         1. شريط التنقل العلوي الموحد (Unified Portal Nav)

      
      /* =========================================================
         Harmonized GDPR Cookie Banner (Adaptive Light & Dark Mode)
         ========================================================= */"""

new_c1 = """      /* =========================================================
         Harmonized GDPR Cookie Banner (Adaptive Light & Dark Mode)
         ========================================================= */"""

if old_c1 in content_norm:
    content_norm = content_norm.replace(old_c1, new_c1, 1)
    print("SUCCESS: fixed comment 1")
else:
    print("WARNING: comment 1 not found")

# 2. Fix line 1256
old_c2 = """      html.light .nav-auth-pill.logged-in {
        color: #059669 !important;
      }

         ========================================================= */
      .unified-portal-nav {"""

new_c2 = """      html.light .nav-auth-pill.logged-in {
        color: #059669 !important;
      }

      /* =========================================================
         1. شريط التنقل الموحد الرئيسي (Unified Portal Nav)
         ========================================================= */
      .unified-portal-nav {"""

if old_c2 in content_norm:
    content_norm = content_norm.replace(old_c2, new_c2, 1)
    print("SUCCESS: fixed comment 2")
else:
    print("WARNING: comment 2 not found")

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/unified-nav.js', 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("SAVED unified-nav.js")

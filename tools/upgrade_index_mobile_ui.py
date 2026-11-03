import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE_PATH = 'R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/index.html'

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# -------------------------------------------------------------
# 1. Update Bento Tools: 4 initially visible, 9 extra
# -------------------------------------------------------------
# Find the bento tools section
# Current structure has 6 tools in first .bento-grid, 7 in bento-extra-grid
# We want 4 tools in first .bento-grid, and tools 5-13 in bento-extra-grid

# Let's inspect where bentoExtraGrid starts and move tools 5 & 6 into it
bento_split_pattern = re.compile(
    r'(<!-- 4\. لوحة الجاهزية وبنك الأخطاء -->[\s\S]*?</a>\s*)'  # Tool 4
    r'(\s*<!-- 5\. معمل الأرقام والمقاييس -->[\s\S]*?<!-- 6\. معجم المترادفات والبدائل -->[\s\S]*?</a>\s*)' # Tools 5 & 6
    r'(\s*</div>\s*<!-- الشبكة الإضافية: باقي 7.*?>\s*<div class="bento-grid bento-extra-grid" id="bentoExtraGrid"[^>]*>)', # Divider
    re.IGNORECASE
)

def move_tools(m):
    tool4 = m.group(1)
    tools5_6 = m.group(2)
    # New closing of first grid and start of extra grid
    new_divider = '\n    </div>\n\n    <!-- الشبكة الإضافية: باقي 9 معامل ذكية -->\n    <div class="bento-grid bento-extra-grid" id="bentoExtraGrid" style="margin-top: 8px;">\n'
    return tool4 + new_divider + tools5_6

new_content, count = bento_split_pattern.subn(move_tools, content)
if count > 0:
    print("SUCCESS: Moved tools 5 and 6 into bentoExtraGrid (now 4 primary + 9 extra)")
    content = new_content
else:
    print("WARNING: bento_split_pattern did not match, checking if already split")

# -------------------------------------------------------------
# 2. Update toggle button text in HTML
# -------------------------------------------------------------
content = content.replace(
    'عرض باقي المعامل الذكية (7 معامل إضافية) ▾',
    'عرض باقي المعامل الذكية (9 معامل إضافية) ▾'
)
content = content.replace(
    'عرض باقي المعامل الذكية (7 معامل إضافية) &#9662;',
    'عرض باقي المعامل الذكية (9 معامل إضافية) ▾'
)

# -------------------------------------------------------------
# 3. Update toggle function to use CSS class .is-expanded
# -------------------------------------------------------------
old_toggle_func = """function toggleBentoExtraTools() {
  const extra = document.getElementById('bentoExtraGrid');
  const txt = document.getElementById('bentoToggleText');
  if (!extra) return;
  const isHidden = extra.style.display === 'none' || getComputedStyle(extra).display === 'none';
  if (isHidden) {
    extra.style.display = 'grid';
    if (txt) txt.textContent = 'إخفاء المعامل الإضافية ▴';
  } else {
    extra.style.display = 'none';
    if (txt) txt.textContent = 'عرض باقي المعامل الذكية (7 معامل إضافية) ▾';
  }
}"""

new_toggle_func = """function toggleBentoExtraTools() {
  const extra = document.getElementById('bentoExtraGrid');
  const txt = document.getElementById('bentoToggleText');
  if (!extra) return;
  const isExpanded = extra.classList.toggle('is-expanded');
  if (txt) {
    txt.textContent = isExpanded ? 'إخفاء المعامل الإضافية ▴' : 'عرض باقي المعامل الذكية (9 معامل إضافية) ▾';
  }
  if (window.soundEngine && window.soundEngine.click) {
    try { window.soundEngine.click(); } catch(e){}
  }
}"""

if old_toggle_func in content:
    content = content.replace(old_toggle_func, new_toggle_func)
    print("SUCCESS: updated toggleBentoExtraTools function")
else:
    # Try flexible replacement
    content = re.sub(
        r'function toggleBentoExtraTools\(\)\s*\{[\s\S]*?\}',
        new_toggle_func,
        content
    )
    print("REPLACED toggleBentoExtraTools via regex")

# -------------------------------------------------------------
# 4. Update CSS for Bento Extra Grid & Toggle Button
# -------------------------------------------------------------
old_bento_extra_css = """.bento-extra-grid {
    display: grid !important;
  }
  .bento-toggle-btn {
    display: none !important;
  }"""

new_bento_extra_css = """/* Default: hidden on mobile and tablet unless expanded */
.bento-extra-grid {
  display: none !important;
}
.bento-extra-grid.is-expanded {
  display: grid !important;
}

@media (min-width: 1024px) {
  .bento-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    gap: 14px !important;
  }
  .bento-extra-grid {
    display: grid !important;
  }
  .bento-toggle-btn {
    display: none !important;
  }
}"""

# -------------------------------------------------------------
# 5. Center Hero Header & Exam Button
# -------------------------------------------------------------
hero_center_css = """
/* Hero Header & Centered Exam CTA */
.ch-portal-header-content {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
  gap: 14px !important;
}
.ch-portal-title-group {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
  gap: 8px !important;
}
.ch-portal-badge-strip {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 8px !important;
  flex-wrap: wrap !important;
}
.ch-portal-heading {
  text-align: center !important;
}
.ch-portal-subtext {
  text-align: center !important;
  max-width: 500px !important;
  margin: 0 auto !important;
}
.ch-portal-quick-actions {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  width: 100% !important;
  margin-top: 4px !important;
}
.btn-portal-exam {
  margin: 0 auto !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  max-width: 320px !important;
  width: auto !important;
  padding: 0 28px !important;
  border-radius: 999px !important;
  box-shadow: 0 4px 18px rgba(37, 99, 235, 0.4) !important;
}
"""

# -------------------------------------------------------------
# 6. Responsive 2-Row Filter Chips (Zero Horizontal Scroll!)
# -------------------------------------------------------------
filter_chips_clean_css = """
/* 2-Row Symmetrical Category Filter Chips (Zero Horizontal Scroll & No Cutoff) */
.filter-chips {
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  gap: 8px !important;
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  overflow-x: visible !important;
  padding: 8px 0 12px !important;
}
@media (max-width: 480px) {
  .filter-chips {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 6px !important;
  }
}
.chip-btn {
  width: 100% !important;
  min-width: 0 !important;
  padding: 8px 4px !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  text-align: center !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  border-radius: 10px !important;
  box-sizing: border-box !important;
  min-height: 40px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
"""

# -------------------------------------------------------------
# 7. Chapter Card Internal Hierarchy & Alignment
# -------------------------------------------------------------
chapter_card_harmonized_css = """
/* Harmonized Chapter Card Hierarchy & Right Alignment */
.chapter-card {
  text-align: right !important;
  direction: rtl !important;
}
.ch-title-it {
  direction: ltr !important;
  text-align: right !important; /* Right aligned in RTL card for visual harmony */
  font-size: 0.92rem !important;
  font-weight: 600 !important;
  color: var(--text-secondary, #94A3B8) !important;
  margin-top: 4px !important;
  margin-bottom: 12px !important;
}
html.light .ch-title-it {
  color: #475569 !important;
}
.ch-title-ar {
  direction: rtl !important;
  text-align: right !important;
  font-size: 1.05rem !important;
  font-weight: 800 !important;
  color: var(--text-primary, #FFFFFF) !important;
  margin-bottom: 2px !important;
}
html.light .ch-title-ar {
  color: #0F172A !important;
}
.card-stats-row {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important; /* Aligned with title on right in RTL */
  gap: 8px !important;
  margin-bottom: 14px !important;
}
.card-actions-strip {
  border-top: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08)) !important;
  padding-top: 12px !important;
}
"""

# Append or replace in style
# We insert our upgrade styles right before </style>
if "/* Hero Header & Centered Exam CTA */" not in content:
    upgrade_bundle = (
        "\n/* === 2026 MOBILE UI UPGRADES (Bento 4-Tools, 2-Row Chips, Centered CTA, Harmonized Cards) === */\n"
        + hero_center_css
        + "\n"
        + filter_chips_clean_css
        + "\n"
        + chapter_card_harmonized_css
        + "\n"
        + """
.bento-extra-grid {
  display: none !important;
}
.bento-extra-grid.is-expanded {
  display: grid !important;
  animation: bentoFadeIn 0.25s ease-out;
}
@keyframes bentoFadeIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}
"""
    )
    content = content.replace('</style>', upgrade_bundle + '\n</style>', 1)
    print("SUCCESS: Injected upgrade bundle into <style>")

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("FILE SAVED SUCCESSFULLY")

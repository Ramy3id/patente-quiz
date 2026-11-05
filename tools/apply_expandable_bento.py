import sys

path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace button HTML
old_btn = '''    <button class="bento-toggle-btn" id="btnToggleBentoTools" onclick="toggleBentoExtraTools()">
      <span id="bentoToggleText">عرض باقي المعامل الذكية (9 معامل إضافية) ▾</span>
    </button>'''

new_btn = '''    <button class="bento-toggle-btn" id="btnToggleBentoTools" onclick="toggleBentoExtraTools()" aria-expanded="false" aria-controls="bentoExtraGrid">
      <span id="bentoToggleText">عرض باقي المعامل الذكية (9 معامل إضافية)</span>
      <svg class="ui-svg bento-chevron-svg" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </button>'''

if old_btn in text:
    text = text.replace(old_btn, new_btn)
    print('Replaced button HTML')
else:
    print('old_btn not found')

old_fn = '''function toggleBentoExtraTools() {
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
}'''

new_fn = '''function toggleBentoExtraTools() {
  const extra = document.getElementById('bentoExtraGrid');
  const btn = document.getElementById('btnToggleBentoTools');
  const txt = document.getElementById('bentoToggleText');
  if (!extra) return;
  const isExpanded = extra.classList.toggle('is-expanded');
  if (btn) {
    btn.classList.toggle('is-active', isExpanded);
    btn.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
  }
  if (txt) {
    txt.textContent = isExpanded ? 'إخفاء المعامل الإضافية' : 'عرض باقي المعامل الذكية (9 معامل إضافية)';
  }
  if (window.soundEngine && window.soundEngine.click) {
    try { window.soundEngine.click(); } catch(e){}
  }
}'''

if old_fn in text:
    text = text.replace(old_fn, new_fn)
    print('Replaced toggle function')
else:
    print('old_fn not found')

text = text.replace('V8_SOLVED_OVERLAP', 'V9_EXPANDABLE_BENTO')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated Capitoli_Divisi/index.html successfully')

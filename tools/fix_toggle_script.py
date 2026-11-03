with open('R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = """<script>
function toggleBentoExtraTools() {
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
} else {
    extra.style.display = 'none';
    if (txt) txt.textContent = 'عرض باقي المعامل الذكية (9 معامل إضافية) ▾';
  }
}
</script>"""

replacement = """<script>
function toggleBentoExtraTools() {
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
}
</script>"""

c_norm = c.replace('\r\n', '\n')
t_norm = target.replace('\r\n', '\n')
r_norm = replacement.replace('\r\n', '\n')

if t_norm in c_norm:
    c_norm = c_norm.replace(t_norm, r_norm, 1)
    with open('R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/index.html', 'w', encoding='utf-8') as f:
        f.write(c_norm)
    print("SUCCESS: Fixed toggle script syntax error")
else:
    print("ERROR: target not found")

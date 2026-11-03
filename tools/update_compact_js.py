import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# Update updateBilingualBtnUI
old_b = """function updateBilingualBtnUI() {
      const btn = document.getElementById("btnToggleBilingual");
      if (!btn || !bilingualEngine) return;
      const isEn = bilingualEngine.isEnabled();
      const txt = document.getElementById("lblBilingualText");
      if (isEn) {
        btn.classList.add("active");
        if (txt) txt.innerText = "تظليل المعاني";
      } else {
        btn.classList.remove("active");
        if (txt) txt.innerText = "تظليل المعاني";
      }
    }"""

new_b = """function updateBilingualBtnUI() {
      const btn = document.getElementById("btnToggleBilingual");
      if (!btn || !bilingualEngine) return;
      const isEn = bilingualEngine.isEnabled();
      const txt = document.getElementById("lblBilingualText");
      if (isEn) {
        btn.classList.add("active");
        if (txt) txt.innerText = "المعاني";
      } else {
        btn.classList.remove("active");
        if (txt) txt.innerText = "المعاني";
      }
    }"""

# Update updateHighlightBtnUI
old_h = """function updateHighlightBtnUI() {
      const btn = document.getElementById("btnToggleHighlight");
      if (!btn) return;
      const isHl = trapEngine ? trapEngine.isHighlightEnabled() : true;
      const txt = document.getElementById("lblHighlightText");
      const icon = document.getElementById("lblHighlightIcon");
      if (isHl) {
        btn.classList.add("active");
        if (icon) icon.innerText = "👁️";
        if (txt) txt.innerText = "تظليل الأفخاخ";
      } else {
        btn.classList.remove("active");
        if (icon) icon.innerText = "👁️‍🗨️";
        if (txt) txt.innerText = "تظليل الأفخاخ";
      }
    }"""

new_h = """function updateHighlightBtnUI() {
      const btn = document.getElementById("btnToggleHighlight");
      if (!btn) return;
      const isHl = trapEngine ? trapEngine.isHighlightEnabled() : true;
      const txt = document.getElementById("lblHighlightText");
      const icon = document.getElementById("lblHighlightIcon");
      if (isHl) {
        btn.classList.add("active");
        if (icon) icon.innerText = "👁️";
        if (txt) txt.innerText = "الأفخاخ";
      } else {
        btn.classList.remove("active");
        if (icon) icon.innerText = "👁️‍🗨️";
        if (txt) txt.innerText = "الأفخاخ";
      }
    }"""

# Update updateDecoderBtnUI
old_d = """function updateDecoderBtnUI() {
      const btn = document.getElementById("btnToggleDecoder");
      if (!btn || !window.questionDecoder) return;
      const isEn = window.questionDecoder.isEnabled();
      const txt = document.getElementById("lblDecoderText");
      if (isEn) {
        btn.classList.add("active");
        if (txt) txt.innerText = "مفكك الـ 3 كتل";
      } else {
        btn.classList.remove("active");
        if (txt) txt.innerText = "مفكك الـ 3 كتل";
      }
    }"""

new_d = """function updateDecoderBtnUI() {
      const btn = document.getElementById("btnToggleDecoder");
      if (!btn || !window.questionDecoder) return;
      const isEn = window.questionDecoder.isEnabled();
      const txt = document.getElementById("lblDecoderText");
      if (isEn) {
        btn.classList.add("active");
        if (txt) txt.innerText = "الـ 3 كتل";
      } else {
        btn.classList.remove("active");
        if (txt) txt.innerText = "الـ 3 كتل";
      }
    }"""

if '\r\n' in content:
    old_b = old_b.replace('\n', '\r\n')
    new_b = new_b.replace('\n', '\r\n')
    old_h = old_h.replace('\n', '\r\n')
    new_h = new_h.replace('\n', '\r\n')
    old_d = old_d.replace('\n', '\r\n')
    new_d = new_d.replace('\n', '\r\n')

if old_b in content:
    content = content.replace(old_b, new_b, 1)
    print("Updated bilingual UI fn")

if old_h in content:
    content = content.replace(old_h, new_h, 1)
    print("Updated highlight UI fn")

if old_d in content:
    content = content.replace(old_d, new_d, 1)
    print("Updated decoder UI fn")

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("Updated JS compact labels!")

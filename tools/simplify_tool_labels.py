import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# Replace updateBilingualBtnUI
old_bilingual_ui = """    function updateBilingualBtnUI() {
      const btn = document.getElementById("btnToggleBilingual");
      if (!btn || !bilingualEngine) return;
      const isEn = bilingualEngine.isEnabled();
      if (isEn) {
        btn.classList.add("active");
        btn.style.color = "var(--tr-cyan)";
        btn.style.borderColor = "var(--tr-cyan)";
        const txt = document.getElementById("lblBilingualText");
        if (txt) txt.innerText = "تظليل المعاني: مفعل";
      } else {
        btn.classList.remove("active");
        btn.style.color = "var(--tr-text-sub)";
        btn.style.borderColor = "var(--tr-border)";
        const txt = document.getElementById("lblBilingualText");
        if (txt) txt.innerText = "تظليل المعاني: معطل";
      }
    }"""

new_bilingual_ui = """    function updateBilingualBtnUI() {
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

# Replace updateHighlightBtnUI
old_highlight_ui = """    function updateHighlightBtnUI() {
      const btn = document.getElementById("btnToggleHighlight");
      if (!btn) return;
      const isHl = trapEngine ? trapEngine.isHighlightEnabled() : true;
      if (isHl) {
        btn.classList.add("active");
        document.getElementById("lblHighlightIcon").innerText = "👁️";
        document.getElementById("lblHighlightText").innerText = "تظليل الأفخاخ: مفعل";
      } else {
        btn.classList.remove("active");
        document.getElementById("lblHighlightIcon").innerText = "👁️‍🗨️";
        document.getElementById("lblHighlightText").innerText = "تظليل الأفخاخ: معطل";
      }
    }"""

new_highlight_ui = """    function updateHighlightBtnUI() {
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

# Replace updateDecoderBtnUI
old_decoder_ui = """    function updateDecoderBtnUI() {
      const btn = document.getElementById("btnToggleDecoder");
      if (!btn || !window.questionDecoder) return;
      const isEn = window.questionDecoder.isEnabled();
      const txt = document.getElementById("lblDecoderText");
      if (isEn) {
        btn.classList.add("active");
        btn.style.color = "var(--tr-amber)";
        btn.style.borderColor = "var(--tr-amber)";
        if (txt) txt.innerText = "مفكك الـ 3 كتل: مفعل";
      } else {
        btn.classList.remove("active");
        btn.style.color = "var(--tr-text-sub)";
        btn.style.borderColor = "var(--tr-border)";
        if (txt) txt.innerText = "مفكك الـ 3 كتل: معطل";
      }
    }"""

new_decoder_ui = """    function updateDecoderBtnUI() {
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

if '\r\n' in content:
    old_bilingual_ui = old_bilingual_ui.replace('\n', '\r\n')
    new_bilingual_ui = new_bilingual_ui.replace('\n', '\r\n')
    old_highlight_ui = old_highlight_ui.replace('\n', '\r\n')
    new_highlight_ui = new_highlight_ui.replace('\n', '\r\n')
    old_decoder_ui = old_decoder_ui.replace('\n', '\r\n')
    new_decoder_ui = new_decoder_ui.replace('\n', '\r\n')

assert old_bilingual_ui in content, "old_bilingual_ui not found"
content = content.replace(old_bilingual_ui, new_bilingual_ui, 1)

assert old_highlight_ui in content, "old_highlight_ui not found"
content = content.replace(old_highlight_ui, new_highlight_ui, 1)

assert old_decoder_ui in content, "old_decoder_ui not found"
content = content.replace(old_decoder_ui, new_decoder_ui, 1)

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("Simplified tool labels applied!")

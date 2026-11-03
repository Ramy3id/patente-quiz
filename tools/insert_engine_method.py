with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    text = f.read()

method = '''    toggleExtraSubtopics() {
      if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
      this.extraSubtopicsExpanded = !this.extraSubtopicsExpanded;
      const container = document.getElementById('extraSubtopicsContainer');
      const txt = document.getElementById('extraSubtopicsToggleText');
      if (container) {
        container.classList.toggle('is-expanded', this.extraSubtopicsExpanded);
      }
      if (txt) {
        const groupKeys = Object.keys(this.groups || {});
        const remCount = Math.max(0, groupKeys.length - 4);
        txt.textContent = this.extraSubtopicsExpanded 
          ? 'إخفاء الأجزاء الإضافية ▴' 
          : `عرض باقي الأجزاء (${remCount} أجزاء إضافية) ▾`;
      }
    },

    bindGlobals() {'''

text = text.replace('bindGlobals() {', method, 1)

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Inserted method toggleExtraSubtopics successfully")

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

engine_file = r'R:\Ramy\PATENTE_PRO_APP\assets\js\modular-chapter-engine.js'
with open(engine_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the broken window.toggleExtraSubtopics block
broken_snippet = '''window.toggleExtraSubtopics = function() {
  if (window.soundEngine && window.soundEngine.click) window.soundEngine.click();
  const engine = window.ModularChapterEngine;
  if (!engine) return;
  engine.extraSubtopicsExpanded = !engine.extraSubtopicsExpanded;
  const container = document.getElementById('extraSubtopicsContainer');
  const txt = document.getElementById('extraSubtopicsToggleText');
  if (container) {
    container.classList.toggle('is-expanded', engine.extraSubtopicsExpanded);
  }
  if (txt) {
    const groupKeys = Object.keys(engine.groups || {});
    const remCount = Math.max(0, groupKeys.length - 4);
    txt.textContent = engine.extraSubtopicsExpanded 
      ? 'إخفاء الأجزاء الإضافية ▴' 
      : `عرض باقي الأجزاء (${remCount} أجزاء إضافية) ▾`;
  }
};'''

if broken_snippet in text:
    text = text.replace(broken_snippet, '')
    print("Removed broken snippet")

# Add method inside ModularChapterEngine
method_code = '''    toggleExtraSubtopics() {
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
'''

if 'toggleExtraSubtopics()' not in text:
    idx_bind = text.find('bindGlobals() {')
    if idx_bind != -1:
        text = text[:idx_bind] + method_code + '\n    ' + text[idx_bind:]
        print("Added toggleExtraSubtopics method to ModularChapterEngine")

# Add binding inside bindGlobals
binding_target = 'window.selectSubtopicFilter = (key) => self.selectSubtopicFilter(key);'
new_binding = '''window.selectSubtopicFilter = (key) => self.selectSubtopicFilter(key);
      window.toggleExtraSubtopics = () => self.toggleExtraSubtopics();'''

if binding_target in text and 'window.toggleExtraSubtopics =' not in text:
    text = text.replace(binding_target, new_binding, 1)
    print("Added window.toggleExtraSubtopics binding to bindGlobals")

with open(engine_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved modular-chapter-engine.js")

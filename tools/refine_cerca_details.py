import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update title CSS and HTML
old_title_html = '<h1 class="cq-title">🔍 محرك البحث الوزاري الفوري (Cerca Quiz)</h1>'
new_title_html = """<h1 class="cq-title">
        <span>🔍 محرك البحث الوزاري الفوري</span>
        <span class="cq-title-it">Cerca Quiz Ministeriale</span>
      </h1>"""

old_title_css = """.cq-title {
      font-size: clamp(1.8rem, 4vw, 2.7rem);
      font-weight: 900;
      letter-spacing: -0.5px;
      margin-bottom: 10px;
      background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 60%, #818CF8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }"""

new_title_css = """.cq-title {
      font-size: clamp(1.4rem, 4vw, 2.4rem);
      font-weight: 900;
      letter-spacing: -0.5px;
      margin-bottom: 10px;
      background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 60%, #818CF8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      line-height: 1.25;
    }

    .cq-title-it {
      display: block;
      font-size: clamp(0.85rem, 2.5vw, 1rem);
      font-weight: 700;
      color: var(--cq-cyan);
      font-family: 'Plus Jakarta Sans', sans-serif;
      direction: ltr;
      margin-top: 4px;
      letter-spacing: 0.5px;
      -webkit-text-fill-color: var(--cq-cyan);
    }
    html.light .cq-title-it {
      color: #0284C7;
      -webkit-text-fill-color: #0284C7;
    }"""

# 2. Update quick pills HTML and CSS
old_pills_html = """        <!-- شارات سريعة للأكثر تداولاً (نقرة واحدة) -->
        <div class="cq-quick-pills-row">
          <button class="cq-quick-pill" onclick="setSearchTerm('sorpasso in curva')">sorpasso in curva</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('frizione')">frizione</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('sempre')">sempre</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('distanza di sicurezza')">distanza</button>
        </div>"""

new_pills_html = """        <!-- شارات سريعة للأكثر تداولاً (نقرة واحدة) -->
        <div class="cq-quick-pills-row">
          <button class="cq-quick-pill" onclick="setSearchTerm('frizione')">frizione (الدبرياج)</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('sempre')">sempre (دائماً)</button>
          <button class="cq-quick-pill" onclick="setSearchTerm('sorpasso')">sorpasso (التجاوز)</button>
        </div>"""

old_pills_css = """    /* Quick Badges */
    .cq-quick-pills-row {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }"""

new_pills_css = """    /* Quick Badges */
    .cq-quick-pills-row {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      flex-wrap: nowrap;
      overflow-x: auto;
      padding: 2px 0;
      scrollbar-width: none;
    }
    .cq-quick-pills-row::-webkit-scrollbar {
      display: none;
    }"""

content_norm = content.replace('\r\n', '\n')

content_norm = content_norm.replace(old_title_html.replace('\r\n', '\n'), new_title_html.replace('\r\n', '\n'))
content_norm = content_norm.replace(old_title_css.replace('\r\n', '\n'), new_title_css.replace('\r\n', '\n'))
content_norm = content_norm.replace(old_pills_html.replace('\r\n', '\n'), new_pills_html.replace('\r\n', '\n'))
content_norm = content_norm.replace(old_pills_css.replace('\r\n', '\n'), new_pills_css.replace('\r\n', '\n'))

if '\r\n' in content:
    final_content = content_norm.replace('\n', '\r\n')
else:
    final_content = content_norm

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Applied final refinements!")

# 1. Update assets/css/theme-modes.css
with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

target_css = '''  .chapter-card {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: var(--card-radius) !important;
    padding: 16px 18px !important;
    box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    gap: 12px !important;
    transition: transform var(--anim-duration-base) var(--spring-ease), border-color 0.2s ease, box-shadow 0.2s ease !important;
  }'''

replacement_css = '''  .chapter-card {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: var(--card-radius) !important;
    padding: 16px 18px !important;
    box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
    display: flex;
    flex-direction: column !important;
    justify-content: space-between !important;
    gap: 12px !important;
    transition: transform var(--anim-duration-base) var(--spring-ease), border-color 0.2s ease, box-shadow 0.2s ease !important;
  }
  .chapter-card.is-hidden,
  .chapter-card[hidden] {
    display: none !important;
  }'''

if target_css in css_content:
    css_content = css_content.replace(target_css, replacement_css)
    print("1. Updated theme-modes.css")
else:
    print("WARNING: target_css not found in theme-modes.css")

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

# 2. Update Capitoli_Divisi/index.html
with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

target_html = '''  window.filterChapters = function() {
    const rawQuery = document.getElementById('chapter-search').value;
    const query = normalizeSearchText(rawQuery);
    const cards = document.querySelectorAll('.chapter-card');
    let visibleCount = 0;

    cards.forEach(card => {
      const cat = card.dataset.cat;
      const searchData = normalizeSearchText(card.dataset.search || '');

      // If user is searching specifically, search across all chapters regardless of category filter
      const matchCat = (query !== '' || activeCategory === 'all' || cat === activeCategory);
      const matchQuery = (query === '' || searchData.includes(query));

      if (matchCat && matchQuery) {
        card.style.display = 'flex';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    document.getElementById('no-results-msg').style.display = (visibleCount === 0) ? 'block' : 'none';
  };'''

replacement_html = '''  window.filterChapters = function() {
    const rawQuery = document.getElementById('chapter-search').value;
    const query = normalizeSearchText(rawQuery);
    const cards = document.querySelectorAll('.chapter-card');
    let visibleCount = 0;

    cards.forEach(card => {
      const cat = card.dataset.cat;
      const searchData = normalizeSearchText(card.dataset.search || '');

      // If user is searching specifically, search across all chapters regardless of category filter
      const matchCat = (query !== '' || activeCategory === 'all' || cat === activeCategory);
      const matchQuery = (query === '' || searchData.includes(query));

      if (matchCat && matchQuery) {
        card.classList.remove('is-hidden');
        card.style.setProperty('display', 'flex', 'important');
        visibleCount++;
      } else {
        card.classList.add('is-hidden');
        card.style.setProperty('display', 'none', 'important');
      }
    });

    const noResults = document.getElementById('no-results-msg');
    if (noResults) {
      noResults.style.display = (visibleCount === 0) ? 'block' : 'none';
    }
  };'''

if target_html in html_content:
    html_content = html_content.replace(target_html, replacement_html)
    print("2. Updated filterChapters in Capitoli_Divisi/index.html")
else:
    print("WARNING: target_html not found in Capitoli_Divisi/index.html")

# Also add CSS in Capitoli_Divisi/index.html for .chapter-card.is-hidden
card_hidden_css = '''
  .chapter-card.is-hidden {
    display: none !important;
  }
'''
if '.chapter-card.is-hidden' not in html_content:
    html_content = html_content.replace('.chapter-card {', card_hidden_css + '\n  .chapter-card {', 1)
    print("3. Added .chapter-card.is-hidden CSS to Capitoli_Divisi/index.html")

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Finished applying chapter filter fixes")

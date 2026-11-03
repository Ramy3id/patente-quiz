index_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS
old_css = """/* 2-Row Symmetrical Category Filter Chips (Zero Horizontal Scroll & No Cutoff) */
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
}"""

new_css = """/* 2-Row Symmetrical Category Filter Chips (Zero Horizontal Scroll & No Cutoff) */
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
  padding: 4px 2px !important;
  height: 48px !important;
  min-height: 48px !important;
  max-height: 48px !important;
  border-radius: 12px !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 2px !important;
  line-height: 1.15 !important;
  transition: all 0.15s ease !important;
}
.chip-btn .chip-title {
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  white-space: nowrap !important;
}
.chip-btn .chip-sub {
  font-size: 0.64rem !important;
  opacity: 0.75 !important;
  font-family: 'JetBrains Mono', monospace !important;
  letter-spacing: 0.2px !important;
}"""

if old_css in text:
    text = text.replace(old_css, new_css)
    print("Replaced CSS successfully")
else:
    print("Old CSS not found (trying CRLF)")
    if old_css.replace('\n', '\r\n') in text:
        text = text.replace(old_css.replace('\n', '\r\n'), new_css.replace('\n', '\r\n'))
        print("Replaced CSS (CRLF) successfully")

# 2. Update HTML Chips
old_chips = """    <div class="filter-chips">
      <button class="chip-btn active" data-cat="all" onclick="setCategory('all')">الكل (25)</button>
      <button class="chip-btn" data-cat="segnali" onclick="setCategory('segnali')">الإشارات (02-10)</button>
      <button class="chip-btn" data-cat="norme" onclick="setCategory('norme')">القواعد والسرعة (11-13)</button>
      <button class="chip-btn" data-cat="precedenze" onclick="setCategory('precedenze')">التقاطعات والأسبقية (14-16)</button>
      <button class="chip-btn" data-cat="sicurezza" onclick="setCategory('sicurezza')">السلامة والمستندات (17-20)</button>
      <button class="chip-btn" data-cat="meccanica" onclick="setCategory('meccanica')">الميكانيكا والتأمين (21-25)</button>
    </div>"""

new_chips = """    <div class="filter-chips">
      <button class="chip-btn active" data-cat="all" onclick="setCategory('all')">
        <span class="chip-title">الكل</span>
        <span class="chip-sub">25 باباً</span>
      </button>
      <button class="chip-btn" data-cat="segnali" onclick="setCategory('segnali')">
        <span class="chip-title">الإشارات</span>
        <span class="chip-sub">02-10</span>
      </button>
      <button class="chip-btn" data-cat="norme" onclick="setCategory('norme')">
        <span class="chip-title">القواعد</span>
        <span class="chip-sub">11-13</span>
      </button>
      <button class="chip-btn" data-cat="precedenze" onclick="setCategory('precedenze')">
        <span class="chip-title">التقاطعات</span>
        <span class="chip-sub">14-16</span>
      </button>
      <button class="chip-btn" data-cat="sicurezza" onclick="setCategory('sicurezza')">
        <span class="chip-title">السلامة</span>
        <span class="chip-sub">17-20</span>
      </button>
      <button class="chip-btn" data-cat="meccanica" onclick="setCategory('meccanica')">
        <span class="chip-title">الميكانيكا</span>
        <span class="chip-sub">21-25</span>
      </button>
    </div>"""

if old_chips in text:
    text = text.replace(old_chips, new_chips)
    print("Replaced HTML Chips successfully")
else:
    print("Old HTML Chips not found (trying CRLF)")
    if old_chips.replace('\n', '\r\n') in text:
        text = text.replace(old_chips.replace('\n', '\r\n'), new_chips.replace('\n', '\r\n'))
        print("Replaced HTML Chips (CRLF) successfully")

# 3. Update JavaScript Filter Logic with Arabic Normalization
old_js = """  // Filter & Search Logic
  let activeCategory = 'all';

  window.setCategory = function(cat) {
    soundEngine.click();
    activeCategory = cat;
    document.querySelectorAll('.chip-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.cat === cat);
    });
    filterChapters();
  };

  window.filterChapters = function() {
    const query = document.getElementById('chapter-search').value.toLowerCase().trim();
    const cards = document.querySelectorAll('.chapter-card');
    let visibleCount = 0;

    cards.forEach(card => {
      const cat = card.dataset.cat;
      const searchData = card.dataset.search.toLowerCase();

      const matchCat = (activeCategory === 'all' || cat === activeCategory);
      const matchQuery = (query === '' || searchData.includes(query));

      if (matchCat && matchQuery) {
        card.style.display = 'flex';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    document.getElementById('no-results-msg').style.display = (visibleCount === 0) ? 'block' : 'none';
  };"""

new_js = """  // Arabic & Multi-language Normalization for instant, forgiving search
  function normalizeSearchText(str) {
    if (!str) return '';
    return String(str)
      .toLowerCase()
      .replace(/[أإآٱ]/g, 'ا')
      .replace(/ة/g, 'ه')
      .replace(/ى/g, 'ي')
      .replace(/[\u064B-\u065F\u0670]/g, '') // remove Arabic tashkeel
      .replace(/[^a-z0-9\u0600-\u06FF\s]/g, ' ') // strip punctuation
      .replace(/\s+/g, ' ')
      .trim();
  }

  // Filter & Search Logic
  let activeCategory = 'all';

  window.setCategory = function(cat) {
    if (window.soundEngine && typeof window.soundEngine.click === 'function') {
      soundEngine.click();
    }
    activeCategory = cat;
    document.querySelectorAll('.chip-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.cat === cat);
    });
    filterChapters();
  };

  window.filterChapters = function() {
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
  };"""

if old_js in text:
    text = text.replace(old_js, new_js)
    print("Replaced JS successfully")
else:
    print("Old JS not found (trying CRLF)")
    if old_js.replace('\n', '\r\n') in text:
        text = text.replace(old_js.replace('\n', '\r\n'), new_js.replace('\n', '\r\n'))
        print("Replaced JS (CRLF) successfully")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Finished writing Capitoli_Divisi/index.html")

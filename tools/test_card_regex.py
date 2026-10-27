import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern for card top strip
pattern = re.compile(
    r'<div class="card-top-strip">\s*'
    r'(<span class="ch-pill-num">.*?</span>)\s*'
    r'(<span class="(?:gate-free-badge|chapter-gated-badge)".*?</span>)?\s*'
    r'<div class="ch-stats-strip">\s*'
    r'<span>📝\s*(\d+)\s*Q</span>\s*'
    r'<span>🖼️\s*(\d+)\s*IMG</span>\s*'
    r'</div>\s*'
    r'</div>\s*'
    r'(<div class="ch-title-it">.*?</div>)\s*'
    r'(<div class="ch-title-ar">.*?</div>)',
    re.DOTALL
)

matches = list(pattern.finditer(text))
print(f"Matched {len(matches)} card headers perfectly!")

if matches:
    m = matches[0]
    print("Match 1:")
    print("  ch_pill:", m.group(1))
    print("  badge:", m.group(2))
    print("  q_count:", m.group(3))
    print("  img_count:", m.group(4))
    print("  title_it:", m.group(5))
    print("  title_ar:", m.group(6))

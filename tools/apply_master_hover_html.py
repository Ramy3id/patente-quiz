with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_block = """  .chapter-card {
    background: var(--bg-surface);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle);
    box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.05), 0 8px 24px -6px rgba(0,0,0,0.5);
    border-radius: 18px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    cursor: pointer;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }
  .chapter-card:hover {
    transform: translateY(-2px);
    border-color: var(--border-highlight);
    box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.1), 0 12px 30px -8px rgba(0,0,0,0.7);
  }
  .chapter-card:active {
    transform: scale(0.98);
  }
  /* Removed rogue chevron */
  html.light .chapter-card {
    background: #ffffff;
    border-color: rgba(15, 23, 42, 0.08);
    box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.06);
  }
  html.light .chapter-card:hover {
    border-color: rgba(15, 23, 42, 0.16);
    box-shadow: 0 10px 25px -4px rgba(15, 23, 42, 0.1);
  }"""

new_block = """  .chapter-card {
    background: var(--bg-surface);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    cursor: pointer;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1), 
                border-color 0.35s ease, 
                background 0.35s ease;
    will-change: transform, box-shadow;
  }"""

assert old_block in html, "old_block not found in Capitoli_Divisi/index.html"
html = html.replace(old_block, new_block)

# Bump cache version
old_v = "v=2026.11.05.V14_TOP_CURVED_ARCH_TRICOLORE"
new_v = "v=2026.11.05.V15_LUXURY_CARD_HOVER_SYSTEM"
assert old_v in html
html = html.replace(old_v, new_v)

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated Capitoli_Divisi/index.html with master luxury card hover and bumped version!")

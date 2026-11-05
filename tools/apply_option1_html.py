with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace .chapter-card block in inline styles
old_inline = """  .chapter-card {
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

new_inline = """  .chapter-card {
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
    transform: none;
    transition: box-shadow 0.24s cubic-bezier(0.16, 1, 0.3, 1), 
                border-color 0.24s ease, 
                background 0.24s ease;
  }"""

assert old_inline in html, "old_inline not found in Capitoli_Divisi/index.html"
html = html.replace(old_inline, new_inline)

# Bump version string
old_v = "v=2026.11.05.V15_LUXURY_CARD_HOVER_SYSTEM"
new_v = "v=2026.11.05.V16_LINEAR_STABLE_HOVER"
assert old_v in html
html = html.replace(old_v, new_v)

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated Capitoli_Divisi/index.html with Option 1 and bumped version to V16!")

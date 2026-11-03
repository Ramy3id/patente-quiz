import sys

with open('R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/dizionario-sinonimi.html', 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

old_card_head = """  .dict-card-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 8px;
  }
  .dict-word-main {
    font-size: 1.35rem;
    font-weight: 800;
    color: #fff;
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    letter-spacing: -0.01em;
  }
  .dict-word-ar {
    font-size: 1rem;
    font-weight: 700;
    color: #38bdf8;
    margin-top: 2px;
  }
  .dict-cat-badge {
    font-size: 0.74rem;
    font-weight: 700;
    padding: 4px 10px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 100px;
    color: #a5b4fc;
    white-space: nowrap;
  }"""

new_card_head = """  .dict-card-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 8px;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
  }
  .dict-word-main {
    font-size: 1.25rem;
    font-weight: 800;
    color: #fff;
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    letter-spacing: -0.01em;
    word-break: break-word;
  }
  .dict-word-ar {
    font-size: 0.95rem;
    font-weight: 700;
    color: #38bdf8;
    margin-top: 2px;
    word-break: break-word;
  }
  .dict-cat-badge {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 10px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 8px;
    color: #a5b4fc;
    white-space: normal;
    word-break: break-word;
    max-width: 100%;
    display: inline-block;
    box-sizing: border-box;
  }"""

if old_card_head in content_norm:
    content_norm = content_norm.replace(old_card_head, new_card_head, 1)
    print("SUCCESS: replaced dict-card-head in dizionario-sinonimi.html")
else:
    print("ERROR: old_card_head not found")

# Also check html, body
old_body = """  body {
    background-color: var(--bg-base);
    color: var(--text-primary);
    font-family: 'Plus Jakarta Sans', 'Cairo', system-ui, -apple-system, sans-serif;
    line-height: 1.5;
    min-height: 100vh;
  }"""

new_body = """  html, body {
    overflow-x: hidden !important;
    max-width: 100vw !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }
  body {
    background-color: var(--bg-base);
    color: var(--text-primary);
    font-family: 'Plus Jakarta Sans', 'Cairo', system-ui, -apple-system, sans-serif;
    line-height: 1.5;
    min-height: 100vh;
  }"""

if old_body in content_norm:
    content_norm = content_norm.replace(old_body, new_body, 1)
    print("SUCCESS: added overflow-x hidden to dizionario-sinonimi body")

with open('R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/dizionario-sinonimi.html', 'w', encoding='utf-8') as f:
    f.write(content_norm)

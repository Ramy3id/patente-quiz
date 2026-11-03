import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

old_btn_css = """    .cq-action-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--cq-text-sub);
      padding: 6px 14px;
      border-radius: 10px;
      font-size: 0.84rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      text-decoration: none;
      transition: all 0.2s ease;
    }"""

new_btn_css = """    .cq-action-btn {
      height: 38px;
      min-height: 38px;
      max-height: 38px;
      box-sizing: border-box;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--cq-text-sub);
      padding: 0 14px;
      border-radius: 10px;
      font-family: inherit;
      font-size: 0.84rem;
      font-weight: 700;
      line-height: 36px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      text-decoration: none;
      transition: all 0.2s ease;
      vertical-align: middle;
      margin: 0;
    }

    .cq-action-btn span {
      display: inline-flex;
      align-items: center;
      line-height: 1;
    }"""

content_norm = content.replace('\r\n', '\n')
old_norm = old_btn_css.replace('\r\n', '\n')
new_norm = new_btn_css.replace('\r\n', '\n')

if old_norm not in content_norm:
    print("Could not find old_btn_css!")
    sys.exit(1)

content_norm = content_norm.replace(old_norm, new_norm, 1)

if '\r\n' in content:
    final_content = content_norm.replace('\n', '\r\n')
else:
    final_content = content_norm

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Unified button heights successfully!")

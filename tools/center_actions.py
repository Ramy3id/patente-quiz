import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

old_css = """    /* Card Actions Footer */
    .cq-card-actions {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 10px;
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .cq-action-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--cq-text-sub);
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .cq-action-btn:hover {
      background: var(--cq-cyan);
      color: #0B0F19;
      border-color: var(--cq-cyan);
    }"""

new_css = """    /* Card Actions Footer */
    .cq-card-actions {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      flex-wrap: wrap;
    }

    html.light .cq-card-actions {
      border-top-color: #E2E8F0;
    }

    .cq-action-btn {
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
    }

    html.light .cq-action-btn {
      background: #F1F5F9;
      border-color: #E2E8F0;
      color: #475569;
    }

    .cq-action-btn:hover {
      background: var(--cq-cyan);
      color: #0B0F19;
      border-color: var(--cq-cyan);
      transform: translateY(-1px);
    }

    html.light .cq-action-btn:hover {
      background: #0284C7;
      color: #FFFFFF;
      border-color: #0284C7;
    }"""

content_norm = content.replace('\r\n', '\n')
old_css_norm = old_css.replace('\r\n', '\n')
new_css_norm = new_css.replace('\r\n', '\n')

if old_css_norm not in content_norm:
    print("Could not find old_css_norm!")
    sys.exit(1)

content_norm = content_norm.replace(old_css_norm, new_css_norm, 1)

if '\r\n' in content:
    final_content = content_norm.replace('\n', '\r\n')
else:
    final_content = content_norm

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Successfully centered cq-card-actions!")

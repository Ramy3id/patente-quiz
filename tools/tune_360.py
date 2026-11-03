import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Update placeholder to be shorter and more concise
old_ph = 'placeholder="ابحث بكلمة إيطالية، عربية، أو برقم السؤال..."'
new_ph = 'placeholder="ابحث بكلمة، جملة، أو برقم السؤال..."'

# Update small screen media query
old_mq = """    @media (max-width: 640px) {
      .cq-search-input {
        padding: 12px 46px 12px 42px;
        font-size: 0.94rem;
        height: 48px;
      }
      .cq-search-icon {
        right: 14px;
        font-size: 1.15rem;
      }
      .cq-shortcut-badge {
        display: none !important;
      }
      .cq-popular-row {
        flex-direction: column;
        align-items: stretch;
        gap: 6px;
      }
      .cq-popular-label {
        font-size: 0.82rem;
      }
      .cq-seg-btn {
        padding: 7px 6px;
        font-size: 0.82rem;
      }
      .cq-toggle-btn {
        font-size: 0.78rem;
        padding: 0 8px;
      }
    }"""

new_mq = """    @media (max-width: 640px) {
      .cq-search-input {
        padding: 10px 42px 10px 38px;
        font-size: 0.9rem;
        height: 46px;
      }
      .cq-search-icon {
        right: 12px;
        font-size: 1.1rem;
      }
      .cq-shortcut-badge {
        display: none !important;
      }
      .cq-popular-row {
        flex-direction: column;
        align-items: stretch;
        gap: 6px;
      }
      .cq-popular-label {
        font-size: 0.82rem;
      }
      .cq-seg-btn {
        padding: 6px 4px;
        font-size: 0.8rem;
        gap: 3px;
        white-space: nowrap;
      }
      .cq-toggle-btn {
        font-size: 0.76rem;
        padding: 0 6px;
      }
      .cq-quick-pill {
        font-size: 0.72rem;
        padding: 3px 6px;
      }
    }"""

content_norm = content.replace('\r\n', '\n')
content_norm = content_norm.replace(old_ph, new_ph)
content_norm = content_norm.replace(old_mq.replace('\r\n', '\n'), new_mq.replace('\r\n', '\n'))

if '\r\n' in content:
    final_content = content_norm.replace('\n', '\r\n')
else:
    final_content = content_norm

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Applied 360px fine-tuning!")

import re

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .exam-q-header, .exam-q-badge, .btn-flag-review to matching 26px height
header_badges_css = '''.exam-q-header {
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      min-height: 28px !important;
      margin-bottom: 4px !important;
      padding-bottom: 5px !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    html.light .exam-q-header { border-bottom-color: rgba(15, 23, 42, 0.08) !important; }

    .exam-q-badge {
      background: rgba(56, 189, 248, 0.15) !important;
      color: var(--accent-cyan) !important;
      border: 1px solid rgba(56, 189, 248, 0.3) !important;
      padding: 0 10px !important;
      border-radius: 999px !important;
      font-size: 0.76rem !important;
      font-weight: 800 !important;
      height: 26px !important;
      min-height: 26px !important;
      max-height: 26px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      box-sizing: border-box !important;
    }

    .btn-flag-review {
      background: rgba(148, 163, 184, 0.1) !important;
      border: 1px solid rgba(148, 163, 184, 0.22) !important;
      color: #64748B !important;
      padding: 0 10px !important;
      border-radius: 999px !important;
      font-size: 0.76rem !important;
      font-weight: 700 !important;
      cursor: pointer !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 5px !important;
      font-family: inherit !important;
      height: 26px !important;
      min-height: 26px !important;
      max-height: 26px !important;
      box-sizing: border-box !important;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .btn-flag-review.active {
      background: #F59E0B !important;
      border-color: #F59E0B !important;
      color: #0F172A !important;
      font-weight: 800 !important;
    }'''

content = re.sub(
    r'\.exam-q-header\s*\{[\s\S]*?\.btn-flag-review\.active\s*\{[^}]*\}',
    header_badges_css,
    content,
    count=1
)

# 2. Update .exam-media-slot to 105px
content = re.sub(
    r'\.exam-media-slot\s*\{[^}]*\}',
    '''.exam-media-slot {
      height: 105px;
      max-height: 105px;
      min-height: 105px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 2px 0 4px;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.exam-sign-frame img\s*\{[^}]*\}',
    '''.exam-sign-frame img {
      max-height: 98px;
      max-width: 220px;
      object-fit: contain;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: #FFFFFF;
      padding: 2px;
    }''',
    content,
    count=1
)

# 3. Update .exam-text-container to 195px and remove margin-top: auto on .exam-tr-wrapper
text_styles = '''.exam-text-container {
      height: 195px;
      min-height: 195px;
      max-height: 195px;
      overflow-y: hidden;
      scrollbar-width: none;
      -ms-overflow-style: none;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      margin: 2px 0 4px;
      text-align: center;
      padding: 2px 6px;
      box-sizing: border-box;
    }
    .exam-text-container::-webkit-scrollbar {
      display: none !important;
    }
    .exam-text-it {
      font-size: 0.94rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.3;
      margin: 0 0 3px;
      direction: ltr;
      text-align: center;
    }
    html.light .exam-text-it { color: #0F172A; }

    .exam-tr-wrapper {
      margin-top: 3px;
      margin-bottom: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 3px;
      width: 100%;
    }
    .btn-toggle-tr {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      height: 24px;
      min-height: 24px;
      padding: 0 10px;
      border-radius: 999px;
      font-size: 0.74rem;
      font-weight: 700;
      background: rgba(56, 189, 248, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: #0284C7;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: inherit;
    }
    html:not(.light) .btn-toggle-tr {
      background: rgba(56, 189, 248, 0.12);
      border-color: rgba(56, 189, 248, 0.3);
      color: #38BDF8;
    }
    .btn-toggle-tr.active {
      background: rgba(148, 163, 184, 0.14) !important;
      border-color: rgba(148, 163, 184, 0.3) !important;
      color: #475569 !important;
    }
    html:not(.light) .btn-toggle-tr.active {
      color: #CBD5E1 !important;
    }
    .exam-text-tr {
      font-size: 0.83rem;
      font-weight: 600;
      color: #CBD5E1;
      line-height: 1.3;
      direction: rtl;
      text-align: center;
      margin: 0;
      width: 100%;
      box-sizing: border-box;
      padding: 5px 8px;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      animation: fadeInTr 0.18s ease-out;
    }'''

content = re.sub(
    r'\.exam-text-container\s*\{[\s\S]*?\.exam-text-tr\s*\{[^}]*\}',
    text_styles,
    content,
    count=1
)

# 4. Choice buttons and nav steps
content = re.sub(
    r'\.choice-btn\s*\{[^}]*\}',
    '''.choice-btn {
      height: 46px !important;
      min-height: 46px !important;
      max-height: 46px !important;
      padding: 0 10px !important;
      font-size: 1.05rem !important;
      font-weight: 800 !important;
      border-radius: 12px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 6px !important;
      cursor: pointer !important;
      transition: all 0.15s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.exam-nav-steps\s*\{[^}]*\}',
    '''.exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 8px;
      margin-bottom: 2px;
      padding: 0;
      height: 38px;
      min-height: 38px;
      border-top: none !important;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.btn-submit-pill\s*\{[^}]*\}',
    '''.btn-submit-pill {
      height: 38px !important;
      min-height: 38px !important;
      padding: 0 12px !important;
      border-radius: 10px !important;
      background: linear-gradient(135deg, #10B981, #059669) !important;
      border: none !important;
      color: #FFFFFF !important;
      font-weight: 800 !important;
      font-size: 0.82rem !important;
      cursor: pointer !important;
      white-space: nowrap !important;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.28) !important;
      font-family: inherit !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.btn-nav-step\s*\{[^}]*padding:[^}]*\}',
    '''.btn-nav-step {
      padding: 0 12px !important;
      height: 38px !important;
      min-height: 38px !important;
      border-radius: 10px !important;
      background: rgba(255, 255, 255, 0.06) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      color: var(--text-primary) !important;
      font-weight: 700 !important;
      font-size: 0.82rem !important;
      cursor: pointer !important;
      font-family: inherit !important;
      transition: all 0.15s ease !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }''',
    content,
    count=1
)

# 5. Card padding
content = re.sub(
    r'\.exam-question-card\s*\{[^}]*background:[^}]*border-radius:[^}]*padding:[^}]*\}',
    '''.exam-question-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 10px 12px 14px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-sizing: border-box;
      margin-bottom: 6px;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.exam-question-card\s*\{\s*padding:[^;]*!important;\s*border-radius:[^;]*!important;[^}]*\}',
    '''.exam-question-card {
        padding: 10px 10px 14px !important;
        border-radius: 18px !important;
        margin-bottom: 4px !important;
      }''',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied super compact layout successfully!")

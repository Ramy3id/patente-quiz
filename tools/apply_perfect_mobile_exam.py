import re

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Hub and Switcher to be compact (36px)
hub_css = '''.exam-control-hub {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 4px 8px;
      margin-bottom: 4px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
    }
    html.light .exam-control-hub {
      background: #FFFFFF;
      border-color: rgba(15, 23, 42, 0.1);
      box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }
    .hub-primary-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      margin-bottom: 0;
    }
    .exam-skin-switcher-mini {
      display: inline-flex;
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 999px;
      padding: 2px;
      gap: 2px;
      box-sizing: border-box;
      height: 32px;
    }
    html.light .exam-skin-switcher-mini {
      background: #F1F5F9;
      border-color: rgba(15, 23, 42, 0.1);
    }
    .skin-btn-mini {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
      padding: 0 8px;
      height: 26px;
      border-radius: 999px;
      border: none;
      background: transparent;
      color: #94A3B8;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    html.light .skin-btn-mini { color: #64748B; }
    .skin-btn-mini.active {
      background: linear-gradient(135deg, #0284C7, #0369A1) !important;
      color: #FFFFFF !important;
      font-weight: 800 !important;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4) !important;
    }
    .hub-progress-badge {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 0 8px;
      height: 28px;
      border-radius: 8px;
      font-size: 0.72rem;
      color: #94A3B8;
    }
    html.light .hub-progress-badge {
      background: #F8FAFC;
      border-color: rgba(15, 23, 42, 0.08);
      color: #475569;
    }
    .hub-progress-badge strong {
      color: var(--accent-cyan);
      font-size: 0.85rem;
      font-family: 'JetBrains Mono', monospace;
    }
    html.light .hub-progress-badge strong { color: #0284C7; }
    .exam-timer-box-mini {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      font-weight: 800;
      color: #38BDF8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.25);
      padding: 0 8px;
      height: 28px;
      display: inline-flex;
      align-items: center;
      border-radius: 8px;
    }
    html.light .exam-timer-box-mini {
      color: #0284C7;
      background: #E0F2FE;
      border-color: #BAE6FD;
    }'''

content = re.sub(
    r'\.exam-control-hub\s*\{[\s\S]*?html\.light \.exam-timer-box-mini\s*\{[^}]*\}',
    hub_css,
    content,
    count=1
)

# 2. Update .exam-nav-pills-row and .q-pill
pills_css = '''.exam-nav-pills-row {
      margin-bottom: 4px;
    }
    .exam-nav-pills {
      display: flex !important;
      overflow-x: auto !important;
      flex-wrap: nowrap !important;
      padding: 2px 2px !important;
      gap: 4px !important;
      scrollbar-width: none !important;
      -webkit-overflow-scrolling: touch !important;
    }
    .exam-nav-pills::-webkit-scrollbar { display: none !important; }
    .q-pill {
      min-width: 28px !important;
      width: 28px !important;
      height: 28px !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      flex-shrink: 0 !important;
      border-radius: 7px !important;
      font-size: 0.74rem !important;
    }'''

content = re.sub(
    r'\.exam-nav-pills-row\s*\{[\s\S]*?\.q-pill\s*\{[^}]*\}',
    pills_css,
    content,
    count=1
)

# 3. Card styling: Header with 26px badge and 26px flag button
card_header_css = '''.exam-question-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 8px 10px 12px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-sizing: border-box;
      margin-bottom: 4px;
    }
    html.light .exam-question-card {
      background: #FFFFFF;
      border-color: rgba(15, 23, 42, 0.1);
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    }
    .exam-q-header {
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      min-height: 26px !important;
      height: 26px !important;
      margin-bottom: 4px !important;
      padding-bottom: 4px !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
      box-sizing: border-box !important;
    }
    html.light .exam-q-header { border-bottom-color: rgba(15, 23, 42, 0.08) !important; }
    .exam-q-badge {
      background: rgba(56, 189, 248, 0.15) !important;
      color: var(--accent-cyan) !important;
      border: 1px solid rgba(56, 189, 248, 0.3) !important;
      padding: 0 8px !important;
      border-radius: 999px !important;
      font-size: 0.74rem !important;
      font-weight: 800 !important;
      height: 24px !important;
      min-height: 24px !important;
      max-height: 24px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      box-sizing: border-box !important;
    }
    .btn-flag-review {
      background: rgba(148, 163, 184, 0.1) !important;
      border: 1px solid rgba(148, 163, 184, 0.22) !important;
      color: #64748B !important;
      padding: 0 8px !important;
      border-radius: 999px !important;
      font-size: 0.74rem !important;
      font-weight: 700 !important;
      cursor: pointer !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 4px !important;
      font-family: inherit !important;
      height: 24px !important;
      min-height: 24px !important;
      max-height: 24px !important;
      box-sizing: border-box !important;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    html.light .btn-flag-review {
      background: #F1F5F9 !important;
      border-color: #CBD5E1 !important;
      color: #475569 !important;
    }
    .btn-flag-review.active {
      background: #F59E0B !important;
      border-color: #F59E0B !important;
      color: #0F172A !important;
      font-weight: 800 !important;
    }'''

content = re.sub(
    r'\.exam-question-card\s*\{[\s\S]*?\.btn-flag-review\.active\s*\{[^}]*\}',
    card_header_css,
    content,
    count=1
)

# 4. Media Slot to 95px
media_css = '''.exam-media-slot {
      height: 95px;
      max-height: 95px;
      min-height: 95px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 2px 0;
    }
    .exam-sign-frame {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      width: 100%;
    }
    .exam-sign-frame img {
      max-height: 90px;
      max-width: 210px;
      object-fit: contain;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: #FFFFFF;
      padding: 2px;
    }
    .exam-no-img-placeholder {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px dashed rgba(255, 255, 255, 0.14);
      color: #94A3B8;
      font-size: 0.74rem;
      font-weight: 600;
    }'''

content = re.sub(
    r'\.exam-media-slot\s*\{[\s\S]*?\.exam-no-img-placeholder\s*\{[^}]*\}',
    media_css,
    content,
    count=1
)

# 5. Text container 165px, with stable translation button directly below Italian text!
text_css = '''.exam-text-container {
      height: 165px;
      min-height: 165px;
      max-height: 165px;
      overflow-y: hidden;
      scrollbar-width: none;
      -ms-overflow-style: none;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      margin: 2px 0;
      text-align: center;
      padding: 2px 6px;
      box-sizing: border-box;
    }
    .exam-text-container::-webkit-scrollbar {
      display: none !important;
    }
    .exam-text-it {
      font-size: 0.93rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.3;
      margin: 0 0 2px;
      direction: ltr;
      text-align: center;
      max-height: 68px;
    }
    html.light .exam-text-it { color: #0F172A; }

    .exam-tr-wrapper {
      margin-top: 2px;
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
      gap: 4px;
      height: 22px;
      min-height: 22px;
      padding: 0 10px;
      border-radius: 999px;
      font-size: 0.72rem;
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
      font-size: 0.82rem;
      font-weight: 600;
      color: #CBD5E1;
      line-height: 1.28;
      direction: rtl;
      text-align: center;
      margin: 0;
      width: 100%;
      box-sizing: border-box;
      padding: 4px 6px;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      animation: fadeInTr 0.15s ease-out;
    }
    html.light .exam-text-tr {
      color: #334155;
      background: #F8FAFC;
      border-color: #E2E8F0;
    }'''

content = re.sub(
    r'\.exam-text-container\s*\{[\s\S]*?html\.light \.exam-text-tr\s*\{[^}]*\}',
    text_css,
    content,
    count=1
)

# 6. Choice buttons to 44px
content = re.sub(
    r'\.choice-btn\s*\{[^}]*\}',
    '''.choice-btn {
      height: 44px !important;
      min-height: 44px !important;
      max-height: 44px !important;
      padding: 0 8px !important;
      font-size: 1.02rem !important;
      font-weight: 800 !important;
      border-radius: 10px !important;
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

# 7. Navigation steps to 36px
content = re.sub(
    r'\.exam-nav-steps\s*\{[^}]*\}',
    '''.exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      justify-content: center;
      gap: 6px;
      margin-top: 6px;
      margin-bottom: 2px;
      padding: 0;
      height: 36px;
      min-height: 36px;
      border-top: none !important;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.btn-submit-pill\s*\{[^}]*\}',
    '''.btn-submit-pill {
      height: 36px !important;
      min-height: 36px !important;
      padding: 0 10px !important;
      border-radius: 8px !important;
      background: linear-gradient(135deg, #10B981, #059669) !important;
      border: none !important;
      color: #FFFFFF !important;
      font-weight: 800 !important;
      font-size: 0.8rem !important;
      cursor: pointer !important;
      white-space: nowrap !important;
      box-shadow: 0 2px 6px rgba(16, 185, 129, 0.25) !important;
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
      padding: 0 10px !important;
      height: 36px !important;
      min-height: 36px !important;
      border-radius: 8px !important;
      background: rgba(255, 255, 255, 0.06) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      color: var(--text-primary) !important;
      font-weight: 700 !important;
      font-size: 0.8rem !important;
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

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied perfect compact layout successfully!")

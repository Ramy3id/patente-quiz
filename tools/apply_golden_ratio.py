import re

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .exam-question-card
content = re.sub(
    r'\.exam-question-card\s*\{[^}]*background:[^}]*border-radius:[^}]*padding:[^}]*\}',
    '''.exam-question-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 14px 14px 22px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-sizing: border-box;
      margin-bottom: 8px;
    }''',
    content,
    count=1
)

# In media query
content = re.sub(
    r'\.exam-question-card\s*\{\s*padding:[^;]*!important;\s*border-radius:[^;]*!important;\s*\}',
    '''.exam-question-card {
        padding: 14px 12px 22px !important;
        border-radius: 20px !important;
        margin-bottom: 6px !important;
      }''',
    content
)

# 2. Update .exam-media-slot and img
content = re.sub(
    r'\.exam-media-slot\s*\{[^}]*\}',
    '''.exam-media-slot {
      height: 125px;
      max-height: 125px;
      min-height: 125px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 2px 0 6px;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.exam-sign-frame img\s*\{[^}]*\}',
    '''.exam-sign-frame img {
      max-height: 118px;
      max-width: 250px;
      object-fit: contain;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: #FFFFFF;
      padding: 2px;
    }''',
    content,
    count=1
)

# 3. Update .exam-text-container, .exam-text-it, .exam-text-tr
content = re.sub(
    r'\.exam-text-container\s*\{[^}]*\}',
    '''.exam-text-container {
      height: 220px;
      min-height: 220px;
      max-height: 220px;
      overflow-y: hidden;
      scrollbar-width: none;
      -ms-overflow-style: none;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      margin: 2px 0 6px;
      text-align: center;
      padding: 2px 8px;
      box-sizing: border-box;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.exam-text-it\s*\{[^}]*\}',
    '''.exam-text-it {
      font-size: 0.98rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.34;
      margin: 0 0 4px;
      direction: ltr;
      text-align: center;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.exam-text-tr\s*\{[^}]*\}',
    '''.exam-text-tr {
      font-size: 0.86rem;
      font-weight: 600;
      color: #CBD5E1;
      line-height: 1.34;
      direction: rtl;
      text-align: center;
      margin: 0;
      width: 100%;
      box-sizing: border-box;
      padding: 6px 10px;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      animation: fadeInTr 0.2s ease-out;
    }''',
    content,
    count=1
)

# 4. Update .exam-choice-buttons and .choice-btn
content = re.sub(
    r'\.choice-btn\s*\{[^}]*\}',
    '''.choice-btn {
      height: 50px !important;
      min-height: 50px !important;
      max-height: 50px !important;
      padding: 0 10px !important;
      font-size: 1.08rem !important;
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

# 5. Update .exam-nav-steps, .btn-nav-step, .btn-submit-pill
content = re.sub(
    r'\.exam-nav-steps\s*\{[^}]*\}',
    '''.exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 10px;
      margin-bottom: 2px;
      padding: 0 2px;
      height: 42px;
      min-height: 42px;
      border-top: none !important;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.btn-submit-pill\s*\{[^}]*\}',
    '''.btn-submit-pill {
      height: 42px !important;
      min-height: 42px !important;
      padding: 0 14px !important;
      border-radius: 10px !important;
      background: linear-gradient(135deg, #10B981, #059669) !important;
      border: none !important;
      color: #FFFFFF !important;
      font-weight: 800 !important;
      font-size: 0.84rem !important;
      cursor: pointer !important;
      white-space: nowrap !important;
      box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3) !important;
      font-family: inherit !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }''',
    content,
    count=1
)

# 6. Top Hub padding refinement
content = re.sub(
    r'\.exam-control-hub\s*\{[^}]*\}',
    '''.exam-control-hub {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 5px 8px;
      margin-bottom: 6px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
    }''',
    content,
    count=1
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied golden ratio dimensions successfully!")

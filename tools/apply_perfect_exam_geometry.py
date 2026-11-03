import re

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .exam-question-card styling
content = re.sub(
    r'\.exam-question-card\s*\{[^}]*background:[^}]*border-radius:[^}]*padding:[^}]*\}',
    '''.exam-question-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 24px;
      padding: 18px 16px 36px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-sizing: border-box;
      margin-bottom: 14px;
    }''',
    content,
    count=1
)

# 2. Update .exam-media-slot and .exam-sign-frame img
media_pattern = r'\.exam-media-slot\s*\{[^}]*\}'
media_replacement = '''.exam-media-slot {
      height: 150px;
      max-height: 150px;
      min-height: 150px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 4px 0 8px;
    }'''
content = re.sub(media_pattern, media_replacement, content, count=1)

img_frame_pattern = r'\.exam-sign-frame img\s*\{[^}]*\}'
img_frame_replacement = '''.exam-sign-frame img {
      max-height: 140px;
      max-width: 260px;
      object-fit: contain;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: #FFFFFF;
      padding: 3px;
    }'''
content = re.sub(img_frame_pattern, img_frame_replacement, content, count=1)

# 3. Update .exam-text-container and .exam-text-tr
text_cont_pattern = r'\.exam-text-container\s*\{[^}]*\}'
text_cont_replacement = '''.exam-text-container {
      height: 280px;
      min-height: 280px;
      max-height: 280px;
      overflow-y: hidden;
      scrollbar-width: none;
      -ms-overflow-style: none;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      margin: 4px 0 8px;
      text-align: center;
      padding: 4px 8px;
      box-sizing: border-box;
    }'''
content = re.sub(text_cont_pattern, text_cont_replacement, content, count=1)

text_tr_pattern = r'\.exam-text-tr\s*\{[^}]*\}'
text_tr_replacement = '''.exam-text-tr {
      font-size: 0.9rem;
      font-weight: 600;
      color: #CBD5E1;
      line-height: 1.4;
      direction: rtl;
      text-align: center;
      margin: 0;
      width: 100%;
      box-sizing: border-box;
      padding: 8px 12px;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      animation: fadeInTr 0.2s ease-out;
    }'''
content = re.sub(text_tr_pattern, text_tr_replacement, content, count=1)

# 4. Update .exam-nav-steps and .btn-submit-pill
nav_steps_pattern = r'\.exam-nav-steps\s*\{[^}]*\}'
nav_steps_replacement = '''.exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 14px;
      margin-bottom: 4px;
      padding: 0 4px;
      height: 44px;
      min-height: 44px;
      border-top: none !important;
    }'''
content = re.sub(nav_steps_pattern, nav_steps_replacement, content, count=1)

btn_submit_pattern = r'\.btn-submit-pill\s*\{[^}]*\}'
btn_submit_replacement = '''.btn-submit-pill {
      height: 44px !important;
      min-height: 44px !important;
      padding: 0 16px !important;
      border-radius: 12px !important;
      background: linear-gradient(135deg, #10B981, #059669) !important;
      border: none !important;
      color: #FFFFFF !important;
      font-weight: 800 !important;
      font-size: 0.86rem !important;
      cursor: pointer !important;
      white-space: nowrap !important;
      box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3) !important;
      font-family: inherit !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }'''
content = re.sub(btn_submit_pattern, btn_submit_replacement, content, count=1)

# 5. Update media query max-width: 640px for .exam-question-card
content = re.sub(
    r'\.exam-question-card\s*\{\s*padding:[^;]*!important;\s*border-radius:[^;]*!important;\s*\}',
    '''.exam-question-card {
        padding: 16px 14px 34px !important;
        border-radius: 24px !important;
      }''',
    content
)

# 6. Update Official Motorizzazione heights
content = re.sub(
    r'\.moto-sign-panel\s*\{[^}]*\}',
    '''.moto-sign-panel {
      background: #0F172A;
      border: 2px solid #334155;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 4px;
      height: 125px;
      min-height: 125px;
      max-height: 125px;
      box-sizing: border-box;
    }''',
    content
)

content = re.sub(
    r'\.moto-sign-img\s*\{[^}]*\}',
    '''.moto-sign-img {
      max-height: 115px;
      max-width: 250px;
      object-fit: contain;
    }''',
    content
)

content = re.sub(
    r'\.moto-text-italian\s*\{[^}]*\}',
    '''.moto-text-italian {
      height: 115px;
      min-height: 115px;
      max-height: 115px;
      overflow-y: auto;
      font-size: 1.05rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.35;
      margin-bottom: 8px;
      direction: ltr;
      text-align: left;
      scrollbar-width: none;
      -ms-overflow-style: none;
      padding: 2px 4px;
      box-sizing: border-box;
    }''',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated scheda-esame.html successfully!')

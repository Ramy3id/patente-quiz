with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean up broken "html.light \n .exam-nav-pills-row"
content = content.replace('html.light \n    .exam-nav-pills-row', '.exam-nav-pills-row')
content = content.replace('html.light\n    .exam-nav-pills-row', '.exam-nav-pills-row')

# 2. Fix html.light .moto-text-italian to have sharp dark text (#0F172A)
old_moto_text_light = '''html.light .moto-text-italian {
      height: 125px;
      min-height: 125px;
      max-height: 125px;
      overflow-y: auto;
      font-size: 1.02rem;
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
    }'''

new_moto_text_light = '''html.light .moto-text-italian {
      height: 130px;
      min-height: 130px;
      max-height: 130px;
      overflow-y: hidden;
      font-size: 1.02rem;
      font-weight: 800;
      color: #0F172A !important;
      line-height: 1.36;
      margin-bottom: 8px;
      direction: ltr;
      text-align: left;
      scrollbar-width: none;
      -ms-overflow-style: none;
      padding: 2px 4px;
      box-sizing: border-box;
    }'''

content = content.replace(old_moto_text_light, new_moto_text_light)

# Also check for any other instance of .moto-text-italian in html.light
import re
content = re.sub(
    r'html\.light\s*\.moto-text-italian\s*\{[^}]*color:\s*#FFFFFF[^}]*\}',
    new_moto_text_light,
    content
)

# 3. Enhance light mode sign panel and terminal contrast
content = re.sub(
    r'html\.light\s*\.moto-sign-panel\s*\{[^}]*\}',
    '''html.light .moto-sign-panel {
      background: #FFFFFF !important;
      border: 2px solid #CBD5E1 !important;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 4px;
      height: 140px;
      min-height: 140px;
      max-height: 140px;
      box-sizing: border-box;
    }''',
    content
)

content = re.sub(
    r'html\.light\s*\.moto-main-terminal\s*\{[^}]*\}',
    '''html.light .moto-main-terminal {
      background: #F8FAFC !important;
      border: 1px solid #E2E8F0 !important;
    }''',
    content
)

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully fixed html.light .moto-text-italian color and light contrast!')

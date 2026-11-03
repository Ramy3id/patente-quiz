import re

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update .exam-text-container to 246px
content = re.sub(
    r'\.exam-text-container\s*\{[^}]*\}',
    '''.exam-text-container {
      height: 246px;
      min-height: 246px;
      max-height: 246px;
      overflow-y: hidden;
      scrollbar-width: none;
      -ms-overflow-style: none;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      margin: 2px 0 6px;
      text-align: center;
      padding: 2px 6px;
      box-sizing: border-box;
    }''',
    content,
    count=1
)

content = re.sub(
    r'\.exam-text-it\s*\{[^}]*\}',
    '''.exam-text-it {
      font-size: 0.96rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.32;
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
      font-size: 0.85rem;
      font-weight: 600;
      color: #CBD5E1;
      line-height: 1.32;
      direction: rtl;
      text-align: center;
      margin: 0;
      width: 100%;
      box-sizing: border-box;
      padding: 5px 8px;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      animation: fadeInTr 0.2s ease-out;
    }''',
    content,
    count=1
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied 246px text container refinement!")

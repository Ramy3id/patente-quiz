with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_media_640 = '''@media (max-width: 640px) {
      .exam-portal-container {
        padding: 4px 10px 8px !important;
        margin: 4px auto 10px !important;
      }
      .exam-nav-pills {
        display: flex !important;
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        padding: 4px 2px !important;
        gap: 5px !important;
        scrollbar-width: none !important;
        -webkit-overflow-scrolling: touch !important;
        margin-bottom: 0 !important;
      }
      .exam-nav-pills::-webkit-scrollbar { display: none !important; }
      .q-pill {
        min-width: 32px !important;
        width: 32px !important;
        height: 32px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
      }
      .btn-submit-exam {
        display: none !important; /* Replaced by the integrated submit buttons */
      }
    }'''

new_media_640 = '''@media (max-width: 640px) {
      .exam-portal-container {
        padding: 4px 10px 8px !important;
        margin: 4px auto 8px !important;
      }
      .exam-control-hub {
        margin-bottom: 8px !important;
        padding: 5px 8px !important;
      }
      .exam-nav-pills-row {
        margin-bottom: 8px !important;
      }
      .exam-nav-pills {
        display: flex !important;
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        padding: 2px 2px !important;
        gap: 5px !important;
        scrollbar-width: none !important;
        -webkit-overflow-scrolling: touch !important;
        margin-bottom: 0 !important;
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
      }
      .btn-submit-exam {
        display: none !important; /* Replaced by the integrated submit buttons */
      }
    }'''

if old_media_640 in content:
    content = content.replace(old_media_640, new_media_640)
    print("Replaced exact old_media_640")
else:
    content = re.sub(
        r'@media\s*\(max-width:\s*640px\)\s*\{[\s\S]*?\.btn-submit-exam\s*\{[^}]*\}\s*\}',
        new_media_640,
        content
    )
    print("Replaced via regex")

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated media 640px successfully!")

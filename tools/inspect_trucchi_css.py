import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\trucchi-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect CSS for tr-hero, tr-stats-strip, tr-tabs-nav, tr-tab-btn
for c in ['.tr-hero', '.tr-stats-strip', '.tr-stat-item', '.tr-tabs-nav', '.tr-tab-btn']:
    pos = content.find(c)
    print(f"=== {c} at {pos} ===")
    print(content[pos:pos+400])

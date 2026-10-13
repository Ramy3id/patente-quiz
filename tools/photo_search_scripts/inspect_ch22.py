import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('interactive_pages/دليل_الباب_22_الكحول_والمخدرات_والإسعافات_الأولية.html', 'r', encoding='utf-8') as f:
    content = f.read()

print('Length of file:', len(content))

# Look for all card structures
cards = re.findall(r'<div class=["\']([^"\']*card[^"\']*)["\']', content)
print('Card classes found:', set(cards))

# Check containers and their parent/sibling headings
containers = list(re.finditer(r'<div class=["\']signal-img-container["\'][^>]*>(.*?)</div>', content, re.DOTALL))
print('Found signal-img-containers:', len(containers))
for i, match in enumerate(containers):
    start = max(0, match.start() - 300)
    end = min(len(content), match.end() + 300)
    snippet = content[start:end]
    # find nearest heading or title
    titles = re.findall(r'<h[234][^>]*>(.*?)</h[234]>', snippet, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', titles[-1]).strip() if titles else 'No heading'
    badge_content = match.group(1).strip()
    badge_clean = re.sub(r'<[^>]+>', '', badge_content).strip()
    print(f'Card {i+1}: Title: {title} | Badge: {badge_clean}')

sim_boxes = list(re.finditer(r'<section class=["\']simulator-box["\'].*?>(.*?)</section>', content, re.DOTALL))
print('Simulator boxes count:', len(sim_boxes))
for i, match in enumerate(sim_boxes):
    box = match.group(1).strip()
    print(f'=== BOX {i+1} (pos {match.start()} to {match.end()}) ===')
    print(box[:350])



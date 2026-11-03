import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\cerca-quiz.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect CSS around cq-search-box-wrapper and cq-filters-panel
css_start = content.find('/* Search Box Wrapper */')
css_end = content.find('/* Stats strip */')

if css_start == -1 or css_end == -1:
    print("Could not find CSS boundaries!")
    sys.exit(1)

print("Found CSS boundaries, length:", css_end - css_start)

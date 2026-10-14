import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECKING LIGHT MODE CSS CONTRAST ISSUES ===")

css_files = [
    'assets/css/theme-modes.css',
    'interactive_pages/interactive_style.css',
    'interactive_pages/دليل_الباب_20_رخص_القيادة_والنقاط_والعقوبات.html',
    'interactive_pages/دليل_الباب_19_أحزمة_الأمان_والخوذة_ومقاعد_الأطفال.html',
    'interactive_pages/دليل_الباب_18_استخدام_الأضواء_ولمبات_التابلوه_والعواكس.html',
    'interactive_pages/دليل_الباب_17_الأوتوستراد_والحمولة_وسحب_المقطورات.html',
    'interactive_pages/دليل_الباب_16_الوقوف_والتوقف_والركن.html'
]

for cf in css_files:
    if not os.path.exists(cf):
        continue
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    
    # Find html.light blocks
    light_rules = re.findall(r'html\.light[^{]*\{([^}]+)\}', txt)
    print(f"\n--- {cf} (found {len(light_rules)} light blocks) ---")
    for r in light_rules[:5]:
        # Print color properties
        colors = [line.strip() for line in r.split(';') if any(k in line.lower() for k in ['color', 'background', '--text', '--bg'])]
        if colors:
            print("   ", " | ".join(colors[:6]))

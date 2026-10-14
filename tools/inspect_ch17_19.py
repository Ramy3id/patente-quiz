import re, sys
sys.stdout.reconfigure(encoding='utf-8')

for ch_num, filename in [(17, 'interactive_pages/دليل_الباب_17_الأوتوستراد_والحمولة_وسحب_المقطورات.html'),
                         (18, 'interactive_pages/دليل_الباب_18_استخدام_الأضواء_ولمبات_التابلوه_والعواكس.html'),
                         (19, 'interactive_pages/دليل_الباب_19_أحزمة_الأمان_والخوذة_ومقاعد_الأطفال.html')]:
    with open(filename, 'r', encoding='utf-8') as f:
        txt = f.read()
    print(f"=== Chapter {ch_num} ({filename}) ===")
    print("  Length:", len(txt))
    print("  Studio present:", 'studio' in txt.lower() or 'studio-card' in txt)
    print("  Gallery present:", 'workshop-gallery' in txt or 'gallery' in txt.lower())
    tech_cards = len(re.findall(r'class=[\'"]technical-card[\'"]', txt))
    signal_cards = len(re.findall(r'class=[\'"]signal-card[\'"]', txt))
    print(f"  Cards: technical-card={tech_cards}, signal-card={signal_cards}")
    trap_cards = len(re.findall(r'class=[\'"](trap-quiz-card|trap-card)[\'"]', txt))
    print(f"  Trap cards count: {trap_cards}")

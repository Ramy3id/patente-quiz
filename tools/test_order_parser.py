import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# Sample raw order strings from SIM_DATABASE
test_orders = [
    ['B (حافلة حمراء)', 'H (حافلة زرقاء)', 'C (سيارة برتقالية)'],
    ['R (سيارة زرقاء من الغرب)', 'A (سيارة برتقالية من الفرع المائل الشمالي الغربي)', 'T (سيارة حمراء من الشرق)'],
    ['L (سيارة سوداء من الشرق)', 'C و A معاً (عبور متزامن contemporaneamente)', 'D (سيارة زرقاء من الغرب)'],
    ['B (يتقدم لمركز التقاطع ويتوقف)', 'R (تعبر أولاً بالكامل)', 'D و N معاً (عبور متزامن contemporaneamente)', 'B (يكمل انعطافه ويخلي التقاطع)'],
    ['T (الترام)', 'A (للمركز)', 'O', 'M (دراجة)', 'A (يكمل)'],
    ['D (سيارة زرقاء من الفرع الجنوبي الغربي)', 'P (سيارة صفراء من الغرب)', 'B (سيارة سوداء من الفرع الشمالي الغربي)', 'N (سيارة حمراء من الشرق)']
]

def parse_order(order_list):
    parsed = []
    flow_letters = []
    
    for idx, item in enumerate(order_list):
        # Match letter and desc
        m = re.match(r'^([A-Za-z0-9\sو\+]+?)(?:\s*\((.*?)\))?$', item.strip())
        if m:
            raw_label = m.group(1).strip()
            desc = m.group(2).strip() if m.group(2) else ''
        else:
            raw_label = item.strip()
            desc = ''
            
        # Clean label for quick flow
        quick_label = raw_label.replace(' و ', ' + ').replace(' معاً', '').strip()
        flow_letters.append(quick_label)
        
        parsed.append({
            'num': idx + 1,
            'label': quick_label,
            'desc': desc if desc else raw_label
        })
    return flow_letters, parsed

for i, o in enumerate(test_orders):
    flow, details = parse_order(o)
    print(f"\nTest {i+1}:")
    print("  Flow (LTR):", " ➔ ".join(flow))
    for d in details:
        print(f"  Step {d['num']}: [{d['label']}] {d['desc']}")

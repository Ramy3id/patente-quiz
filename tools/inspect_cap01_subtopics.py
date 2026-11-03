import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\Capitolo_01_definizioni_generali_doveri_strada\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check subtopic buttons / chips
buttons = re.findall(r'<button[^>]*class="[^"]*subtopic[^"]*"[^>]*>(.*?)</button>', content, re.DOTALL)
print(f"Subtopic buttons in Capitolo 01 ({len(buttons)}):")
for b in buttons:
    clean = re.sub(r'\s+', ' ', b).strip()
    print("  ", clean[:80])

# Check subtopic sections
sections = re.findall(r'<section[^>]*id="([^"]+)"[^>]*>.*?<h[1-4][^>]*>(.*?)</h[1-4]>', content, re.DOTALL)
print(f"\nSections in Capitolo 01 ({len(sections)}):")
for s_id, s_title in sections:
    clean = re.sub(r'\s+', ' ', s_title).strip()
    print(f"   [{s_id}] {clean[:80]}")

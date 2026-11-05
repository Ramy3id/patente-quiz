import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'<div class="bento-icon-box"[^>]*>(.*?)</div>', re.DOTALL)
matches = pattern.findall(text)
print("Bento icons count:", len(matches))
for i, m in enumerate(matches):
    print(f"{i+1}: {repr(m)}")

# Check chapter cards
ch_pattern = re.compile(r'<div class="card-stats-row">(.*?)</div>', re.DOTALL)
ch_matches = ch_pattern.findall(text)
print("Card stats rows count:", len(ch_matches))
if ch_matches:
    print("Sample:", repr(ch_matches[0]))

btn_pattern = re.compile(r'<a[^>]*class="btn-action-study"[^>]*>(.*?)</a>', re.DOTALL)
btn_matches = btn_pattern.findall(text)
print("Btn action study count:", len(btn_matches))
if btn_matches:
    print("Sample btn:", repr(btn_matches[0]))

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    piano = f.read()

# Question 2 snippet
q2_idx = piano.find('كم ساعة تستطيع')
if q2_idx != -1:
    print("=== Question 2 HTML snippet ===")
    print(piano[q2_idx-100:q2_idx+1200])

# Question 3 snippet
q3_idx = piano.find('مستواك في اللغة')
if q3_idx != -1:
    print("\n=== Question 3 HTML snippet ===")
    print(piano[q3_idx-100:q3_idx+1200])

# Question 4 snippet
q4_idx = piano.find('منهجية ترتيب')
if q4_idx != -1:
    print("\n=== Question 4 HTML snippet ===")
    print(piano[q4_idx-100:q4_idx+1500])

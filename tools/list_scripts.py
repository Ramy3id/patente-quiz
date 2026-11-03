import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html', 'r', encoding='utf-8') as f:
    text = f.read()

scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', text)
for s in scripts:
    print(s)

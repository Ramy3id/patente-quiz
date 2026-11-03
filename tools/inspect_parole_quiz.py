# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/parole-quiz.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<script\s+[^>]*src=[\'"](.*?)[\'"]', text):
    print("Script src:", m.group(1))

# Check search function
print("\n--- Search logic in parole-quiz.html ---")
matches = re.findall(r'function\s+(\w+)\s*\(.*?\)', text)
print("Functions:", matches)

# Find where search input is handled
m_search = re.search(r'function\s+.*?(search|filter|performSearch|find).*?\{[\s\S]*?\}', text, re.I)
if m_search:
    print("\nSearch function code snippet:")
    print(m_search.group(0)[:1500])

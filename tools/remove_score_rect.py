with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\modular-chapter.css', 'r', encoding='utf-8') as f:
    text = f.read()

old_rule = '''/* 3-Column Metrics Score Strip */
.score-strip {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
  gap: 8px !important;
  width: 100% !important;
  padding-top: 14px !important;
  border-top: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08)) !important;
  margin-top: 14px !important;
  box-sizing: border-box !important;
  direction: rtl !important;
}
html.light .score-strip {
  border-top-color: rgba(15, 23, 42, 0.08) !important;
}'''

new_rule = '''/* 3-Column Metrics Score Strip - NO SHARP OUTER RECTANGLE BORDER */
.score-strip,
html.light .score-strip,
html.dark .score-strip {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
  gap: 8px !important;
  width: 100% !important;
  padding: 12px 0 0 0 !important;
  border: none !important;
  background: transparent !important;
  box-shadow: none !important;
  border-radius: 0 !important;
  margin-top: 12px !important;
  box-sizing: border-box !important;
  direction: rtl !important;
}'''

if old_rule in text:
    text = text.replace(old_rule, new_rule, 1)
    print("Replaced score-strip rule in modular-chapter.css successfully")
else:
    print("WARNING: old_rule not found")

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\modular-chapter.css', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved modular-chapter.css")

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\dizionario-sinonimi.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("File size:", len(text))
print("Has hardcoded #fecdd3:", "#fecdd3" in text)
print("Has categoryChipsDeck:", "categoryChipsDeck" in text)
print("Has hero-stats-row:", "hero-stats-row" in text)

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.chapter-card:hover' in l:
        start = max(0, i - 4)
        end = min(len(lines), i + 10)
        print(f"=== theme-modes.css lines {start} to {end} ===")
        print("".join(lines[start:end]))

with open(r'R:\Ramy\PATENTE\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

classes = ['.nav-chapters-btn {', '.nav-dropdown-tab {', '.nav-search-trigger {', '.nav-progress-pill {', '.nav-theme-btn {', '.nav-auth-pill {']

for cls in classes:
    pos = text.find(cls)
    if pos != -1:
        end = text.find('}', pos)
        print("===" + cls + "===")
        print(text[pos:end+1].strip())

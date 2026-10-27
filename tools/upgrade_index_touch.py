path = r'R:\Ramy\PATENTE\Capitoli_Divisi\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''.btn-action-study {
    flex: 1;
    text-align: center;
    text-decoration: none;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-subtle);
    color: #fff;
    padding: 9px 14px;
    border-radius: 9px;
    font-size: 0.85rem;'''

replacement = '''.btn-action-study {
    flex: 1;
    text-align: center;
    text-decoration: none;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-subtle);
    color: #fff;
    padding: 9px 14px;
    min-height: 44px;
    border-radius: 9px;
    font-size: 0.85rem;'''

target2 = '''.btn-action-md {
    text-decoration: none;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
    padding: 9px 12px;
    border-radius: 9px;
    font-size: 0.82rem;'''

replacement2 = '''.btn-action-md {
    text-decoration: none;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
    padding: 9px 12px;
    min-height: 44px;
    border-radius: 9px;
    font-size: 0.82rem;'''

if target in content and target2 in content:
    content = content.replace(target, replacement, 1)
    content = content.replace(target2, replacement2, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Capitoli_Divisi/index.html touch targets set to min-height: 44px!")
else:
    print("Targets not matched in Capitoli_Divisi/index.html")

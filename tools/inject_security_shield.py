import os

files = [
    (r'R:\Ramy\PATENTE\Simulatore_Esame.html', 'assets/js/security-shield.js'),
    (r'R:\Ramy\PATENTE\Capitoli_Divisi\index.html', '../assets/js/security-shield.js')
]

for fp, script_path in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    target = '<script src="' + script_path.replace('security-shield', 'theme-engine') + '"></script>'
    replacement = f'<script src="{script_path}"></script>\n' + target
    
    if target in content and script_path not in content:
        content = content.replace(target, replacement, 1)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Injected security-shield into {os.path.basename(fp)}')
    else:
        print(f'Skipped or already injected in {os.path.basename(fp)}')

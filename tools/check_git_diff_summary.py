import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
cwd = r'R:\Ramy\PATENTE_PRO_APP'

res = subprocess.run('git status --porcelain', cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
lines = res.stdout.split('\n')
untracked = [l for l in lines if l.startswith('??')]
modified = [l for l in lines if l.startswith(' M')]
print(f'Total modified: {len(modified)}')
print(f'Total untracked: {len(untracked)}')
print('\nSample modified:')
for m in modified[:10]:
    print(m)
print('\nSample untracked:')
for u in untracked[:15]:
    print(u)

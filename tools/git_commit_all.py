import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
cwd = r'R:\Ramy\PATENTE_PRO_APP'

def run(cmd):
    print(f'>>> {cmd}')
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.stdout:
        print(res.stdout)
    if res.stderr:
        print('STDERR:', res.stderr)
    return res.returncode

# 1. Add all changes
print("Staging all changes...")
run('git add -A')

# 2. Commit
commit_msg = "feat(app): modernize UI, word bank, ministerial search, and mobile responsiveness"
print("Committing changes...")
run(f'git commit -m "{commit_msg}"')

# 3. Check status
run('git status --short')

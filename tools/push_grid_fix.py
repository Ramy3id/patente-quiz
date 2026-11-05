import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
cwd = r'R:\Ramy\PATENTE_PRO_APP'

print("Staging all changes...")
subprocess.run(['git', 'add', '-A'], cwd=cwd, check=True)

msg = "fix(layout): unify all banners and interactive containers to exact 1164px/1200px grid matching home portal"
print(f"Committing: {msg}")
r = subprocess.run(['git', 'commit', '-m', msg], cwd=cwd, capture_output=True, text=True)
print("Commit STDOUT:", r.stdout)
if r.stderr:
    print("Commit STDERR:", r.stderr)

print("Pushing to origin main...")
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=cwd, capture_output=True, text=True)
print("Push STDOUT:", p.stdout)
if p.stderr:
    print("Push STDERR:", p.stderr)
print("Push RC:", p.returncode)

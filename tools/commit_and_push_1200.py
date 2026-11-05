import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
cwd = r'R:\Ramy\PATENTE_PRO_APP'

print("Adding all files...")
r1 = subprocess.run(['git', 'add', '-A'], cwd=cwd, capture_output=True, text=True)
print("Add RC:", r1.returncode)

commit_msg = "feat(layout): unify all platform containers to standard 1200px grid matching home portal"
print(f"Committing: {commit_msg}")
r2 = subprocess.run(['git', 'commit', '-m', commit_msg], cwd=cwd, capture_output=True, text=True)
print("Commit output:\n", r2.stdout)
if r2.stderr:
    print("Commit err:\n", r2.stderr)

print("Pushing to origin main...")
r3 = subprocess.run(['git', 'push', 'origin', 'main'], cwd=cwd, capture_output=True, text=True)
print("Push output:\n", r3.stdout)
if r3.stderr:
    print("Push err:\n", r3.stderr)
print("Push RC:", r3.returncode)

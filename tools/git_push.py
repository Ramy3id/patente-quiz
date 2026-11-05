import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
cwd = r'R:\Ramy\PATENTE_PRO_APP'

print("Pushing to origin main...")
res = subprocess.run('git push origin main', cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
print("Return code:", res.returncode)

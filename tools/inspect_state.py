import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    piano = f.read()

print("piano-studio length:", len(piano))

# Check Q4
idx = piano.find('id="optFlowCluster"')
if idx != -1:
    print("=== Q4 HTML snippet ===")
    print(piano[idx-100:idx+600])

# Check modal media queries
idx_media = piano.find('@media (max-width: 768px)')
while idx_media != -1:
    block = piano[idx_media:idx_media+1200]
    if 'planSetupModal' in block or 'sp-modal-actions-bar' in block:
        print("=== Media Query block ===")
        print(block[:800])
        print("--------------------")
    idx_media = piano.find('@media (max-width: 768px)', idx_media+1)

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html', 'r', encoding='utf-8') as f:
    piano = f.read()

idx = 0
while True:
    idx = piano.find('.sp-modal-backdrop', idx)
    if idx == -1:
        break
    print("=== .sp-modal-backdrop match ===")
    print(piano[idx:idx+350].replace('\n', ' '))
    print("---")
    idx += len('.sp-modal-backdrop')

idx = 0
while True:
    idx = piano.find('.sp-modal-box', idx)
    if idx == -1:
        break
    print("=== .sp-modal-box match ===")
    print(piano[idx:idx+350].replace('\n', ' '))
    print("---")
    idx += len('.sp-modal-box')

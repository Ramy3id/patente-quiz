import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Inspect modal close button and modal HTML
idx_modal = text.find('fig-modal')
print("--- MODAL CSS / HTML ---")
print(text[idx_modal-50:idx_modal+1500])

# 2. Inspect modal HTML in body
idx_modal_html = text.rfind('fig-modal-card')
print("\n--- MODAL HTML IN BODY ---")
print(text[idx_modal_html-100:idx_modal_html+1200])

# 3. Inspect sim arrows HTML
idx_arrows = text.find('sim-arrows-wrap')
print("\n--- SIM ARROWS HTML ---")
print(text[idx_arrows-50:idx_arrows+600])

# 4. Inspect simulation buttons HTML
idx_sim_btns = text.find('btn-sim-play')
print("\n--- SIM BUTTONS HTML ---")
print(text[idx_sim_btns-100:idx_sim_btns+800])

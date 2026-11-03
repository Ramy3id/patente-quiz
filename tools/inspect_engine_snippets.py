import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('R:/Ramy/PATENTE_PRO_APP/assets/js/modular-chapter-engine.js', 'r', encoding='utf-8') as f:
    engine_code = f.read()

# 1. View mode buttons around character 11660
print("--- VIEW MODE BUTTONS ---")
print(engine_code[11400:12200])

# 2. Reset progress button around character 13151
print("\n--- RESET PROGRESS BUTTON ---")
print(engine_code[13000:13600])

# 3. Subtopic stats badges
idx_sub = engine_code.find('subtopic-meta')
if idx_sub != -1:
    print("\n--- SUBTOPIC META ---")
    print(engine_code[idx_sub-100:idx_sub+600])
else:
    # Let's search for 'إتقان' or 'أتقان'
    idx_itq = engine_code.find('إتقان')
    if idx_itq != -1:
        print("\n--- SUBTOPIC STATS BADGES (found إتقان) ---")
        print(engine_code[idx_itq-200:idx_itq+500])

# 4. Question card rendering
idx_qc = engine_code.find('renderQuestion(')
if idx_qc != -1:
    print("\n--- RENDER QUESTION FUNCTION ---")
    print(engine_code[idx_qc:idx_qc+1800])

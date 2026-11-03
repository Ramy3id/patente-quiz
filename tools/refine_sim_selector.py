import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = 'R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

old_css = """.sim-selector-btn {
      width: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(14, 165, 233, 0.35);
      border-radius: 12px;
      padding: 9px 14px;
      color: var(--inc-text);
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s ease;
      text-align: right;
    }"""

new_css = """.sim-selector-btn {
      width: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(14, 165, 233, 0.35);
      border-radius: 12px;
      padding: 9px 14px;
      color: var(--inc-text);
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s ease;
      text-align: right;
      overflow: hidden;
      box-sizing: border-box;
    }
    .sim-sel-text-wrap {
      flex: 1;
      min-width: 0 !important;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .sim-sel-val {
      font-size: 0.92rem;
      font-weight: 900;
      color: #FFFFFF;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      min-width: 0 !important;
    }
    .sim-sel-arrow {
      font-size: 0.75rem;
      color: var(--inc-cyan);
      transition: transform 0.2s;
      flex-shrink: 0;
    }"""

if old_css in text:
    text = text.replace(old_css, new_css, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Refined .sim-selector-btn and .sim-sel-text-wrap ellipsis")
else:
    print("WARNING: old_css not found")

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Remove duplicate .btn-flag-review at lines 909-928
duplicate_flag_block = '''    .btn-flag-review {
      background: transparent;
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: #FBBF24;
      padding: 3px 10px;
      border-radius: 8px;
      font-size: 0.76rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-family: inherit;
      transition: all 0.15s ease;
    }
    .btn-flag-review.active {
      background: rgba(245, 158, 11, 0.25);
      border-color: #F59E0B;
      color: #F59E0B;
    }'''

if duplicate_flag_block in c:
    c = c.replace(duplicate_flag_block, '')
    print('1. Removed duplicate .btn-flag-review')
else:
    print('1. duplicate_flag_block not found exactly')

# 2. Fix media slot height: 90px
c = c.replace('height: 120px;\n      max-height: 90px;\n      min-height: 90px;', 'height: 90px;\n      max-height: 90px;\n      min-height: 90px;')

# 3. Fine tune text container and fonts
old_tc = '''    .exam-text-container {
      height: 175px;
      min-height: 175px;
      max-height: 175px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      margin: 6px 0 8px;
      text-align: center;
      padding: 4px 8px;
      scrollbar-width: thin;
      box-sizing: border-box;
    }
    .exam-text-it {
      font-size: 1.08rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.4;
      margin: 0 0 8px;
      direction: ltr;
      text-align: center;
    }'''

new_tc = '''    .exam-text-container {
      height: 185px;
      min-height: 185px;
      max-height: 185px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      margin: 4px 0 6px;
      text-align: center;
      padding: 2px 8px;
      scrollbar-width: thin;
      box-sizing: border-box;
    }
    .exam-text-it {
      font-size: 1.02rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.35;
      margin: 0 0 6px;
      direction: ltr;
      text-align: center;
    }'''

if old_tc in c:
    c = c.replace(old_tc, new_tc)
    print('2. Updated text container to 185px and font to 1.02rem')
else:
    print('2. old_tc not found')

# 4. Timer in Motorizzazione
c = c.replace('motoTimer.textContent = `TEMPO: ${formattedTime}`;', 'motoTimer.textContent = `⏱️ ${formattedTime}`;')
c = c.replace('<div class="moto-timer-badge" id="motoTimerBadge">TEMPO: 20:00</div>', '<div class="moto-timer-badge" id="motoTimerBadge">⏱️ 20:00</div>')
c = c.replace('<span>🌟 الوضع العصري</span>', '<span>🌟 عصري</span>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Done refinements.')

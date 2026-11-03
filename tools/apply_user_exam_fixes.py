file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. High-prominence Active Question Pill (.q-pill.active)
old_pill_active = '''    .q-pill.active {
      border-color: var(--accent-cyan);
      background: rgba(56, 189, 248, 0.2);
      color: var(--accent-cyan);
    }'''

new_pill_active = '''    .q-pill.active,
    html.light .q-pill.active,
    .q-pill.active.answered,
    html.light .q-pill.active.answered {
      background: linear-gradient(135deg, #0284C7, #0369A1) !important;
      border: 2px solid #38BDF8 !important;
      color: #FFFFFF !important;
      font-weight: 900 !important;
      transform: scale(1.14) !important;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.5) !important;
      z-index: 5 !important;
      outline: 2px solid rgba(56, 189, 248, 0.3) !important;
    }'''

if old_pill_active in c:
    c = c.replace(old_pill_active, new_pill_active)
    print('1. Replaced .q-pill.active with prominent style')
else:
    print('1. old_pill_active not found directly')

# 2. Fix .exam-q-header height and padding so button is never cut by the separator line
old_q_header = '''    .exam-q-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      padding-bottom: 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      height: 28px;
    }'''

new_q_header = '''    .exam-q-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      padding-bottom: 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      min-height: 34px;
      box-sizing: border-box;
    }'''

if old_q_header in c:
    c = c.replace(old_q_header, new_q_header)
    print('2. Fixed .exam-q-header padding and removed height:28px')
else:
    print('2. old_q_header not found')

# 3. Card padding and nav steps breathing space
old_card_css = '''    .exam-question-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 16px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
      box-sizing: border-box;
      margin-bottom: 12px;
    }'''

new_card_css = '''    .exam-question-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 22px;
      padding: 16px 16px 20px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
      box-sizing: border-box;
      margin-bottom: 14px;
    }'''

if old_card_css in c:
    c = c.replace(old_card_css, new_card_css)
    print('3. Updated .exam-question-card padding to 16px 16px 20px')
else:
    print('3. old_card_css not found')

old_nav_steps = '''    .exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 6px;
      height: 42px;
    }'''

new_nav_steps = '''    .exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 10px;
      margin-bottom: 4px;
      height: 42px;
    }'''

if old_nav_steps in c:
    c = c.replace(old_nav_steps, new_nav_steps)
    print('4. Updated .exam-nav-steps margin')
else:
    print('4. old_nav_steps not found')

# 4. Expand media slot (110px) and text container (220px)
old_media_slot = '''    .exam-media-slot {
      height: 90px;
      max-height: 90px;
      min-height: 90px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 4px 0;
      overflow: hidden;
    }'''

new_media_slot = '''    .exam-media-slot {
      height: 110px;
      max-height: 110px;
      min-height: 110px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 4px 0;
      overflow: hidden;
    }'''

if old_media_slot in c:
    c = c.replace(old_media_slot, new_media_slot)
    print('5. Updated .exam-media-slot to 110px')
else:
    print('5. old_media_slot not found')

# Sign img max-height
c = c.replace('max-height: 80px;\n      object-fit: contain;', 'max-height: 100px;\n      object-fit: contain;')

# Text container height to 220px
old_tc2 = '''    .exam-text-container {
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
    }'''

new_tc2 = '''    .exam-text-container {
      height: 220px;
      min-height: 220px;
      max-height: 220px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      margin: 4px 0 6px;
      text-align: center;
      padding: 4px 8px;
      scrollbar-width: thin;
      box-sizing: border-box;
    }'''

if old_tc2 in c:
    c = c.replace(old_tc2, new_tc2)
    print('6. Updated .exam-text-container to 220px')
else:
    print('6. old_tc2 not found')

# 5. Add complete Light Mode styling for Motorizzazione
moto_light_css = '''
    /* =========================================================
       Motorizzazione Official Skin - Light Mode Theme
       ========================================================= */
    html.light .motorizzazione-screen-wrap {
      background: #FFFFFF !important;
      border: 3px solid #CBD5E1 !important;
      box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08) !important;
    }
    html.light .moto-top-header {
      background: #F8FAFC !important;
      border-bottom: 2px solid #0284C7 !important;
      color: #0F172A !important;
    }
    html.light .moto-titles-text strong {
      color: #0F172A !important;
    }
    html.light .moto-titles-text span {
      color: #64748B !important;
    }
    html.light .moto-timer-badge {
      background: #E0F2FE !important;
      border-color: #38BDF8 !important;
      color: #0284C7 !important;
    }
    html.light .moto-timer-badge.warning {
      background: #FEE2E2 !important;
      border-color: #EF4444 !important;
      color: #DC2626 !important;
    }
    html.light .moto-main-terminal {
      background: #FFFFFF !important;
    }
    html.light .moto-sign-panel {
      background: #F8FAFC !important;
      border-color: #CBD5E1 !important;
    }
    html.light .moto-no-sign-official {
      background: #F1F5F9 !important;
      color: #64748B !important;
    }
    html.light .moto-q-num-badge {
      background: #E2E8F0 !important;
      color: #1E293B !important;
    }
    html.light .btn-moto-flag {
      background: #FEF3C7 !important;
      border-color: #F59E0B !important;
      color: #B45309 !important;
    }
    html.light .btn-moto-flag.active {
      background: #F59E0B !important;
      color: #FFFFFF !important;
    }
    html.light .moto-text-italian {
      color: #0F172A !important;
    }
    html.light .moto-bottom-controls {
      background: #F8FAFC !important;
      border-top-color: #E2E8F0 !important;
    }
    html.light .btn-moto-step {
      background: #FFFFFF !important;
      border-color: #CBD5E1 !important;
      color: #1E293B !important;
    }
    html.light .btn-moto-step:hover:not(:disabled) {
      background: #F1F5F9 !important;
      border-color: #0284C7 !important;
    }
    html.light .moto-cell {
      background: #FFFFFF !important;
      border-color: #CBD5E1 !important;
      color: #475569 !important;
    }
    html.light .moto-cell.active {
      border-color: #0284C7 !important;
      background: #E0F2FE !important;
      color: #0284C7 !important;
      box-shadow: 0 0 8px rgba(2, 132, 199, 0.4) !important;
    }
    html.light .moto-cell.v {
      background: #0284C7 !important;
      color: #FFFFFF !important;
      border-color: #0369A1 !important;
    }
    html.light .moto-cell.f {
      background: #DC2626 !important;
      color: #FFFFFF !important;
      border-color: #B91C1C !important;
    }
'''

if 'Motorizzazione Official Skin - Light Mode Theme' not in c:
    c = c.replace('/* Mobile-Optimized 1-Line Question Pill Scroll', moto_light_css + '\n    /* Mobile-Optimized 1-Line Question Pill Scroll')
    print('7. Added Motorizzazione Light Mode styles')
else:
    print('7. Motorizzazione Light Mode already present')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

print('All fixes applied successfully.')

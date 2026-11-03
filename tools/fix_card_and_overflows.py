file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update Media query for exam-question-card (line 840)
old_media_card = '''.exam-question-card {
        padding: 12px 12px 16px !important;
        border-radius: 22px !important;
      }'''

new_media_card = '''.exam-question-card {
        padding: 16px 14px 28px !important;
        border-radius: 24px !important;
      }'''

if old_media_card in c:
    c = c.replace(old_media_card, new_media_card)
    print('1. Updated mobile media query card padding to 28px bottom')
else:
    print('1. old_media_card not found')

# 2. Update .exam-question-card base styles (line 970)
old_base_card = '''.exam-question-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 12px 14px 16px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 384px;
      box-sizing: border-box;
      margin-bottom: 12px;
    }'''

new_base_card = '''.exam-question-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 24px;
      padding: 16px 16px 28px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-sizing: border-box;
      margin-bottom: 14px;
    }'''

if old_base_card in c:
    c = c.replace(old_base_card, new_base_card)
    print('2. Updated base card padding to 28px bottom')
else:
    print('2. old_base_card not found')

# 3. Increase media slot to 135px and img to 125px (no overflow hidden chop!)
old_media_slot = '''.exam-media-slot {
      height: 100px;
      max-height: 100px;
      min-height: 100px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 4px 0;
      overflow: hidden;
    }'''

new_media_slot = '''.exam-media-slot {
      height: 135px;
      max-height: 135px;
      min-height: 135px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 4px 0 8px;
    }'''

if old_media_slot in c:
    c = c.replace(old_media_slot, new_media_slot)
    print('3. Updated .exam-media-slot to 135px')
else:
    print('3. old_media_slot not found')

c = c.replace('max-height: 112px;\n      max-width: 140px;\n      object-fit: contain;',
              'max-height: 125px;\n      max-width: 200px;\n      object-fit: contain;')

# 4. Increase text container to 230px and hide scrollbars completely
old_tc = '''.exam-text-container {
      height: 170px;
      min-height: 170px;
      max-height: 170px;
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

new_tc = '''.exam-text-container {
      height: 230px;
      min-height: 230px;
      max-height: 230px;
      overflow-y: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      margin: 4px 0 8px;
      text-align: center;
      padding: 4px 10px;
      box-sizing: border-box;
    }
    .exam-text-container::-webkit-scrollbar {
      display: none !important;
    }'''

if old_tc in c:
    c = c.replace(old_tc, new_tc)
    print('4. Updated .exam-text-container to 230px with hidden scrollbar')
else:
    print('4. old_tc not found')

# 5. Nav steps spacing
old_nav_steps = '''.exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 6px;
      margin-bottom: 0px;
      height: 38px;
    }'''

new_nav_steps = '''.exam-nav-steps {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 14px;
      margin-bottom: 2px;
      padding: 0 4px;
      height: 40px;
      border-top: none !important;
    }'''

if old_nav_steps in c:
    c = c.replace(old_nav_steps, new_nav_steps)
    print('5. Updated .exam-nav-steps spacing')
else:
    print('5. old_nav_steps not found')

# Remove duplicate old definitions of .btn-nav-step and .btn-submit-pill that had height 38px
c = c.replace('''    .btn-nav-step {
      height: 38px !important;
      min-height: 38px !important;
      max-height: 38px !important;
      font-size: 0.85rem !important;
      padding: 0 12px !important;
      border-radius: 10px !important;
      background: rgba(255, 255, 255, 0.06) !important;
      border: 1px solid rgba(255, 255, 255, 0.1) !important;
      color: var(--text-secondary) !important;
      cursor: pointer !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }''', '')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Done applying card and overflow fixes.')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .fig-modal-close CSS
old_close_css = '''.fig-modal-close {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--inc-text-sub);
      width: 36px;
      height: 36px;
      min-width: 36px;
      min-height: 36px;
      max-width: 36px;
      max-height: 36px;
      aspect-ratio: 1 / 1;
      flex-shrink: 0;
      border-radius: 50%;
      padding: 0;
      margin: 0;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 1.15rem;
      line-height: 1;
      cursor: pointer;
      box-sizing: border-box;
      transition: all 0.2s;
    }'''

new_close_css = '''.fig-modal-close {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--inc-text-sub);
      width: 38px !important;
      height: 38px !important;
      min-width: 38px !important;
      min-height: 38px !important;
      max-width: 38px !important;
      max-height: 38px !important;
      aspect-ratio: 1 / 1 !important;
      flex-shrink: 0 !important;
      border-radius: 50% !important;
      padding: 0 !important;
      margin: 0 !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      font-size: 1.15rem !important;
      line-height: 1 !important;
      cursor: pointer;
      box-sizing: border-box !important;
      transition: all 0.2s;
    }'''

if old_close_css in content:
    content = content.replace(old_close_css, new_close_css)
    print("Replaced base .fig-modal-close CSS")
else:
    print("WARNING: old_close_css not found directly")

# Also check html.light .fig-modal-close
old_light_close = '''html.light .fig-modal-close {
      background: #F1F5F9 !important;
      border-color: #CBD5E1 !important;
      color: #475569 !important;
    }'''

new_light_close = '''html.light .fig-modal-close {
      background: #F1F5F9 !important;
      border-color: #CBD5E1 !important;
      color: #475569 !important;
      width: 38px !important;
      height: 38px !important;
      min-width: 38px !important;
      min-height: 38px !important;
      max-width: 38px !important;
      max-height: 38px !important;
      border-radius: 50% !important;
      aspect-ratio: 1 / 1 !important;
      padding: 0 !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }'''

if old_light_close in content:
    content = content.replace(old_light_close, new_light_close)
    print("Replaced html.light .fig-modal-close CSS")
else:
    print("WARNING: old_light_close not found directly")

# 2. Update navigation arrows in .sim-arrows-wrap
old_arrows = '''        <div class="sim-arrows-wrap">
          <button class="sim-nav-arrow-btn" onclick="navSimFigure(-1)" title="التقاطع السابق">
            <span>◀ السابق</span>
          </button>
          <span class="sim-nav-counter" id="simNavCounter">1 / 43</span>
          <button class="sim-nav-arrow-btn" onclick="navSimFigure(1)" title="التقاطع التالي">
            <span>التالي ▶</span>
          </button>
        </div>'''

new_arrows = '''        <div class="sim-arrows-wrap">
          <button class="sim-nav-arrow-btn" onclick="navSimFigure(-1)" title="التقاطع السابق">
            <span>السابق ▶</span>
          </button>
          <span class="sim-nav-counter" id="simNavCounter">1 / 43</span>
          <button class="sim-nav-arrow-btn" onclick="navSimFigure(1)" title="التقاطع التالي">
            <span>◀ التالي</span>
          </button>
        </div>'''

if old_arrows in content:
    content = content.replace(old_arrows, new_arrows)
    print("Replaced navigation arrows in .sim-arrows-wrap")
else:
    print("WARNING: old_arrows not found directly")

# 3. Update simulation action buttons in HTML to use ↺
old_sim_actions = '''          <div class="sim-actions-row">
            <button class="btn-sim-play" id="btnSimPlay" onclick="playFullSimulation()" title="تشغيل المحاكاة الحية" aria-label="تشغيل المحاكاة الحية">
              <span>▶️</span>
            </button>
            <button class="btn-sim-step" id="btnSimStep" onclick="stepSimulation()" title="التقدم خطوة بخطوة" aria-label="خطوة بخطوة">
              <span>⏭️</span>
            </button>
            <button class="btn-sim-reset" onclick="resetSimulation()" title="إعادة ضبط التقاطع" aria-label="إعادة ضبط">
              <span>🔄</span>
            </button>
          </div>'''

new_sim_actions = '''          <div class="sim-actions-row">
            <button class="btn-sim-play" id="btnSimPlay" onclick="playFullSimulation()" title="تشغيل المحاكاة" aria-label="تشغيل المحاكاة">
              <span>▶️</span>
            </button>
            <button class="btn-sim-step" id="btnSimStep" onclick="stepSimulation()" title="خطوة بخطوة" aria-label="خطوة بخطوة">
              <span>⏭️</span>
            </button>
            <button class="btn-sim-reset" onclick="resetSimulation()" title="إعادة ضبط التقاطع" aria-label="إعادة ضبط">
              <span>↺</span>
            </button>
          </div>'''

if old_sim_actions in content:
    content = content.replace(old_sim_actions, new_sim_actions)
    print("Replaced simulation action buttons")
else:
    print("WARNING: old_sim_actions not found directly")

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done processing decodificatore-incroci.html")

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update arrows in .sim-arrows-wrap
old_arrows = '''        <div class="sim-arrows-wrap">
          <button class="sim-nav-arrow-btn" onclick="navSimFigure(-1)" title="التقاطع السابق">
            <span>السابق ▶</span>
          </button>
          <span class="sim-nav-counter" id="simNavCounter">1 / 43</span>
          <button class="sim-nav-arrow-btn" onclick="navSimFigure(1)" title="التقاطع التالي">
            <span>◀ التالي</span>
          </button>
        </div>'''

new_arrows = '''        <div class="sim-arrows-wrap">
          <button class="sim-nav-arrow-btn" onclick="navSimFigure(-1)" title="التقاطع السابق">
            <span class="nav-arrow-icon">▶</span>
            <span>السابق</span>
          </button>
          <span class="sim-nav-counter" id="simNavCounter">1 / 43</span>
          <button class="sim-nav-arrow-btn" onclick="navSimFigure(1)" title="التقاطع التالي">
            <span>التالي</span>
            <span class="nav-arrow-icon">◀</span>
          </button>
        </div>'''

if old_arrows in c:
    c = c.replace(old_arrows, new_arrows)
    print("1. Arrows updated successfully")
else:
    print("WARNING: old_arrows not found directly")

# 2. Update CSS for mobile actions row & sub-actions row
old_mobile_actions = '''.sim-actions-row {
        flex-direction: row !important;
        gap: 8px !important;
        width: 100% !important;
      }
      .btn-sim-play, .btn-sim-step, .btn-sim-reset {
        flex: 1 !important;
        width: auto !important;
        height: 48px !important;
      }'''

new_mobile_actions = '''.sim-actions-row {
        flex-direction: row !important;
        gap: 8px !important;
        width: 100% !important;
      }
      .btn-sim-play, .btn-sim-step, .btn-sim-reset {
        flex: 1 !important;
        width: auto !important;
        height: 40px !important;
        min-height: 40px !important;
        font-size: 1.25rem !important;
      }
      .sim-sub-actions-row {
        flex-direction: row !important;
        gap: 8px !important;
        width: 100% !important;
      }
      .sim-sub-btn {
        flex: 1 !important;
        height: 38px !important;
        min-height: 38px !important;
        font-size: 0.74rem !important;
        padding: 0 4px !important;
      }'''

if old_mobile_actions in c:
    c = c.replace(old_mobile_actions, new_mobile_actions)
    print("2. Mobile actions CSS updated successfully")
else:
    print("WARNING: old_mobile_actions not found directly")

# 3. Update base CSS for actions row & add sub-actions row
old_base_actions = '''.sim-stage-col {
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
    }
    .sim-actions-row {
      display: flex;
      flex-direction: row;
      gap: 10px;
      width: 100%;
      align-items: stretch;
    }
    .btn-sim-play, .btn-sim-step, .btn-sim-reset {
      flex: 1;
      height: 48px;
      min-height: 48px;
      padding: 0;
      border-radius: 14px;
      font-family: inherit;
      font-size: 1.35rem;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
      box-sizing: border-box;
    }'''

new_base_actions = '''.sim-stage-col {
      display: flex;
      flex-direction: column;
      gap: 10px;
      width: 100%;
    }
    .sim-actions-row {
      display: flex;
      flex-direction: row;
      gap: 10px;
      width: 100%;
      align-items: stretch;
    }
    .btn-sim-play, .btn-sim-step, .btn-sim-reset {
      flex: 1;
      height: 40px;
      min-height: 40px;
      padding: 0;
      border-radius: 12px;
      font-family: inherit;
      font-size: 1.25rem;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
      box-sizing: border-box;
    }
    .sim-sub-actions-row {
      display: flex;
      flex-direction: row;
      gap: 10px;
      width: 100%;
      align-items: stretch;
    }
    .sim-sub-btn {
      flex: 1;
      height: 38px;
      min-height: 38px;
      padding: 0 8px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--inc-card-border);
      color: var(--inc-text-sub);
      font-family: inherit;
      font-size: 0.78rem;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s ease;
      box-sizing: border-box;
      white-space: nowrap;
    }
    .sim-sub-btn:hover {
      background: rgba(255, 255, 255, 0.08);
      color: var(--inc-text);
      transform: translateY(-1px);
    }
    .sim-sub-btn.active {
      background: rgba(16, 185, 129, 0.15);
      border-color: #10B981;
      color: #10B981;
    }
    #btnSpeedCycle.active {
      background: rgba(14, 165, 233, 0.18);
      border-color: #0EA5E9;
      color: #38BDF8;
    }'''

if old_base_actions in c:
    c = c.replace(old_base_actions, new_base_actions)
    print("3. Base actions CSS updated successfully")
else:
    print("WARNING: old_base_actions not found directly")

# 4. Add Light Mode CSS for .sim-sub-btn
old_light_marker = '''    html.light .btn-sim-reset:hover {
      background: #E2E8F0 !important;
      border-color: #94A3B8 !important;
      color: #0F172A !important;
    }'''

new_light_marker = '''    html.light .btn-sim-reset:hover {
      background: #E2E8F0 !important;
      border-color: #94A3B8 !important;
      color: #0F172A !important;
    }
    html.light .sim-sub-btn {
      background: #FFFFFF !important;
      border-color: #CBD5E1 !important;
      color: #475569 !important;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    }
    html.light .sim-sub-btn:hover {
      background: #F8FAFC !important;
      border-color: #94A3B8 !important;
      color: #0F172A !important;
    }
    html.light .sim-sub-btn.active {
      background: #ECFDF5 !important;
      border-color: #10B981 !important;
      color: #059669 !important;
    }
    html.light #btnSpeedCycle.active {
      background: #F0F9FF !important;
      border-color: #0EA5E9 !important;
      color: #0284C7 !important;
    }'''

if old_light_marker in c:
    c = c.replace(old_light_marker, new_light_marker)
    print("4. Light mode CSS for sub-btns added successfully")
else:
    print("WARNING: old_light_marker not found directly")

# 5. Update HTML: Add .sim-sub-actions-row under .sim-actions-row, and remove .sim-options-bar
old_actions_markup = '''          <!-- أزرار التشغيل والتفاعل السريع في صف واحد تحت المعاينة مباشرة بأيقونات معبرة -->
          <div class="sim-actions-row">
            <button class="btn-sim-play" id="btnSimPlay" onclick="playFullSimulation()" title="تشغيل المحاكاة" aria-label="تشغيل المحاكاة">
              <span>▶️</span>
            </button>
            <button class="btn-sim-step" id="btnSimStep" onclick="stepSimulation()" title="خطوة بخطوة" aria-label="خطوة بخطوة">
              <span>⏭️</span>
            </button>
            <button class="btn-sim-reset" onclick="resetSimulation()" title="إعادة ضبط التقاطع" aria-label="إعادة ضبط">
              <span>↺</span>
            </button>
          </div>
        </div>'''

new_actions_markup = '''          <!-- أزرار التشغيل والتفاعل السريع في صف واحد تحت المعاينة مباشرة بأيقونات معبرة -->
          <div class="sim-actions-row">
            <button class="btn-sim-play" id="btnSimPlay" onclick="playFullSimulation()" title="تشغيل المحاكاة" aria-label="تشغيل المحاكاة">
              <span>▶️</span>
            </button>
            <button class="btn-sim-step" id="btnSimStep" onclick="stepSimulation()" title="خطوة بخطوة" aria-label="خطوة بخطوة">
              <span>⏭️</span>
            </button>
            <button class="btn-sim-reset" onclick="resetSimulation()" title="إعادة ضبط التقاطع" aria-label="إعادة ضبط">
              <span>↺</span>
            </button>
          </div>

          <!-- الصف الثاني مباشرة تحت التشغيل: رادار اليمين + صوت الغماز + السرعة التفاعلية بالضغط -->
          <div class="sim-sub-actions-row">
            <button class="sim-sub-btn active" id="btnRadarToggle" onclick="toggleRadar()" title="تفعيل/تعطيل رادار اليمين الخالي">
              <span class="sub-btn-icon">🎯</span>
              <span class="sub-btn-label">رادار اليمين</span>
            </button>
            <button class="sim-sub-btn active" id="btnAudioToggle" onclick="toggleAudio()" title="تشغيل/كتم صوت الغماز">
              <span class="sub-btn-icon" id="btnAudioIcon">🔊</span>
              <span class="sub-btn-label" id="btnAudioText">صوت الغماز</span>
            </button>
            <button class="sim-sub-btn" id="btnSpeedCycle" onclick="cycleSimSpeed()" title="انقر لتغيير السرعة (1.0x عادي / 1.6x سريع / 0.6x بطيء)">
              <span class="sub-btn-icon">⚡</span>
              <span class="sub-btn-label" id="btnSpeedLabel">1.0x عادي</span>
            </button>
          </div>
        </div>'''

if old_actions_markup in c:
    c = c.replace(old_actions_markup, new_actions_markup)
    print("5. HTML actions markup updated successfully")
else:
    print("WARNING: old_actions_markup not found directly")

# Remove redundant .sim-options-bar from .sim-control-panel
old_options_bar = '''          <!-- شريط الخيارات: سرعة الحركة + الصوت + رادار اليمين -->
          <div class="sim-options-bar">
            <div class="sim-speed-wrap">
              <span>السرعة:</span>
              <button class="btn-speed-opt" onclick="setSimSpeed(0.6, this)">0.6x بطيء</button>
              <button class="btn-speed-opt active" onclick="setSimSpeed(1.0, this)">1.0x عادي</button>
              <button class="btn-speed-opt" onclick="setSimSpeed(1.6, this)">1.6x سريع</button>
            </div>
            <div style="display:flex; gap:6px;">
              <button class="sim-toggle-btn active" id="btnRadarToggle" onclick="toggleRadar()">
                <span>🎯 رادار اليمين</span>
              </button>
              <button class="sim-toggle-btn active" id="btnAudioToggle" onclick="toggleAudio()">
                <span>🔊 صوت الغماز</span>
              </button>
            </div>
          </div>'''

if old_options_bar in c:
    c = c.replace(old_options_bar, '')
    print("6. Redundant sim-options-bar removed from control panel")
else:
    print("WARNING: old_options_bar not found directly")

# 7. Update JS for cycleSimSpeed and toggleAudio
old_js_funcs = '''    function setSimSpeed(speed, btn) {
      simSpeedMultiplier = speed;
      document.querySelectorAll('.btn-speed-opt').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
    }

    function toggleRadar() {
      showRadarState = !showRadarState;
      const btn = document.getElementById('btnRadarToggle');
      if (btn) btn.classList.toggle('active', showRadarState);
      document.querySelectorAll('.car-radar-cone').forEach(el => {
        el.style.display = showRadarState ? 'block' : 'none';
      });
    }

    function toggleAudio() {
      audioFxEnabled = !audioFxEnabled;
      const btn = document.getElementById('btnAudioToggle');
      if (btn) {
        btn.classList.toggle('active', audioFxEnabled);
        btn.innerHTML = audioFxEnabled ? '<span>🔊 صوت الغماز</span>' : '<span>🔇 الصوت مكتوم</span>';
      }
    }'''

new_js_funcs = '''    const SIM_SPEED_OPTIONS = [
      { speed: 1.0, label: '1.0x عادي' },
      { speed: 1.6, label: '1.6x سريع' },
      { speed: 0.6, label: '0.6x بطيء' }
    ];
    let currentSpeedIndex = 0;

    function cycleSimSpeed() {
      currentSpeedIndex = (currentSpeedIndex + 1) % SIM_SPEED_OPTIONS.length;
      const opt = SIM_SPEED_OPTIONS[currentSpeedIndex];
      simSpeedMultiplier = opt.speed;
      const labelEl = document.getElementById('btnSpeedLabel');
      if (labelEl) labelEl.textContent = opt.label;
      const btn = document.getElementById('btnSpeedCycle');
      if (btn) {
        btn.classList.toggle('active', opt.speed !== 1.0);
      }
    }

    function setSimSpeed(speed, btn) {
      simSpeedMultiplier = speed;
      const matchIdx = SIM_SPEED_OPTIONS.findIndex(o => o.speed === speed);
      if (matchIdx !== -1) currentSpeedIndex = matchIdx;
      const labelEl = document.getElementById('btnSpeedLabel');
      if (labelEl) labelEl.textContent = (SIM_SPEED_OPTIONS[currentSpeedIndex] || {}).label || `${speed}x`;
      const cycleBtn = document.getElementById('btnSpeedCycle');
      if (cycleBtn) cycleBtn.classList.toggle('active', speed !== 1.0);
    }

    function toggleRadar() {
      showRadarState = !showRadarState;
      const btn = document.getElementById('btnRadarToggle');
      if (btn) btn.classList.toggle('active', showRadarState);
      document.querySelectorAll('.car-radar-cone').forEach(el => {
        el.style.display = showRadarState ? 'block' : 'none';
      });
    }

    function toggleAudio() {
      audioFxEnabled = !audioFxEnabled;
      const btn = document.getElementById('btnAudioToggle');
      if (btn) {
        btn.classList.toggle('active', audioFxEnabled);
        const iconEl = document.getElementById('btnAudioIcon');
        const textEl = document.getElementById('btnAudioText');
        if (iconEl) iconEl.textContent = audioFxEnabled ? '🔊' : '🔇';
        if (textEl) textEl.textContent = audioFxEnabled ? 'صوت الغماز' : 'الصوت صامت';
      }
    }'''

if old_js_funcs in c:
    c = c.replace(old_js_funcs, new_js_funcs)
    print("7. JS functions updated successfully")
else:
    print("WARNING: old_js_funcs not found directly")

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Finished updating decodificatore-incroci.html")

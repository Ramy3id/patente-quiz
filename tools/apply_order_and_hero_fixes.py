with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'r', encoding='utf-8') as f:
    content = f.read()

# -------------------------------------------------------------
# 1. Update .inc-stats-strip and items (Remove loud outlier style)
# -------------------------------------------------------------
old_stats_strip = '''      <div class="inc-stats-strip">
        <div class="inc-stat-item">
          <span>🚗</span>
          <span>415 سؤالاً تغطي كافة تقاطعات الوزارة</span>
        </div>
        <div class="inc-stat-item" style="color:var(--inc-rose); border-color:rgba(244,63,94,0.3);">
          <span>💥</span>
          <span>32 سؤالاً لكلمة contemporaneamente (28 منها FALSO)</span>
        </div>
        <div class="inc-stat-item" style="color:var(--inc-emerald); border-color:rgba(16,185,129,0.3);">
          <span>✨</span>
          <span>1 خوارزمية بصرية تحل أي رسمة بلا استثناء</span>
        </div>
      </div>'''

new_stats_strip = '''      <div class="inc-stats-strip">
        <div class="inc-stat-item">
          <span>🚗</span>
          <span>415 سؤالاً لكافة تقاطعات الوزارة</span>
        </div>
        <div class="inc-stat-item">
          <span>⚡</span>
          <span>32 سؤالاً لفخ Contemporaneamente</span>
        </div>
        <div class="inc-stat-item">
          <span>✨</span>
          <span>خوارزمية بصرية شاملة لحل أي رسمة</span>
        </div>
      </div>'''

if old_stats_strip in content:
    content = content.replace(old_stats_strip, new_stats_strip)
    print("1. Hero stats strip updated successfully")
else:
    print("WARNING: old_stats_strip not found directly")

# Update CSS for .inc-stat-item in light mode
old_light_hero = '''    html.light .traffic-sim-section {'''
new_light_hero = '''    html.light .inc-stat-item {
      background: #FFFFFF !important;
      border-color: #E2E8F0 !important;
      color: #1E293B !important;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    }
    html.light .inc-stat-item:hover {
      border-color: #BAE6FD !important;
      background: #F8FAFC !important;
    }

    html.light .traffic-sim-section {'''

if old_light_hero in content:
    content = content.replace(old_light_hero, new_light_hero)
    print("2. Light mode CSS for inc-stat-item added successfully")
else:
    print("WARNING: old_light_hero not found directly")

# -------------------------------------------------------------
# 2. Update .sim-status-box HTML structure to include .sim-order-card
# -------------------------------------------------------------
old_status_box_html = '''          <!-- بطاقة حالة الترتيب والتفسير القانوني الفوري -->
          <div class="sim-status-box">
            <div class="sim-status-step" id="simStepBadge">🏁 جاهز للمحاكاة</div>
            <div class="sim-status-reason" id="simReasonText">
              اضغط على «▶️ تشغيل المحاكاة» لمشاهدة دوران السيارات وانسيابها وفق قاعدة اليمين الخالي خطوة بخطوة.
            </div>
            <div class="sim-status-order-strip">
              <span>🏆 الترتيب النهائي:</span>
              <span id="simFinalOrderText" style="color:var(--inc-cyan); font-family:'JetBrains Mono',monospace;">B ➔ H ➔ C</span>
            </div>
          </div>'''

new_status_box_html = '''          <!-- بطاقة حالة الترتيب والتفسير القانوني الفوري -->
          <div class="sim-status-box">
            <div class="sim-status-step" id="simStepBadge">🏁 جاهز للمحاكاة</div>
            <div class="sim-status-reason" id="simReasonText">
              اضغط على «▶️ تشغيل المحاكاة» لمشاهدة دوران السيارات وانسيابها وفق قاعدة اليمين الخالي خطوة بخطوة.
            </div>

            <!-- بطاقة الترتيب الأكاديمية الواضحة بدون أي تداخل أو ارتباك -->
            <div class="sim-order-card" id="simOrderCard">
              <div id="simOrderDisplayArea">
                <!-- يتم توليده ديناميكياً بواسطة renderOrderDisplay -->
              </div>
              <span id="simFinalOrderText" style="display:none;">B ➔ H ➔ C</span>
            </div>
          </div>'''

if old_status_box_html in content:
    content = content.replace(old_status_box_html, new_status_box_html)
    print("3. Status box HTML updated successfully")
else:
    print("WARNING: old_status_box_html not found directly")

# -------------------------------------------------------------
# 3. Add CSS for .sim-order-card and sub-elements
# -------------------------------------------------------------
old_order_strip_css = '''.sim-status-order-strip {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-size: 0.92rem;
      font-weight: 800;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.25);
      padding: 8px 14px;
      border-radius: 10px;
    }'''

new_order_card_css = '''.sim-status-order-strip {
      display: none;
    }
    /* حاوية ترتيب وأسبقية عبور السيارات الأكاديمية الاحترافية */
    .sim-order-card {
      background: rgba(15, 23, 42, 0.45);
      border: 1px solid rgba(16, 185, 129, 0.3);
      border-radius: 14px;
      padding: 12px 14px;
      margin-top: 10px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .sim-order-flow-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .sim-order-flow-title {
      font-size: 0.88rem;
      font-weight: 800;
      color: #10B981;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .sim-order-flow-track {
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
    }
    .sim-flow-badge {
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid #38BDF8;
      color: #38BDF8;
      font-size: 0.82rem;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 6px;
      white-space: nowrap;
    }
    .sim-flow-badge.together {
      background: rgba(244, 63, 94, 0.15);
      border-color: #F43F5E;
      color: #FDA4AF;
    }
    .sim-flow-arrow {
      color: var(--inc-text-sub);
      font-size: 0.85rem;
      font-weight: 900;
    }
    .sim-order-steps-grid {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .sim-order-step-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.84rem;
      line-height: 1.4;
      padding: 6px 10px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.04);
    }
    .sim-order-step-item .step-num {
      width: 22px;
      height: 22px;
      min-width: 22px;
      border-radius: 50%;
      background: rgba(16, 185, 129, 0.15);
      color: #10B981;
      border: 1px solid #10B981;
      font-size: 0.72rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .sim-order-step-item .step-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.84rem;
      font-weight: 900;
      color: var(--inc-cyan);
      background: rgba(14, 165, 233, 0.12);
      border: 1px solid rgba(14, 165, 233, 0.3);
      padding: 2px 8px;
      border-radius: 6px;
      min-width: 26px;
      text-align: center;
    }
    .sim-order-step-item.together .step-badge {
      color: #FDA4AF;
      border-color: #F43F5E;
      background: rgba(244, 63, 94, 0.15);
    }
    .sim-order-step-item .step-desc {
      color: var(--inc-text);
      font-weight: 600;
      flex: 1;
    }

    /* أنماط الوضع النهاري لبطاقة الترتيب */
    html.light .sim-order-card {
      background: #F0FDF4 !important;
      border-color: #A7F3D0 !important;
      box-shadow: 0 1px 4px rgba(16, 185, 129, 0.08) !important;
    }
    html.light .sim-order-flow-row {
      border-bottom-color: #D1FAE5 !important;
    }
    html.light .sim-order-flow-title {
      color: #065F46 !important;
    }
    html.light .sim-flow-badge {
      background: #E0F2FE !important;
      border-color: #38BDF8 !important;
      color: #0369A1 !important;
    }
    html.light .sim-flow-badge.together {
      background: #FFE4E6 !important;
      border-color: #FB7185 !important;
      color: #BE123C !important;
    }
    html.light .sim-flow-arrow {
      color: #94A3B8 !important;
    }
    html.light .sim-order-step-item {
      background: #FFFFFF !important;
      border-color: #E2E8F0 !important;
    }
    html.light .sim-order-step-item .step-num {
      background: #ECFDF5 !important;
      color: #059669 !important;
      border-color: #10B981 !important;
    }
    html.light .sim-order-step-item .step-badge {
      background: #E0F2FE !important;
      border-color: #7DD3FC !important;
      color: #0284C7 !important;
    }
    html.light .sim-order-step-item.together .step-badge {
      background: #FFE4E6 !important;
      border-color: #FDA4AF !important;
      color: #E11D48 !important;
    }
    html.light .sim-order-step-item .step-desc {
      color: #1E293B !important;
    }'''

if old_order_strip_css in content:
    content = content.replace(old_order_strip_css, new_order_card_css)
    print("4. Order card CSS added successfully")
else:
    print("WARNING: old_order_strip_css not found directly")

# -------------------------------------------------------------
# 4. Add renderOrderDisplay function and call in loadSimIncrocio
# -------------------------------------------------------------
old_load_incrocio_call = '''        document.getElementById('simFinalOrderText').innerText = data.order.join(' ➔ ');'''
new_load_incrocio_call = '''        renderOrderDisplay(data);'''

if old_load_incrocio_call in content:
    content = content.replace(old_load_incrocio_call, new_load_incrocio_call)
    print("5. loadSimIncrocio call updated to renderOrderDisplay")
else:
    print("WARNING: old_load_incrocio_call not found directly")

old_fallback_call = '''        document.getElementById('simFinalOrderText').innerText = figMeta.vehs || 'قيد المعالجة';'''
new_fallback_call = '''        renderOrderFallback(figMeta);'''

if old_fallback_call in content:
    content = content.replace(old_fallback_call, new_fallback_call)
    print("6. Fallback call updated to renderOrderFallback")
else:
    print("WARNING: old_fallback_call not found directly")

# Add renderOrderDisplay and renderOrderFallback definitions
order_render_js = '''
    function renderOrderDisplay(data) {
      const container = document.getElementById('simOrderDisplayArea');
      if (!container) return;

      if (!data || !data.order || !data.order.length) {
        container.innerHTML = '<div style="font-size:0.82rem; color:var(--inc-text-sub); padding:4px;">قيد التحديث للرسمة</div>';
        return;
      }

      const parsedItems = data.order.map((itemStr, idx) => {
        const raw = (itemStr || '').trim();
        const match = raw.match(/^([^()]+?)(?:\s*\((.*?)\))?$/);
        let label = raw;
        let desc = '';
        if (match) {
          label = match[1].trim();
          desc = match[2] ? match[2].trim() : '';
        }

        let badgeText = label.replace(/\\s*و\\s*/g, ' + ').replace(/\\s*معاً\\s*/g, '').trim();

        let carColor = '#38BDF8';
        if (data.cars && data.cars[badgeText]) {
          carColor = data.cars[badgeText].color || '#38BDF8';
        } else if (data.cars && data.cars[badgeText[0]]) {
          carColor = data.cars[badgeText[0]].color || '#38BDF8';
        }

        if (!desc) {
          desc = label;
        }

        return {
          stepNum: idx + 1,
          badgeText: badgeText,
          desc: desc,
          color: carColor
        };
      });

      // 1. Quick flow letters
      const flowHtml = parsedItems.map((item, i) => {
        const isTogether = item.badgeText.includes('+');
        const badgeClass = isTogether ? 'sim-flow-badge together' : 'sim-flow-badge';
        const arrow = (i < parsedItems.length - 1)
          ? '<span class="sim-flow-arrow">➔</span>'
          : '';
        return '<span class="' + badgeClass + '">' + item.badgeText + '</span>' + arrow;
      }).join('');

      // 2. Step by step list
      const stepsListHtml = parsedItems.map(item => {
        const isTogether = item.badgeText.includes('+');
        const stepClass = isTogether ? 'sim-order-step-item together' : 'sim-order-step-item';
        return '<div class="' + stepClass + '">' +
          '<span class="step-num">' + item.stepNum + '</span>' +
          '<span class="step-badge">' + item.badgeText + '</span>' +
          '<span class="step-desc">' + item.desc + '</span>' +
        '</div>';
      }).join('');

      container.innerHTML = 
        '<div class="sim-order-flow-row">' +
          '<div class="sim-order-flow-title">' +
            '<span>🏆</span>' +
            '<span>تسلسل وأسبقية المرور:</span>' +
          '</div>' +
          '<div class="sim-order-flow-track" dir="ltr">' +
            flowHtml +
          '</div>' +
        '</div>' +
        '<div class="sim-order-steps-grid">' +
          stepsListHtml +
        '</div>';

      const hiddenText = document.getElementById('simFinalOrderText');
      if (hiddenText) {
        hiddenText.innerText = data.order.join(' ➔ ');
      }
    }

    function renderOrderFallback(figMeta) {
      const container = document.getElementById('simOrderDisplayArea');
      if (!container) return;
      const vehs = (figMeta && figMeta.vehs) ? figMeta.vehs : 'قيد المعالجة';
      container.innerHTML = 
        '<div class="sim-order-flow-row">' +
          '<div class="sim-order-flow-title">' +
            '<span>🏆</span>' +
            '<span>مركبات التقاطع:</span>' +
          '</div>' +
          '<div class="sim-order-flow-track" dir="ltr">' +
            '<span class="sim-flow-badge">' + vehs + '</span>' +
          '</div>' +
        '</div>';
      const hiddenText = document.getElementById('simFinalOrderText');
      if (hiddenText) hiddenText.innerText = vehs;
    }
'''

# Insert functions right before loadSimIncrocio
old_load_func = '''    function loadSimIncrocio(key, btn) {'''
new_load_func = order_render_js + '\n    function loadSimIncrocio(key, btn) {'

if old_load_func in content:
    content = content.replace(old_load_func, new_load_func)
    print("7. JS render functions inserted successfully")
else:
    print("WARNING: old_load_func not found directly")

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\decodificatore-incroci.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating decodificatore-incroci.html for order card and stats strip")

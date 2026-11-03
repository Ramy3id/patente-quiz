with open('R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = """      <!-- 4. لوحة الجاهزية وبنك الأخطاء -->
      <a href="../interactive_pages/dashboard.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(245, 158, 11, 0.12); color: #F59E0B;">⚠️</div>
        <div class="bento-info">
          <div class="bento-title">بنك الأخطاء والجاهزية</div>
          <div class="bento-meta">تتبع تقدمك الذكي</div>
        </div>
      </a>

      <!-- 5. معمل الأرقام والمقاييس -->
      <a href="../interactive_pages/laboratorio-numeri.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(139, 92, 246, 0.12); color: #8B5CF6;">📐</div>
        <div class="bento-info">
          <div class="bento-title">معمل الأرقام والمقاييس</div>
          <div class="bento-meta">السرعات والمسافات</div>
        </div>
      </a>

      <!-- 6. معجم المترادفات والبدائل -->
      <a href="dizionario-sinonimi.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(6, 182, 212, 0.12); color: #06B6D4;">📖</div>
        <div class="bento-info">
          <div class="bento-title">معجم المترادفات</div>
          <div class="bento-meta">فروق الوزارة الخادعة</div>
        </div>
      </a>
    </div>

    <!-- المعامل الإضافية الـ 7 (قابلة للطي والتوسيع على الموبايل، ظاهرة في الديسكتوب) -->
    <div class="bento-grid bento-extra-grid" id="bentoExtraGrid" style="display: none; margin-top: 10px;">"""

replacement = """      <!-- 4. لوحة الجاهزية وبنك الأخطاء -->
      <a href="../interactive_pages/dashboard.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(245, 158, 11, 0.12); color: #F59E0B;">⚠️</div>
        <div class="bento-info">
          <div class="bento-title">بنك الأخطاء والجاهزية</div>
          <div class="bento-meta">تتبع تقدمك الذكي</div>
        </div>
      </a>
    </div>

    <!-- المعامل الإضافية الـ 9 (ديناميكية مع زر العرض والطي) -->
    <div class="bento-grid bento-extra-grid" id="bentoExtraGrid" style="margin-top: 8px;">
      <!-- 5. معمل الأرقام والمقاييس -->
      <a href="../interactive_pages/laboratorio-numeri.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(139, 92, 246, 0.12); color: #8B5CF6;">📐</div>
        <div class="bento-info">
          <div class="bento-title">معمل الأرقام والمقاييس</div>
          <div class="bento-meta">السرعات والمسافات</div>
        </div>
      </a>

      <!-- 6. معجم المترادفات والبدائل -->
      <a href="dizionario-sinonimi.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(6, 182, 212, 0.12); color: #06B6D4;">📖</div>
        <div class="bento-info">
          <div class="bento-title">معجم المترادفات</div>
          <div class="bento-meta">فروق الوزارة الخادعة</div>
        </div>
      </a>"""

c_norm = c.replace('\r\n', '\n')
t_norm = target.replace('\r\n', '\n')
r_norm = replacement.replace('\r\n', '\n')

if t_norm in c_norm:
    c_norm = c_norm.replace(t_norm, r_norm, 1)
    with open('R:/Ramy/PATENTE_PRO_APP/Capitoli_Divisi/index.html', 'w', encoding='utf-8') as f:
        f.write(c_norm)
    print("SUCCESS: 4 primary tools + 9 extra tools split cleanly!")
else:
    print("ERROR: target block not found")

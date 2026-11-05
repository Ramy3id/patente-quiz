import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_bento_block = '''<!-- الشبكة الرئيسية: أول 6 معامل أساسية تظهر فوراً -->
    <div class="bento-grid">
      <!-- 1. محاكي الامتحان -->
      <a href="../interactive_pages/scheda-esame.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(14, 165, 233, 0.12); color: #0EA5E9;">⏱️</div>
        <div class="bento-info">
          <div class="bento-title">محاكي الامتحان</div>
          <div class="bento-meta">30 سؤالاً • 20 دقيقة</div>
        </div>
      </a>

      <!-- 2. رادار الكلمات السحرية -->
      <a href="../interactive_pages/parole-spia.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(236, 72, 153, 0.12); color: #EC4899;">🎯</div>
        <div class="bento-info">
          <div class="bento-title">رادار الكلمات السحرية</div>
          <div class="bento-meta">حسم 462 سؤالاً V/F</div>
        </div>
      </a>

      <!-- 3. مفكك التقاطعات -->
      <a href="../interactive_pages/decodificatore-incroci.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(16, 185, 129, 0.12); color: #10B981;">🔄</div>
        <div class="bento-info">
          <div class="bento-title">مفكك التقاطعات</div>
          <div class="bento-meta">أسبقيات الباب 14</div>
        </div>
      </a>

      <!-- 4. لوحة الجاهزية وبنك الأخطاء -->
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
      </a>
      <!-- 7. تحدي الـ 0 أخطاء -->
      <a href="../interactive_pages/zero-mistake.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(239, 68, 68, 0.12); color: #EF4444;">🎮</div>
        <div class="bento-info">
          <div class="bento-title">تحدي الـ 0 أخطاء</div>
          <div class="bento-meta">وضع البقاء الناري</div>
        </div>
      </a>

      <!-- 8. مفكك الـ 3 كتل -->
      <a href="../interactive_pages/allenamento-capitolo.html?mode=decoder&count=20" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(59, 130, 246, 0.12); color: #3B82F6;">🧩</div>
        <div class="bento-info">
          <div class="bento-title">مفكك الـ 3 كتل</div>
          <div class="bento-meta">المعادلة المنطقية</div>
        </div>
      </a>

      <!-- 9. خزينة التريكات ودستور الأبواب -->
      <a href="../interactive_pages/trucchi-esame.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(234, 179, 8, 0.12); color: #EAB308;">💎</div>
        <div class="bento-info">
          <div class="bento-title">دستور التريكات</div>
          <div class="bento-meta">كبسولات A4 ليلة الامتحان</div>
        </div>
      </a>

      <!-- 10. كبسولة الإسعافات والكحول -->
      <a href="Capitolo_22_alcool_droga_primo_soccorso/index.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(16, 185, 129, 0.12); color: #10B981;">🚑</div>
        <div class="bento-info">
          <div class="bento-title">الإسعافات والكحول</div>
          <div class="bento-meta">الباب 22 في 96 سؤالاً</div>
        </div>
      </a>

      <!-- 11. محرك البحث الوزاري -->
      <a href="../interactive_pages/cerca-quiz.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(14, 165, 233, 0.12); color: #0EA5E9;">🔍</div>
        <div class="bento-info">
          <div class="bento-title">محرك البحث الوزاري</div>
          <div class="bento-meta">بحث صوتي ولحظي</div>
        </div>
      </a>

      <!-- 12. خطة المذاكرة الذكية -->
      <a href="../interactive_pages/piano-studio.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(168, 85, 247, 0.12); color: #A855F7;">📅</div>
        <div class="bento-info">
          <div class="bento-title">خطة الـ 30 يوماً</div>
          <div class="bento-meta">جدول إتقان المنهج</div>
        </div>
      </a>

      <!-- 13. بنك كلماتي ومستكشف الفخاخ -->
      <a href="parole-quiz.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(249, 115, 22, 0.12); color: #F97316;">🔤</div>
        <div class="bento-info">
          <div class="bento-title">بنك كلماتي ومستكشف الفخاخ</div>
          <div class="bento-meta">قاموس المشتقات والمصطلحات</div>
        </div>
      </a>
    </div>'''

new_bento_block = '''<!-- الشبكة الرئيسية: أول 4 معامل أساسية تظهر فوراً -->
    <div class="bento-grid">
      <!-- 1. خطة المذاكرة الذكية (خطة الـ 30 يوماً في المركز الأول) -->
      <a href="../interactive_pages/piano-studio.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(168, 85, 247, 0.12); color: #A855F7;">📅</div>
        <div class="bento-info">
          <div class="bento-title">خطة الـ 30 يوماً</div>
          <div class="bento-meta">جدول إتقان المنهج</div>
        </div>
      </a>

      <!-- 2. محاكي الامتحان -->
      <a href="../interactive_pages/scheda-esame.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(14, 165, 233, 0.12); color: #0EA5E9;">⏱️</div>
        <div class="bento-info">
          <div class="bento-title">محاكي الامتحان</div>
          <div class="bento-meta">30 سؤالاً • 20 دقيقة</div>
        </div>
      </a>

      <!-- 3. رادار الكلمات السحرية -->
      <a href="../interactive_pages/parole-spia.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(236, 72, 153, 0.12); color: #EC4899;">🎯</div>
        <div class="bento-info">
          <div class="bento-title">رادار الكلمات السحرية</div>
          <div class="bento-meta">حسم 462 سؤالاً V/F</div>
        </div>
      </a>

      <!-- 4. مفكك التقاطعات -->
      <a href="../interactive_pages/decodificatore-incroci.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(16, 185, 129, 0.12); color: #10B981;">🔄</div>
        <div class="bento-info">
          <div class="bento-title">مفكك التقاطعات</div>
          <div class="bento-meta">أسبقيات الباب 14</div>
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
      </a>
      <!-- 7. تحدي الـ 0 أخطاء -->
      <a href="../interactive_pages/zero-mistake.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(239, 68, 68, 0.12); color: #EF4444;">🎮</div>
        <div class="bento-info">
          <div class="bento-title">تحدي الـ 0 أخطاء</div>
          <div class="bento-meta">وضع البقاء الناري</div>
        </div>
      </a>

      <!-- 8. مفكك الـ 3 كتل -->
      <a href="../interactive_pages/allenamento-capitolo.html?mode=decoder&count=20" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(59, 130, 246, 0.12); color: #3B82F6;">🧩</div>
        <div class="bento-info">
          <div class="bento-title">مفكك الـ 3 كتل</div>
          <div class="bento-meta">المعادلة المنطقية</div>
        </div>
      </a>

      <!-- 9. خزينة التريكات ودستور الأبواب -->
      <a href="../interactive_pages/trucchi-esame.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(234, 179, 8, 0.12); color: #EAB308;">💎</div>
        <div class="bento-info">
          <div class="bento-title">دستور التريكات</div>
          <div class="bento-meta">كبسولات A4 ليلة الامتحان</div>
        </div>
      </a>

      <!-- 10. كبسولة الإسعافات والكحول -->
      <a href="Capitolo_22_alcool_droga_primo_soccorso/index.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(16, 185, 129, 0.12); color: #10B981;">🚑</div>
        <div class="bento-info">
          <div class="bento-title">الإسعافات والكحول</div>
          <div class="bento-meta">الباب 22 في 96 سؤالاً</div>
        </div>
      </a>

      <!-- 11. محرك البحث الوزاري -->
      <a href="../interactive_pages/cerca-quiz.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(14, 165, 233, 0.12); color: #0EA5E9;">🔍</div>
        <div class="bento-info">
          <div class="bento-title">محرك البحث الوزاري</div>
          <div class="bento-meta">بحث صوتي ولحظي</div>
        </div>
      </a>

      <!-- 12. لوحة الجاهزية وبنك الأخطاء -->
      <a href="../interactive_pages/dashboard.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(245, 158, 11, 0.12); color: #F59E0B;">⚠️</div>
        <div class="bento-info">
          <div class="bento-title">بنك الأخطاء والجاهزية</div>
          <div class="bento-meta">تتبع تقدمك الذكي</div>
        </div>
      </a>

      <!-- 13. بنك كلماتي ومستكشف الفخاخ -->
      <a href="parole-quiz.html" class="bento-card" onclick="if(window.soundEngine)soundEngine.click()">
        <div class="bento-icon-box" style="background: rgba(249, 115, 22, 0.12); color: #F97316;">🔤</div>
        <div class="bento-info">
          <div class="bento-title">بنك كلماتي ومستكشف الفخاخ</div>
          <div class="bento-meta">قاموس المشتقات والمصطلحات</div>
        </div>
      </a>
    </div>'''

if old_bento_block in content:
    content = content.replace(old_bento_block, new_bento_block, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Swapped plan card to position #1 in Capitoli_Divisi/index.html successfully!")
else:
    print("ERROR: old_bento_block not found in content!")
    sys.exit(1)

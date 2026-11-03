import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\dizionario-sinonimi.html'

with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Hero Markup
old_hero = '''    <div class="glass-card hero-main-card">
      <h1>
        <span>📖</span>
        <span>معجم المترادفات وفروق الوزارة الخادعة</span>
      </h1>
      <p>
        المعجم الأكاديمي الشامل للكلمات ذات نفس المعنى القانوني في رخصة القيادة الإيطالية (<span dir="ltr">Codice della Strada</span>). مصمم خصيصاً لتفكيك <strong>الفروق الخادعة وفخاخ الوزارة (<span dir="ltr">Falsi Sinonimi</span>)</strong> التي يتعمد واضع الامتحان استخدامها لإرباك الطلاب.
      </p>
      <div class="hero-stats-strip">
        <div class="hero-stat-card stat-families">
          <div class="stat-num" id="statTotalFamilies">18</div>
          <div class="stat-label">📚 العائلات الدلالية</div>
        </div>
        <div class="hero-stat-card stat-synonyms">
          <div class="stat-num" id="statTotalSyns">85+</div>
          <div class="stat-label">🟢 المترادفات القانونية</div>
        </div>
        <div class="hero-stat-card stat-traps">
          <div class="stat-num" id="statTotalTraps">38</div>
          <div class="stat-label">🔴 الفخاخ المفككة</div>
        </div>
      </div>
    </div>'''

new_hero = '''    <div class="glass-card hero-main-card">
      <div class="hero-pill-badge">
        <span>📖</span>
        <span>معجم رخصة القيادة الإيطالية</span>
      </div>
      <h1 class="hero-page-title">معجم المترادفات وفروق الوزارة الخادعة</h1>
      <p class="hero-page-desc">
        المعجم الأكاديمي الشامل للكلمات ذات نفس المعنى القانوني في رخصة القيادة (<span dir="ltr">Codice della Strada</span>). مصمم خصيصاً لتفكيك <strong>الفروق الخادعة وفخاخ الامتحان (<span dir="ltr">Falsi Sinonimi</span>)</strong> التي يتعمد واضع الامتحان استخدامها لإرباك الطلاب.
      </p>
      <div class="hero-stats-strip">
        <div class="hero-stat-card stat-families">
          <div class="stat-num" id="statTotalFamilies">18</div>
          <div class="stat-label">📚 العائلات</div>
        </div>
        <div class="hero-stat-card stat-synonyms">
          <div class="stat-num" id="statTotalSyns">64+</div>
          <div class="stat-label">🟢 المترادفات</div>
        </div>
        <div class="hero-stat-card stat-traps">
          <div class="stat-num" id="statTotalTraps">43</div>
          <div class="stat-label">🔴 فخاخ الوزارة</div>
        </div>
      </div>
    </div>'''

if old_hero in text:
    text = text.replace(old_hero, new_hero, 1)
    print("Updated Hero markup successfully")
else:
    print("Warning: old_hero not found")

# 2. Fix JS headings bidirectional structure
old_js_syn = '''            <div class="synonyms-section">
              <h4>
                <span>🟢</span>
                <span>المترادفات الحقيقية في قانون السير <bdi>(Sinonimi)</bdi>:</span>
              </h4>'''

new_js_syn = '''            <div class="synonyms-section">
              <h4>
                <span>🟢</span>
                <span>المترادفات الحقيقية في قانون السير:</span>
                <span dir="ltr" class="section-tag-ltr">(Sinonimi)</span>
              </h4>'''

if old_js_syn in text:
    text = text.replace(old_js_syn, new_js_syn, 1)
    print("Updated JS syn heading")

old_js_trap = '''            <div class="traps-section" style="margin-top:12px;">
              <h4>
                <span>🔴</span>
                <span>انتبه! مترادفات خادعة وفروق قاتلة <bdi>(Falsi Sinonimi)</bdi>:</span>
              </h4>'''

new_js_trap = '''            <div class="traps-section" style="margin-top:12px;">
              <h4>
                <span>🔴</span>
                <span>انتبه! مترادفات خادعة وفروق قاتلة:</span>
                <span dir="ltr" class="section-tag-ltr">(Falsi Sinonimi)</span>
              </h4>'''

if old_js_trap in text:
    text = text.replace(old_js_trap, new_js_trap, 1)
    print("Updated JS trap heading")

# 3. Add refined styles
refined_css = '''
    /* Refined Hero Elements */
    .hero-pill-badge {
      display: inline-flex !important;
      align-items: center !important;
      gap: 6px !important;
      padding: 5px 12px !important;
      border-radius: 999px !important;
      background: rgba(56, 189, 248, 0.12) !important;
      border: 1px solid rgba(56, 189, 248, 0.28) !important;
      color: #38BDF8 !important;
      font-size: 0.78rem !important;
      font-weight: 700 !important;
      margin-bottom: 12px !important;
    }
    html.light .hero-pill-badge {
      background: rgba(2, 132, 199, 0.08) !important;
      border-color: rgba(2, 132, 199, 0.25) !important;
      color: #0284C7 !important;
    }
    .hero-page-title {
      font-size: 1.45rem !important;
      font-weight: 800 !important;
      line-height: 1.3 !important;
      margin-bottom: 10px !important;
      color: #FFFFFF !important;
      text-align: right !important;
    }
    html.light .hero-page-title {
      color: #0F172A !important;
    }
    .hero-page-desc {
      font-size: 0.88rem !important;
      line-height: 1.6 !important;
      color: var(--text-secondary) !important;
      margin-bottom: 16px !important;
      text-align: right !important;
    }
    html.light .hero-page-desc {
      color: #475569 !important;
    }
    .search-input {
      direction: rtl !important;
      text-align: right !important;
      padding-right: 48px !important;
      padding-left: 16px !important;
    }
    .section-tag-ltr {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.82rem !important;
      font-weight: 700 !important;
      opacity: 0.85 !important;
      margin-right: 4px !important;
    }
'''

style_idx = text.find('</style>')
if style_idx != -1:
    text = text[:style_idx] + refined_css + '\n' + text[style_idx:]
    print("Appended refined CSS successfully")

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated file successfully")

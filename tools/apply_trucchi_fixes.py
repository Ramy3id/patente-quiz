import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\trucchi-esame.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Hero and Tabs CSS
old_css_part = """    /* الهيرو والترحيب */
    .tr-hero {
      text-align: center;
      padding: 28px 16px 32px;
      background: linear-gradient(180deg, rgba(168, 85, 247, 0.12) 0%, rgba(15, 23, 42, 0) 100%);
      border-radius: 24px;
      margin-bottom: 24px;
      border: 1px solid var(--tr-card-border);
    }
    html.light .tr-hero {
      background: linear-gradient(180deg, rgba(168, 85, 247, 0.08) 0%, rgba(255, 255, 255, 0) 100%);
    }

    .tr-badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(168, 85, 247, 0.15);
      color: #C084FC;
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 800;
      margin-bottom: 12px;
      border: 1px solid rgba(168, 85, 247, 0.3);
    }

    .tr-title {
      font-size: 1.95rem;
      font-weight: 900;
      margin: 0 0 10px;
      color: var(--tr-text);
      letter-spacing: -0.5px;
    }

    .tr-subtitle {
      font-size: 1rem;
      color: var(--tr-text-sub);
      max-width: 760px;
      margin: 0 auto 18px;
      line-height: 1.6;
    }

    .tr-stats-strip {
      display: flex;
      justify-content: center;
      gap: 14px;
      flex-wrap: wrap;
      margin-top: 14px;
    }
    .tr-stat-item {
      background: var(--tr-card-bg);
      border: 1px solid var(--tr-card-border);
      padding: 8px 16px;
      border-radius: 12px;
      font-size: 0.85rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* تبويبات الأقسام */
    .tr-tabs-nav {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--tr-card-border);
    }
    .tr-tab-btn {
      background: var(--tr-card-bg);
      border: 1px solid var(--tr-card-border);
      color: var(--tr-text-sub);
      padding: 10px 18px;
      border-radius: 12px;
      font-family: inherit;
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
      transition: all 0.2s;
    }
    .tr-tab-btn:hover {
      color: var(--tr-text);
      border-color: rgba(168, 85, 247, 0.4);
    }
    .tr-tab-btn.active {
      background: #A855F7;
      color: #FFFFFF;
      border-color: #A855F7;
      font-weight: 800;
      box-shadow: 0 4px 14px rgba(168, 85, 247, 0.35);
    }"""

new_css_part = """    /* الهيرو والترحيب */
    .tr-hero {
      text-align: center;
      padding: 24px 16px 24px;
      background: linear-gradient(180deg, rgba(168, 85, 247, 0.12) 0%, rgba(15, 23, 42, 0) 100%);
      border-radius: 24px;
      margin-bottom: 20px;
      border: 1px solid var(--tr-card-border);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    html.light .tr-hero {
      background: linear-gradient(180deg, rgba(168, 85, 247, 0.08) 0%, rgba(255, 255, 255, 0) 100%);
      box-shadow: 0 4px 20px rgba(168, 85, 247, 0.06);
    }

    .tr-badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(168, 85, 247, 0.15);
      color: #C084FC;
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 800;
      margin-bottom: 12px;
      border: 1px solid rgba(168, 85, 247, 0.3);
      max-width: 95%;
      box-sizing: border-box;
      line-height: 1.3;
    }
    html.light .tr-badge-pill {
      background: #F3E8FF;
      color: #7E22CE;
      border-color: #E9D5FF;
    }

    .tr-title {
      font-size: clamp(1.35rem, 4.5vw, 1.95rem);
      font-weight: 900;
      margin: 0 0 10px;
      color: var(--tr-text);
      letter-spacing: -0.5px;
      line-height: 1.3;
    }

    .tr-subtitle {
      font-size: 0.92rem;
      color: var(--tr-text-sub);
      max-width: 720px;
      margin: 0 auto 16px;
      line-height: 1.6;
    }

    /* بطاقات إحصائيات الهيرو - شبكة متناسقة بدون تراكم رأسي */
    .tr-stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      max-width: 720px;
      margin: 16px auto 0;
    }
    .tr-stat-card {
      background: var(--tr-card-bg);
      border: 1px solid var(--tr-card-border);
      padding: 12px 6px;
      border-radius: 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      transition: all 0.2s ease;
    }
    .tr-stat-card:hover {
      transform: translateY(-2px);
    }
    .tr-stat-card.stat-cyan { border-color: rgba(56, 189, 248, 0.3); }
    .tr-stat-card.stat-purple { border-color: rgba(168, 85, 247, 0.3); }
    .tr-stat-card.stat-emerald { border-color: rgba(16, 185, 129, 0.3); }

    html.light .tr-stat-card {
      background: #FFFFFF;
      border-color: #E2E8F0;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }
    html.light .tr-stat-card.stat-cyan { border-color: #BAE6FD; }
    html.light .tr-stat-card.stat-purple { border-color: #E9D5FF; }
    html.light .tr-stat-card.stat-emerald { border-color: #A7F3D0; }

    .tr-stat-val {
      font-family: 'JetBrains Mono', 'Cairo', sans-serif;
      font-size: clamp(1.15rem, 3.2vw, 1.45rem);
      font-weight: 900;
      line-height: 1.2;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
    }
    .stat-cyan .tr-stat-val { color: var(--tr-cyan); }
    .stat-purple .tr-stat-val { color: #C084FC; }
    .stat-emerald .tr-stat-val { color: var(--tr-emerald); }
    html.light .stat-cyan .tr-stat-val { color: #0284C7; }
    html.light .stat-purple .tr-stat-val { color: #9333EA; }
    html.light .stat-emerald .tr-stat-val { color: #059669; }

    .tr-stat-label {
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--tr-text-sub);
      line-height: 1.25;
    }
    html.light .tr-stat-label {
      color: #64748B;
    }

    /* تبويبات الأقسام - شبكة متجاوبة بدون أي اسكرول أفقي */
    .tr-tabs-nav {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin-bottom: 24px;
      overflow-x: visible;
      padding-bottom: 0;
      border-bottom: none;
    }
    @media (min-width: 768px) {
      .tr-tabs-nav {
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
      }
    }
    .tr-tab-btn {
      min-height: 48px;
      padding: 10px 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 700;
      border-radius: 14px;
      background: var(--tr-card-bg);
      border: 1px solid var(--tr-card-border);
      color: var(--tr-text-sub);
      cursor: pointer;
      white-space: normal;
      line-height: 1.35;
      width: 100%;
      box-sizing: border-box;
      transition: all 0.2s ease;
    }
    @media (max-width: 767px) {
      .tr-tab-btn:last-child {
        grid-column: 1 / -1;
      }
    }
    .tr-tab-btn:hover {
      color: var(--tr-text);
      border-color: rgba(168, 85, 247, 0.4);
      transform: translateY(-1px);
    }
    .tr-tab-btn.active {
      background: #A855F7;
      color: #FFFFFF !important;
      border-color: #A855F7 !important;
      font-weight: 800;
      box-shadow: 0 4px 14px rgba(168, 85, 247, 0.35);
    }
    html.light .tr-tab-btn {
      background: #FFFFFF;
      border-color: #E2E8F0;
      color: #475569;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    html.light .tr-tab-btn:hover {
      background: #F8FAFC;
      color: #0F172A;
      border-color: #CBD5E1;
    }
    html.light .tr-tab-btn.active {
      background: #9333EA !important;
      color: #FFFFFF !important;
      border-color: #9333EA !important;
      box-shadow: 0 4px 12px rgba(147, 51, 234, 0.25);
    }"""

# 2. Update HTML Hero markup & Tabs markup
old_html_part = """    <!-- قسم الهيرو -->
    <section class="tr-hero">
      <div class="tr-badge-pill">
        <span>💎</span>
        <span>دستور الهندسة العكسية | Trucchi e Scorciatoie</span>
      </div>
      <h1 class="tr-title">خزينة التريكات ودستور الأبواب الـ 25</h1>
      <p class="tr-subtitle">
        الخلاصة الجنائية الشاملة لكافة قواعد وخبايا امتحان الباتنتي B الإيطالي؛ تم تحويل 7,139 سؤالاً إلى معادلات ذهبية تحسم الأسئلة في ثوانٍ.
      </p>

      <div class="tr-stats-strip">
        <div class="tr-stat-item">
          <span>📊</span>
          <span>7,139 سؤالاً تم تشريحها هندسياً</span>
        </div>
        <div class="tr-stat-item" style="color:var(--tr-purple); border-color:rgba(168,85,247,0.3);">
          <span>📜</span>
          <span>25 باباً ملخصة في سطور ذهبية</span>
        </div>
        <div class="tr-stat-item" style="color:var(--tr-emerald); border-color:rgba(16,185,129,0.3);">
          <span>⚡</span>
          <span>حسم فوري للأفخاخ بدون حفظ عشوائي</span>
        </div>
      </div>
    </section>

    <!-- شريط التبويبات -->
    <nav class="tr-tabs-nav">
      <button class="tr-tab-btn active" onclick="switchTab('constitution', this)">
        <span>📜</span>
        <span>دستور الأبواب الـ 25</span>
      </button>
      <button class="tr-tab-btn" onclick="switchTab('duals', this)">
        <span>🎭</span>
        <span>فخاخ اللوحات والمصطلحات التوأم</span>
      </button>
      <button class="tr-tab-btn" onclick="switchTab('responsibility', this)">
        <span>⚖️</span>
        <span>مثلث المسؤولية والتأمين</span>
      </button>
      <button class="tr-tab-btn" onclick="switchTab('physics', this)">
        <span>🔧</span>
        <span>فيزياء وميكانيكا الحركة</span>
      </button>
      <button class="tr-tab-btn" onclick="switchTab('quiz', this)">
        <span>⚡</span>
        <span>كويز التحدي الشامل</span>
      </button>
    </nav>"""

new_html_part = """    <!-- قسم الهيرو -->
    <section class="tr-hero">
      <div class="tr-badge-pill">
        <span>💎</span>
        <span>دستور الهندسة العكسية • Trucchi e Scorciatoie</span>
      </div>
      <h1 class="tr-title">خزينة التريكات ودستور الأبواب الـ 25</h1>
      <p class="tr-subtitle">
        الخلاصة الجنائية الشاملة لكافة قواعد وخبايا امتحان الباتنتي B الإيطالي؛ تم تحويل 7,139 سؤالاً إلى معادلات ذهبية تحسم الأسئلة في ثوانٍ.
      </p>

      <div class="tr-stats-grid">
        <div class="tr-stat-card stat-cyan">
          <div class="tr-stat-val">
            <span style="font-size:0.95em;">📊</span>
            <span>7,139</span>
          </div>
          <div class="tr-stat-label">سؤالاً مشرحاً هندسياً</div>
        </div>
        <div class="tr-stat-card stat-purple">
          <div class="tr-stat-val">
            <span style="font-size:0.95em;">📜</span>
            <span>25</span>
          </div>
          <div class="tr-stat-label">باباً بسطور ذهبية</div>
        </div>
        <div class="tr-stat-card stat-emerald">
          <div class="tr-stat-val">
            <span style="font-size:0.95em;">⚡</span>
            <span>100%</span>
          </div>
          <div class="tr-stat-label">حسم فوري للأفخاخ</div>
        </div>
      </div>
    </section>

    <!-- شريط التبويبات -->
    <nav class="tr-tabs-nav">
      <button class="tr-tab-btn active" onclick="switchTab('constitution', this)">
        <span>📜</span>
        <span>دستور الأبواب الـ 25</span>
      </button>
      <button class="tr-tab-btn" onclick="switchTab('duals', this)">
        <span>🎭</span>
        <span>فخاخ اللوحات والمصطلحات</span>
      </button>
      <button class="tr-tab-btn" onclick="switchTab('responsibility', this)">
        <span>⚖️</span>
        <span>مثلث المسؤولية والتأمين</span>
      </button>
      <button class="tr-tab-btn" onclick="switchTab('physics', this)">
        <span>🔧</span>
        <span>فيزياء وميكانيكا الحركة</span>
      </button>
      <button class="tr-tab-btn" onclick="switchTab('quiz', this)">
        <span>⚡</span>
        <span>كويز التحدي الشامل</span>
      </button>
    </nav>"""

# Normalize line endings
content_norm = content.replace('\r\n', '\n')
old_css_norm = old_css_part.replace('\r\n', '\n')
new_css_norm = new_css_part.replace('\r\n', '\n')

old_html_norm = old_html_part.replace('\r\n', '\n')
new_html_norm = new_html_part.replace('\r\n', '\n')

if old_css_norm not in content_norm:
    print("Error: old_css_norm not found!")
    sys.exit(1)

content_norm = content_norm.replace(old_css_norm, new_css_norm, 1)

if old_html_norm not in content_norm:
    print("Error: old_html_norm not found!")
    sys.exit(1)

content_norm = content_norm.replace(old_html_norm, new_html_norm, 1)

# Write back preserving \r\n if needed
if '\r\n' in content:
    content_final = content_norm.replace('\n', '\r\n')
else:
    content_final = content_norm

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content_final)

print("Successfully applied trucchi updates!")

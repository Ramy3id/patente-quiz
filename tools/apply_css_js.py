import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# CSS to add before </style>
new_css = """
    /* شريط الأدوات المساعدة الذكية في بلوك مستقل */
    .tr-smart-tools-card {
      background: var(--tr-surface);
      border: 1px solid var(--tr-border);
      border-radius: var(--tr-radius);
      padding: 10px 14px;
      margin-bottom: 16px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }

    .tr-smart-tools-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      align-items: center;
    }

    .tr-smart-tool-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 12px;
      border-radius: 10px;
      font-size: 0.88rem;
      font-weight: 700;
      cursor: pointer;
      font-family: inherit;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--tr-border);
      color: var(--tr-text-sub);
      transition: all 0.2s ease;
      min-height: 44px;
      white-space: nowrap;
    }

    .tr-smart-tool-btn:hover {
      background: rgba(255, 255, 255, 0.08);
      color: var(--tr-text);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .tr-smart-tool-btn.active {
      background: rgba(99, 102, 241, 0.18);
      border-color: var(--tr-indigo);
      color: #FFFFFF;
      box-shadow: 0 0 12px rgba(99, 102, 241, 0.35);
      font-weight: 800;
    }

    /* توسيط أزرار الصح والخطأ في منتصف الكارت بدقة */
    .tr-choice-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(130px, 220px)) !important;
      justify-content: center !important;
      gap: 16px;
      margin: 24px auto 16px !important;
      width: 100%;
    }

    /* شريط التنقل المتناسق (السابق / الخطة / التالي) */
    .tr-card-footer {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 24px;
      gap: 12px;
      width: 100%;
    }

    .tr-nav-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      gap: 12px;
    }

    .tr-nav-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 20px;
      border-radius: 12px;
      font-size: 0.95rem;
      font-weight: 800;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s ease;
      min-height: 44px;
      white-space: nowrap;
    }

    .tr-nav-prev {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--tr-border);
      color: var(--tr-text);
    }
    .tr-nav-prev:hover:not(:disabled) {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.25);
    }
    .tr-nav-prev:disabled {
      opacity: 0.35;
      cursor: not-allowed;
    }

    .tr-nav-next {
      background: linear-gradient(135deg, #0284C7, #0EA5E9);
      border: 1px solid rgba(14, 165, 233, 0.5);
      color: #FFFFFF;
      box-shadow: 0 4px 14px rgba(14, 165, 233, 0.35);
    }
    .tr-nav-next:hover {
      background: linear-gradient(135deg, #0369A1, #0284C7);
      box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
      transform: translateY(-1px);
    }
    .tr-nav-next.highlight-next {
      animation: pulseNext 1.5s infinite;
    }

    .tr-nav-plan-link {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: 10px;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--tr-cyan);
      background: rgba(56, 189, 248, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.25);
      text-decoration: none;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .tr-nav-plan-link:hover {
      background: rgba(56, 189, 248, 0.16);
      border-color: var(--tr-cyan);
    }

    .tr-srs-tip {
      width: 100%;
      text-align: center;
      font-size: 0.82rem;
      color: var(--tr-text-sub);
      padding-top: 10px;
      border-top: 1px dashed rgba(255, 255, 255, 0.08);
    }

    /* Light Mode Overrides */
    html.light .tr-smart-tools-card {
      background: #FFFFFF;
      border-color: #E2E8F0;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
    }

    html.light .tr-smart-tool-btn {
      background: #F8FAFC;
      border-color: #E2E8F0;
      color: #475569;
    }

    html.light .tr-smart-tool-btn:hover {
      background: #F1F5F9;
      color: #0F172A;
      border-color: #CBD5E1;
    }

    html.light .tr-smart-tool-btn.active {
      background: #EEF2FF;
      border-color: #6366F1;
      color: #4338CA;
      box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
    }

    html.light .tr-nav-prev {
      background: #F8FAFC;
      border-color: #CBD5E1;
      color: #334155;
    }
    html.light .tr-nav-prev:hover:not(:disabled) {
      background: #F1F5F9;
      border-color: #94A3B8;
    }
    html.light .tr-nav-plan-link {
      background: #F0F9FF;
      border-color: #BAE6FD;
      color: #0284C7;
    }
    html.light .tr-srs-tip {
      color: #64748B;
      border-top-color: #E2E8F0;
    }

    @media (max-width: 480px) {
      .tr-smart-tools-grid {
        gap: 6px;
      }
      .tr-smart-tool-btn {
        padding: 8px 6px;
        font-size: 0.8rem;
        gap: 4px;
      }
      .tr-nav-btn {
        padding: 10px 12px;
        font-size: 0.88rem;
      }
    }
"""

target_style_end = "</style>"
if '\r\n' in content:
    new_css = new_css.replace('\n', '\r\n')

assert target_style_end in content
content = content.replace(target_style_end, new_css + "\r\n  " + target_style_end if '\r\n' in content else new_css + "\n  " + target_style_end, 1)

# Now update the JS navigation buttons text & functions
old_nav_js = """      // حالة أزرار التالي والسابق
      document.getElementById("btnPrevQ").disabled = (currentIndex === 0);
      if (btnNextQ) {
        btnNextQ.innerText = (currentIndex === sessionQuestions.length - 1) ? "إنهاء التدريب 🏁" : "السؤال التالي ⬅";
      }"""

new_nav_js = """      // حالة أزرار التالي والسابق بتوجيه أسهم للخارج دائماً
      const btnPrevEl = document.getElementById("btnPrevQ");
      if (btnPrevEl) {
        btnPrevEl.disabled = (currentIndex === 0);
        btnPrevEl.innerHTML = '<span class="nav-arrow">▶</span> <span>السؤال السابق</span>';
      }
      if (btnNextQ) {
        btnNextQ.innerHTML = (currentIndex === sessionQuestions.length - 1)
          ? '<span>إنهاء التدريب 🏁</span>'
          : '<span>السؤال التالي</span> <span class="nav-arrow">◀</span>';
      }"""

if '\r\n' in content:
    old_nav_js = old_nav_js.replace('\n', '\r\n')
    new_nav_js = new_nav_js.replace('\n', '\r\n')

assert old_nav_js in content, "old_nav_js not found"
content = content.replace(old_nav_js, new_nav_js, 1)

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("CSS and JS updates applied successfully!")

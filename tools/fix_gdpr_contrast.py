# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'R:/Ramy/PATENTE/assets/js/unified-nav.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update banner CSS classes in navStyles
style_marker = '/* =========================================================\n         Harmonized Apple HIG Header System'
gdpr_styles = '''
      /* =========================================================
         Harmonized GDPR Cookie Banner (Adaptive Light & Dark Mode)
         ========================================================= */
      .patente-gdpr-banner {
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%) translateY(20px);
        width: calc(100% - 32px);
        max-width: 620px;
        background: #FFFFFF;
        border: 1.5px solid rgba(16, 185, 129, 0.45);
        box-shadow: 0 20px 45px -10px rgba(15, 23, 42, 0.22), 0 4px 12px rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 22px 24px;
        z-index: 9999999;
        color: #0F172A;
        font-family: 'Plus Jakarta Sans', 'Cairo', system-ui, -apple-system, sans-serif;
        opacity: 0;
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        direction: rtl;
        text-align: right;
      }
      html:not(.light) .patente-gdpr-banner {
        background: #111827;
        border-color: rgba(16, 185, 129, 0.4);
        box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.85), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        color: #F8FAFC;
      }
      .patente-gdpr-title {
        font-weight: 800;
        font-size: 0.98rem;
        color: #0F172A;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
      html:not(.light) .patente-gdpr-title {
        color: #FFFFFF;
      }
      .patente-gdpr-badge {
        font-size: 0.75rem;
        font-weight: 700;
        color: #059669;
        direction: ltr;
        font-family: 'JetBrains Mono', monospace;
        background: rgba(16, 185, 129, 0.1);
        padding: 2px 7px;
        border-radius: 6px;
      }
      html:not(.light) .patente-gdpr-badge {
        color: #34D399;
        background: rgba(16, 185, 129, 0.18);
      }
      .patente-gdpr-body-ar {
        font-size: 0.86rem;
        color: #334155;
        line-height: 1.6;
        margin: 0;
        font-weight: 500;
      }
      html:not(.light) .patente-gdpr-body-ar {
        color: #E2E8F0;
      }
      .patente-gdpr-body-it {
        font-size: 0.78rem;
        color: #64748B;
        line-height: 1.45;
        margin: 8px 0 0 0;
        direction: ltr;
        text-align: left;
        font-style: italic;
      }
      html:not(.light) .patente-gdpr-body-it {
        color: #94A3B8;
      }
      .patente-gdpr-footer {
        display: flex;
        gap: 12px;
        justify-content: flex-end;
        align-items: center;
        border-top: 1px solid rgba(15, 23, 42, 0.08);
        padding-top: 14px;
        margin-top: 14px;
      }
      html:not(.light) .patente-gdpr-footer {
        border-top-color: rgba(255, 255, 255, 0.1);
      }
      .patente-gdpr-link-btn {
        background: transparent;
        border: none;
        color: #0284C7;
        font-size: 0.82rem;
        font-weight: 700;
        cursor: pointer;
        padding: 8px 12px;
        text-decoration: underline;
        transition: color 0.2s;
        font-family: inherit;
      }
      html:not(.light) .patente-gdpr-link-btn {
        color: #38BDF8;
      }
      .patente-gdpr-link-btn:hover {
        color: #0369A1;
      }
      html:not(.light) .patente-gdpr-link-btn:hover {
        color: #7DD3FC;
      }
      .patente-gdpr-accept-btn {
        background: #10B981;
        color: #FFFFFF;
        border: none;
        font-size: 0.86rem;
        font-weight: 800;
        padding: 9px 24px;
        border-radius: 10px;
        cursor: pointer;
        transition: transform 0.15s, background 0.15s, box-shadow 0.15s;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
        font-family: inherit;
      }
      .patente-gdpr-accept-btn:hover {
        background: #059669;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.45);
      }
'''

if 'Harmonized GDPR Cookie Banner' not in content:
    content = content.replace(style_marker, gdpr_styles + '\n      ' + style_marker, 1)

# 2. Replace initGdprBanner HTML structure
old_banner_start = '    const bannerHtml = `'
old_banner_end = '    document.body.insertAdjacentHTML(\'beforeend\', bannerHtml);'

p_start = content.find(old_banner_start)
p_end = content.find(old_banner_end)

if p_start != -1 and p_end != -1:
    new_banner_block = '''    const bannerHtml = `
      <div id="patenteGdprBanner" class="patente-gdpr-banner">
        <div style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 8px;">
          <div style="font-size: 1.7rem; line-height: 1; flex-shrink: 0; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">🛡️</div>
          <div style="flex: 1; min-width: 0;">
            <div class="patente-gdpr-title">
              <span>الخصوصية وحماية البيانات (GDPR)</span>
              <span class="patente-gdpr-badge">EU 2016/679</span>
            </div>
            <p class="patente-gdpr-body-ar">
              نستخدم ملفات تعريف ارتباط تقنية وتخزيناً محلياً لحفظ تقدمك الدراسي ومزامنة بنك الأخطاء مع سيرفرات Firebase المشفرة. <strong>لا نبيع بياناتك ولا نستخدم أي تتبع إعلاني خارجي.</strong>
            </p>
            <p class="patente-gdpr-body-it">
              Utilizziamo cookie tecnici per memorizzare i progressi di studio e sincronizzare gli errori in conformità al GDPR europeo. Nessun tracciamento pubblicitario.
            </p>
          </div>
        </div>
        <div class="patente-gdpr-footer">
          <button id="btnGdprDetails" class="patente-gdpr-link-btn">تفاصيل السياسة / Dettagli</button>
          <button id="btnGdprAccept" class="patente-gdpr-accept-btn">قبول ومتابعة (Accetta)</button>
        </div>
      </div>
    `;\n\n'''
    content = content[:p_start] + new_banner_block + content[p_end:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Cookie banner rewritten successfully with high contrast and light/dark theme adaptation!')

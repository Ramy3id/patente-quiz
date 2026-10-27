path = r'R:\Ramy\PATENTE\assets\js\unified-nav.js'

with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

gdpr_code = '''
  // 6. ==================== موديول حماية البيانات والخصوصية الأوروبية (GDPR Suite) ====================
  function initGdprConsentBanner(ctx) {
    if (localStorage.getItem('patente_gdpr_consent') === 'accepted') return;
    if (document.getElementById('patenteGdprBanner')) return;

    const bannerHtml = `
      <div id="patenteGdprBanner" style="
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%) translateY(20px);
        width: calc(100% - 32px);
        max-width: 620px;
        background: rgba(18, 18, 22, 0.94);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(16, 185, 129, 0.35);
        box-shadow: 0 16px 40px -10px rgba(0,0,0,0.8), inset 0 1px 0 rgba(255,255,255,0.1);
        border-radius: 18px;
        padding: 20px 24px;
        z-index: 9999999;
        color: #f4f4f5;
        font-family: 'Plus Jakarta Sans', 'Cairo', system-ui, sans-serif;
        opacity: 0;
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        direction: rtl;
        text-align: right;
      ">
        <div style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 12px;">
          <div style="font-size: 1.6rem; line-height: 1; flex-shrink: 0;">🛡️</div>
          <div style="flex: 1;">
            <div style="font-weight: 800; font-size: 0.95rem; color: #fff; margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between;">
              <span>الخصوصية وحماية البيانات (GDPR)</span>
              <span style="font-size: 0.75rem; font-weight: 600; color: #10b981; direction: ltr; font-family: monospace;">EU 2016/679</span>
            </div>
            <p style="font-size: 0.82rem; color: #a1a1aa; line-height: 1.55; margin: 0;">
              نستخدم ملفات تعريف ارتباط تقنية وتخزيناً محلياً لحفظ تقدمك الدراسي ومزامنة بنك الأخطاء مع سيرفرات Firebase المشفرة. لا نبيع بياناتك ولا نستخدم أي تتبع إعلاني خارجي.
            </p>
            <p style="font-size: 0.74rem; color: #71717a; line-height: 1.4; margin: 6px 0 0 0; direction: ltr; text-align: left;">
              Utilizziamo cookie tecnici per memorizzare i progressi di studio e sincronizzare gli errori in conformità al GDPR europeo.
            </p>
          </div>
        </div>
        <div style="display: flex; gap: 10px; justify-content: flex-end; align-items: center; border-top: 1px solid rgba(255,255,255,0.07); padding-top: 14px;">
          <button id="btnGdprDetails" style="
            background: transparent;
            border: none;
            color: #38bdf8;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            padding: 8px 12px;
            text-decoration: underline;
          ">تفاصيل السياسة / Dettagli</button>
          <button id="btnGdprAccept" style="
            background: #10b981;
            color: #09090b;
            border: none;
            font-size: 0.85rem;
            font-weight: 700;
            padding: 9px 22px;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.15s, background 0.15s;
          ">قبول ومتابعة (Accetta)</button>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', bannerHtml);
    const banner = document.getElementById('patenteGdprBanner');

    requestAnimationFrame(() => {
      setTimeout(() => {
        banner.style.opacity = '1';
        banner.style.transform = 'translateX(-50%) translateY(0)';
      }, 300);
    });

    document.getElementById('btnGdprAccept').onclick = () => {
      localStorage.setItem('patente_gdpr_consent', 'accepted');
      banner.style.opacity = '0';
      banner.style.transform = 'translateX(-50%) translateY(20px)';
      setTimeout(() => banner.remove(), 400);
    };

    document.getElementById('btnGdprDetails').onclick = () => {
      alert(
        "سياسة الخصوصية وحماية البيانات — Patente B Pro\\n\\n" +
        "1. الغرض: حفظ تقدم الطالب في امتحانات رخصة القيادة ومزامنة بنك الأخطاء.\\n" +
        "2. البيانات المخزنة: الاسم، البريد الإلكتروني، إجابات الامتحانات.\\n" +
        "3. المعالجة: تُعالج البيانات حصرياً على بنية Google Firebase السحابية المشفرة.\\n" +
        "4. حقوق المستخدم: يحق لك في أي وقت حذف حسابك وكافة بياناتك بضغطة زر واحدة من قائمة الملف الشخصي (حق النسيان وفق المادة 17 من GDPR).\\n" +
        "5. الإعلانات: لا نشارك أو نبيع بياناتك لأي أطراف إعلانية خارجية إطلاقاً."
      );
    };
  }
'''

target_call = 'setupInteractiveEvents(ctx);'
replacement_call = 'setupInteractiveEvents(ctx);\n\n    // 6. تفعيل شريط الموافقة الأوروبي للخصوصية (GDPR Consent Suite)\n    initGdprConsentBanner(ctx);'

if target_call in code:
    code = code.replace(target_call, replacement_call, 1)
    
    # Insert gdpr function right before initUnifiedPortalUI
    target_func_insert = 'function initUnifiedPortalUI() {'
    code = code.replace(target_func_insert, gdpr_code + '\n  ' + target_func_insert, 1)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("GDPR module cleanly injected into unified-nav.js!")
else:
    print("target_call not found in unified-nav.js")

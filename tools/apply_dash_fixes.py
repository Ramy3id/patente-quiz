with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update guestDashboardNotice HTML
old_banner_html = '''    <div id="guestDashboardNotice" style="display:none; background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(16, 185, 129, 0.12)); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 18px; padding: 14px 18px; margin-bottom: 16px; text-align: right; direction: rtl;">
      <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="font-size: 1.8rem;">☁️</div>
          <div>
            <strong style="font-size: 0.95rem; color: #38BDF8; display: block; margin-bottom: 2px;">أنت تتصفح كزائر — بياناتك وإنجازك محفوظان على هذا المتصفح فقط</strong>
            <span style="font-size: 0.78rem; color: #94A3B8;">أنشئ حسابك المجاني في 10 ثوانٍ لربط بنك أخطائك بالسحابة ومزامنة تقدمك تلقائياً عبر هاتفك والكمبيوتر.</span>
          </div>
        </div>
        <button onclick="window.PatenteAuth && window.PatenteAuth.openAuthModal(true)" style="background: #10B981; color: #FFF; border: none; border-radius: 9px; padding: 7px 15px; font-weight: 800; font-size: 0.82rem; cursor: pointer; font-family: inherit; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); white-space: nowrap;">
          <span>🚀 حفظ بالسحابة ومزامنة مجاناً</span>
        </button>
      </div>
    </div>'''

new_banner_html = '''    <div id="guestDashboardNotice" style="display:none; background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(16, 185, 129, 0.12)); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 18px; padding: 16px; margin-bottom: 18px; text-align: center; direction: rtl;">
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; width: 100%;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px; text-align: center;">
          <div style="font-size: 1.8rem;">☁️</div>
          <div>
            <strong style="font-size: 0.92rem; color: #38BDF8; display: block; margin-bottom: 3px;">أنت تتصفح كزائر — بياناتك وإنجازك محفوظان على هذا المتصفح فقط</strong>
            <span style="font-size: 0.78rem; color: #94A3B8; line-height: 1.4;">أنشئ حسابك المجاني في 10 ثوانٍ لربط بنك أخطائك بالسحابة ومزامنة تقدمك تلقائياً عبر هاتفك والكمبيوتر.</span>
          </div>
        </div>
        <div style="display: flex; justify-content: center; width: 100%; margin-top: 2px;">
          <button type="button" onclick="window.PatenteAuth && window.PatenteAuth.openAuthModal(true)" style="background: linear-gradient(135deg, #10B981, #059669); color: #FFF; border: none; border-radius: 12px; padding: 10px 24px; font-weight: 800; font-size: 0.85rem; cursor: pointer; font-family: inherit; box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35); white-space: nowrap; display: inline-flex; align-items: center; justify-content: center; gap: 6px; margin: 0 auto; transition: transform 0.15s ease;">
            <span>🚀 حفظ بالسحابة ومزامنة مجاناً</span>
          </button>
        </div>
      </div>
    </div>'''

if old_banner_html in text:
    text = text.replace(old_banner_html, new_banner_html, 1)
    print('Replaced guest banner HTML successfully')
else:
    print('old_banner_html not found!')

# 2. Add responsive grid CSS for dash-tabs-bar and light theme for banner
tabs_css = '''
    /* =========================================================
       ZERO-SCROLL BALANCED TABS GRID (No Horizontal Scroll)
       ========================================================= */
    .dash-tabs-bar {
      display: grid !important;
      grid-template-columns: repeat(2, 1fr) !important;
      gap: 6px !important;
      background: rgba(15, 23, 42, 0.7) !important;
      backdrop-filter: blur(16px) !important;
      -webkit-backdrop-filter: blur(16px) !important;
      border: 1px solid var(--border-subtle) !important;
      border-radius: 16px !important;
      padding: 6px !important;
      margin-bottom: 20px !important;
      overflow: visible !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }
    html.light .dash-tabs-bar {
      background: #FFFFFF !important;
      border-color: rgba(15, 23, 42, 0.1) !important;
      box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04) !important;
    }
    @media (min-width: 768px) {
      .dash-tabs-bar {
        grid-template-columns: repeat(5, 1fr) !important;
      }
    }
    .dash-tab-btn {
      width: 100% !important;
      height: 42px !important;
      min-height: 42px !important;
      max-height: 42px !important;
      padding: 0 6px !important;
      border-radius: 10px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 6px !important;
      box-sizing: border-box !important;
      white-space: nowrap !important;
      font-size: 0.80rem !important;
      font-weight: 700 !important;
      font-family: inherit !important;
      transition: all 0.15s ease !important;
    }
    html.light .dash-tab-btn {
      color: #475569 !important;
    }
    .dash-tab-btn.active {
      background: rgba(56, 189, 248, 0.15) !important;
      border-color: rgba(56, 189, 248, 0.35) !important;
      color: var(--accent-cyan) !important;
    }
    html.light .dash-tab-btn.active {
      background: rgba(2, 132, 199, 0.1) !important;
      border-color: rgba(2, 132, 199, 0.3) !important;
      color: #0284C7 !important;
    }
    .dash-tab-btn:last-child {
      grid-column: 1 / -1 !important;
    }
    @media (min-width: 768px) {
      .dash-tab-btn:last-child {
        grid-column: auto !important;
      }
    }
    html.light #guestDashboardNotice {
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.08), rgba(16, 185, 129, 0.08)) !important;
      border-color: rgba(2, 132, 199, 0.25) !important;
    }
    html.light #guestDashboardNotice strong {
      color: #0284C7 !important;
    }
    html.light #guestDashboardNotice span {
      color: #475569 !important;
    }
'''

style_idx = text.find('</style>')
if style_idx != -1:
    text = text[:style_idx] + tabs_css + '\n' + text[style_idx:]
    print('Appended tabs CSS successfully')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated dashboard.html successfully.')

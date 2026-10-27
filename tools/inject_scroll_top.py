path = r'R:\Ramy\PATENTE\assets\js\unified-nav.js'

with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

scroll_top_code = '''
  // 7. ==================== زر العودة للأعلى الذكي (Scroll to Top Floating Pill) ====================
  function initScrollToTopButton() {
    if (document.getElementById('patenteScrollTopBtn')) return;

    const btn = document.createElement('button');
    btn.id = 'patenteScrollTopBtn';
    btn.setAttribute('aria-label', 'العودة لأعلى الصفحة / Torna su');
    btn.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
      </svg>
    `;
    btn.style.cssText = `
      position: fixed;
      bottom: 24px;
      left: 24px;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: rgba(24, 24, 27, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.14);
      color: #38bdf8;
      box-shadow: 0 8px 24px -4px rgba(0,0,0,0.6);
      cursor: pointer;
      z-index: 99999;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transform: translateY(12px) scale(0.9);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    `;

    document.body.appendChild(btn);

    window.addEventListener('scroll', () => {
      if (window.scrollY > 380) {
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
        btn.style.transform = 'translateY(0) scale(1)';
      } else {
        btn.style.opacity = '0';
        btn.style.pointerEvents = 'none';
        btn.style.transform = 'translateY(12px) scale(0.9)';
      }
    }, { passive: true });

    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    btn.addEventListener('mouseenter', () => {
      btn.style.background = '#10b981';
      btn.style.color = '#09090b';
      btn.style.borderColor = '#34d399';
      btn.style.transform = 'translateY(-2px) scale(1.05)';
    });

    btn.addEventListener('mouseleave', () => {
      btn.style.background = 'rgba(24, 24, 27, 0.85)';
      btn.style.color = '#38bdf8';
      btn.style.borderColor = 'rgba(255, 255, 255, 0.14)';
      btn.style.transform = 'translateY(0) scale(1)';
    });
  }
'''

target_call = 'initGdprConsentBanner(ctx);'
replacement_call = 'initGdprConsentBanner(ctx);\n\n    // 7. زر العودة للأعلى التلقائي\n    initScrollToTopButton();'

if target_call in code and 'initScrollToTopButton' not in code:
    code = code.replace(target_call, replacement_call, 1)
    
    # insert function right before initUnifiedPortalUI
    target_func = 'function initUnifiedPortalUI() {'
    code = code.replace(target_func, scroll_top_code + '\n  ' + target_func, 1)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Scroll-to-Top Floating Button added to unified-nav.js!")
else:
    print("Target call not found or already injected.")

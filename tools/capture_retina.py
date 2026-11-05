import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

def capture_retina():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.add_init_script("localStorage.setItem('patente_theme', 'light');")

        url = 'http://localhost:8080/Capitoli_Divisi/index.html'

        # 1. OPTION 1
        page.goto(url, wait_until='networkidle')
        page.evaluate("() => { document.documentElement.className = 'light'; }")
        page.wait_for_timeout(300)

        js_option1 = """
        () => {
            const nav = document.getElementById('globalPortalNav');
            if (!nav) return;
            let inner = nav.querySelector('.nav-inner-container');
            if (!inner) {
                inner = document.createElement('div');
                inner.className = 'nav-inner-container';
                inner.style.cssText = `
                    display: flex !important;
                    justify-content: space-between !important;
                    align-items: center !important;
                    width: 100% !important;
                    max-width: 1200px !important;
                    margin: 0 auto !important;
                    padding: 0 18px !important;
                    box-sizing: border-box !important;
                    height: 100% !important;
                `;
                const children = Array.from(nav.children);
                children.forEach(child => inner.appendChild(child));
                nav.appendChild(inner);
            }
            nav.style.padding = '0 !important';
            nav.style.display = 'block !important';
        }
        """
        page.evaluate(js_option1)
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'nav_option1_retina.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 550})

        # 2. OPTION 2
        page.goto(url, wait_until='networkidle')
        page.evaluate("() => { document.documentElement.className = 'light'; }")
        page.wait_for_timeout(300)

        js_option2 = """
        () => {
            const nav = document.getElementById('globalPortalNav');
            if (!nav) return;
            nav.style.maxWidth = '1200px';
            nav.style.margin = '14px auto 0 auto';
            nav.style.borderRadius = '16px';
            nav.style.position = 'sticky';
            nav.style.top = '12px';
            nav.style.padding = '0 18px';
            nav.style.border = '1px solid rgba(15, 23, 42, 0.12)';
            nav.style.boxShadow = '0 12px 30px rgba(15, 23, 42, 0.08), 0 2px 6px rgba(15, 23, 42, 0.04)';
            nav.style.width = 'calc(100% - 36px)';
            const container = document.querySelector('.container');
            if (container) container.style.marginTop = '20px';
        }
        """
        page.evaluate(js_option2)
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'nav_option2_retina.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 550})

        browser.close()
        print("Captured retina previews successfully!")

if __name__ == '__main__':
    capture_retina()

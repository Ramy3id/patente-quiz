import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

def capture_dark():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.add_init_script("localStorage.setItem('patente_theme', 'dark');")

        url = 'http://localhost:8080/Capitoli_Divisi/index.html'

        # 1. OPTION 1 DARK
        page.goto(url, wait_until='networkidle')
        page.evaluate("() => { document.documentElement.className = 'dark'; }")
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
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'nav_option1_dark_retina.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 550})

        browser.close()
        print("Captured dark mode preview successfully!")

if __name__ == '__main__':
    capture_dark()

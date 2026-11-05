import os
import sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

def capture_options():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 850})
        page = context.new_page()
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.add_init_script("localStorage.setItem('patente_theme', 'light');")
        page.add_init_script("document.documentElement.className = 'light';")

        url = 'http://localhost:8080/Capitoli_Divisi/index.html'

        # -------------------------------------------------------------
        # 1. CURRENT STATE
        # -------------------------------------------------------------
        page.goto(url, wait_until='networkidle')
        page.evaluate("() => { document.documentElement.classList.remove('dark'); document.documentElement.classList.add('light'); }")
        page.wait_for_timeout(500)
        
        path_current = os.path.join(ARTIFACT_DIR, 'nav_proposal_current.png')
        page.screenshot(path=path_current, clip={"x": 0, "y": 0, "width": 1440, "height": 650})
        print(f"Captured current state to {path_current}")

        # -------------------------------------------------------------
        # 2. OPTION 1: Full-width glass navbar with 1200px inner container
        # -------------------------------------------------------------
        js_option1 = """
        () => {
            const nav = document.getElementById('globalPortalNav');
            if (!nav) return;
            
            // Check if inner wrapper already exists
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
                // Move existing nav children into inner container (except mobile drawer)
                const children = Array.from(nav.children);
                children.forEach(child => {
                    inner.appendChild(child);
                });
                nav.appendChild(inner);
            }
            nav.style.padding = '0 !important';
            nav.style.display = 'block !important';
        }
        """
        page.evaluate(js_option1)
        page.wait_for_timeout(300)
        path_opt1 = os.path.join(ARTIFACT_DIR, 'nav_proposal_option1.png')
        page.screenshot(path=path_opt1, clip={"x": 0, "y": 0, "width": 1440, "height": 650})
        print(f"Captured Option 1 to {path_opt1}")

        # -------------------------------------------------------------
        # 3. OPTION 2: Modern Floating Island Capsule
        # -------------------------------------------------------------
        # Reload fresh page
        page.goto(url, wait_until='networkidle')
        page.evaluate("() => { document.documentElement.classList.remove('dark'); document.documentElement.classList.add('light'); }")
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
            
            // Adjust margin of container below so spacing is perfect
            const container = document.querySelector('.container');
            if (container) {
                container.style.marginTop = '20px';
            }
        }
        """
        page.evaluate(js_option2)
        page.wait_for_timeout(300)
        path_opt2 = os.path.join(ARTIFACT_DIR, 'nav_proposal_option2.png')
        page.screenshot(path=path_opt2, clip={"x": 0, "y": 0, "width": 1440, "height": 650})
        print(f"Captured Option 2 to {path_opt2}")

        browser.close()

if __name__ == '__main__':
    capture_options()

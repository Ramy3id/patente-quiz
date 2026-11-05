import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # 1. Desktop Light (1440x900)
        context_dt = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page_dt = context_dt.new_page()
        page_dt.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page_dt.add_init_script("localStorage.setItem('patente_theme', 'light');")
        page_dt.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page_dt.wait_for_timeout(400)
        
        # Capture Top View
        page_dt.screenshot(path=os.path.join(ARTIFACT_DIR, 'final_nav_desktop_light.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured final_nav_desktop_light.png")

        # Scroll to see sticky float
        page_dt.evaluate("() => window.scrollTo(0, 400)")
        page_dt.wait_for_timeout(300)
        page_dt.screenshot(path=os.path.join(ARTIFACT_DIR, 'final_nav_desktop_scrolled.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured final_nav_desktop_scrolled.png")

        # Megamenu open test
        page_dt.evaluate("() => window.scrollTo(0, 0)")
        page_dt.evaluate("() => { const b = document.getElementById('btnToggleChaptersMenu'); if(b) b.click(); }")
        page_dt.wait_for_timeout(300)
        page_dt.screenshot(path=os.path.join(ARTIFACT_DIR, 'final_nav_megamenu_open.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 720})
        print("Captured final_nav_megamenu_open.png")

        # Spotlight search modal test
        page_dt.evaluate("() => { const b = document.getElementById('btnToggleChaptersMenu'); if(b) b.click(); }") # close megamenu
        page_dt.evaluate("() => { const b = document.getElementById('btnOpenGlobalSearch'); if(b) b.click(); }")
        page_dt.wait_for_timeout(300)
        page_dt.screenshot(path=os.path.join(ARTIFACT_DIR, 'final_nav_search_modal_open.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured final_nav_search_modal_open.png")

        # 2. Desktop Dark (1440x900)
        page_dt.evaluate("() => { const b = document.getElementById('btnCloseGlobalSearch'); if(b) b.click(); }") # close search
        page_dt.evaluate("() => { document.documentElement.className = 'dark'; localStorage.setItem('patente_theme', 'dark'); }")
        page_dt.wait_for_timeout(300)
        page_dt.screenshot(path=os.path.join(ARTIFACT_DIR, 'final_nav_desktop_dark.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 620})
        print("Captured final_nav_desktop_dark.png")

        # 3. Mobile Check (390x844)
        context_mb = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, device_scale_factor=2)
        page_mb = context_mb.new_page()
        page_mb.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page_mb.add_init_script("localStorage.setItem('patente_theme', 'light');")
        page_mb.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page_mb.wait_for_timeout(400)
        page_mb.screenshot(path=os.path.join(ARTIFACT_DIR, 'final_nav_mobile_intact.png'))
        print("Captured final_nav_mobile_intact.png")

        browser.close()

if __name__ == '__main__':
    verify()

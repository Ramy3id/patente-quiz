import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 1100})
    
    # 1. Capitolo 01
    page.goto("http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html")
    page.evaluate("() => { localStorage.setItem('cookie_consent', 'accepted'); document.getElementById('cookie-consent-banner')?.remove(); }")
    page.wait_for_selector('.subtopic-section-box', timeout=10000)
    
    # Scroll to show 8, 9, 10, 11 together
    sec8 = page.query_selector('#subtopic-sec-rimorchi_camper')
    if sec8:
        sec8.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=f"{artifact_dir}/cap01_verified_order_8_9_10_11.png")

    # 2. Capitolo 02
    page.goto("http://localhost:8080/Capitoli_Divisi/Capitolo_02_segnali_pericolo/index.html")
    page.evaluate("() => { localStorage.setItem('cookie_consent', 'accepted'); document.getElementById('cookie-consent-banner')?.remove(); }")
    page.wait_for_selector('.subtopic-section-box', timeout=10000)

    # Scroll to show 18, 19, 20, 21 together
    sec18 = page.query_selector('#subtopic-sec-semafori')
    if sec18:
        sec18.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=f"{artifact_dir}/cap02_verified_order_18_19_20_21.png")

    # 3. Capitolo 03 (which was previously 1, 9, 8, 10, 2, 3...)
    page.goto("http://localhost:8080/Capitoli_Divisi/Capitolo_03_segnali_divieto/index.html")
    page.evaluate("() => { localStorage.setItem('cookie_consent', 'accepted'); document.getElementById('cookie-consent-banner')?.remove(); }")
    page.wait_for_selector('.subtopic-section-box', timeout=10000)
    
    # Click toggle extra subtopics so chips are fully visible
    btn_toggle = page.query_selector('#btnToggleExtraSubtopics')
    if btn_toggle:
        btn_toggle.click()
        page.wait_for_timeout(300)

    page.screenshot(path=f"{artifact_dir}/cap03_verified_order_1_2_3_4.png")

    browser.close()

print("Clean verification screenshots taken!")

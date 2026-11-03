import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932}) # iPhone 14 Pro Max viewport
    
    # 1. Capitolo 01
    page.goto("http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html")
    page.wait_for_selector('.subtopic-section-box', timeout=10000)
    
    # Click toggle extra subtopics to expand all chips
    btn_toggle = page.query_selector('#btnToggleExtraSubtopics')
    if btn_toggle:
        btn_toggle.click()
        page.wait_for_timeout(300)

    # Screenshot chips hub in Cap 01
    hub = page.query_selector('#subtopics-hub-card')
    if hub:
        hub.screenshot(path=f"{artifact_dir}/cap01_chips_hub.png")

    # Scroll to sections 8, 9, 10, 11
    sec9 = page.query_selector('#subtopic-sec-utenti_deboli')
    if sec9:
        sec9.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=f"{artifact_dir}/cap01_sections_8_9_10_11.png")

    # 2. Capitolo 02
    page.goto("http://localhost:8080/Capitoli_Divisi/Capitolo_02_segnali_pericolo/index.html")
    page.wait_for_selector('.subtopic-section-box', timeout=10000)

    btn_toggle2 = page.query_selector('#btnToggleExtraSubtopics')
    if btn_toggle2:
        btn_toggle2.click()
        page.wait_for_timeout(300)

    hub2 = page.query_selector('#subtopics-hub-card')
    if hub2:
        hub2.screenshot(path=f"{artifact_dir}/cap02_chips_hub.png")

    # Scroll to sections 18, 19, 20, 21
    sec19 = page.query_selector('#subtopic-sec-banchina_cedevole')
    if sec19:
        sec19.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=f"{artifact_dir}/cap02_sections_18_19_20_21.png")

    browser.close()

print("Captured screenshots successfully!")

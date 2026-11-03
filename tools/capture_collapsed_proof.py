import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 800, "height": 1000})

    # Capitolo 01
    page.goto("http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html")
    page.wait_for_selector('.subtopic-section-box', timeout=10000)
    
    # Click Accept Cookies if present
    try:
        btn_cookie = page.wait_for_selector('button:has-text("قبول ومتابعة")', timeout=1500)
        if btn_cookie:
            btn_cookie.click()
            page.wait_for_timeout(300)
    except Exception:
        pass

    # Collapse all sections so headers are visible in one view
    btn_col = page.query_selector('button[onclick="collapseAllSections()"]')
    if btn_col:
        btn_col.click()
        page.wait_for_timeout(400)

    # Scroll to section 8
    sec8 = page.query_selector('#subtopic-sec-rimorchi_camper')
    if sec8:
        sec8.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=f"{artifact_dir}/verified_cap01_sections_order.png")

    # Capitolo 02
    page.goto("http://localhost:8080/Capitoli_Divisi/Capitolo_02_segnali_pericolo/index.html")
    page.wait_for_selector('.subtopic-section-box', timeout=10000)
    
    try:
        btn_cookie = page.wait_for_selector('button:has-text("قبول ومتابعة")', timeout=1500)
        if btn_cookie:
            btn_cookie.click()
            page.wait_for_timeout(300)
    except Exception:
        pass

    btn_col2 = page.query_selector('button[onclick="collapseAllSections()"]')
    if btn_col2:
        btn_col2.click()
        page.wait_for_timeout(400)

    # Scroll to section 18
    sec18 = page.query_selector('#subtopic-sec-semafori')
    if sec18:
        sec18.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=f"{artifact_dir}/verified_cap02_sections_order.png")

    browser.close()

print("Collapsed overview screenshots captured!")

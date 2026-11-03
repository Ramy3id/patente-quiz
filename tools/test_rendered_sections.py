import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def test_chapter(url, name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('.subtopic-section-box', timeout=10000)
        
        # Extract all section titles and numbers
        sections = page.query_selector_all('.subtopic-section-box')
        print(f"\n=== {name} (found {len(sections)} sections) ===")
        for idx, sec in enumerate(sections):
            num_pill = sec.query_selector('.subtopic-num-pill')
            heading = sec.query_selector('.subtopic-ar-heading')
            num_text = num_pill.inner_text() if num_pill else ''
            head_text = heading.inner_text() if heading else ''
            print(f"  Sec {idx+1:2d}: {num_text:20} | {head_text[:40]}")
        
        browser.close()

test_chapter("http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html", "Capitolo 01 (BEFORE)")
test_chapter("http://localhost:8080/Capitoli_Divisi/Capitolo_02_segnali_pericolo/index.html", "Capitolo 02 (BEFORE)")

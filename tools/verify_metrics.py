import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})
    url = "http://localhost:8080/interactive_pages/allenamento-capitolo.html?mode=decoder&count=20"
    page.goto(url)

    # Click accept on GDPR
    try:
        btn_acc = page.wait_for_selector('button:has-text("قبول ومتابعة")', timeout=3000)
        if btn_acc:
            btn_acc.click()
            page.wait_for_timeout(400)
    except Exception:
        pass

    # Inspect heights and borders of btnPlan vs btnCount15
    metrics = page.evaluate("""() => {
        const plan = document.querySelector('.tr-controls-wrap a.tr-count-btn');
        const c15 = document.getElementById('btnCount15');
        const c20 = document.getElementById('btnCount20');
        const planStyle = window.getComputedStyle(plan);
        const c15Style = window.getComputedStyle(c15);
        const c20Style = window.getComputedStyle(c20);
        const backBtn = document.getElementById('btnReturnToPlanTop');
        const arrow = backBtn.querySelector('.tr-back-arrow');
        return {
            plan: {
                height: plan.getBoundingClientRect().height,
                border: planStyle.border,
                borderColor: planStyle.borderColor,
                bg: planStyle.backgroundColor,
                color: planStyle.color
            },
            c15: {
                height: c15.getBoundingClientRect().height,
                border: c15Style.border,
                borderColor: c15Style.borderColor,
                bg: c15Style.backgroundColor,
                color: c15Style.color
            },
            arrowText: arrow.innerText
        };
    }""")
    import json
    print(json.dumps(metrics, indent=2))

    # Take screenshot of the top area
    page.screenshot(path=f"{artifact_dir}/verified_arrow_and_buttons_match.png")

    browser.close()

print("Verification complete!")

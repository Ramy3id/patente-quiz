import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:8080/interactive_pages/piano-studio.html')
    page.evaluate('openPlanSetupModal()')
    metrics = page.evaluate("""() => {
        const modal = document.getElementById('planSetupModal');
        const box = modal.querySelector('.sp-modal-box');
        const actions = modal.querySelector('.sp-modal-actions-bar');
        return {
            modalScrollHeight: modal.scrollHeight,
            modalClientHeight: modal.clientHeight,
            modalBoxScrollHeight: box.scrollHeight,
            modalBoxClientHeight: box.clientHeight,
            actionsRect: actions.getBoundingClientRect(),
            bodyScrollHeight: document.body.scrollHeight,
            windowInnerHeight: window.innerHeight
        };
    }""")
    print(metrics)
    browser.close()

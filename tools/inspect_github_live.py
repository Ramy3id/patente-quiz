import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    page = context.new_page()
    page.goto('https://ramy3id.github.io/patente-quiz/Capitoli_Divisi/index.html', wait_until='networkidle')
    page.wait_for_timeout(1000)

    # Inspect right actions
    actions_info = page.evaluate("""() => {
        const list = [];
        document.querySelectorAll('.nav-desktop-actions > *').forEach(el => {
            const r = el.getBoundingClientRect();
            list.push({
                id: el.id || el.className,
                left: r.left,
                right: r.right,
                top: r.top,
                bottom: r.bottom,
                width: r.width,
                height: r.height,
                text: el.innerText.trim()
            });
        });
        return list;
    }""")
    print("Actions on GitHub Pages:")
    for a in actions_info:
        print(a)

    page.screenshot(path=os.path.join(ARTIFACT_DIR, 'live_github_pages_inspect.png'), clip={"x": 0, "y": 0, "width": 1440, "height": 300})
    browser.close()

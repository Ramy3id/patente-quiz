import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def measure():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        page = ctx.new_page()
        page.add_init_script("""
            localStorage.setItem('patente_gdpr_consent', 'accepted');
            localStorage.setItem('patente_theme', 'light');
            document.documentElement.className = 'light';
        """)
        page.goto('http://localhost:8080/interactive_pages/cerca-quiz.html')
        page.wait_for_timeout(800)
        
        # Measure all 3 buttons in the first card
        metrics = page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('.cq-card-actions .cq-action-btn')).slice(0, 3);
            return btns.map((b, i) => {
                const rect = b.getBoundingClientRect();
                const comp = window.getComputedStyle(b);
                return {
                    index: i,
                    text: b.innerText.trim(),
                    tag: b.tagName,
                    height: rect.height,
                    computedHeight: comp.height
                };
            });
        }""")
        
        print("Buttons metrics:")
        for m in metrics:
            print(f"  {m['tag']} '{m['text']}': height={m['height']}px (computed: {m['computedHeight']})")
        
        h0 = metrics[0]['height']
        h1 = metrics[1]['height']
        h2 = metrics[2]['height']
        assert h0 == h1 == h2 == 40, f"All buttons must be exactly 40px, got {h0}, {h1}, {h2}"
        
        # Take screenshot of the actions bar
        actions_bar = page.locator('.cq-card-actions').first
        actions_bar.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        actions_bar.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_equal_height_buttons.png')
        
        browser.close()
        print("Verified: ALL 3 BUTTONS HAVE THE EXACT SAME HEIGHT (40px)!")

if __name__ == '__main__':
    measure()

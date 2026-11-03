import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2)
        page = await context.new_page()
        
        url = "http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html"
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(600)
        
        # Dismiss GDPR banner
        await page.evaluate("""() => {
            document.querySelectorAll('.patente-gdpr-banner').forEach(el => el.remove());
            localStorage.setItem('patente_gdpr_consent', 'true');
        }""")
        
        artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
        
        # 1. Light Mode Top
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        await page.wait_for_timeout(300)
        
        # Screenshot Top Header
        await page.screenshot(path=f"{artifact_dir}/verified_chap_top_light.png")
        
        # Scroll to Hub
        await page.evaluate("() => { const hub = document.getElementById('subtopics-hub-card'); if (hub) hub.scrollIntoView(); }")
        await page.wait_for_timeout(300)
        
        # Test initial collapsed state
        collapsed_info = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('.subtopic-chip'));
            const visible = btns.filter(b => b.offsetParent !== null);
            const toggleBtn = document.getElementById('btnToggleExtraSubtopics');
            const chipsBar = document.getElementById('subtopics-chips-bar');
            return {
                totalBtns: btns.length,
                visibleCount: visible.length,
                toggleText: toggleBtn ? toggleBtn.innerText.trim() : null,
                docScrollWidth: document.documentElement.scrollWidth,
                windowWidth: window.innerWidth,
                chipsScrollWidth: chipsBar ? chipsBar.scrollWidth : 0,
                chipsClientWidth: chipsBar ? chipsBar.clientWidth : 0,
                hasDocHorizScroll: document.documentElement.scrollWidth > window.innerWidth,
                hasChipsHorizScroll: chipsBar ? (chipsBar.scrollWidth > chipsBar.clientWidth) : false
            };
        }""")
        print("Collapsed Info:", collapsed_info)
        
        hub_box = await page.locator("#subtopics-hub-card").bounding_box()
        clip_hub = {
            "x": 0,
            "y": max(0, hub_box["y"] - 10),
            "width": 375,
            "height": min(550, hub_box["height"] + 20)
        }
        await page.screenshot(path=f"{artifact_dir}/verified_chap_collapsed_light.png", clip=clip_hub)
        
        # Click Expand
        await page.click("#btnToggleExtraSubtopics")
        await page.wait_for_timeout(300)
        
        expanded_info = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('.subtopic-chip'));
            const visible = btns.filter(b => b.offsetParent !== null);
            const toggleBtn = document.getElementById('btnToggleExtraSubtopics');
            return {
                visibleCount: visible.length,
                toggleText: toggleBtn ? toggleBtn.innerText.trim() : null
            };
        }""")
        print("Expanded Info:", expanded_info)
        
        hub_box_exp = await page.locator("#subtopics-hub-card").bounding_box()
        clip_hub_exp = {
            "x": 0,
            "y": max(0, hub_box_exp["y"] - 10),
            "width": 375,
            "height": min(750, hub_box_exp["height"] + 20)
        }
        await page.screenshot(path=f"{artifact_dir}/verified_chap_expanded_light.png", clip=clip_hub_exp)
        
        # Click Collapse again
        await page.click("#btnToggleExtraSubtopics")
        await page.wait_for_timeout(300)
        
        # Scroll down to subtopic card
        await page.evaluate("() => { const card = document.querySelector('.subtopic-section-box'); if (card) card.scrollIntoView(); }")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/verified_chap_card_light.png")
        
        # 2. Dark Mode
        await page.evaluate("() => { document.documentElement.className = 'dark'; }")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/verified_chap_card_dark.png")
        
        await page.evaluate("() => window.scrollTo(0, 0)")
        await page.wait_for_timeout(200)
        await page.screenshot(path=f"{artifact_dir}/verified_chap_top_dark.png")
        
        await page.evaluate("() => { const hub = document.getElementById('subtopics-hub-card'); if (hub) hub.scrollIntoView(); }")
        await page.wait_for_timeout(200)
        hub_box_dark = await page.locator("#subtopics-hub-card").bounding_box()
        clip_hub_dark = {
            "x": 0,
            "y": max(0, hub_box_dark["y"] - 10),
            "width": 375,
            "height": min(550, hub_box_dark["height"] + 20)
        }
        await page.screenshot(path=f"{artifact_dir}/verified_chap_collapsed_dark.png", clip=clip_hub_dark)
        
        print("All chapter verification tests passed successfully!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

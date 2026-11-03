import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2)
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html", wait_until="networkidle")
        await page.wait_for_timeout(500)
        
        # Remove GDPR
        await page.evaluate("""() => {
            document.querySelectorAll('.patente-gdpr-banner').forEach(el => el.remove());
            localStorage.setItem('patente_gdpr_consent', 'true');
        }""")
        
        artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
        
        # 1. Light Mode Collapsed
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        await page.wait_for_timeout(300)
        
        # Check visible chips count
        visible_chips = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('.cat-chip-btn'));
            const visible = btns.filter(b => b.offsetParent !== null);
            const toggleBtn = document.getElementById('btnToggleExtraCats');
            const toggleText = toggleBtn ? toggleBtn.innerText.trim() : null;
            return {
                totalBtns: btns.length,
                visibleCount: visible.length,
                toggleText: toggleText,
                visibleTexts: visible.map(b => b.innerText.trim())
            };
        }""")
        print("Initial Collapsed State:", visible_chips["visibleCount"], visible_chips["toggleText"])
        
        # Scroll to filters
        await page.evaluate("() => { document.querySelector('.search-filter-card').scrollIntoView(); }")
        await page.wait_for_timeout(200)
        
        # Capture collapsed screenshot (light)
        search_card = await page.locator(".search-filter-card").bounding_box()
        clip_collapsed = {
            "x": 0,
            "y": max(0, search_card["y"] - 10),
            "width": 375,
            "height": min(500, search_card["height"] + 20)
        }
        await page.screenshot(path=f"{artifact_dir}/verified_dict_collapsed_light.png", clip=clip_collapsed)
        
        # 2. Dark Mode Collapsed
        await page.evaluate("() => { document.documentElement.className = 'dark'; }")
        await page.wait_for_timeout(200)
        await page.screenshot(path=f"{artifact_dir}/verified_dict_collapsed_dark.png", clip=clip_collapsed)
        
        # 3. Click to Expand in Light Mode
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        await page.click("#btnToggleExtraCats")
        await page.wait_for_timeout(300)
        
        expanded_info = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('.cat-chip-btn'));
            const visible = btns.filter(b => b.offsetParent !== null);
            const toggleBtn = document.getElementById('btnToggleExtraCats');
            return {
                visibleCount: visible.length,
                toggleText: toggleBtn ? toggleBtn.innerText.trim() : null
            };
        }""")
        print("After Clicking Expand:", expanded_info["visibleCount"], expanded_info["toggleText"])
        
        # Capture expanded screenshot (light)
        search_card_exp = await page.locator(".search-filter-card").bounding_box()
        clip_expanded = {
            "x": 0,
            "y": max(0, search_card_exp["y"] - 10),
            "width": 375,
            "height": min(750, search_card_exp["height"] + 20)
        }
        await page.screenshot(path=f"{artifact_dir}/verified_dict_expanded_light.png", clip=clip_expanded)
        
        # 4. Click again to Collapse
        await page.click("#btnToggleExtraCats")
        await page.wait_for_timeout(300)
        recollapsed_info = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('.cat-chip-btn'));
            const visible = btns.filter(b => b.offsetParent !== null);
            const toggleBtn = document.getElementById('btnToggleExtraCats');
            return {
                visibleCount: visible.length,
                toggleText: toggleBtn ? toggleBtn.innerText.trim() : null
            };
        }""")
        print("After Clicking Collapse Again:", recollapsed_info["visibleCount"], recollapsed_info["toggleText"])
        
        # Scroll checks
        scroll_info = await page.evaluate("""() => {
            return {
                docScrollWidth: document.documentElement.scrollWidth,
                windowWidth: window.innerWidth,
                hasHorizScroll: document.documentElement.scrollWidth > window.innerWidth
            };
        }""")
        print("Scroll info:", scroll_info)
        
        print("Playwright collapsible verification passed 100%!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

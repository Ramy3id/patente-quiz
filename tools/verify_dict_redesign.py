import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2)
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html", wait_until="networkidle")
        await page.wait_for_timeout(500)
        
        # Dismiss GDPR banner
        await page.evaluate("""() => {
            document.querySelectorAll('.patente-gdpr-banner').forEach(el => el.remove());
            localStorage.setItem('patente_gdpr_consent', 'true');
        }""")
        
        artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
        
        # 1. Test Light Mode
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        await page.wait_for_timeout(300)
        
        # Check scroll metrics
        scroll_info = await page.evaluate("""() => {
            const chips = document.getElementById('categoryChipsDeck');
            return {
                windowWidth: window.innerWidth,
                docScrollWidth: document.documentElement.scrollWidth,
                chipsScrollWidth: chips ? chips.scrollWidth : 0,
                chipsClientWidth: chips ? chips.clientWidth : 0,
                hasDocHorizScroll: document.documentElement.scrollWidth > window.innerWidth,
                hasChipsHorizScroll: chips ? (chips.scrollWidth > chips.clientWidth) : false
            };
        }""")
        print("Light Mode Scroll Info:", scroll_info)
        
        # Inspect colors in traps section
        trap_colors = await page.evaluate("""() => {
            const h4 = document.querySelector('.traps-section h4');
            const term = document.querySelector('.trap-term-title');
            const exp = document.querySelector('.trap-explanation');
            const section = document.querySelector('.traps-section');
            const subitem = document.querySelector('.trap-subitem');
            return {
                section_bg: section ? window.getComputedStyle(section).backgroundColor : null,
                h4_color: h4 ? window.getComputedStyle(h4).color : null,
                term_color: term ? window.getComputedStyle(term).color : null,
                exp_color: exp ? window.getComputedStyle(exp).color : null,
                subitem_bg: subitem ? window.getComputedStyle(subitem).backgroundColor : null
            };
        }""")
        print("Light Mode Trap Colors:", trap_colors)
        
        # Screenshot Hero Light
        await page.evaluate("() => window.scrollTo(0, 0)")
        await page.wait_for_timeout(200)
        await page.screenshot(path=f"{artifact_dir}/verified_dict_hero_light.png")
        
        # Screenshot Search & Filters Light
        search_card = await page.locator(".search-filter-card").bounding_box()
        clip_search = {
            "x": 0,
            "y": max(0, search_card["y"] - 10),
            "width": 375,
            "height": min(650, search_card["height"] + 20)
        }
        await page.screenshot(path=f"{artifact_dir}/verified_dict_filters_light.png", clip=clip_search)
        
        # Screenshot Cards & Traps Light
        await page.evaluate("() => { const card = document.querySelector('.dict-card'); if (card) card.scrollIntoView(); }")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/verified_dict_cards_light.png")
        
        # Zoomed Traps section Light
        trap_box = await page.locator(".traps-section").first.bounding_box()
        if trap_box:
            clip_trap = {
                "x": 0,
                "y": max(0, trap_box["y"] - 10),
                "width": 375,
                "height": min(400, trap_box["height"] + 20)
            }
            await page.screenshot(path=f"{artifact_dir}/verified_dict_traps_zoom_light.png", clip=clip_trap)
        
        # 2. Test Dark Mode
        await page.evaluate("() => { document.documentElement.className = 'dark'; }")
        await page.wait_for_timeout(300)
        
        await page.evaluate("() => window.scrollTo(0, 0)")
        await page.wait_for_timeout(200)
        await page.screenshot(path=f"{artifact_dir}/verified_dict_hero_dark.png")
        
        # Search & Filters Dark
        search_card_dark = await page.locator(".search-filter-card").bounding_box()
        clip_search_dark = {
            "x": 0,
            "y": max(0, search_card_dark["y"] - 10),
            "width": 375,
            "height": min(650, search_card_dark["height"] + 20)
        }
        await page.screenshot(path=f"{artifact_dir}/verified_dict_filters_dark.png", clip=clip_search_dark)
        
        # Cards & Traps Dark
        await page.evaluate("() => { const card = document.querySelector('.dict-card'); if (card) card.scrollIntoView(); }")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/verified_dict_cards_dark.png")
        
        # Zoomed Traps section Dark
        trap_box_dark = await page.locator(".traps-section").first.bounding_box()
        if trap_box_dark:
            clip_trap_dark = {
                "x": 0,
                "y": max(0, trap_box_dark["y"] - 10),
                "width": 375,
                "height": min(400, trap_box_dark["height"] + 20)
            }
            await page.screenshot(path=f"{artifact_dir}/verified_dict_traps_zoom_dark.png", clip=clip_trap_dark)
        
        print("All verification screenshots and measurements completed successfully!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

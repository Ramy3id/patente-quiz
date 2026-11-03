import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2)
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html")
        await page.evaluate("""() => {
            document.querySelectorAll('.patente-gdpr-banner').forEach(el => el.remove());
            localStorage.setItem('patente_gdpr_consent', 'true');
            document.documentElement.className = 'light';
        }""")
        await page.wait_for_timeout(300)
        
        # Scroll to search filter card
        await page.evaluate("() => { document.querySelector('.search-filter-card').scrollIntoView(); }")
        await page.wait_for_timeout(300)
        
        artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
        await page.screenshot(path=f"{artifact_dir}/verified_dict_filters_full_light.png")
        
        await page.evaluate("() => { document.documentElement.className = 'dark'; }")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/verified_dict_filters_full_dark.png")
        
        print("Captured full filter views")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect())

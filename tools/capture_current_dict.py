import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2)
        page = await context.new_page()
        
        await page.goto("http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html", wait_until="networkidle")
        await page.wait_for_timeout(600)
        
        await page.evaluate("""() => {
            document.querySelectorAll('.patente-gdpr-banner').forEach(el => el.remove());
        }""")
        
        artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
        
        # Light mode scroll to trap section
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        await page.evaluate("() => window.scrollTo(0, 950)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/dict_traps_light.png")
        
        # Dark mode
        await page.evaluate("() => { document.documentElement.className = 'dark'; }")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/dict_traps_dark.png")
        
        print("Captured traps views")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

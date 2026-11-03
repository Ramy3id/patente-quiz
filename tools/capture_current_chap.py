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
        
        # Remove GDPR banner
        await page.evaluate("""() => {
            document.querySelectorAll('.patente-gdpr-banner').forEach(el => el.remove());
            localStorage.setItem('patente_gdpr_consent', 'true');
        }""")
        
        artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
        
        # Light mode top
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/current_chap_top_light.png")
        
        # Scroll to hub
        await page.evaluate("() => window.scrollTo(0, 320)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/current_chap_hub_light.png")
        
        # Scroll to group card
        await page.evaluate("() => window.scrollTo(0, 750)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/current_chap_card_light.png")
        
        print("Captured current chapter screenshots")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

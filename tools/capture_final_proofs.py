import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 375, 'height': 812})
        
        # 1. Bento Grid on index.html
        await page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
        await page.wait_for_timeout(500)
        # Dismiss cookie banner if present
        await page.evaluate('''() => {
            const b = document.getElementById('gdprConsentBanner') || document.querySelector('.gdpr-banner-container');
            if (b) b.remove();
            try { localStorage.setItem('patente_gdpr_consent', 'true'); } catch(e){}
        }''')
        await page.wait_for_timeout(300)
        
        # Scroll down slightly so Bento Grid is perfectly centered
        await page.evaluate('window.scrollTo(0, 240)')
        await page.wait_for_timeout(300)
        await page.screenshot(
            path='C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_mobile_bento_fixed.png'
        )
        
        # 2. Dizionario Sinonimi
        await page.goto('http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html')
        await page.wait_for_timeout(500)
        await page.evaluate('''() => {
            const b = document.getElementById('gdprConsentBanner') || document.querySelector('.gdpr-banner-container');
            if (b) b.remove();
        }''')
        await page.evaluate('window.scrollTo(0, 180)')
        await page.wait_for_timeout(300)
        await page.screenshot(
            path='C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_mobile_dizionario_fixed.png'
        )
        
        await b.close()
        print("ALL VERIFICATION SCREENSHOTS SAVED!")

if __name__ == '__main__':
    asyncio.run(run())

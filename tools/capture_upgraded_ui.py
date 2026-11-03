import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        context = await b.new_context(viewport={'width': 375, 'height': 812})
        await context.add_init_script("localStorage.setItem('patente_gdpr_consent', 'true'); localStorage.setItem('patente_cookie_consent', 'accepted');")
        page = await context.new_page()
        
        await page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
        await page.wait_for_timeout(600)
        await page.evaluate('''() => {
            const b = document.getElementById('gdprConsentBanner') || document.querySelector('.gdpr-banner-container') || document.querySelector('.patente-gdpr-banner');
            if (b) b.remove();
        }''')
        await page.wait_for_timeout(300)
        
        # 1. Collapsed Hero + Bento (4 cards) + 2-Row Chips
        await page.evaluate('window.scrollTo(0, 100)')
        await page.screenshot(
            path='C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_4_bento_centered_hero_chips.png',
            clip={'x': 0, 'y': 0, 'width': 375, 'height': 720}
        )
        
        # 2. Click button to expand and capture expanded bento
        await page.click('#btnToggleBentoTools')
        await page.wait_for_timeout(400)
        await page.screenshot(
            path='C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_bento_expanded_13.png',
            clip={'x': 0, 'y': 150, 'width': 375, 'height': 700}
        )
        
        # 3. Scroll down to chapter cards (Capitolo 16-18)
        # Also remove scroll-top button from blocking screenshot or adjust it
        await page.evaluate('window.scrollTo(0, 5200)')
        await page.wait_for_timeout(600)
        await page.screenshot(
            path='C:/Users/Ramy Fahmy/.gemini/antigravity/brain/e7065af7-148e-49c5-9b06-fabf7a80a8e1/verified_chapter_cards_harmonized.png',
            clip={'x': 0, 'y': 0, 'width': 375, 'height': 600}
        )
        
        await b.close()
        print("PERFECT PROOFS CAPTURED WITHOUT POPUPS!")

if __name__ == '__main__':
    asyncio.run(run())

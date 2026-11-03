import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 375, "height": 812},
            device_scale_factor=2
        )
        page = await context.new_page()
        
        # Navigate to dashboard.html
        await page.goto("http://localhost:8080/interactive_pages/dashboard.html", wait_until="networkidle")
        
        # Dismiss cookie banner
        try:
            btn = page.get_by_role("button", name="قبول ومتابعة")
            if await btn.is_visible():
                await btn.click()
        except Exception:
            pass

        await page.evaluate("""() => {
            const el = document.getElementById('cookieConsentBanner') || document.querySelector('.cookie-consent-overlay') || document.querySelector('.cookie-banner');
            if (el) el.remove();
        }""")
        
        # Ensure guestDashboardNotice is visible for verification
        await page.evaluate("""() => {
            const el = document.getElementById('guestDashboardNotice');
            if (el) el.style.display = 'block';
        }""")
        
        await page.wait_for_timeout(500)
        
        artifact_dir = r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1"
        
        # 1. Test Light Mode
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        await page.wait_for_timeout(300)
        
        # Button text color check
        btn_span_color = await page.evaluate("""() => {
            const span = document.querySelector('#guestDashboardNotice button span');
            return span ? window.getComputedStyle(span).color : null;
        }""")
        print(f"Light Mode Button Span Color: {btn_span_color}")
        
        await page.screenshot(path=f"{artifact_dir}/verified_dash_light.png")
        
        # 2. Test Dark Mode
        await page.evaluate("() => { document.documentElement.className = 'dark'; }")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/verified_dash_dark.png")
        
        # Zoomed clip on banner + tabs (height 450 to show everything cleanly)
        banner_box = await page.locator("#guestDashboardNotice").bounding_box()
        clip_box = {
            "x": 0,
            "y": max(0, banner_box["y"] - 10),
            "width": 375,
            "height": 450
        }
        await page.screenshot(path=f"{artifact_dir}/verified_dash_header_zoom_dark.png", clip=clip_box)
        
        await page.evaluate("() => { document.documentElement.className = 'light'; }")
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{artifact_dir}/verified_dash_header_zoom_light.png", clip=clip_box)
        
        print("All screenshots captured successfully.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

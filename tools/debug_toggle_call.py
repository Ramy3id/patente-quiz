import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        
        url = "http://localhost:8080/Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/index.html"
        await page.goto(url, wait_until="networkidle")
        
        res = await page.evaluate("""() => {
            console.log('window.toggleExtraSubtopics type:', typeof window.toggleExtraSubtopics);
            try {
                window.toggleExtraSubtopics();
                const container = document.getElementById('extraSubtopicsContainer');
                return {
                    success: true,
                    isExpanded: container ? container.classList.contains('is-expanded') : false,
                    className: container ? container.className : null
                };
            } catch(e) {
                return { success: false, error: e.toString() };
            }
        }""")
        print("Toggle call result:", res)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect())

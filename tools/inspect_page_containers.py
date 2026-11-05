import asyncio
from playwright.async_api import async_playwright

async def inspect_page_containers():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()
        
        pages = [
            ("dizionario", "http://localhost:8080/Capitoli_Divisi/dizionario-sinonimi.html"),
            ("piano_studio", "http://localhost:8080/interactive_pages/piano-studio.html"),
            ("scheda_esame", "http://localhost:8080/interactive_pages/scheda-esame.html"),
            ("decodificatore", "http://localhost:8080/interactive_pages/decodificatore-incroci.html")
        ]
        
        for name, url in pages:
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(400)
            
            res = await page.evaluate("""() => {
                const bodyChildren = Array.from(document.body.children)
                    .filter(el => el.id !== 'globalPortalNav' && el.id !== 'globalPortalFooter' && el.tagName !== 'SCRIPT' && el.tagName !== 'STYLE');
                return bodyChildren.map(el => {
                    const cs = window.getComputedStyle(el);
                    const r = el.getBoundingClientRect();
                    return {
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        width: r.width,
                        maxWidth: cs.maxWidth,
                        margin: cs.margin
                    };
                });
            }""")
            print(f"=== {name} ===")
            for item in res:
                print(f"  <{item['tag']}#{item['id']}.{item['className']}> width={item['width']} maxWidth={item['maxWidth']}")
                
        await browser.close()

asyncio.run(inspect_page_containers())

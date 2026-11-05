from playwright.sync_api import sync_playwright

widths = [1920, 1440, 1366, 1280, 1200, 1150, 1100, 1050, 1024, 992, 850, 768, 412, 390]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for w in widths:
        context = browser.new_context(viewport={"width": w, "height": 800})
        page = context.new_page()
        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        page.wait_for_timeout(300)
        overlap = page.evaluate("""() => {
            const search = document.getElementById('btnOpenGlobalSearch');
            const auth = document.getElementById('globalAuthPill');
            if (!search || !auth) return 'elements missing';
            const s = search.getBoundingClientRect();
            const a = auth.getBoundingClientRect();
            // Check intersection
            const xOverlap = Math.max(0, Math.min(s.right, a.right) - Math.max(s.left, a.left));
            const yOverlap = Math.max(0, Math.min(s.bottom, a.bottom) - Math.max(s.top, a.top));
            return {
                search: {left: s.left, right: s.right, top: s.top, bottom: s.bottom, visible: s.width > 0 && s.height > 0},
                auth: {left: a.left, right: a.right, top: a.top, bottom: a.bottom, visible: a.width > 0 && a.height > 0},
                xOverlap, yOverlap
            };
        }""")
        print(f"Width {w}:", overlap)
        context.close()
    browser.close()

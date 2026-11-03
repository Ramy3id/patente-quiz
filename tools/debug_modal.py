from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 375, 'height': 812})
    page = context.new_page()
    page.goto('http://localhost:8080/interactive_pages/decodificatore-incroci.html')
    page.wait_for_load_state('networkidle')
    html_class = page.evaluate('document.documentElement.className')
    print('Initial html class:', html_class)
    
    # 1. Open modal in initial state
    page.click('#btnOpenFigureModal')
    page.wait_for_timeout(400)
    
    data_initial = page.evaluate('''() => {
        const card = document.querySelector(".fig-modal-card");
        const search = document.querySelector(".fig-modal-search");
        const close = document.querySelector(".fig-modal-close");
        const cardS = window.getComputedStyle(card);
        const searchS = window.getComputedStyle(search);
        const closeS = window.getComputedStyle(close);
        const closeRect = close.getBoundingClientRect();
        return {
            htmlClass: document.documentElement.className,
            cardBg: cardS.backgroundColor,
            searchBg: searchS.backgroundColor,
            searchColor: searchS.color,
            closeWidth: closeS.width,
            closeHeight: closeS.height,
            closeRectWidth: closeRect.width,
            closeRectHeight: closeRect.height,
            closeBorderRadius: closeS.borderRadius
        };
    }''')
    print('Initial state data:', data_initial)
    page.screenshot(path='test_initial_modal.png')
    
    # 2. Test in Light mode
    page.evaluate('''() => {
        localStorage.setItem("patente_theme", "light");
        window.applyTheme("light");
    }''')
    page.wait_for_timeout(300)
    data_light = page.evaluate('''() => {
        const card = document.querySelector(".fig-modal-card");
        const search = document.querySelector(".fig-modal-search");
        const close = document.querySelector(".fig-modal-close");
        const cardS = window.getComputedStyle(card);
        const searchS = window.getComputedStyle(search);
        const closeS = window.getComputedStyle(close);
        const closeRect = close.getBoundingClientRect();
        return {
            htmlClass: document.documentElement.className,
            cardBg: cardS.backgroundColor,
            searchBg: searchS.backgroundColor,
            searchColor: searchS.color,
            closeWidth: closeS.width,
            closeHeight: closeS.height,
            closeRectWidth: closeRect.width,
            closeRectHeight: closeRect.height
        };
    }''')
    print('Light state data:', data_light)
    page.screenshot(path='test_light_modal.png')
    
    # 3. Test in Dark mode
    page.evaluate('''() => {
        localStorage.setItem("patente_theme", "dark");
        window.applyTheme("dark");
    }''')
    page.wait_for_timeout(300)
    data_dark = page.evaluate('''() => {
        const card = document.querySelector(".fig-modal-card");
        const search = document.querySelector(".fig-modal-search");
        const close = document.querySelector(".fig-modal-close");
        const cardS = window.getComputedStyle(card);
        const searchS = window.getComputedStyle(search);
        const closeS = window.getComputedStyle(close);
        const closeRect = close.getBoundingClientRect();
        return {
            htmlClass: document.documentElement.className,
            cardBg: cardS.backgroundColor,
            searchBg: searchS.backgroundColor,
            searchColor: searchS.color,
            closeWidth: closeS.width,
            closeHeight: closeS.height,
            closeRectWidth: closeRect.width,
            closeRectHeight: closeRect.height
        };
    }''')
    print('Dark state data:', data_dark)
    page.screenshot(path='test_dark_modal.png')

    browser.close()

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8080/interactive_pages/decodificatore-incroci.html')
    rules = page.evaluate('''() => {
        const btn = document.querySelector(".fig-modal-close");
        const styles = window.getComputedStyle(btn);
        return {
            minHeight: styles.minHeight,
            height: styles.height,
            maxHeight: styles.maxHeight,
            lineHeight: styles.lineHeight,
            padding: styles.padding,
            boxSizing: styles.boxSizing
        };
    }''')
    print('Computed:', rules)
    browser.close()

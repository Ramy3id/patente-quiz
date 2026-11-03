import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8080/Capitoli_Divisi/index.html')
    
    rules = page.evaluate('''() => {
        const el = document.querySelector(".chapter-card");
        const matched = [];
        for (const sheet of document.styleSheets) {
            try {
                for (const rule of sheet.cssRules) {
                    if (rule.selectorText && el.matches(rule.selectorText)) {
                        if (rule.style.display && rule.style.getPropertyPriority('display') === 'important') {
                            matched.push({
                                sheet: sheet.href || 'inline',
                                selector: rule.selectorText,
                                display: rule.style.display,
                                important: rule.style.getPropertyPriority('display')
                            });
                        }
                    }
                }
            } catch(e) {}
        }
        return matched;
    }''')
    print('Matching important display rules:', rules)
    browser.close()

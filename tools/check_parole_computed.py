from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto('http://localhost:8080/Capitoli_Divisi/parole-quiz.html', wait_until='networkidle')
        
        info = page.evaluate("""() => {
            const chipsActions = document.querySelector('.chips-actions');
            const segBar = document.querySelector('.segmented-filter-bar');
            const shelf = document.querySelector('.families-shelf');
            return {
                theme: document.documentElement.className,
                chipsActions: chipsActions ? {
                    bg: window.getComputedStyle(chipsActions).backgroundColor,
                    border: window.getComputedStyle(chipsActions).border,
                    boxShadow: window.getComputedStyle(chipsActions).boxShadow
                } : null,
                segBar: segBar ? {
                    bg: window.getComputedStyle(segBar).backgroundColor,
                    border: window.getComputedStyle(segBar).border,
                    boxShadow: window.getComputedStyle(segBar).boxShadow
                } : null,
                shelf: shelf ? {
                    display: window.getComputedStyle(shelf).display,
                    overflowX: window.getComputedStyle(shelf).overflowX,
                    gridTemplateColumns: window.getComputedStyle(shelf).gridTemplateColumns
                } : null
            };
        }""")
        print("Computed info light/dark:", info)
        
        # Now let's force light mode and check
        page.evaluate("() => { document.documentElement.className = 'light'; }")
        info_light = page.evaluate("""() => {
            const chipsActions = document.querySelector('.chips-actions');
            const segBar = document.querySelector('.segmented-filter-bar');
            const shelf = document.querySelector('.families-shelf');
            return {
                chipsActions: chipsActions ? {
                    bg: window.getComputedStyle(chipsActions).backgroundColor,
                    border: window.getComputedStyle(chipsActions).border,
                } : null,
                segBar: segBar ? {
                    bg: window.getComputedStyle(segBar).backgroundColor,
                    border: window.getComputedStyle(segBar).border,
                } : null,
                shelf: shelf ? {
                    display: window.getComputedStyle(shelf).display,
                    overflowX: window.getComputedStyle(shelf).overflowX,
                } : null
            };
        }""")
        print("Computed info light mode:", info_light)
        browser.close()

if __name__ == '__main__':
    test()

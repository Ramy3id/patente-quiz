import sys
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

def test_dom():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:8080/Capitoli_Divisi/index.html', wait_until='networkidle')
        
        info = page.evaluate("""() => {
            const canonical = document.querySelector('link[rel="canonical"]');
            const opensearch = document.querySelector('link[rel="search"]');
            const ogTitle = document.querySelector('meta[property="og:title"]');
            const ogImage = document.querySelector('meta[property="og:image"]');
            const twitter = document.querySelector('meta[name="twitter:card"]');
            return {
                canonical: canonical ? canonical.href : null,
                opensearch: opensearch ? opensearch.href : null,
                ogTitle: ogTitle ? ogTitle.content : null,
                ogImage: ogImage ? ogImage.content : null,
                twitter: twitter ? twitter.content : null,
            };
        }""")
        print("DOM SEO Info for Capitoli_Divisi/index.html:", info)
        browser.close()

if __name__ == '__main__':
    test_dom()

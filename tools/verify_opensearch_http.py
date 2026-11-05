from playwright.sync_api import sync_playwright

def test_opensearch():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        res = page.goto('http://localhost:8080/opensearch.xml')
        print("opensearch.xml HTTP status:", res.status)
        content = page.content()
        print("Has OpenSearchDescription:", 'OpenSearchDescription' in content)
        print("Has ShortName:", 'Patente B Pro' in content)
        browser.close()

if __name__ == '__main__':
    test_opensearch()

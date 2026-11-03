import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 390, 'height': 844})
        page.add_init_script("localStorage.setItem('patente_gdpr_consent', 'accepted');")
        page.goto('http://localhost:8080/interactive_pages/trucchi-esame.html')
        page.wait_for_timeout(600)
        
        # Click Tab 2
        btn_duals = page.locator('.tr-tab-btn:has-text("فخاخ اللوحات")')
        btn_duals.click()
        page.wait_for_timeout(300)
        assert page.is_visible('#tabDuals'), "tabDuals should be visible"
        print("Tab 2 (Duals) switch verified!")
        
        # Click Tab 5 (Quiz)
        btn_quiz = page.locator('.tr-tab-btn:has-text("كويز التحدي")')
        btn_quiz.click()
        page.wait_for_timeout(300)
        assert page.is_visible('#tabQuiz'), "tabQuiz should be visible"
        print("Tab 5 (Quiz) switch verified!")
        
        # Click Tab 1 (Constitution)
        btn_const = page.locator('.tr-tab-btn:has-text("دستور الأبواب")')
        btn_const.click()
        page.wait_for_timeout(300)
        assert page.is_visible('#tabConstitution'), "tabConstitution should be visible"
        print("Tab 1 (Constitution) switch verified!")
        
        browser.close()

if __name__ == '__main__':
    test()

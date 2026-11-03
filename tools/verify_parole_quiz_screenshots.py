import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

output_dir = r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1'

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Mobile Light Mode (390x844)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://127.0.0.1:8080/Capitoli_Divisi/parole-quiz.html')
    page.wait_for_load_state('networkidle')
    
    # Ensure Light Mode
    page.evaluate("() => { document.documentElement.classList.remove('dark'); document.documentElement.classList.add('light'); localStorage.setItem('patente_theme_mode', 'light'); }")
    page.wait_for_timeout(300)
    
    # Click on preset pack to populate words
    page.click('.btn-action-preset:first-child')
    page.wait_for_timeout(500)
    
    # Screenshot top view (Hero, Presets, and Word Bank)
    page.screenshot(path=f'{output_dir}\\parole_quiz_mobile_light_verified.png')
    print('Captured parole_quiz_mobile_light_verified.png')
    
    # Scroll slightly to see chips in full glory
    page.evaluate("window.scrollTo(0, 260)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\parole_quiz_chips_light_verified.png')
    print('Captured parole_quiz_chips_light_verified.png')
    
    # 2. Mobile Dark Mode (390x844)
    page.evaluate("() => { document.documentElement.classList.remove('light'); document.documentElement.classList.add('dark'); localStorage.setItem('patente_theme_mode', 'dark'); }")
    page.wait_for_timeout(300)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{output_dir}\\parole_quiz_mobile_dark_verified.png')
    print('Captured parole_quiz_mobile_dark_verified.png')
    
    # 3. Desktop Light Mode (1200x800)
    desktop_page = browser.new_page(viewport={'width': 1200, 'height': 900})
    desktop_page.goto('http://127.0.0.1:8080/Capitoli_Divisi/parole-quiz.html')
    desktop_page.wait_for_load_state('networkidle')
    desktop_page.evaluate("() => { document.documentElement.classList.remove('dark'); document.documentElement.classList.add('light'); localStorage.setItem('patente_theme_mode', 'light'); }")
    desktop_page.wait_for_timeout(300)
    desktop_page.click('.btn-action-preset:first-child')
    desktop_page.wait_for_timeout(500)
    desktop_page.screenshot(path=f'{output_dir}\\parole_quiz_desktop_light_verified.png')
    print('Captured parole_quiz_desktop_light_verified.png')
    
    browser.close()
    print('All screenshots taken successfully.')

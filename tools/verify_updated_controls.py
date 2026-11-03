import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 375, 'height': 812})
    page = context.new_page()
    page.goto('http://localhost:8080/interactive_pages/decodificatore-incroci.html')
    page.wait_for_load_state('networkidle')
    
    # 1. Force light mode
    page.evaluate('window.applyTheme("light")')
    page.wait_for_timeout(300)
    
    # Verify arrow geometry
    arrow_data = page.evaluate('''() => {
        const wrap = document.querySelector(".sim-arrows-wrap");
        const prevBtn = wrap.querySelectorAll("button")[0];
        const nextBtn = wrap.querySelectorAll("button")[1];
        
        const prevArrow = prevBtn.querySelector(".nav-arrow-icon").getBoundingClientRect();
        const prevText = prevBtn.querySelector("span:not(.nav-arrow-icon)").getBoundingClientRect();
        
        const nextArrow = nextBtn.querySelector(".nav-arrow-icon").getBoundingClientRect();
        const nextText = nextBtn.querySelector("span:not(.nav-arrow-icon)").getBoundingClientRect();
        
        return {
            prevHTML: prevBtn.innerHTML.trim(),
            nextHTML: nextBtn.innerHTML.trim(),
            prevArrowX: prevArrow.x,
            prevTextX: prevText.x,
            isPrevArrowBeforeInRTL: prevArrow.x > prevText.x,
            nextArrowX: nextArrow.x,
            nextTextX: nextText.x,
            isNextArrowAfterInRTL: nextArrow.x < nextText.x
        };
    }''')
    print('Arrow check:', arrow_data)
    
    # Verify playback buttons & sub-actions row
    btns_data = page.evaluate('''() => {
        const playBtn = document.getElementById("btnSimPlay");
        const stepBtn = document.getElementById("btnSimStep");
        const resetBtn = document.querySelector(".btn-sim-reset");
        const radarBtn = document.getElementById("btnRadarToggle");
        const audioBtn = document.getElementById("btnAudioToggle");
        const speedBtn = document.getElementById("btnSpeedCycle");
        
        const playS = window.getComputedStyle(playBtn);
        const subS = window.getComputedStyle(radarBtn);
        
        return {
            playHeight: playS.height,
            subHeight: subS.height,
            radarText: radarBtn.innerText.trim(),
            audioText: audioBtn.innerText.trim(),
            speedText: speedBtn.innerText.trim()
        };
    }''')
    print('Buttons data:', btns_data)
    
    # Test clicking speed cycle button
    speed1 = page.evaluate('document.getElementById("btnSpeedLabel").textContent')
    page.click('#btnSpeedCycle')
    page.wait_for_timeout(100)
    speed2 = page.evaluate('document.getElementById("btnSpeedLabel").textContent')
    page.click('#btnSpeedCycle')
    page.wait_for_timeout(100)
    speed3 = page.evaluate('document.getElementById("btnSpeedLabel").textContent')
    page.click('#btnSpeedCycle')
    page.wait_for_timeout(100)
    speed4 = page.evaluate('document.getElementById("btnSpeedLabel").textContent')
    print('Speed cycle progression:', [speed1, speed2, speed3, speed4])
    
    # Test clicking audio toggle
    audio1 = page.evaluate('document.getElementById("btnAudioText").textContent')
    page.click('#btnAudioToggle')
    page.wait_for_timeout(100)
    audio2 = page.evaluate('document.getElementById("btnAudioText").textContent')
    page.click('#btnAudioToggle')
    page.wait_for_timeout(100)
    audio3 = page.evaluate('document.getElementById("btnAudioText").textContent')
    print('Audio toggle progression:', [audio1, audio2, audio3])
    
    # Capture screenshots of simulation section in Light Mode
    sim_section = page.locator('#trafficSimSection')
    sim_section.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_sim_full_controls_light.png')
    
    # Capture zoom-in of the nav header and the control buttons
    page.locator('.sim-nav-header').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_sim_arrows_exact_light.png')
    page.locator('.sim-stage-col').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_sim_canvas_and_controls_light.png')
    
    # 2. Switch to Dark Mode & capture
    page.evaluate('window.applyTheme("dark")')
    page.wait_for_timeout(300)
    sim_section.screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_sim_full_controls_dark.png')
    page.locator('.sim-stage-col').screenshot(path=r'C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\verified_sim_canvas_and_controls_dark.png')
    
    browser.close()
    print('Verification completed successfully!')

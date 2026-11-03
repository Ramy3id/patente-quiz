import sys
import os
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi"
chapters = sorted([d for d in os.listdir(base_dir) if d.startswith("Capitolo_") and os.path.isdir(os.path.join(base_dir, d))])

failed = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for chap in chapters:
        url = f"http://localhost:8080/Capitoli_Divisi/{chap}/index.html"
        page.goto(url)
        page.wait_for_selector('.subtopic-section-box', timeout=10000)

        # 1. Check chips order
        chip_spans = page.query_selector_all('#subtopics-chips-bar .subtopic-chip:not([data-filter="all"]) span:first-child')
        chip_nums = []
        for s in chip_spans:
            text = s.inner_text()
            m = re.search(r'(\d+)\.', text)
            if m:
                chip_nums.append(int(m.group(1)))

        # 2. Check sections order
        sections = page.query_selector_all('.subtopic-section-box')
        sec_nums = []
        for sec in sections:
            num_pill = sec.query_selector('.subtopic-num-pill')
            if num_pill:
                m = re.search(r'الجزء\s*(\d+)', num_pill.inner_text())
                if m:
                    sec_nums.append(int(m.group(1)))

        chips_ok = (chip_nums == sorted(chip_nums) and len(chip_nums) > 0)
        secs_ok = (sec_nums == sorted(sec_nums) and len(sec_nums) > 0)

        if chips_ok and secs_ok:
            print(f"✅ {chap}: {len(sec_nums)} sections sorted ({sec_nums[0]}..{sec_nums[-1]}) | {len(chip_nums)} chips sorted ({chip_nums[0]}..{chip_nums[-1]})")
        else:
            print(f"❌ {chap}: secs={sec_nums}, chips={chip_nums}")
            failed.append((chap, sec_nums, chip_nums))

    browser.close()

if failed:
    print(f"\nFAILED CHAPTERS: {len(failed)}")
else:
    print(f"\n🎉 ALL 25 CHAPTERS ARE 100% PERFECTLY SORTED!")

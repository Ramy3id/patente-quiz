# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject script include for data-radar-expanded.js
target_script = '<script src="../assets/js/question-decoder.js"></script>'
replacement_script = '<script src="../assets/js/question-decoder.js"></script>\n  <script src="../assets/js/data-radar-expanded.js"></script>'

if target_script in html and 'data-radar-expanded.js' not in html:
    html = html.replace(target_script, replacement_script)
    print("Injected data-radar-expanded.js script tag.")
else:
    print("Script tag already present or target not found.")

# 2. Add CSS rules in <style>
extra_css = """
    /* ================= MASTER RADAR TABS ================= */
    .ps-master-tabs {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-bottom: 24px;
    }
    @media (max-width: 768px) {
      .ps-master-tabs {
        grid-template-columns: 1fr;
        gap: 10px;
      }
    }
    .ps-master-tab {
      background: var(--ps-card-bg);
      border: 1px solid var(--ps-card-border);
      border-radius: 18px;
      padding: 16px;
      display: flex;
      align-items: center;
      gap: 14px;
      cursor: pointer;
      text-align: right;
      transition: all 0.25s ease;
      position: relative;
      color: var(--ps-text);
      font-family: inherit;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    .ps-master-tab:hover {
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    .ps-master-tab.active {
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.14) 0%, rgba(15, 23, 42, 0.85) 100%);
      border-color: var(--ps-cyan);
      box-shadow: 0 0 24px rgba(56, 189, 248, 0.18);
    }
    html.light .ps-master-tab.active {
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.08) 0%, #FFFFFF 100%);
      border-color: #0284C7;
      box-shadow: 0 6px 18px rgba(2, 132, 199, 0.15);
    }
    .pmt-icon {
      font-size: 2rem;
      line-height: 1;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }
    .pmt-content {
      flex: 1;
    }
    .pmt-title {
      display: block;
      font-weight: 800;
      font-size: 1.05rem;
      margin-bottom: 3px;
      color: var(--ps-text);
    }
    .pmt-desc {
      display: block;
      font-size: 0.8rem;
      color: var(--ps-text-sub);
    }
    .pmt-badge {
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 999px;
      background: rgba(245, 158, 11, 0.15);
      color: var(--ps-amber);
      border: 1px solid rgba(245, 158, 11, 0.3);
      position: absolute;
      top: 12px;
      left: 12px;
    }

    /* Radar Section Wrapper */
    .radar-tab-section {
      animation: fadeInTab 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes fadeInTab {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Mini Hero Intro Strip */
    .radar-intro-strip {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--ps-card-border);
      border-radius: 16px;
      padding: 16px 20px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 16px;
    }
    html.light .radar-intro-strip {
      background: #F8FAFC;
    }
    .radar-intro-icon {
      font-size: 2.2rem;
      line-height: 1;
    }
    .radar-intro-body h3 {
      margin: 0 0 4px 0;
      font-size: 1.05rem;
      font-weight: 800;
    }
    .radar-intro-body p {
      margin: 0;
      font-size: 0.86rem;
      color: var(--ps-text-sub);
      line-height: 1.5;
    }

    /* Sign & Theory Cards */
    .ps-sign-card, .ps-theory-card {
      background: var(--ps-card-bg);
      border: 1px solid var(--ps-card-border);
      border-radius: 18px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      position: relative;
    }
    .ps-sign-card:hover, .ps-theory-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
      border-color: rgba(56, 189, 248, 0.3);
    }
    .sign-card-thumb-wrap {
      text-align: center;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--ps-card-border);
      border-radius: 14px;
      padding: 12px;
      margin: 12px 0;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 110px;
    }
    html.light .sign-card-thumb-wrap {
      background: #F1F5F9;
    }
    .sign-card-thumb {
      max-height: 95px;
      max-width: 100%;
      object-fit: contain;
      filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15));
    }
    .trap-keyword-box {
      background: rgba(244, 63, 94, 0.08);
      border: 1px dashed rgba(244, 63, 94, 0.3);
      border-radius: 10px;
      padding: 8px 12px;
      margin-bottom: 10px;
      font-size: 0.88rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .trap-keyword-box.vero-key {
      background: rgba(16, 185, 129, 0.08);
      border-color: rgba(16, 185, 129, 0.3);
    }
    .trap-expl-text {
      font-size: 0.86rem;
      line-height: 1.6;
      color: var(--ps-text-sub);
      margin-bottom: 12px;
    }
    .rule-action-btn {
      width: 100%;
      background: rgba(56, 189, 248, 0.1);
      color: var(--ps-cyan);
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 12px;
      padding: 10px;
      font-weight: 800;
      font-family: inherit;
      font-size: 0.88rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s ease;
    }
    .rule-action-btn:hover {
      background: var(--ps-cyan);
      color: #0F172A;
      border-color: var(--ps-cyan);
    }
"""

if '/* ================= MASTER RADAR TABS ================= */' not in html:
    html = html.replace('</style>', extra_css + '\n  </style>', 1)
    print("Injected CSS for master tabs and cards.")

with open('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'w', encoding='utf-8') as f:
    f.write(html)

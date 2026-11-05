import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Comprehensive Master CSS Overhaul for piano-studio.html
modern_piano_css = """
  /* ==========================================================================
     PROFESSIONAL BENTO & MODULAR OVERHAUL FOR PIANO-STUDIO
     ========================================================================== */

  /* Global Surface Polish */
  .sp-container {
    max-width: 1100px !important;
    margin: 16px auto 70px !important;
    padding: 0 16px !important;
  }

  /* Block 1: Hero & Live Metrics */
  .sp-hero {
    background: var(--sp-surface) !important;
    border: 1px solid var(--sp-border) !important;
    border-radius: 22px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04) !important;
  }
  @media (max-width: 600px) {
    .sp-hero {
      padding: 18px 14px !important;
      border-radius: 18px !important;
    }
  }

  .sp-hero-top {
    display: flex !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    gap: 16px !important;
    flex-wrap: wrap !important;
    margin-bottom: 16px !important;
  }
  .sp-hero-title {
    font-size: 1.55rem !important;
    font-weight: 900 !important;
    color: var(--sp-text) !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    margin-bottom: 6px !important;
    letter-spacing: -0.02em !important;
  }
  .sp-hero-desc {
    font-size: 0.92rem !important;
    color: var(--sp-text-sub) !important;
    max-width: 680px !important;
    line-height: 1.6 !important;
  }

  /* Hero Actions: Balanced Grid on Mobile */
  .sp-hero-actions {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 8px !important;
    width: 100% !important;
  }
  .sp-hero-actions button:last-child {
    grid-column: span 2 !important;
  }
  @media (min-width: 768px) {
    .sp-hero-actions {
      display: flex !important;
      width: auto !important;
      gap: 10px !important;
    }
    .sp-hero-actions button:last-child {
      grid-column: auto !important;
    }
  }

  .sp-btn {
    height: 40px !important;
    min-height: 40px !important;
    padding: 0 14px !important;
    border-radius: 12px !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    box-sizing: border-box !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
  }

  /* 4 Metrics Micro-Grid (2x2 on Mobile, 4 Cols on Desktop) */
  .sp-metrics-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 10px !important;
    margin-top: 16px !important;
  }
  @media (min-width: 768px) {
    .sp-metrics-grid {
      grid-template-columns: repeat(4, 1fr) !important;
    }
  }

  .sp-metric-box {
    background: var(--sp-surface-card) !important;
    border: 1px solid var(--sp-border) !important;
    border-radius: 14px !important;
    padding: 12px 8px !important;
    text-align: center !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
  }
  .sp-metric-num {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    color: var(--sp-cyan) !important;
    line-height: 1.2 !important;
    margin-bottom: 3px !important;
  }
  .sp-metric-lbl {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    color: var(--sp-text-sub) !important;
    white-space: nowrap !important;
  }

  /* Quick Training Modes: Balanced Bento Grid */
  .sp-quick-modes-grid {
    display: grid !important;
    grid-template-columns: 1fr !important;
    gap: 10px !important;
    margin-top: 18px !important;
    padding-top: 16px !important;
    border-top: 1px solid var(--sp-border) !important;
  }
  @media (min-width: 600px) {
    .sp-quick-modes-grid {
      grid-template-columns: repeat(2, 1fr) !important;
    }
  }
  @media (min-width: 1024px) {
    .sp-quick-modes-grid {
      grid-template-columns: repeat(3, 1fr) !important;
    }
  }

  .sp-quick-mode-card {
    background: var(--sp-surface-card) !important;
    border: 1px solid var(--sp-border) !important;
    border-radius: 14px !important;
    padding: 12px 14px !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    text-decoration: none !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-sizing: border-box !important;
  }
  .sp-quick-mode-card:hover {
    transform: translateY(-2px) !important;
    border-color: var(--sp-cyan) !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.12) !important;
  }
  .sp-quick-mode-icon {
    font-size: 1.5rem !important;
    width: 40px !important;
    height: 40px !important;
    border-radius: 10px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid var(--sp-border) !important;
  }
  .sp-quick-mode-info {
    flex: 1 !important;
    min-width: 0 !important;
  }
  .sp-quick-mode-title {
    font-size: 0.9rem !important;
    font-weight: 800 !important;
    color: var(--sp-text) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 6px !important;
    margin-bottom: 2px !important;
  }
  .sp-quick-mode-desc {
    font-size: 0.78rem !important;
    color: var(--sp-text-sub) !important;
    line-height: 1.3 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
  }

  /* Block 2: Readiness Index Card */
  .sp-readiness-card {
    background: var(--sp-surface) !important;
    border: 1px solid var(--sp-border) !important;
    border-radius: 22px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04) !important;
  }
  @media (max-width: 600px) {
    .sp-readiness-card {
      padding: 18px 14px !important;
      border-radius: 18px !important;
    }
  }

  .sp-readiness-chips-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 10px !important;
    margin: 16px 0 !important;
  }
  @media (min-width: 768px) {
    .sp-readiness-chips-grid {
      grid-template-columns: repeat(4, 1fr) !important;
    }
  }

  .sp-readiness-chip {
    background: var(--sp-surface-card) !important;
    border: 1px solid var(--sp-border) !important;
    border-radius: 12px !important;
    padding: 10px !important;
    text-align: center !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 4px !important;
  }
  .sp-readiness-chip-val {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    color: var(--sp-cyan) !important;
    line-height: 1.2 !important;
  }
  .sp-readiness-chip-label {
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    color: var(--sp-text-sub) !important;
    white-space: nowrap !important;
  }

  /* Block 3: Mission Card (Active Day) */
  .sp-mission-card {
    background: var(--sp-surface) !important;
    border: 2px solid rgba(2, 132, 199, 0.4) !important;
    border-radius: 22px !important;
    padding: 24px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 10px 32px rgba(2, 132, 199, 0.08) !important;
  }
  @media (max-width: 600px) {
    .sp-mission-card {
      padding: 18px 14px !important;
      border-radius: 18px !important;
    }
  }

  .sp-station-item {
    background: var(--sp-surface-card) !important;
    border: 1px solid var(--sp-border) !important;
    border-radius: 16px !important;
    padding: 14px 16px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 12px !important;
    margin-bottom: 10px !important;
    transition: all 0.2s ease !important;
  }
  @media (max-width: 550px) {
    .sp-station-item {
      flex-direction: column !important;
      align-items: stretch !important;
      gap: 10px !important;
    }
    .sp-station-main {
      width: 100% !important;
    }
  }

  /* Block 4: Timeline Map Section */
  .sp-timeline-section {
    background: var(--sp-surface) !important;
    border: 1px solid var(--sp-border) !important;
    border-radius: 22px !important;
    padding: 24px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04) !important;
  }
  @media (max-width: 600px) {
    .sp-timeline-section {
      padding: 18px 14px !important;
      border-radius: 18px !important;
    }
  }

  .sp-days-grid {
    display: grid !important;
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
  @media (min-width: 480px) {
    .sp-days-grid {
      grid-template-columns: repeat(2, 1fr) !important;
    }
  }
  @media (min-width: 900px) {
    .sp-days-grid {
      grid-template-columns: repeat(3, 1fr) !important;
    }
  }
  @media (min-width: 1100px) {
    .sp-days-grid {
      grid-template-columns: repeat(4, 1fr) !important;
    }
  }

  /* Block 5: Setup Wizard Modal Polished Blocks */
  .sp-modal-box {
    border-radius: 22px !important;
    padding: 24px !important;
    max-width: 680px !important;
  }
  @media (max-width: 600px) {
    .sp-modal-box {
      padding: 20px 16px !important;
      border-radius: 18px !important;
    }
  }
  .sp-question-block {
    background: var(--sp-surface-card) !important;
    border: 1px solid var(--sp-border) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    margin-bottom: 14px !important;
  }
  .sp-options-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
  }
  @media (min-width: 600px) {
    .sp-options-grid {
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)) !important;
    }
  }

  .sp-opt-card {
    border-radius: 12px !important;
    padding: 12px 8px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  }
  .sp-opt-card.selected {
    box-shadow: 0 3px 12px rgba(2, 132, 199, 0.2) !important;
  }

  /* Light Mode Specific Overrides: Crisp, Modern & No Ugly Grays */
  html.light .sp-hero,
  html.light .sp-readiness-card,
  html.light .sp-mission-card,
  html.light .sp-timeline-section,
  html.light .sp-modal-box {
    background: #FFFFFF !important;
    border-color: #E2E8F0 !important;
  }
  html.light .sp-metric-box,
  html.light .sp-readiness-chip,
  html.light .sp-station-item,
  html.light .sp-day-card,
  html.light .sp-question-block,
  html.light .sp-quick-mode-card {
    background: #F8FAFC !important;
    border-color: #E2E8F0 !important;
  }
  html.light .sp-quick-mode-icon {
    background: #FFFFFF !important;
    border-color: #E2E8F0 !important;
  }
  html.light .sp-opt-card {
    background: #FFFFFF !important;
    border-color: #CBD5E1 !important;
    color: #1E293B !important;
  }
  html.light .sp-opt-card.selected {
    background: #E0F2FE !important;
    border-color: #0284C7 !important;
    color: #0284C7 !important;
  }
"""

# Append before </style>
if '</style>' in content:
    content = content.replace('</style>', modern_piano_css + '\n</style>', 1)
    print("Injected modern piano CSS overhaul successfully.")
else:
    print("ERROR: </style> not found.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated piano-studio.html successfully.")

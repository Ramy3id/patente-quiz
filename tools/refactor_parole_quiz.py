import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Refine CSS in parole-quiz.html
refined_css = """
  /* ==========================================================================
     PERFECTED PAROLE-QUIZ UI (HERO STATS, PRESETS 2-ROW ON MOBILE, CRISP CHIPS)
     ========================================================================== */
  @media (max-width: 600px) {
    .glass-card {
      padding: 18px 14px !important;
      border-radius: 18px !important;
    }
  }

  /* Block 1: Hero Stats 3-Col Compact Grid */
  .hero-stats-row {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 8px !important;
    border-top: 1px solid var(--border-subtle) !important;
    padding-top: 14px !important;
    margin-top: 12px !important;
  }
  .stat-chip {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 8px 4px !important;
    border-radius: 12px !important;
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
  }
  .stat-chip strong {
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    color: #38bdf8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    line-height: 1.1 !important;
  }
  .stat-chip span {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    white-space: nowrap !important;
    margin-top: 2px !important;
  }

  /* Block 2: Preset Packs - 2 balanced rows on Mobile, 3 cols on Desktop */
  .preset-btn-group {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
    margin-top: 8px !important;
  }
  .preset-btn-group button:last-child {
    grid-column: span 2 !important;
  }
  @media (min-width: 640px) {
    .preset-btn-group {
      grid-template-columns: repeat(3, 1fr) !important;
    }
    .preset-btn-group button:last-child {
      grid-column: span 1 !important;
    }
  }

  .btn-action-preset {
    width: 100% !important;
    min-height: 38px !important;
    height: 38px !important;
    padding: 0 12px !important;
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #e4e4e7 !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 6px !important;
    transition: all 0.2s ease !important;
    font-family: inherit !important;
    box-sizing: border-box !important;
  }
  .preset-plus {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #38bdf8 !important;
    line-height: 1 !important;
  }
  .btn-action-preset:hover {
    background: rgba(56, 189, 248, 0.12) !important;
    border-color: rgba(56, 189, 248, 0.35) !important;
    color: #38bdf8 !important;
    transform: translateY(-1px) !important;
  }

  /* Block 3: Word Bank Input Row */
  @media (min-width: 480px) {
    .input-group-row {
      display: flex !important;
      gap: 8px !important;
    }
    .input-group-row .custom-input {
      flex: 1 !important;
    }
    .input-group-row .btn-primary {
      width: auto !important;
      white-space: nowrap !important;
    }
  }

  /* Block 3: Chips Toolbar & Actions */
  .chips-header {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    margin-bottom: 12px !important;
  }
  .chips-title {
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    color: #e4e4e7 !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
  }
  .chips-actions {
    display: inline-flex !important;
    align-items: center !important;
    gap: 4px !important;
    background: rgba(255, 255, 255, 0.03) !important;
    padding: 3px 5px !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
  }
  .btn-subtle {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #a1a1aa !important;
    padding: 4px 8px !important;
    height: 28px !important;
    line-height: 1 !important;
    border-radius: 6px !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 4px !important;
    transition: all 0.15s ease !important;
    font-family: inherit !important;
  }
  .btn-subtle:hover {
    color: #fff !important;
    background: rgba(255, 255, 255, 0.08) !important;
  }
  .btn-subtle.btn-subtle-danger:hover {
    color: #f43f5e !important;
    background: rgba(244, 63, 94, 0.12) !important;
  }

  /* Clean Chips Deck Container */
  .chips-wrapper {
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 6px 8px !important;
    min-height: 52px !important;
    padding: 12px 10px !important;
    background: rgba(24, 24, 27, 0.65) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    transition: all 0.25s ease !important;
  }

  .word-chip {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    background: rgba(39, 39, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 100px !important;
    padding: 4px 10px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: #f4f4f5 !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    user-select: none !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
  }
  .word-chip:hover {
    background: rgba(56, 189, 248, 0.15) !important;
    border-color: rgba(56, 189, 248, 0.4) !important;
    color: #38bdf8 !important;
    transform: translateY(-1px) !important;
  }
  .word-chip.active {
    background: linear-gradient(135deg, #0284c7, #2563eb) !important;
    border-color: #0284c7 !important;
    color: #ffffff !important;
    box-shadow: 0 3px 10px rgba(2, 132, 199, 0.35) !important;
  }
  .chip-count {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    padding: 1px 5px !important;
    background: rgba(255, 255, 255, 0.12) !important;
    border-radius: 100px !important;
    color: #cbd5e1 !important;
  }
  .word-chip.active .chip-count {
    background: rgba(255, 255, 255, 0.25) !important;
    color: #ffffff !important;
  }
  .chip-del {
    color: #a1a1aa !important;
    font-size: 1rem !important;
    line-height: 1 !important;
    margin-right: -2px !important;
    border-radius: 50% !important;
    width: 18px !important;
    height: 18px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.15s ease !important;
  }
  .word-chip.active .chip-del {
    color: rgba(255, 255, 255, 0.85) !important;
  }
  .chip-del:hover {
    color: #ffffff !important;
    background: rgba(244, 63, 94, 0.7) !important;
  }

  /* ==========================================================================
     LIGHT MODE OVERRIDES FOR PAROLE-QUIZ (CRISP, PURE WHITE & ACCENT BLUE)
     ========================================================================== */
  html.light .hero-stats-row {
    border-top: 1px solid rgba(15, 23, 42, 0.08) !important;
  }
  html.light .stat-chip {
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02) !important;
  }
  html.light .stat-chip strong {
    color: #0284c7 !important;
  }
  html.light .stat-chip span {
    color: #475569 !important;
  }
  html.light .btn-action-preset {
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    color: #1e293b !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
  }
  html.light .preset-plus {
    color: #0284c7 !important;
  }
  html.light .btn-action-preset:hover {
    background: #f0f9ff !important;
    border-color: #38bdf8 !important;
    color: #0284c7 !important;
  }
  html.light .chips-title {
    color: #0f172a !important;
  }
  html.light .chips-actions {
    background: #f1f5f9 !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
  }
  html.light .btn-subtle {
    color: #475569 !important;
  }
  html.light .btn-subtle:hover {
    color: #0f172a !important;
    background: rgba(15, 23, 42, 0.06) !important;
  }
  html.light .btn-subtle.btn-subtle-danger:hover {
    color: #e11d48 !important;
    background: rgba(225, 29, 72, 0.1) !important;
  }

  /* NO UGLY GRAY IN LIGHT MODE: PURE CLEAN WHITE CONTAINER WITH SUBTLE BORDER */
  html.light .chips-wrapper {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
  }
  html.light .word-chip {
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    color: #1e293b !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
  }
  html.light .word-chip:hover {
    background: #f0f9ff !important;
    border-color: #38bdf8 !important;
    color: #0284c7 !important;
  }
  html.light .word-chip.active {
    background: linear-gradient(135deg, #0284c7, #2563eb) !important;
    border-color: #0284c7 !important;
    color: #ffffff !important;
    box-shadow: 0 3px 10px rgba(2, 132, 199, 0.28) !important;
  }
  html.light .chip-count {
    background: #e2e8f0 !important;
    color: #334155 !important;
  }
  html.light .word-chip.active .chip-count {
    background: rgba(255, 255, 255, 0.25) !important;
    color: #ffffff !important;
  }
  html.light .chip-del {
    color: #64748b !important;
  }
  html.light .word-chip.active .chip-del {
    color: #ffffff !important;
  }
  html.light .chip-del:hover {
    color: #ffffff !important;
    background: #ef4444 !important;
  }
  html.light .empty-chips-msg {
    color: #64748b !important;
  }
"""

# Replace the previous custom CSS block
idx_start = content.find('/* ==========================================================================\n     ULTRA-REFINED PAROLE-QUIZ UI')
if idx_start == -1:
    idx_start = content.find('/* ==========================================================================\n     RESTRUCTURED & MODERNIZED HERO')
if idx_start != -1:
    idx_end = content.find('</style>', idx_start)
    content = content[:idx_start] + refined_css + '\n' + content[idx_end:]
    print("Updated custom CSS block with perfected styling.")
else:
    content = content.replace('</style>', refined_css + '\n</style>', 1)
    print("Inserted perfected styles.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated parole-quiz.html successfully.")

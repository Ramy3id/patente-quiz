import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Eliminate background completely from behind chips-actions and segmented-filter-bar
# Both in general and specifically in light / dark modes
removal_css = """
  /* ==========================================================================
     STRICT REMOVAL OF BACKGROUND BEHIND BUTTONS & REMOVAL OF HORIZONTAL SCROLL
     ========================================================================== */

  /* Absolutely NO background behind Word Bank buttons (تحديد الكل / إلغاء / تفريغ) */
  .chips-actions,
  html.light .chips-actions,
  html.dark .chips-actions {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 6px auto 0 !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 8px !important;
    width: 100% !important;
  }

  /* Absolutely NO background behind Filter buttons (الكل / VERO / FALSO) */
  .segmented-filter-bar,
  html.light .segmented-filter-bar,
  html.dark .segmented-filter-bar {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    width: 100% !important;
    max-width: 440px !important;
    height: auto !important;
    min-height: 42px !important;
  }

  /* Enhance segmented buttons when floating with no container background */
  .segmented-btn {
    height: 40px !important;
    min-height: 40px !important;
    border-radius: 12px !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    border: 1px solid #cbd5e1 !important;
    background: #ffffff !important;
    color: #475569 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  }
  .segmented-btn:hover {
    transform: translateY(-1px) !important;
  }
  .segmented-btn.active {
    background: linear-gradient(135deg, #0284c7, #2563eb) !important;
    color: #ffffff !important;
    border-color: #0284c7 !important;
    box-shadow: 0 3px 10px rgba(2, 132, 199, 0.35) !important;
  }
  .segmented-btn.active-vero {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: #ffffff !important;
    border-color: #10b981 !important;
    box-shadow: 0 3px 10px rgba(16, 185, 129, 0.35) !important;
  }
  .segmented-btn.active-falso {
    background: linear-gradient(135deg, #f43f5e, #e11d48) !important;
    color: #ffffff !important;
    border-color: #f43f5e !important;
    box-shadow: 0 3px 10px rgba(244, 63, 94, 0.35) !important;
  }

  html.dark .segmented-btn {
    background: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: #e2e8f0 !important;
  }

  /* 2. COMPLETELY ELIMINATE HORIZONTAL SCROLL FROM FAMILIES SHELF */
  .families-shelf {
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 8px !important;
    overflow-x: visible !important;
    overflow-y: visible !important;
    overflow: visible !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 12px 0 24px 0 !important;
  }
  .family-pill {
    flex-shrink: 0 !important;
    height: 36px !important;
    min-height: 36px !important;
    padding: 0 14px !important;
    border-radius: 100px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
  }
"""

# Append before </style>
if '</style>' in content:
    content = content.replace('</style>', removal_css + '\n</style>', 1)
    print("Injected strict removal CSS successfully.")
else:
    print("ERROR: </style> not found.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated parole-quiz.html successfully.")

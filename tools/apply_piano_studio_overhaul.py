import io
import os

target_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\piano-studio.html'

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Refine timeline filter pills for mobile
old_timeline_pills = """.sp-filter-pills {
    display: flex !important;
    gap: 8px !important;
    flex-wrap: wrap !important;
  }
  .sp-pill-btn {
    padding: 8px 16px !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    border: 1px solid #E2E8F0 !important;
    background: #F8FAFC !important;
    color: #475569 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
  }"""

new_timeline_pills = """.sp-timeline-header {
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    margin-bottom: 16px !important;
  }
  @media (min-width: 641px) {
    .sp-timeline-header {
      flex-direction: row !important;
      justify-content: space-between !important;
      align-items: center !important;
    }
  }
  .sp-filter-pills {
    display: flex !important;
    gap: 8px !important;
    flex-wrap: nowrap !important;
    width: 100% !important;
    max-width: 380px !important;
  }
  .sp-pill-btn {
    flex: 1 !important;
    text-align: center !important;
    padding: 9px 12px !important;
    border-radius: 10px !important;
    font-size: 0.84rem !important;
    font-weight: 700 !important;
    border: 1px solid #E2E8F0 !important;
    background: #F8FAFC !important;
    color: #475569 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
  }"""

if old_timeline_pills in content:
    content = content.replace(old_timeline_pills, new_timeline_pills)
    print("Replaced timeline pills styles with balanced responsive flex.")
else:
    print("Notice: old_timeline_pills not matched verbatim, will append refinement.")
    refinement = """
  /* Timeline Header & Balanced Pills */
  .sp-timeline-header {
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    margin-bottom: 16px !important;
  }
  @media (min-width: 641px) {
    .sp-timeline-header {
      flex-direction: row !important;
      justify-content: space-between !important;
      align-items: center !important;
    }
  }
  .sp-filter-pills {
    display: flex !important;
    gap: 8px !important;
    flex-wrap: nowrap !important;
    width: 100% !important;
    max-width: 380px !important;
  }
  .sp-pill-btn {
    flex: 1 !important;
    text-align: center !important;
    padding: 9px 12px !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
  }
"""
    content = content.replace('</style>', refinement + '\n  </style>')

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated piano-studio.html with UTF-8 successfully.")

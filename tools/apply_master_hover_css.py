with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Clean up first old hover rule around line 2178
old_r1 = """html.light .chapter-card:hover {
  border-color: #0284c7 !important;
  box-shadow: 
    0 4px 6px -1px rgba(15, 23, 42, 0.07),
    0 16px 32px -4px rgba(2, 132, 199, 0.12) !important;
  transform: translateY(-2px);
}"""

assert old_r1 in css, "old_r1 not found"
css = css.replace(old_r1, "/* old chapter-card:hover removed in favor of master luxury hover */")

# 2. Replace the second old hover block around line 2890
old_r2 = """.chapter-card:hover {
  transform: translateY(-2px) !important;
  border-color: rgba(56, 189, 248, 0.35) !important;
  box-shadow: 0 12px 32px -4px rgba(0, 0, 0, 0.45) !important;
}

html.light .chapter-card:hover {
  border-color: rgba(2, 132, 199, 0.35) !important;
  box-shadow: 0 8px 28px -4px rgba(15, 23, 42, 0.09) !important;
}"""

assert old_r2 in css, "old_r2 not found"

master_rules = """/* Master Luxury Chapter Card Hover Physics */
.chapter-card {
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), 
              box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1), 
              border-color 0.35s ease, 
              background 0.35s ease !important;
  will-change: transform, box-shadow !important;
  transform: translateZ(0) !important;
  backface-visibility: hidden !important;
}

html.light .chapter-card {
  background: #ffffff !important;
  border: 1px solid rgba(226, 232, 240, 0.95) !important;
  box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.05), 0 1px 3px rgba(15, 23, 42, 0.03) !important;
}

html.light .chapter-card:hover {
  transform: translateY(-6px) translateZ(0) !important;
  border-color: rgba(16, 185, 129, 0.45) !important;
  box-shadow: 0 22px 40px -10px rgba(15, 23, 42, 0.12), 
              0 8px 18px -4px rgba(15, 23, 42, 0.04), 
              0 0 0 1px rgba(16, 185, 129, 0.22) !important;
}

html.dark .chapter-card {
  background: rgba(18, 24, 38, 0.85) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
}

html.dark .chapter-card:hover {
  transform: translateY(-6px) translateZ(0) !important;
  border-color: rgba(52, 211, 153, 0.45) !important;
  box-shadow: 0 24px 48px -10px rgba(0, 0, 0, 0.75), 
              0 0 26px -4px rgba(16, 185, 129, 0.22), 
              inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
}

.chapter-card:active {
  transform: translateY(-2px) scale(0.992) !important;
  transition: transform 0.1s ease !important;
}

.chapter-card .btn-action-study {
  transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
              box-shadow 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
              filter 0.28s ease !important;
}

.chapter-card:hover .btn-action-study {
  filter: brightness(1.06) !important;
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.42) !important;
}

.chapter-card .btn-arrow-svg {
  transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
  will-change: transform !important;
}

.chapter-card:hover .btn-arrow-svg {
  transform: translateX(-5px) !important;
}

.chapter-card .ch-pill-num {
  transition: border-color 0.28s ease, background-color 0.28s ease, color 0.28s ease !important;
}

.chapter-card:hover .ch-pill-num {
  border-color: rgba(16, 185, 129, 0.4) !important;
  background: rgba(16, 185, 129, 0.08) !important;
}

.chapter-card .stat-pill {
  transition: border-color 0.28s ease !important;
}

.chapter-card:hover .stat-pill {
  border-color: rgba(16, 185, 129, 0.22) !important;
}"""

css = css.replace(old_r2, master_rules)

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated theme-modes.css with master luxury hover system successfully!")

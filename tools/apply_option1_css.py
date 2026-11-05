with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace Master Luxury Chapter Card Hover Physics block with Option 1: Linear / Stripe Stable Hover
old_block = """/* Master Luxury Chapter Card Hover Physics */
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

new_block = """/* Master Option 1: Linear / Stripe Calm & Stable Hover System */
.chapter-card {
  transform: none !important;
  transition: box-shadow 0.24s cubic-bezier(0.16, 1, 0.3, 1), 
              border-color 0.24s ease, 
              background 0.24s ease !important;
  will-change: box-shadow, border-color !important;
  cursor: pointer !important;
}

html.light .chapter-card {
  background: #ffffff !important;
  border: 1px solid rgba(15, 23, 42, 0.08) !important;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 4px 12px rgba(15, 23, 42, 0.02) !important;
}

html.light .chapter-card:hover {
  transform: none !important;
  border-color: rgba(15, 23, 42, 0.18) !important;
  box-shadow: 0 14px 30px -4px rgba(15, 23, 42, 0.09), 0 4px 10px -2px rgba(15, 23, 42, 0.03) !important;
}

html.dark .chapter-card {
  background: rgba(18, 24, 38, 0.85) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
}

html.dark .chapter-card:hover {
  transform: none !important;
  border-color: rgba(255, 255, 255, 0.18) !important;
  box-shadow: 0 14px 32px -4px rgba(0, 0, 0, 0.72) !important;
}

.chapter-card:active {
  transform: scale(0.995) !important;
  transition: transform 0.08s ease !important;
}

.chapter-card .btn-action-study {
  transform: none !important;
  transition: filter 0.2s ease, box-shadow 0.2s ease !important;
}

.chapter-card:hover .btn-action-study {
  filter: brightness(1.05) !important;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35) !important;
}

.chapter-card .btn-arrow-svg {
  transition: transform 0.2s ease !important;
}

.chapter-card:hover .btn-arrow-svg {
  transform: translateX(-3px) !important;
}"""

assert old_block in css, "old_block not found in theme-modes.css"
css = css.replace(old_block, new_block)

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated theme-modes.css with Option 1 successfully!")

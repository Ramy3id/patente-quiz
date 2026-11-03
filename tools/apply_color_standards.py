css_path = r'R:\Ramy\PATENTE_PRO_APP\assets\css\theme-modes.css'
with open(css_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update .ch-title-ar to authoritative Slate colors instead of link blue/cyan
old_ch_title = """.ch-title-ar {
  margin-bottom: 8px !important;
  color: #38BDF8 !important;
}
html.light .ch-title-ar {
  color: #0284C7 !important;
}"""

new_ch_title = """.ch-title-ar {
  margin-bottom: 8px !important;
  color: #F8FAFC !important; /* Crisp, authoritative White/Slate-50 in Dark mode */
}
html.light .ch-title-ar {
  color: #1E293B !important; /* Deep, authoritative Slate-800 in Light mode */
}"""

if old_ch_title in text:
    text = text.replace(old_ch_title, new_ch_title)
    print("Updated .ch-title-ar colors")
elif old_ch_title.replace('\n', '\r\n') in text:
    text = text.replace(old_ch_title.replace('\n', '\r\n'), new_ch_title.replace('\n', '\r\n'))
    print("Updated .ch-title-ar colors (CRLF)")
else:
    print("old_ch_title not found")

# 2. Add full 60-30-10 & Daltonism Accessibility Block
accessibility_block = """
/* ==========================================================================
   60-30-10 Semantic Color Harmony & Daltonism High-Contrast Engine (2026)
   ========================================================================== */
:root {
  --text-secondary: #CBD5E1 !important; /* Slate-300: High-clarity subtext in Dark Mode (10.5:1 AAA) */
  --text-muted: #94A3B8 !important;
  --card-border-subtle: rgba(255, 255, 255, 0.12) !important;
}

html.light {
  --text-secondary: #334155 !important; /* Slate-700: High-clarity subtext in Light Mode */
  --text-muted: #475569 !important;
  --card-border-subtle: rgba(15, 23, 42, 0.10) !important;
}

/* Reinforced Card Borders for Budget LCDs & OLED Dislays */
.glass-card,
.chapter-card,
.q-card,
.dict-card,
.tool-quick-card {
  border: 1px solid var(--card-border-subtle) !important;
}
html.light .glass-card,
html.light .chapter-card,
html.light .q-card,
html.light .dict-card,
html.light .tool-quick-card {
  border: 1px solid rgba(15, 23, 42, 0.10) !important;
  box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.06) !important;
}

/* Explanations, Translations & Traps: WCAG AAA Contrast */
.q-trans,
.q-trans-text,
.explanation-text,
.sp-box,
.tb-box,
.ch-sp-text,
.flashcard-explanation,
.trap-explanation {
  color: #CBD5E1 !important;
  line-height: 1.65 !important;
}
html.light .q-trans,
html.light .q-trans-text,
html.light .explanation-text,
html.light .sp-box,
html.light .tb-box,
html.light .ch-sp-text,
html.light .flashcard-explanation,
html.light .trap-explanation {
  color: #334155 !important;
}

/* Dual Coding: VERO / FALSO Buttons with Daltonismo Protection */
.btn-ans-v,
.choice-btn.vero,
.choice-btn-vero {
  background: rgba(16, 185, 129, 0.14) !important;
  color: #10B981 !important;
  border: 1.5px solid rgba(16, 185, 129, 0.45) !important;
}
.btn-ans-v:hover,
.choice-btn.vero:hover,
.choice-btn-vero:hover,
.choice-btn-vero.selected {
  background: #10B981 !important;
  color: #FFFFFF !important;
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4) !important;
}

html.light .btn-ans-v,
html.light .choice-btn.vero,
html.light .choice-btn-vero {
  background: #ECFDF5 !important;
  color: #047857 !important;
  border: 1.5px solid #10B981 !important;
}
html.light .btn-ans-v:hover,
html.light .choice-btn.vero:hover,
html.light .choice-btn-vero:hover,
html.light .choice-btn-vero.selected {
  background: #059669 !important;
  color: #FFFFFF !important;
}

.btn-ans-f,
.choice-btn.falso,
.choice-btn-falso {
  background: rgba(239, 68, 68, 0.14) !important;
  color: #F87171 !important;
  border: 1.5px solid rgba(239, 68, 68, 0.45) !important;
}
.btn-ans-f:hover,
.choice-btn.falso:hover,
.choice-btn-falso:hover,
.choice-btn-falso.selected {
  background: #EF4444 !important;
  color: #FFFFFF !important;
  box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4) !important;
}

html.light .btn-ans-f,
html.light .choice-btn.falso,
html.light .choice-btn-falso {
  background: #FEF2F2 !important;
  color: #B91C1C !important;
  border: 1.5px solid #EF4444 !important;
}
html.light .btn-ans-f:hover,
html.light .choice-btn.falso:hover,
html.light .choice-btn-falso:hover,
html.light .choice-btn-falso.selected {
  background: #DC2626 !important;
  color: #FFFFFF !important;
}
"""

text += accessibility_block

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied 60-30-10 & Accessibility improvements to theme-modes.css successfully")

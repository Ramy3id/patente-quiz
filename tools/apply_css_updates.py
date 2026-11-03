import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

css_path = 'R:/Ramy/PATENTE_PRO_APP/assets/css/modular-chapter.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Marker to avoid duplicate appending
marker = '/* === USER POLISH: CONTROLS, STATS, & SPLIT QUESTION CARDS === */'
if marker in css_content:
    print("Found existing polish block, stripping before re-adding...")
    idx = css_content.find(marker)
    css_content = css_content[:idx].rstrip()

new_styles = f"""

{marker}

/* 1. Full-Width Sticky Controls Bar & 100% Search Box */
.controls-bar {{
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
  width: 100% !important;
  box-sizing: border-box !important;
  padding: 14px 16px !important;
  border-radius: 16px !important;
  position: sticky !important;
  top: 60px !important;
  z-index: 90 !important;
}}

.controls-bar .search-box,
#q-search.search-box {{
  width: 100% !important;
  flex: 1 1 100% !important;
  min-width: 100% !important;
  box-sizing: border-box !important;
  direction: rtl !important;
  text-align: right !important;
  font-size: 0.92rem !important;
  padding: 12px 16px !important;
  border-radius: 12px !important;
  height: 46px !important;
}}

.controls-bar .filter-btns-wrap {{
  width: 100% !important;
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
  gap: 8px !important;
  box-sizing: border-box !important;
}}

.controls-bar .filter-btns-wrap .f-btn {{
  width: 100% !important;
  padding: 8px 6px !important;
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  border-radius: 10px !important;
  text-align: center !important;
  white-space: nowrap !important;
  justify-content: center !important;
  box-sizing: border-box !important;
}}

.controls-bar .study-toggle-label {{
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  margin: 0 !important;
  padding-top: 6px !important;
  border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
  font-size: 0.84rem !important;
  cursor: pointer !important;
}}

html.light .controls-bar .study-toggle-label {{
  border-top-color: rgba(15, 23, 42, 0.06) !important;
}}

/* 2. Center Chapter Progress Meta & Reset Button */
.chapter-progress-meta {{
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  text-align: center !important;
  width: 100% !important;
}}

.chapter-progress-stats-row {{
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 12px !important;
  flex-wrap: wrap !important;
  text-align: center !important;
  width: 100% !important;
}}

.chapter-reset-btn {{
  margin: 4px auto 0 auto !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}}

/* 3. Center Subtopic Header Stats (Questions / V•F / Mastery) */
.subtopic-header-stats {{
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  flex-wrap: wrap !important;
  width: 100% !important;
  margin: 10px auto 0 auto !important;
  text-align: center !important;
}}

.subtopic-stat-pill {{
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}}

/* 4. Modern Mobile Question Cards (Hero Image Top + 2-Column Split Answers) */
.q-card {{
  background: var(--bg-surface, rgba(24, 24, 27, 0.75)) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08)) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
  border-radius: 18px !important;
  padding: 16px !important;
  margin-bottom: 16px !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  gap: 14px !important;
  box-sizing: border-box !important;
  width: 100% !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

html.light .q-card {{
  background: #ffffff !important;
  border: 1px solid rgba(15, 23, 42, 0.08) !important;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05) !important;
}}

.q-card.answered-correct {{
  border-color: rgba(16, 185, 129, 0.45) !important;
}}
html.light .q-card.answered-correct {{
  border-color: #10b981 !important;
  background: #f0fdf4 !important;
}}

.q-card.answered-wrong {{
  border-color: rgba(239, 68, 68, 0.45) !important;
}}
html.light .q-card.answered-wrong {{
  border-color: #ef4444 !important;
  background: #fef2f2 !important;
}}

/* Hero Question Image Container at Top */
.q-img-wrap {{
  width: 100% !important;
  max-width: 320px !important;
  margin: 0 auto !important;
  height: auto !important;
  min-height: 80px !important;
  max-height: 180px !important;
  background: rgba(0, 0, 0, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 14px !important;
  padding: 10px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-sizing: border-box !important;
}}

html.light .q-img-wrap {{
  background: #f1f5f9 !important;
  border-color: rgba(15, 23, 42, 0.08) !important;
}}

.q-img-wrap img {{
  max-width: 100% !important;
  max-height: 150px !important;
  width: auto !important;
  height: auto !important;
  object-fit: contain !important;
  border-radius: 8px !important;
  cursor: pointer !important;
  transition: transform 0.2s ease !important;
}}

.q-img-wrap img:active {{
  transform: scale(0.98) !important;
}}

/* Card Body */
.q-body {{
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
  width: 100% !important;
  box-sizing: border-box !important;
  flex: 1 1 auto !important;
}}

/* Top Meta Row (Question ID & Subtopic Badge) */
.q-card-top {{
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  gap: 10px !important;
  width: 100% !important;
  direction: rtl !important;
  box-sizing: border-box !important;
}}

.q-id-pill {{
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.82rem !important;
  font-weight: 800 !important;
  color: var(--text-muted, #94a3b8) !important;
  background: rgba(255, 255, 255, 0.06) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  padding: 4px 10px !important;
  border-radius: 8px !important;
  letter-spacing: 0.5px !important;
  white-space: nowrap !important;
}}

html.light .q-id-pill {{
  background: #f1f5f9 !important;
  border-color: rgba(15, 23, 42, 0.08) !important;
  color: #475569 !important;
}}

.q-sub-badge {{
  font-size: 0.76rem !important;
  font-weight: 700 !important;
  color: #38bdf8 !important;
  background: rgba(56, 189, 248, 0.1) !important;
  border: 1px solid rgba(56, 189, 248, 0.25) !important;
  padding: 4px 12px !important;
  border-radius: 8px !important;
  max-width: 75% !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  text-align: right !important;
}}

html.light .q-sub-badge {{
  background: #e0f2fe !important;
  border-color: #7dd3fc !important;
  color: #0284c7 !important;
}}

/* Italian Question Text */
.q-text-content {{
  font-size: 1.05rem !important;
  font-weight: 600 !important;
  line-height: 1.6 !important;
  direction: ltr !important;
  text-align: left !important;
  color: #f8fafc !important;
  margin: 2px 0 6px 0 !important;
  word-break: break-word !important;
}}

html.light .q-text-content {{
  color: #0f172a !important;
}}

/* Question Action Container */
.q-actions-row {{
  display: flex !important;
  flex-direction: column !important;
  gap: 10px !important;
  width: 100% !important;
  box-sizing: border-box !important;
}}

/* 2-Column Split Answers Grid (VERO / FALSO side-by-side) */
.q-answers-grid {{
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 12px !important;
  width: 100% !important;
  box-sizing: border-box !important;
}}

.btn-ans {{
  height: 48px !important;
  min-height: 48px !important;
  border-radius: 12px !important;
  font-size: 1.05rem !important;
  font-weight: 800 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  user-select: none !important;
  transition: all 0.18s ease !important;
  box-sizing: border-box !important;
}}

.btn-ans-v {{
  background: rgba(16, 185, 129, 0.12) !important;
  border: 1.5px solid rgba(16, 185, 129, 0.4) !important;
  color: #34d399 !important;
}}

html.light .btn-ans-v {{
  background: #f0fdf4 !important;
  border-color: #86efac !important;
  color: #15803d !important;
}}

.btn-ans-v:hover,
.btn-ans-v:active {{
  background: rgba(16, 185, 129, 0.22) !important;
  border-color: #10b981 !important;
}}

.btn-ans-v.selected {{
  background: #10b981 !important;
  border-color: #10b981 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
}}

.btn-ans-f {{
  background: rgba(239, 68, 68, 0.12) !important;
  border: 1.5px solid rgba(239, 68, 68, 0.4) !important;
  color: #f87171 !important;
}}

html.light .btn-ans-f {{
  background: #fef2f2 !important;
  border-color: #fca5a5 !important;
  color: #b91c1c !important;
}}

.btn-ans-f:hover,
.btn-ans-f:active {{
  background: rgba(239, 68, 68, 0.22) !important;
  border-color: #ef4444 !important;
}}

.btn-ans-f.selected {{
  background: #ef4444 !important;
  border-color: #ef4444 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4) !important;
}}

/* Feedback Row (Status Tag & Quick Study Badge) */
.q-feedback-row {{
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 10px !important;
  flex-wrap: wrap !important;
  width: 100% !important;
  box-sizing: border-box !important;
  min-height: 0 !important;
}}

.status-tag {{
  display: none !important;
  font-size: 0.84rem !important;
  font-weight: 700 !important;
  padding: 6px 14px !important;
  border-radius: 8px !important;
  text-align: center !important;
}}

.status-tag.ok {{
  display: inline-flex !important;
  background: rgba(16, 185, 129, 0.15) !important;
  border: 1px solid rgba(16, 185, 129, 0.3) !important;
  color: #34d399 !important;
}}

html.light .status-tag.ok {{
  background: #dcfce7 !important;
  border-color: #86efac !important;
  color: #166534 !important;
}}

.status-tag.err {{
  display: inline-flex !important;
  background: rgba(239, 68, 68, 0.15) !important;
  border: 1px solid rgba(239, 68, 68, 0.3) !important;
  color: #f87171 !important;
}}

html.light .status-tag.err {{
  background: #fee2e2 !important;
  border-color: #fca5a5 !important;
  color: #991b1b !important;
}}

.study-badge-direct {{
  display: none !important;
  font-size: 0.84rem !important;
  font-weight: 800 !important;
  padding: 6px 14px !important;
  border-radius: 8px !important;
  text-align: center !important;
}}

.study-badge-direct.show {{
  display: inline-flex !important;
}}

.study-badge-direct.is-v {{
  background: rgba(16, 185, 129, 0.15) !important;
  border: 1px solid #10b981 !important;
  color: #34d399 !important;
}}

html.light .study-badge-direct.is-v {{
  background: #dcfce7 !important;
  border-color: #22c55e !important;
  color: #15803d !important;
}}

.study-badge-direct.is-f {{
  background: rgba(239, 68, 68, 0.15) !important;
  border: 1px solid #ef4444 !important;
  color: #f87171 !important;
}}

html.light .study-badge-direct.is-f {{
  background: #fee2e2 !important;
  border-color: #ef4444 !important;
  color: #b91c1c !important;
}}

/* Translation & Explanation Drawer Button */
.btn-explain-toggle {{
  width: 100% !important;
  height: 44px !important;
  min-height: 44px !important;
  border-radius: 12px !important;
  background: rgba(56, 189, 248, 0.08) !important;
  border: 1px solid rgba(56, 189, 248, 0.25) !important;
  color: #38bdf8 !important;
  font-size: 0.88rem !important;
  font-weight: 700 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  cursor: pointer !important;
  transition: all 0.18s ease !important;
  box-sizing: border-box !important;
  margin-top: 4px !important;
}}

html.light .btn-explain-toggle {{
  background: #f0f9ff !important;
  border-color: #bae6fd !important;
  color: #0284c7 !important;
}}

.btn-explain-toggle:hover,
.btn-explain-toggle:active {{
  background: rgba(56, 189, 248, 0.16) !important;
  border-color: #38bdf8 !important;
}}

html.light .btn-explain-toggle:hover {{
  background: #e0f2fe !important;
  border-color: #38bdf8 !important;
}}
"""

css_content += new_styles

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Updated modular-chapter.css successfully")

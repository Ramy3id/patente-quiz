with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add CSS rules for .moto-summary-box
target_css = '''.btn-moto-step {
  padding: 8px 18px;
  border-radius: 8px;
  background: #334155;
  border: 2px solid #475569;
  color: #FFFFFF !important;
  font-weight: 800;
  font-size: 0.9rem;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.15s ease;
}'''

repl_css = '''.btn-moto-step {
  padding: 8px 14px;
  border-radius: 8px;
  background: #334155;
  border: 2px solid #475569;
  color: #FFFFFF !important;
  font-weight: 800;
  font-size: 0.88rem;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.moto-summary-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 4px;
  line-height: 1.15;
  min-width: 76px;
  user-select: none;
}
.moto-summary-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.70rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: #94A3B8;
  text-transform: uppercase;
  display: block;
}
.moto-summary-count {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.95rem;
  font-weight: 800;
  color: #38BDF8;
  display: block;
  margin-top: 1px;
}
.moto-summary-count strong {
  font-size: 1.05rem;
  font-weight: 900;
  color: #FFFFFF;
}'''

if target_css in text:
    text = text.replace(target_css, repl_css, 1)
    print('Updated CSS successfully')
else:
    print('target_css not found')

# 2. Add light theme CSS for .moto-summary-box
target_light = '''    html.light .btn-moto-step {
      background: #E2E8F0 !important;
      border-color: #CBD5E1 !important;
      color: #0F172A !important;
    }'''

repl_light = '''    html.light .btn-moto-step {
      background: #E2E8F0 !important;
      border-color: #CBD5E1 !important;
      color: #0F172A !important;
    }
    html.light .moto-summary-label {
      color: #64748B !important;
    }
    html.light .moto-summary-count {
      color: #0284C7 !important;
    }
    html.light .moto-summary-count strong {
      color: #0F172A !important;
    }'''

if target_light in text:
    text = text.replace(target_light, repl_light, 1)
    print('Updated light CSS successfully')
else:
    print('target_light not found')

# 3. Update HTML
target_html = '<span style="color:#94A3B8; font-weight:700; font-size:0.85rem;" id="motoSummaryAnswered">RISPOSTE: 0 / 30</span>'
repl_html = '''<div class="moto-summary-box" id="motoSummaryAnswered">
            <span class="moto-summary-label">RISPOSTE</span>
            <span class="moto-summary-count"><strong id="motoAnsweredCount">0</strong> / 30</span>
          </div>'''

if target_html in text:
    text = text.replace(target_html, repl_html, 1)
    print('Updated HTML successfully')
else:
    print('target_html not found')

# 4. Update JS in renderPills
target_js = '''        const count = exam.getAnsweredCount();
        const ansCnt = document.getElementById("answeredCounter");
        const motoAnsCnt = document.getElementById("motoSummaryAnswered");
        if (ansCnt) ansCnt.textContent = count;
        if (motoAnsCnt) motoAnsCnt.textContent = `RISPOSTE: ${count} / 30`;'''

repl_js = '''        const count = exam.getAnsweredCount();
        const ansCnt = document.getElementById("answeredCounter");
        const motoCountEl = document.getElementById("motoAnsweredCount");
        if (ansCnt) ansCnt.textContent = count;
        if (motoCountEl) {
          motoCountEl.textContent = count;
        } else {
          const motoAnsCnt = document.getElementById("motoSummaryAnswered");
          if (motoAnsCnt) motoAnsCnt.innerHTML = `<span class="moto-summary-label">RISPOSTE</span><span class="moto-summary-count"><strong>${count}</strong> / 30</span>`;
        }'''

if target_js in text:
    text = text.replace(target_js, repl_js, 1)
    print('Updated JS successfully')
else:
    print('target_js not found')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('File written.')

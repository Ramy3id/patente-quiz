# -*- coding: utf-8 -*-
"""
Perfect UX & Mobile Responsive Redesign for Part Quiz Modal in modular-chapter-engine.js
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'R:/Ramy/PATENTE/assets/js/modular-chapter-engine.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update renderQuizModal structure
old_render_modal = """      modal.innerHTML = `
        <div class="quiz-modal-card">
          <!-- Top Bar -->
          <div class="quiz-modal-topbar">
            <div class="quiz-modal-part-info">
              <span class="quiz-modal-part-badge">⚡ كويز الجزء</span>
              <span class="quiz-modal-part-name">${partName}</span>
            </div>
            <button class="quiz-modal-close-btn" onclick="closePartQuiz()" title="إغلاق والعودة لصفحة الباب">✕</button>
          </div>

          <!-- Progress Strip -->
          <div class="quiz-modal-prog-wrap">
            <div class="quiz-modal-prog-text">
              <span>السؤال <strong>${curIdx + 1}</strong> من <strong>${total}</strong></span>
              <span>${pct}% مكتمل</span>
            </div>
            <div class="quiz-modal-prog-track">
              <div class="quiz-modal-prog-fill" style="width:${pct}%;"></div>
            </div>
          </div>

          <!-- Question Body -->
          <div class="quiz-modal-q-body">
            ${imgHtml}
            <div class="quiz-modal-q-text">
              ${q.domanda}
            </div>
            <div class="quiz-modal-q-tr">
              ${q.traduzione || ''}
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="quiz-modal-actions-row">
            <button class="btn-quiz-choice vero" onclick="answerPartQuiz(true)">
              <span class="choice-icon">✅</span>
              <span class="choice-lbl">VERO</span>
              <span class="choice-sub">صحيح</span>
            </button>
            <button class="btn-quiz-choice falso" onclick="answerPartQuiz(false)">
              <span class="choice-icon">❌</span>
              <span class="choice-lbl">FALSO</span>
              <span class="choice-sub">خطأ</span>
            </button>
          </div>
        </div>
      `;"""

new_render_modal = """      modal.innerHTML = `
        <div class="quiz-modal-card">
          <!-- Header: Clean Left-to-Right Balanced Layout -->
          <div class="quiz-modal-topbar">
            <div class="quiz-modal-part-info">
              <span class="quiz-modal-part-badge">⚡ كويز الجزء</span>
              <span class="quiz-modal-part-name" title="${escapeHtml(partName)}">${escapeHtml(partName)}</span>
            </div>
            <button class="quiz-modal-close-btn" onclick="closePartQuiz()" aria-label="إغلاق" title="إغلاق الكويز">✕</button>
          </div>

          <!-- Progress Strip: Fixed LTR direction for correct 0% to 100% reading -->
          <div class="quiz-modal-prog-wrap">
            <div class="quiz-modal-prog-text">
              <span class="prog-q-num">السؤال <strong>${curIdx + 1}</strong> من <strong>${total}</strong></span>
              <span class="prog-pct-num">${pct}% مكتمل</span>
            </div>
            <div class="quiz-modal-prog-track">
              <div class="quiz-modal-prog-fill" style="width:${pct}%;"></div>
            </div>
          </div>

          <!-- Question Content -->
          <div class="quiz-modal-q-body">
            ${imgHtml}
            <div class="quiz-modal-q-text">
              ${escapeHtml(q.domanda)}
            </div>
            <div class="quiz-modal-q-tr">
              ${escapeHtml(q.traduzione || '')}
            </div>
          </div>

          <!-- Action Buttons: VERO on Right, FALSO on Left (Standard Natural Driving Exam Ergonomics) -->
          <div class="quiz-modal-actions-row">
            <button class="btn-quiz-choice vero" onclick="answerPartQuiz(true)">
              <span class="choice-icon">✔</span>
              <span class="choice-lbl">VERO</span>
              <span class="choice-sub">صحيح</span>
            </button>
            <button class="btn-quiz-choice falso" onclick="answerPartQuiz(false)">
              <span class="choice-icon">✖</span>
              <span class="choice-lbl">FALSO</span>
              <span class="choice-sub">خطأ</span>
            </button>
          </div>
        </div>
      `;"""

code = code.replace(old_render_modal, new_render_modal, 1)

# 2. Update injectQuizStyles CSS
old_styles_marker = "injectQuizStyles() {"
pos_styles_start = code.find(old_styles_marker)
pos_styles_end = code.find("updateScoreDisplay() {", pos_styles_start)

new_styles_block = """injectQuizStyles() {
      if (document.getElementById('part-quiz-injected-styles')) return;
      const s = document.createElement('style');
      s.id = 'part-quiz-injected-styles';
      s.textContent = `
        /* =========================================================
           Part Quiz (Active Mastery) Modal & Mobile-First Styling
           ========================================================= */
        body.quiz-modal-open {
          overflow: hidden !important;
          touch-action: none !important;
        }
        .part-quiz-modal-backdrop {
          position: fixed;
          inset: 0;
          background: rgba(11, 15, 25, 0.88);
          backdrop-filter: blur(20px);
          -webkit-backdrop-filter: blur(20px);
          z-index: 100000;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 16px;
          opacity: 0;
          visibility: hidden;
          transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.22s;
          direction: rtl;
        }
        .part-quiz-modal-backdrop.open {
          opacity: 1;
          visibility: visible;
        }
        .quiz-modal-card {
          width: 100%;
          max-width: 620px;
          background: #111827;
          border: 1px solid rgba(255, 255, 255, 0.14);
          border-radius: 24px;
          box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.85), 0 0 0 1px rgba(255, 255, 255, 0.05);
          padding: 24px 26px 28px;
          max-height: 92vh;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
          color: #F8FAFC;
          font-family: 'Plus Jakarta Sans', 'Cairo', system-ui, -apple-system, sans-serif;
          position: relative;
          transform: translateY(14px) scale(0.97);
          transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        html.light .quiz-modal-card {
          background: #FFFFFF;
          border-color: rgba(15, 23, 42, 0.12);
          box-shadow: 0 25px 60px -12px rgba(15, 23, 42, 0.22), 0 4px 12px rgba(15, 23, 42, 0.06);
          color: #0F172A;
        }
        .part-quiz-modal-backdrop.open .quiz-modal-card {
          transform: translateY(0) scale(1);
        }

        /* Topbar Header */
        .quiz-modal-topbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
          padding-bottom: 14px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          margin-bottom: 16px;
        }
        html.light .quiz-modal-topbar {
          border-bottom-color: rgba(15, 23, 42, 0.08);
        }
        .quiz-modal-part-info {
          display: flex;
          align-items: center;
          gap: 10px;
          min-width: 0;
          flex: 1;
        }
        .quiz-modal-part-badge {
          background: rgba(99, 102, 241, 0.15);
          color: #818CF8;
          border: 1px solid rgba(99, 102, 241, 0.3);
          border-radius: 8px;
          font-size: 0.74rem;
          font-weight: 800;
          padding: 3px 9px;
          white-space: nowrap;
          flex-shrink: 0;
        }
        html.light .quiz-modal-part-badge {
          background: rgba(99, 102, 241, 0.08);
          color: #4F46E5;
          border-color: rgba(99, 102, 241, 0.25);
        }
        .quiz-modal-part-name {
          font-size: 0.92rem;
          font-weight: 800;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          color: inherit;
        }
        .quiz-modal-close-btn {
          width: 34px;
          height: 34px;
          border-radius: 10px;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: #94A3B8;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.95rem;
          font-weight: 700;
          transition: all 0.18s ease;
          flex-shrink: 0;
        }
        html.light .quiz-modal-close-btn {
          background: rgba(15, 23, 42, 0.05);
          border-color: rgba(15, 23, 42, 0.1);
          color: #475569;
        }
        .quiz-modal-close-btn:hover {
          background: rgba(239, 68, 68, 0.15);
          color: #EF4444;
          border-color: rgba(239, 68, 68, 0.3);
          transform: rotate(90deg);
        }

        /* Progress Wrap with Clean LTR/RTL Geometry */
        .quiz-modal-prog-wrap {
          margin-bottom: 22px;
        }
        .quiz-modal-prog-text {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 0.82rem;
          font-weight: 700;
          margin-bottom: 8px;
        }
        .prog-q-num {
          color: var(--text-primary, inherit);
        }
        .prog-pct-num {
          font-family: 'JetBrains Mono', monospace;
          color: #38BDF8;
          font-size: 0.86rem;
          font-weight: 800;
        }
        html.light .prog-pct-num {
          color: #0284C7;
        }
        .quiz-modal-prog-track {
          width: 100%;
          height: 7px;
          background: rgba(255, 255, 255, 0.08);
          border-radius: 99px;
          overflow: hidden;
          direction: ltr; /* Fills smoothly left to right */
        }
        html.light .quiz-modal-prog-track {
          background: rgba(15, 23, 42, 0.08);
        }
        .quiz-modal-prog-fill {
          height: 100%;
          background: linear-gradient(90deg, #6366F1, #10B981);
          border-radius: 99px;
          transition: width 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* Question Body Typography */
        .quiz-modal-q-body {
          margin-bottom: 26px;
        }
        .quiz-modal-img-wrap {
          text-align: center;
          margin-bottom: 18px;
        }
        .quiz-modal-img-wrap img {
          max-height: 150px;
          max-width: 100%;
          border-radius: 14px;
          background: #FFFFFF;
          padding: 8px;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }
        .quiz-modal-q-text {
          font-size: 1.22rem;
          font-weight: 800;
          line-height: 1.55;
          margin-bottom: 12px;
          direction: ltr;
          text-align: left;
          color: #FFFFFF;
          letter-spacing: -0.01em;
        }
        html.light .quiz-modal-q-text {
          color: #0F172A;
        }
        .quiz-modal-q-tr {
          font-size: 0.94rem;
          color: #94A3B8;
          line-height: 1.65;
          direction: rtl;
          text-align: right;
          font-weight: 500;
        }
        html.light .quiz-modal-q-tr {
          color: #475569;
        }

        /* Action Buttons: Ergonomic Grid */
        .quiz-modal-actions-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 14px;
        }
        .btn-quiz-choice {
          height: 64px;
          border-radius: 16px;
          border: 1.5px solid transparent;
          cursor: pointer;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
          font-family: inherit;
          user-select: none;
          -webkit-tap-highlight-color: transparent;
        }
        .btn-quiz-choice:active {
          transform: scale(0.97);
        }
        .btn-quiz-choice.vero {
          background: rgba(16, 185, 129, 0.12);
          border-color: rgba(16, 185, 129, 0.38);
          color: #34D399;
        }
        html.light .btn-quiz-choice.vero {
          background: rgba(16, 185, 129, 0.08);
          border-color: rgba(16, 185, 129, 0.38);
          color: #059669;
        }
        .btn-quiz-choice.vero:hover {
          background: #10B981;
          color: #FFFFFF;
          border-color: #10B981;
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(16, 185, 129, 0.35);
        }
        .btn-quiz-choice.falso {
          background: rgba(239, 68, 68, 0.12);
          border-color: rgba(239, 68, 68, 0.38);
          color: #F87171;
        }
        html.light .btn-quiz-choice.falso {
          background: rgba(239, 68, 68, 0.08);
          border-color: rgba(239, 68, 68, 0.38);
          color: #DC2626;
        }
        .btn-quiz-choice.falso:hover {
          background: #EF4444;
          color: #FFFFFF;
          border-color: #EF4444;
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(239, 68, 68, 0.35);
        }
        .choice-icon {
          font-size: 1.1rem;
          line-height: 1;
          margin-bottom: 2px;
        }
        .choice-lbl {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.2rem;
          font-weight: 900;
          line-height: 1.1;
        }
        .choice-sub {
          font-size: 0.72rem;
          font-weight: 700;
          opacity: 0.85;
        }

        /* Results Card */
        .quiz-results-card {
          text-align: center;
        }
        .quiz-results-header {
          margin-bottom: 20px;
        }
        .quiz-results-title {
          font-size: 1.4rem;
          font-weight: 900;
          color: #F8FAFC;
          margin-bottom: 4px;
        }
        html.light .quiz-results-title {
          color: #0F172A;
        }
        .quiz-results-subtitle {
          font-size: 0.88rem;
          color: #94A3B8;
        }
        html.light .quiz-results-subtitle {
          color: #64748B;
        }

        .quiz-score-badge-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 12px;
          margin-bottom: 20px;
        }
        .quiz-score-box {
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 16px;
          padding: 14px;
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        html.light .quiz-score-box {
          background: rgba(15, 23, 42, 0.03);
          border-color: rgba(15, 23, 42, 0.08);
        }
        .quiz-score-val {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.45rem;
          font-weight: 900;
          color: #38BDF8;
          line-height: 1.2;
        }
        .quiz-score-box.perfect .quiz-score-val {
          color: #10B981;
        }
        .quiz-score-lbl {
          font-size: 0.74rem;
          color: #94A3B8;
          font-weight: 700;
          margin-top: 4px;
        }
        html.light .quiz-score-lbl {
          color: #64748B;
        }

        .quiz-mistakes-container {
          background: rgba(239, 68, 68, 0.05);
          border: 1px solid rgba(239, 68, 68, 0.2);
          border-radius: 14px;
          padding: 14px;
          text-align: right;
          margin-bottom: 20px;
          max-height: 240px;
          overflow-y: auto;
        }
        .quiz-mistakes-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 0.82rem;
          font-weight: 800;
          color: #F87171;
          margin-bottom: 10px;
          padding-bottom: 6px;
          border-bottom: 1px solid rgba(239, 68, 68, 0.15);
        }
        .quiz-mistake-item {
          padding: 10px 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .quiz-mistake-item:last-child {
          border-bottom: none;
        }

        .quiz-results-actions {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .btn-quiz-action {
          width: 100%;
          height: 46px;
          border-radius: 12px;
          font-weight: 800;
          font-size: 0.9rem;
          cursor: pointer;
          border: none;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          font-family: inherit;
          transition: all 0.2s ease;
        }
        .btn-quiz-action.retest {
          background: #EF4444;
          color: #FFFFFF;
          box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
        }
        .btn-quiz-action.retest:hover {
          background: #DC2626;
          transform: translateY(-1px);
        }
        .btn-quiz-action.repeat {
          background: rgba(56, 189, 248, 0.15);
          border: 1px solid rgba(56, 189, 248, 0.3);
          color: #38BDF8;
        }
        html.light .btn-quiz-action.repeat {
          background: rgba(2, 132, 199, 0.08);
          color: #0284C7;
          border-color: rgba(2, 132, 199, 0.25);
        }
        .btn-quiz-action.finish {
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: #CBD5E1;
        }
        html.light .btn-quiz-action.finish {
          background: rgba(15, 23, 42, 0.05);
          color: #334155;
          border-color: rgba(15, 23, 42, 0.1);
        }
        .btn-quiz-action:hover {
          transform: translateY(-1px);
        }

        /* Buttons in Section Header */
        .part-quiz-actions-wrap {
          display: inline-flex;
          align-items: center;
          gap: 6px;
        }
        .btn-part-quiz-trigger {
          height: 30px;
          display: inline-flex;
          align-items: center;
          gap: 4px;
          padding: 0 11px;
          border-radius: 8px;
          background: rgba(99, 102, 241, 0.15);
          border: 1px solid rgba(99, 102, 241, 0.35);
          color: #818CF8;
          font-size: 0.76rem;
          font-weight: 800;
          cursor: pointer;
          transition: all 0.18s ease;
          font-family: inherit;
          white-space: nowrap;
        }
        html.light .btn-part-quiz-trigger {
          background: rgba(99, 102, 241, 0.08);
          border-color: rgba(99, 102, 241, 0.3);
          color: #4F46E5;
        }
        .btn-part-quiz-trigger:hover {
          background: #6366F1;
          color: #FFFFFF;
          transform: translateY(-1px);
          box-shadow: 0 3px 10px rgba(99, 102, 241, 0.3);
        }
        .btn-part-quiz-trigger.full {
          background: rgba(16, 185, 129, 0.12);
          border-color: rgba(16, 185, 129, 0.3);
          color: #34D399;
        }
        html.light .btn-part-quiz-trigger.full {
          background: rgba(16, 185, 129, 0.08);
          border-color: rgba(16, 185, 129, 0.28);
          color: #059669;
        }
        .btn-part-quiz-trigger.full:hover {
          background: #10B981;
          color: #FFFFFF;
          box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3);
        }

        /* Mobile & Smartphone Bottom-Sheet Ergonomics (< 640px) */
        @media (max-width: 640px) {
          .part-quiz-modal-backdrop {
            padding: 0;
            align-items: flex-end; /* Slides up like native iOS/Android sheet */
          }
          .quiz-modal-card {
            border-radius: 24px 24px 0 0;
            max-height: 88vh;
            padding: 20px 18px env(safe-area-inset-bottom, 24px);
            margin: 0;
            border-bottom: none;
            transform: translateY(100%);
          }
          .part-quiz-modal-backdrop.open .quiz-modal-card {
            transform: translateY(0);
          }
          .quiz-modal-part-name {
            font-size: 0.84rem;
            max-width: 170px;
          }
          .quiz-modal-q-text {
            font-size: 1.05rem;
            line-height: 1.5;
          }
          .quiz-modal-q-tr {
            font-size: 0.86rem;
          }
          .btn-quiz-choice {
            height: 58px;
          }
          .choice-lbl {
            font-size: 1.05rem;
          }
          .choice-sub {
            font-size: 0.68rem;
          }
          .part-quiz-actions-wrap {
            width: 100%;
            margin-top: 8px;
            display: flex;
            gap: 8px;
          }
          .btn-part-quiz-trigger {
            flex: 1;
            height: 36px;
            justify-content: center;
            font-size: 0.82rem;
          }
        }
      `;
      document.head.appendChild(s);
    },
    """

code = code[:pos_styles_start] + new_styles_block + code[pos_styles_end:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Part Quiz Modal redesigned with perfection and mobile ergonomics!")

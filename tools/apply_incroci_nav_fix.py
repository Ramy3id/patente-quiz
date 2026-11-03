import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = 'R:/Ramy/PATENTE_PRO_APP/interactive_pages/decodificatore-incroci.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """.sim-nav-counter {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--inc-text-sub);
      padding: 0 6px;
      white-space: nowrap;
    }"""

replacement = """.sim-nav-counter {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--inc-text-sub);
      padding: 0 6px;
      white-space: nowrap;
    }

    /* تحسينات الاستجابة لشاشات الموبايل لشريط التنقل والمحاكي */
    @media (max-width: 768px) {
      .traffic-sim-section {
        padding: 14px !important;
        border-radius: 20px !important;
      }
      .sim-header {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 10px !important;
      }
      .sim-title {
        font-size: 1.15rem !important;
        line-height: 1.4 !important;
      }
      .sim-subdesc {
        font-size: 0.82rem !important;
        line-height: 1.5 !important;
      }
      .sim-nav-header {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 10px !important;
        padding: 10px !important;
      }
      .sim-selector-wrap {
        width: 100% !important;
        min-width: 0 !important;
        flex: none !important;
      }
      .sim-selector-btn {
        width: 100% !important;
        padding: 9px 12px !important;
        box-sizing: border-box !important;
      }
      .sim-sel-val {
        font-size: 0.88rem !important;
      }
      .sim-arrows-wrap {
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 8px !important;
        box-sizing: border-box !important;
      }
      .sim-nav-arrow-btn {
        flex: 1 !important;
        justify-content: center !important;
        text-align: center !important;
        padding: 9px 12px !important;
        font-size: 0.84rem !important;
        box-sizing: border-box !important;
      }
      .sim-nav-counter {
        padding: 0 10px !important;
        text-align: center !important;
        flex-shrink: 0 !important;
        font-size: 0.85rem !important;
      }
      .sim-actions-row {
        flex-direction: column !important;
        gap: 8px !important;
      }
      .btn-sim-play, .btn-sim-step, .btn-sim-reset {
        width: 100% !important;
        flex: none !important;
      }
      .sim-options-bar {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 10px !important;
      }
      .sim-speed-wrap {
        justify-content: space-between !important;
        width: 100% !important;
      }
    }

    /* أنماط الوضع النهاري لمحاكي التقاطعات */
    html.light .traffic-sim-section {
      background: #FFFFFF !important;
      border-color: #E2E8F0 !important;
      box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06) !important;
    }
    html.light .sim-title {
      color: #0F172A !important;
    }
    html.light .sim-subdesc {
      color: #64748B !important;
    }
    html.light .sim-nav-header {
      background: #F8FAFC !important;
      border-color: #E2E8F0 !important;
    }
    html.light .sim-selector-btn {
      background: #FFFFFF !important;
      border-color: #BAE6FD !important;
      color: #0F172A !important;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    }
    html.light .sim-sel-val {
      color: #0F172A !important;
    }
    html.light .sim-nav-arrow-btn {
      background: #FFFFFF !important;
      border-color: #CBD5E1 !important;
      color: #1E293B !important;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    }
    html.light .sim-nav-arrow-btn:hover {
      background: #E0F2FE !important;
      border-color: #38BDF8 !important;
      color: #0284C7 !important;
    }
    html.light .sim-nav-counter {
      color: #475569 !important;
    }
    html.light .sim-official-compare-card,
    html.light .sim-status-box,
    html.light .sim-options-bar {
      background: #F8FAFC !important;
      border-color: #E2E8F0 !important;
    }
    html.light .sim-status-step {
      color: #0F172A !important;
    }
    html.light .sim-status-reason {
      color: #475569 !important;
    }
    html.light .sim-toggle-btn {
      background: #FFFFFF !important;
      border-color: #CBD5E1 !important;
      color: #1E293B !important;
    }"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Updated decodificatore-incroci.html with responsive simulator nav styles")
else:
    print("WARNING: target not found in decodificatore-incroci.html")

/**
 * =======================================================================
 * Patente B Pro - Bilingual Synchronized Highlighter Engine
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محرك التظليل اللوني المتقابل بين الإيطالية والعربية:
 *  - تظليل الكلمات والمصطلحات والعبارات المركبة في السؤال الإيطالي
 *  - تظليل المعنى المطابق لها في الترجمة العربية بنفس اللون بدقة
 *  - استخدام لوحة ألوان متباينة (سماوي، ذهبي، زمردي، بنفسجي، وردي)
 *  - تفاعل حي: عند لمس أو تمرير الفأرة على المصطلح يضيء المعنى المقابل له فوراً
 *  - إمكانية تشغيل وإيقاف التظليل حسب رغبة الطالب
 */

class PatenteBilingualHighlighter {
  constructor() {
    this.storageKey = "patente_bilingual_hl";
    this.palette = [
      { id: 0, class: "sync-hl-0", colorDark: "#38BDF8", colorLight: "#0284C7", bgDark: "rgba(56, 189, 248, 0.24)", bgLight: "rgba(2, 132, 199, 0.16)", border: "rgba(56, 189, 248, 0.5)" },
      { id: 1, class: "sync-hl-1", colorDark: "#F59E0B", colorLight: "#D97706", bgDark: "rgba(245, 158, 11, 0.24)", bgLight: "rgba(217, 119, 6, 0.16)", border: "rgba(245, 158, 11, 0.5)" },
      { id: 2, class: "sync-hl-2", colorDark: "#10B981", colorLight: "#059669", bgDark: "rgba(16, 185, 129, 0.24)", bgLight: "rgba(5, 150, 105, 0.16)", border: "rgba(16, 185, 129, 0.5)" },
      { id: 3, class: "sync-hl-3", colorDark: "#A855F7", colorLight: "#7C3AED", bgDark: "rgba(168, 85, 247, 0.24)", bgLight: "rgba(124, 58, 237, 0.16)", border: "rgba(168, 85, 247, 0.5)" },
      { id: 4, class: "sync-hl-4", colorDark: "#F43F5E", colorLight: "#E11D48", bgDark: "rgba(244, 63, 94, 0.24)", bgLight: "rgba(225, 29, 72, 0.16)", border: "rgba(244, 63, 94, 0.5)" }
    ];
    this.injectStyles();
  }

  isEnabled() {
    if (typeof localStorage === "undefined") return true;
    const saved = localStorage.getItem(this.storageKey);
    return saved === null ? true : (saved === "true");
  }

  setEnabled(val) {
    if (typeof localStorage === "undefined") return;
    localStorage.setItem(this.storageKey, val ? "true" : "false");
  }

  toggle() {
    const current = this.isEnabled();
    this.setEnabled(!current);
    return !current;
  }

  escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  normalizeArabic(text) {
    return (text || "")
      .replace(/[أإآ]/g, 'ا')
      .replace(/ة/g, 'ه')
      .replace(/ى/g, 'ي')
      .replace(/[\u064B-\u065F]/g, '');
  }

  /**
   * استخراج أزواج المصطلحات وترجمتها من السؤال
   */
  extractPairs(qObj) {
    const pairs = [];
    if (!qObj) return pairs;

    const rawPk = qObj.pk || qObj.parole_chiave;
    if (Array.isArray(rawPk)) {
      for (const item of rawPk) {
        let itTerm = "";
        let arTerm = "";

        if (typeof item === 'object') {
          if (item.it && item.ar && item.ar.trim()) {
            itTerm = item.it.trim();
            arTerm = item.ar.trim();
          } else if (item.it) {
            const m = item.it.match(/^([^(]+)\s*\(([^)]+)\)$/);
            if (m) {
              itTerm = m[1].trim();
              arTerm = m[2].trim();
            } else {
              itTerm = item.it.trim();
            }
          }
        } else if (typeof item === 'string') {
          const m = item.match(/^([^(]+)\s*\(([^)]+)\)$/);
          if (m) {
            itTerm = m[1].trim();
            arTerm = m[2].trim();
          } else {
            itTerm = item.trim();
          }
        }

        if (arTerm) {
          arTerm = arTerm.replace(/\s*-\s*(خطأ|صحيح|باطل|ليس من اختصاصه).*$/i, '').replace(/\/.*$/, '').trim();
        }

        if (itTerm && itTerm.length >= 3) {
          // فحص هل المصطلح الإيطالي موجود فعلاً في نص السؤال
          const qText = (qObj.q || qObj.domanda || "").toLowerCase();
          if (qText.includes(itTerm.toLowerCase())) {
            pairs.push({ it: itTerm, ar: arTerm });
          }
        }
      }
    }

    return pairs;
  }

  /**
   * تنظيف أداة التعريف من كلمات العبارة المركبة
   */
  cleanAl(text) {
    return (text || "").split(/\s+/).map(w => w.startsWith('ال') ? w.slice(2) : w).join(' ');
  }

  dualNormalize(text) {
    return (text || "").replace(/([\p{L}]+)ان(?=\s|$|[^\p{L}])/gu, '$1ين');
  }

  /**
   * البحث عن موضع الترجمة العربية المطابقة داخل نص الترجمة
   */
  findArabicMatch(sourceAr, searchAr) {
    if (!searchAr || !sourceAr) return null;

    // 1. تطابق حرفي مباشر
    const idx = sourceAr.indexOf(searchAr);
    if (idx !== -1) {
      return { start: idx, end: idx + searchAr.length };
    }

    // 2. فحص مع أو بدون "ال" التعريف للعبارة ككل
    let altSearch = searchAr.startsWith('ال') ? searchAr.slice(2) : ('ال' + searchAr);
    let altIdx = sourceAr.indexOf(altSearch);
    if (altIdx !== -1) {
      return { start: altIdx, end: altIdx + altSearch.length };
    }

    // 3. فحص صيغة المثنى بالياء (مثل "اتجاهان" -> "اتجاهين")
    const dualSearch = this.dualNormalize(searchAr);
    if (dualSearch !== searchAr) {
      const dIdx = sourceAr.indexOf(dualSearch);
      if (dIdx !== -1) {
        return { start: dIdx, end: dIdx + dualSearch.length };
      }
    }

    // 4. فحص تنظيف "ال" من كلمات العبارة المركبة (مثل "نهر الطريق" -> "نهر طريق")
    const cleanSearch = this.cleanAl(searchAr);
    if (cleanSearch !== searchAr) {
      const cIdx = sourceAr.indexOf(cleanSearch);
      if (cIdx !== -1) {
        return { start: cIdx, end: cIdx + cleanSearch.length };
      }
    }

    // 4. تطابق مع تطبيع الحروف (الهمزات والتاء المربوطة)
    const normSource = this.normalizeArabic(sourceAr);
    const normSearch = this.normalizeArabic(searchAr);
    const normIdx = normSource.indexOf(normSearch);
    if (normIdx !== -1) {
      return { start: normIdx, end: normIdx + searchAr.length };
    }

    const normCleanSearch = this.normalizeArabic(cleanSearch);
    const normCleanIdx = normSource.indexOf(normCleanSearch);
    if (normCleanIdx !== -1) {
      return { start: normCleanIdx, end: normCleanIdx + cleanSearch.length };
    }

    // 5. إذا كانت جملة مركبة، محاولة البحث عن الكلمات الرئيسية
    const words = searchAr.split(/\s+/).filter(w => w.length >= 3);
    if (words.length > 1) {
      for (const w of words) {
        const wIdx = sourceAr.indexOf(w);
        if (wIdx !== -1) {
          return { start: wIdx, end: wIdx + w.length };
        }
      }
    }

    return null;
  }

  /**
   * تطبيق التظليل المتقابل على النص الإيطالي والعربي
   */
  highlightQuestion(qObj) {
    const rawIt = qObj.q || qObj.domanda || "";
    const rawAr = qObj.tr || qObj.traduzione || "";

    if (!this.isEnabled()) {
      return {
        itHtml: rawIt,
        arHtml: rawAr,
        matchedPairs: [],
        enabled: false
      };
    }

    const pairs = this.extractPairs(qObj);
    if (!pairs.length) {
      return {
        itHtml: rawIt,
        arHtml: rawAr,
        matchedPairs: [],
        enabled: true
      };
    }

    let itResult = rawIt;
    let arResult = rawAr;
    const matchedPairs = [];

    pairs.forEach((pair, idx) => {
      const paletteIndex = idx % this.palette.length;
      const colorClass = `sync-hl-${paletteIndex}`;
      const colorStyle = this.palette[paletteIndex];

      // تظليل في السؤال الإيطالي
      let itMatched = false;
      if (pair.it) {
        const itRegex = new RegExp('(' + this.escapeRegex(pair.it) + ')', 'gi');
        if (itRegex.test(itResult)) {
          itResult = itResult.replace(itRegex, `<mark class="sync-hl-term ${colorClass}" data-pair="${idx}" title="المعنى بالعربية: ${pair.ar || ''}">$1</mark>`);
          itMatched = true;
        }
      }

      // تظليل في الترجمة العربية
      let arMatched = false;
      if (pair.ar) {
        const match = this.findArabicMatch(arResult, pair.ar);
        if (match) {
          const before = arResult.slice(0, match.start);
          const matchedText = arResult.slice(match.start, match.end);
          const after = arResult.slice(match.end);
          arResult = before + `<mark class="sync-hl-term ${colorClass}" data-pair="${idx}" title="المصطلح الإيطالي: ${pair.it}">${matchedText}</mark>` + after;
          arMatched = true;
        }
      }

      if (itMatched || arMatched) {
        matchedPairs.push({
          idx: idx,
          it: pair.it,
          ar: pair.ar,
          colorClass: colorClass,
          colorDark: colorStyle.colorDark,
          colorLight: colorStyle.colorLight
        });
      }
    });

    return {
      itHtml: itResult,
      arHtml: arResult,
      matchedPairs: matchedPairs,
      enabled: true
    };
  }

  /**
   * توليد أشرطة المفردات المتقابلة (Chips / Legend) أسفل السؤال
   */
  renderPairChips(matchedPairs) {
    if (!matchedPairs || !matchedPairs.length) return "";
    return `
      <div class="sync-hl-chips-wrap">
        <span class="sync-hl-chips-lbl">🎨 المصطلحات المظللة في السؤال:</span>
        <div class="sync-hl-chips-list">
          ${matchedPairs.map(p => `
            <div class="sync-hl-chip ${p.colorClass}" data-pair="${p.idx}">
              <strong class="sync-chip-it">${p.it}</strong>
              <span class="sync-chip-arrow">⇄</span>
              <span class="sync-chip-ar">${p.ar || 'موضح في السياق'}</span>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  /**
   * ربط التفاعل اللمسي والحركي التلقائي (Hover & Touch Sync)
   */
  bindEvents(container) {
    const root = container || document;
    const marks = root.querySelectorAll(".sync-hl-term, .sync-hl-chip");

    marks.forEach(el => {
      const pairId = el.getAttribute("data-pair");
      if (!pairId) return;

      const activate = () => {
        root.querySelectorAll(`[data-pair="${pairId}"]`).forEach(m => m.classList.add("sync-active"));
      };
      const deactivate = () => {
        root.querySelectorAll(`[data-pair="${pairId}"]`).forEach(m => m.classList.remove("sync-active"));
      };

      el.addEventListener("mouseenter", activate);
      el.addEventListener("mouseleave", deactivate);
      el.addEventListener("touchstart", activate, { passive: true });
      el.addEventListener("touchend", deactivate, { passive: true });
    });
  }

  /**
   * حقن الأنماط المرئية الأنيقة المتوافقة مع الوضعين النهاري والليلي
   */
  injectStyles() {
    if (typeof document === "undefined") return;
    if (document.getElementById("sync-hl-styles")) return;
    const style = document.createElement("style");
    style.id = "sync-hl-styles";
    style.textContent = `
      /* Base Synchronized Highlight Term */
      .sync-hl-term {
        padding: 1px 7px;
        border-radius: 6px;
        font-weight: 800;
        cursor: pointer;
        display: inline-block;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        border: 1px solid transparent;
        text-decoration: none;
      }
      .sync-hl-term.sync-active, .sync-hl-term:hover {
        transform: scale(1.05);
        box-shadow: 0 0 14px currentColor;
        z-index: 2;
        position: relative;
      }

      /* Color 0: Sky Blue (سماوي) */
      .sync-hl-0 {
        background: rgba(56, 189, 248, 0.22);
        border-color: rgba(56, 189, 248, 0.5);
        color: #7DD3FC;
      }
      html.light .sync-hl-0 {
        background: rgba(2, 132, 199, 0.14);
        border-color: rgba(2, 132, 199, 0.4);
        color: #0369A1;
      }

      /* Color 1: Amber Gold (ذهبي / برتقالي) */
      .sync-hl-1 {
        background: rgba(245, 158, 11, 0.22);
        border-color: rgba(245, 158, 11, 0.5);
        color: #FCD34D;
      }
      html.light .sync-hl-1 {
        background: rgba(217, 119, 6, 0.14);
        border-color: rgba(217, 119, 6, 0.4);
        color: #B45309;
      }

      /* Color 2: Emerald Green (زمردي / أخضر) */
      .sync-hl-2 {
        background: rgba(16, 185, 129, 0.22);
        border-color: rgba(16, 185, 129, 0.5);
        color: #6EE7B7;
      }
      html.light .sync-hl-2 {
        background: rgba(5, 150, 105, 0.14);
        border-color: rgba(5, 150, 105, 0.4);
        color: #047857;
      }

      /* Color 3: Purple Violet (بنفسجي) */
      .sync-hl-3 {
        background: rgba(168, 85, 247, 0.22);
        border-color: rgba(168, 85, 247, 0.5);
        color: #D8B4FE;
      }
      html.light .sync-hl-3 {
        background: rgba(124, 58, 237, 0.14);
        border-color: rgba(124, 58, 237, 0.4);
        color: #6D28D9;
      }

      /* Color 4: Rose Coral (وردي / أحمر مرجاني) */
      .sync-hl-4 {
        background: rgba(244, 63, 94, 0.22);
        border-color: rgba(244, 63, 94, 0.5);
        color: #FDA4AF;
      }
      html.light .sync-hl-4 {
        background: rgba(225, 29, 72, 0.14);
        border-color: rgba(225, 29, 72, 0.4);
        color: #BE123C;
      }

      /* Pair Chips Legend Bar */
      .sync-hl-chips-wrap {
        margin-top: 12px;
        padding-top: 10px;
        border-top: 1px dashed rgba(255, 255, 255, 0.08);
      }
      html.light .sync-hl-chips-wrap {
        border-top-color: rgba(15, 23, 42, 0.08);
      }
      .sync-hl-chips-lbl {
        font-size: 0.76rem;
        font-weight: 700;
        color: var(--tr-text-sub, #94A3B8);
        display: block;
        margin-bottom: 6px;
      }
      .sync-hl-chips-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }
      .sync-hl-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
      }
      .sync-hl-chip.sync-active, .sync-hl-chip:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      }
      .sync-chip-it {
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
        font-weight: 700;
        direction: ltr;
      }
      .sync-chip-arrow {
        opacity: 0.7;
        font-size: 0.85rem;
      }
      .sync-chip-ar {
        font-weight: 600;
      }
    `;
    document.head.appendChild(style);
  }
}

// Make globally accessible
if (typeof window !== "undefined") {
  window.PatenteBilingualHighlighter = PatenteBilingualHighlighter;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = { PatenteBilingualHighlighter };
}

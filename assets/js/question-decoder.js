/**
 * =======================================================================
 * Patente B Pro - 3-Block Question Decoder Engine (Il Metodo dei 3 Blocchi)
 * =======================================================================
 * @author Patente B Pro Pedagogical & Engineering Team
 * @description محرك تفكيك أسئلة كود السير الإيطالي إلى 3 كتل منطقية ومعادلة رياضية:
 *   1. الكتلة 1 (المسرح / الظرف / السياق - Il Contesto / Dove e Quando)
 *   2. الكتلة 2 (الموضوع / المناورة / العنصر القانوني - L'Oggetto / Di cosa parliamo)
 *   3. الكتلة 3 (الحكم القانوني / الإلزام - Il Verbo di Giudizio / Cosa dice la legge)
 *   + المعادلة الرياضية المنطقية (Formula Logica):
 *     [📍 المسرح] + [🎯 الموضوع] ➔ [⚖️ الحكم] = ✅ VERO / ❌ FALSO
 */

class PatenteQuestionDecoder {
  constructor() {
    this.storageKey = "patente_question_decoder";

    // 1. Context Matchers (المسرح - أين ومتى والظرف)
    this.contextRegex = /^(In una carreggiata[^,;]*|Nell['’]incrocio[^,;]*|In un incrocio[^,;]*|Sulle strade[^,;]*|Sulla carreggiata[^,;]*|In autostrada[^,;]*|In caso di[^,;]*|In presenza del segnale[^,;]*|In presenza di[^,;]*|Il segnale raffigurato[^,;]*|Il segnale in figura[^,;]*|Il pannello integrativo[^,;]*|Alla guida di[^,;]*|Di notte[^,;]*|Fuori dei centri abitati[^,;]*|Fuori dai centri abitati[^,;]*|Nei centri abitati[^,;]*|Sui dossi[^,;]*|In curva[^,;]*|Nelle curve[^,;]*|Nelle gallerie[^,;]*|Durante la marcia[^,;]*|Prima di[^,;]*|Quando si[^,;]*|Se si[^,;]*|Su strade[^,;]*|Lungo le autostrade[^,;]*|Nei passaggi a livello[^,;]*|A un passaggio a livello[^,;]*|In corrispondenza di[^,;]*|Per svoltare[^,;]*|Giungendo all['’]incrocio[^,;]*|Viaggiando[^,;]*|Dopo aver[^,;]*|Durante il[^,;]*|Nel caso in cui[^,;]*|Con la patente[^,;]*)/i;

    // 2. Judgment Matchers (الحكم القانوني - ماذا يقرر القانون)
    this.judgmentRegex = /(non è consentit[oa]|non è permess[oa]|non è vietat[oa]|non è obbligatori[oa]|è consentit[oa]|è permess[oa]|è vietat[oa]|è obbligatori[oa]|è facoltativ[oa]|non si può|non si possono|si può|si possono|non si deve|non si devono|si deve|si devono|non bisogna|bisogna|non occorre|occorre|impone di|prescrive di|obbliga a|vieta di|consente di|permette di|autorizza a|aumenta|diminuisce|raddoppia|si riduce|deve accertarsi|deve assicurarsi|deve verificare|deve moderare|deve rallentare|deve fermarsi|è tenuto a|è tenuto ad|ha l['’]obbligo di|non ha l['’]obbligo di|ha la precedenza|deve dare la precedenza|passa per primo|passa per ultimo|passa dopo|è di \d+ km\/h|è di \d+|non può superare|non deve superare|deve essere utilizzato|non deve essere|è opportuno|non è opportuno|è consigliabile|comporta la sospensione|comporta la revoca|comporta la decurtazione|costituisce reato|è punito|non fa parte|fa parte|è destinato a|non è destinato a)/i;

    // Sorted glossary for smart semantic annotation
    this.termsList = [
      { it: "limite massimo di velocità", ar: "الحد الأقصى للسرعة" },
      { it: "limite di velocità", ar: "حد السرعة" },
      { it: "distanza di sicurezza", ar: "مسافة الأمان" },
      { it: "inversione di marcia", ar: "الدوران للخلف (U-turn)" },
      { it: "cinture di sicurezza", ar: "أحزمة الأمان" },
      { it: "proiettori anabbaglianti", ar: "الأضواء المنخفضة (الكوديك)" },
      { it: "proiettori abbaglianti", ar: "الأضواء العالية (الفار)" },
      { it: "anabbaglianti", ar: "الأضواء المنخفضة" },
      { it: "abbaglianti", ar: "الأضواء العالية" },
      { it: "passo carrabile", ar: "ممر عبور المركبات" },
      { it: "attraversamento pedonale", ar: "معبر المشاة" },
      { it: "dare la precedenza", ar: "إعطاء الأسبقية" },
      { it: "ha la precedenza", ar: "له حق الأسبقية" },
      { it: "fuori dei centri abitati", ar: "خارج المناطق السكنية" },
      { it: "fuori dai centri abitati", ar: "خارج المناطق السكنية" },
      { it: "centri abitati", ar: "المناطق السكنية" },
      { it: "carreggiata", ar: "نهر الطريق" },
      { it: "autostrada", ar: "الطريق السريع" },
      { it: "corsia", ar: "المسار" },
      { it: "sorpasso", ar: "التجاوز" },
      { it: "sorpassare", ar: "التجاوز" },
      { it: "sosta", ar: "الركن (الانتظار)" },
      { it: "fermata", ar: "التوقف المؤقت" },
      { it: "incrocio", ar: "التقاطع" },
      { it: "precedenza", ar: "أسبقية المرور" },
      { it: "freno di stazionamento", ar: "فرامل التوقف (اليد)" },
      { it: "freno", ar: "الفرامل" },
      { it: "precipitazioni", ar: "هطول الأمطار" },
      { it: "pioggia", ar: "المطر" },
      { it: "nebbia", ar: "الضباب" },
      { it: "dossi", ar: "المرتفعات (Dossi)" },
      { it: "curva", ar: "المنعطف" },
      { it: "segnale", ar: "الإشارة المرورية" },
      { it: "pannello integrativo", ar: "اللوحة الإضافية" },
      { it: "veicolo", ar: "المركبة" },
      { it: "visibilità", ar: "وضوح الرؤية" },
      { it: "marcia ordinaria", ar: "السير العادي" },
      { it: "file parallele", ar: "الصفوف المتوازية" }
    ];

    this.injectStyles();
  }

  isEnabled() {
    if (typeof localStorage === "undefined") return true;
    const val = localStorage.getItem(this.storageKey);
    return val === null ? true : (val === "true");
  }

  setEnabled(val) {
    if (typeof localStorage === "undefined") return;
    localStorage.setItem(this.storageKey, val ? "true" : "false");
    window.dispatchEvent(new CustomEvent("decoderStateChanged", { detail: { enabled: val } }));
  }

  toggle() {
    const next = !this.isEnabled();
    this.setEnabled(next);
    return next;
  }

  /**
   * تفكيك أي سؤال وزاري إلى كتل ومكونات المعادلة
   */
  decode(qObj) {
    if (!qObj) return null;

    const rawIt = (qObj.q || qObj.domanda || "").trim();
    const rawAr = (qObj.tr || qObj.traduzione || "").trim();
    const isTrue = Boolean(
      qObj.a !== undefined
        ? qObj.a
        : qObj.risposta !== undefined
        ? qObj.risposta
        : qObj.correctAnswer
    );

    let b1It = "";
    let b2It = "";
    let b3It = "";

    const jdgMatch = rawIt.match(this.judgmentRegex);

    if (jdgMatch) {
      const jdgIdx = rawIt.search(this.judgmentRegex);
      const jdgStr = jdgMatch[0];
      const beforeJdg = rawIt.slice(0, jdgIdx).trim();
      const afterJdg = rawIt.slice(jdgIdx + jdgStr.length).trim();

      const ctxMatch = beforeJdg.match(this.contextRegex);
      if (ctxMatch) {
        b1It = ctxMatch[0].replace(/[,;:\s]+$/, "").trim();
        const objPart1 = beforeJdg
          .slice(ctxMatch[0].length)
          .replace(/^[,;:\s]+/, "")
          .replace(/[,;:\s]+$/, "")
          .trim();

        if (afterJdg && objPart1) {
          b2It = `${objPart1} (${afterJdg})`;
        } else if (afterJdg) {
          b2It = afterJdg;
        } else if (objPart1) {
          b2It = objPart1;
        } else {
          b2It = "la manovra / la condizione indicata";
        }
      } else {
        if (beforeJdg) {
          b1It = "Norma generale di circolazione (قاعدة سير عامة)";
          b2It = beforeJdg;
        } else {
          b1It = "Norma generale di circolazione";
          b2It = afterJdg || "la manovra indicata";
        }
        if (afterJdg && !b2It.includes(afterJdg)) {
          b2It = b2It ? `${b2It} ➔ ${afterJdg}` : afterJdg;
        }
      }

      b3It = jdgStr;
    } else {
      const ctxMatch = rawIt.match(this.contextRegex);
      if (ctxMatch) {
        b1It = ctxMatch[0].replace(/[,;:\s]+$/, "").trim();
        b2It = rawIt.slice(ctxMatch[0].length).replace(/^[,;:\s]+/, "").trim();
      } else {
        b1It = "Norma generale di circolazione";
        b2It = rawIt;
      }
      b3It = isTrue ? "è conforme alla legge" : "non è conforme alla legge";
    }

    if (!b1It) b1It = "Norma generale di circolazione";
    b1It = b1It.replace(/[,;:\s]+$/, "").trim();
    b2It = (b2It || "la manovra o condizione indicata").replace(/[,;:\s]+$/, "").trim();
    b3It = (b3It || (isTrue ? "è consentito" : "è vietato")).replace(/[,;:\s]+$/, "").trim();

    const fCtx = this.simplifyForFormula(b1It);
    const fObj = this.simplifyForFormula(b2It);
    const fJdg = this.simplifyForFormula(b3It);

    const formulaText = `[📍 ${fCtx}] + [🎯 ${fObj}] ➔ [⚖️ ${fJdg}] = ${isTrue ? "✅ VERO (صح)" : "❌ FALSO (خطأ)"}`;

    return {
      b1: {
        titleAr: "المسرح والظرف",
        titleIt: "Il Contesto",
        icon: "📍",
        it: b1It,
        ar: this.extractContextArabic(b1It, rawAr)
      },
      b2: {
        titleAr: "الموضوع والمناورة",
        titleIt: "L'Oggetto",
        icon: "🎯",
        it: b2It,
        ar: this.extractSubjectArabic(b2It, rawAr)
      },
      b3: {
        titleAr: "الحكم القانوني",
        titleIt: "Il Giudizio",
        icon: "⚖️",
        it: b3It,
        ar: this.extractJudgmentArabic(b3It, isTrue)
      },
      formula: {
        text: formulaText,
        ctx: fCtx,
        obj: fObj,
        jdg: fJdg,
        isTrue: isTrue
      },
      isTrue: isTrue,
      explanation: qObj.sp || qObj.spiegazione || "",
      trap: qObj.tb || qObj.trabocchetto || ""
    };
  }

  simplifyForFormula(text) {
    if (!text) return "...";
    let s = text
      .replace(/^(In una|In un|Nell'|Sulle|Sulla|In|Alla|Di|Fuori dei|Nei)\s+/i, "")
      .replace(/del tipo rappresentato/gi, "")
      .replace(/rappresentat[oa]\s*(nella figura)?/gi, "")
      .replace(/in figura/gi, "")
      .trim();
    if (s.length > 38) {
      s = s.slice(0, 36) + "...";
    }
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  extractContextArabic(itSnippet, fullArabic) {
    for (const item of this.termsList) {
      if (new RegExp(item.it, "i").test(itSnippet)) {
        return item.ar;
      }
    }
    if (fullArabic) {
      const parts = fullArabic.split(/[,،]/);
      if (parts.length > 1) return parts[0].trim();
    }
    return "سياق وظرف السؤال";
  }

  extractSubjectArabic(itSnippet, fullArabic) {
    for (const item of this.termsList) {
      if (new RegExp(item.it, "i").test(itSnippet)) {
        return item.ar;
      }
    }
    return "المناورة أو المسألة المطروحة";
  }

  extractJudgmentArabic(itSnippet, isTrue) {
    const s = itSnippet.toLowerCase();
    if (s.includes("vietat") || s.includes("non si può") || s.includes("non è consentit")) return "🚫 ممنوع قانوناً (Vietato)";
    if (s.includes("obbligatori") || s.includes("si deve") || s.includes("impone") || s.includes("obbliga") || s.includes("deve accertarsi") || s.includes("ha l'obbligo")) return "⚡ إلزامي وإجباري (Obbligatorio)";
    if (s.includes("consentit") || s.includes("si può") || s.includes("permess")) return "🟢 مسموح وجائز (Consentito)";
    if (s.includes("facoltativ")) return "⚪ اختياري (Facoltativo)";
    if (s.includes("dare la precedenza")) return "🛑 إعطاء الأسبقية";
    if (s.includes("ha la precedenza")) return "👑 له حق الأسبقية";
    if (s.includes("aumenta")) return "📈 يزداد";
    if (s.includes("diminuisce") || s.includes("riduce")) return "📉 ينخفض ويقل";
    return isTrue ? "✅ سليم ومطابق للقانون" : "❌ باطل ومخالف للقانون";
  }

  /**
   * توليد بطاقة HTML متكاملة لتفكيك السؤال
   */
  renderDecoderCard(qObj, options = {}) {
    const dec = this.decode(qObj);
    if (!dec) return "";

    const isCollapsed = options.collapsed || false;
    const cardId = "decCard_" + Math.random().toString(36).substring(2, 9);

    return `
      <div class="pt-decoder-card ${dec.isTrue ? 'res-is-vero' : 'res-is-falso'}" id="${cardId}">
        <div class="pt-dec-header" onclick="window.questionDecoder.toggleCardContent('${cardId}')" style="cursor: pointer;" title="انقر للطي أو الفتح">
          <div class="pt-dec-title">
            <span class="pt-dec-icon">🧩</span>
            <strong>مفكك الـ 3 كتل المنطقية</strong>
            <span class="pt-dec-sub">(Il Metodo dei 3 Blocchi)</span>
          </div>
          <div class="pt-dec-meta">
            <span class="pt-dec-status-badge ${dec.isTrue ? 'badge-v' : 'badge-f'}">
              ${dec.isTrue ? 'VERO (صح)' : 'FALSO (خطأ)'}
            </span>
            <span class="pt-dec-toggle-arrow">▾</span>
          </div>
        </div>

        <div class="pt-dec-content" style="${isCollapsed ? 'display:none;' : ''}">
          <!-- شبكة الكتل الثلاث -->
          <div class="pt-dec-grid">
            <!-- 1. المسرح -->
            <div class="pt-dec-cell cell-ctx">
              <div class="pt-dec-badge">
                <span class="ico">📍</span>
                <span>1. المسرح (Contesto)</span>
              </div>
              <div class="pt-dec-it">${this.escapeHtml(dec.b1.it)}</div>
              <div class="pt-dec-ar">${this.escapeHtml(dec.b1.ar)}</div>
            </div>

            <!-- 2. الموضوع -->
            <div class="pt-dec-cell cell-obj">
              <div class="pt-dec-badge">
                <span class="ico">🎯</span>
                <span>2. الموضوع (Oggetto)</span>
              </div>
              <div class="pt-dec-it">${this.escapeHtml(dec.b2.it)}</div>
              <div class="pt-dec-ar">${this.escapeHtml(dec.b2.ar)}</div>
            </div>

            <!-- 3. الحكم -->
            <div class="pt-dec-cell cell-jdg">
              <div class="pt-dec-badge">
                <span class="ico">⚖️</span>
                <span>3. الحكم (Giudizio)</span>
              </div>
              <div class="pt-dec-it">${this.escapeHtml(dec.b3.it)}</div>
              <div class="pt-dec-ar">${this.escapeHtml(dec.b3.ar)}</div>
            </div>
          </div>

          <!-- المعادلة الرياضية المنطقية -->
          <div class="pt-dec-formula-bar ${dec.isTrue ? 'form-v' : 'form-f'}">
            <div class="pt-form-head">
              <span>📐 المعادلة الرياضية للمسألة (Formula Logica):</span>
            </div>
            <div class="pt-form-math" dir="ltr">
              <span class="pt-f-part f-c" title="المسرح">[📍 ${this.escapeHtml(dec.formula.ctx)}]</span>
              <span class="pt-f-plus">+</span>
              <span class="pt-f-part f-o" title="الموضوع">[🎯 ${this.escapeHtml(dec.formula.obj)}]</span>
              <span class="pt-f-arrow">➔</span>
              <span class="pt-f-part f-j" title="الحكم">[⚖️ ${this.escapeHtml(dec.formula.jdg)}]</span>
              <span class="pt-f-eq">=</span>
              <span class="pt-f-res ${dec.isTrue ? 'res-v' : 'res-f'}">
                ${dec.isTrue ? 'VERO (✅)' : 'FALSO (❌)'}
              </span>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * شريط مصغر خفيف للمعادلة المنطقية فقط
   */
  renderFormula(qObj) {
    const dec = this.decode(qObj);
    if (!dec) return "";
    return `
      <div class="pt-dec-mini-formula ${dec.isTrue ? 'form-v' : 'form-f'}" dir="ltr">
        <span class="pt-f-part f-c">[📍 ${this.escapeHtml(dec.formula.ctx)}]</span>
        <span class="pt-f-plus">+</span>
        <span class="pt-f-part f-o">[🎯 ${this.escapeHtml(dec.formula.obj)}]</span>
        <span class="pt-f-arrow">➔</span>
        <span class="pt-f-part f-j">[⚖️ ${this.escapeHtml(dec.formula.jdg)}]</span>
        <span class="pt-f-eq">=</span>
        <span class="pt-f-res ${dec.isTrue ? 'res-v' : 'res-f'}">
          ${dec.isTrue ? 'VERO ✅' : 'FALSO ❌'}
        </span>
      </div>
    `;
  }

  toggleCardContent(cardId) {
    const card = document.getElementById(cardId);
    if (!card) return;
    const content = card.querySelector(".pt-dec-content");
    const arrow = card.querySelector(".pt-dec-toggle-arrow");
    if (!content) return;
    const isHidden = content.style.display === "none";
    content.style.display = isHidden ? "block" : "none";
    if (arrow) arrow.innerText = isHidden ? "▾" : "◀";
  }

  escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  injectStyles() {
    if (document.getElementById("patente-decoder-styles")) return;

    const css = `
      /* =========================================================
         Patente B Pro - 3-Block Question Decoder UI Styles
         ========================================================= */
      .pt-decoder-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 14px 16px;
        margin: 12px 0;
        font-family: 'Cairo', system-ui, sans-serif;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        backdrop-filter: blur(12px);
        transition: all 0.25s ease;
      }
      html.light .pt-decoder-card {
        background: #FFFFFF;
        border: 1px solid rgba(15, 23, 42, 0.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
      }

      .pt-decoder-card.res-is-vero {
        border-left: 4px solid #10B981;
      }
      .pt-decoder-card.res-is-falso {
        border-left: 4px solid #F43F5E;
      }

      .pt-dec-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        user-select: none;
      }
      .pt-dec-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.95rem;
        color: #F8FAFC;
      }
      html.light .pt-dec-title {
        color: #0F172A;
      }
      .pt-dec-icon {
        font-size: 1.2rem;
      }
      .pt-dec-sub {
        font-size: 0.8rem;
        color: #94A3B8;
        font-family: 'Plus Jakarta Sans', sans-serif;
      }
      .pt-dec-meta {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .pt-dec-status-badge {
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 800;
      }
      .pt-dec-status-badge.badge-v {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.35);
      }
      .pt-dec-status-badge.badge-f {
        background: rgba(244, 63, 94, 0.15);
        color: #F43F5E;
        border: 1px solid rgba(244, 63, 94, 0.35);
      }
      .pt-dec-toggle-arrow {
        color: #94A3B8;
        font-size: 0.85rem;
        transition: transform 0.2s;
      }

      /* Grid of 3 Blocks */
      .pt-dec-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 14px;
      }
      @media (max-width: 768px) {
        .pt-dec-grid {
          grid-template-columns: 1fr;
        }
      }

      .pt-dec-cell {
        border-radius: 12px;
        padding: 10px 12px;
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      .pt-dec-cell.cell-ctx {
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
      }
      html.light .pt-dec-cell.cell-ctx {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
      }
      .pt-dec-cell.cell-obj {
        background: rgba(168, 85, 247, 0.08);
        border: 1px solid rgba(168, 85, 247, 0.25);
      }
      html.light .pt-dec-cell.cell-obj {
        background: #FAF5FF;
        border: 1px solid #E9D5FF;
      }
      .pt-dec-cell.cell-jdg {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.25);
      }
      html.light .pt-dec-cell.cell-jdg {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
      }

      .pt-dec-badge {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.78rem;
        font-weight: 800;
      }
      .cell-ctx .pt-dec-badge { color: #38BDF8; }
      html.light .cell-ctx .pt-dec-badge { color: #0284C7; }
      .cell-obj .pt-dec-badge { color: #C084FC; }
      html.light .cell-obj .pt-dec-badge { color: #7E22CE; }
      .cell-jdg .pt-dec-badge { color: #FBBF24; }
      html.light .cell-jdg .pt-dec-badge { color: #B45309; }

      .pt-dec-it {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 0.88rem;
        direction: ltr;
        text-align: left;
        line-height: 1.45;
        color: #F1F5F9;
      }
      html.light .pt-dec-it {
        color: #1E293B;
      }

      .pt-dec-ar {
        font-size: 0.82rem;
        color: #94A3B8;
        line-height: 1.4;
      }
      html.light .pt-dec-ar {
        color: #475569;
      }

      /* Formula Bar */
      .pt-dec-formula-bar {
        margin-top: 12px;
        border-radius: 12px;
        padding: 10px 14px;
        background: rgba(0, 0, 0, 0.35);
        border: 1px dashed rgba(255, 255, 255, 0.15);
      }
      html.light .pt-dec-formula-bar {
        background: #F8FAFC;
        border: 1px dashed rgba(15, 23, 42, 0.15);
      }
      .pt-dec-formula-bar.form-v {
        border-color: rgba(16, 185, 129, 0.4);
      }
      .pt-dec-formula-bar.form-f {
        border-color: rgba(244, 63, 94, 0.4);
      }

      .pt-form-head {
        font-size: 0.82rem;
        font-weight: 800;
        margin-bottom: 6px;
        color: #94A3B8;
      }
      html.light .pt-form-head {
        color: #64748B;
      }

      .pt-form-math {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.84rem;
        line-height: 1.6;
      }
      .pt-f-part {
        padding: 2px 7px;
        border-radius: 6px;
        font-weight: 700;
      }
      .pt-f-part.f-c {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
      }
      html.light .pt-f-part.f-c {
        background: rgba(2, 132, 199, 0.12);
        color: #0284C7;
      }
      .pt-f-part.f-o {
        background: rgba(168, 85, 247, 0.15);
        color: #C084FC;
      }
      html.light .pt-f-part.f-o {
        background: rgba(126, 34, 206, 0.12);
        color: #7E22CE;
      }
      .pt-f-part.f-j {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
      }
      html.light .pt-f-part.f-j {
        background: rgba(180, 83, 9, 0.12);
        color: #B45309;
      }
      .pt-f-plus, .pt-f-arrow, .pt-f-eq {
        color: #94A3B8;
        font-weight: 800;
      }
      .pt-f-res {
        font-weight: 900;
        padding: 2px 8px;
        border-radius: 6px;
      }
      .pt-f-res.res-v {
        background: #10B981;
        color: #FFFFFF;
      }
      .pt-f-res.res-f {
        background: #F43F5E;
        color: #FFFFFF;
      }

      /* Mini formula bar */
      .pt-dec-mini-formula {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 5px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        padding: 6px 10px;
        border-radius: 8px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin: 6px 0;
      }
      html.light .pt-dec-mini-formula {
        background: #F1F5F9;
        border: 1px solid rgba(15, 23, 42, 0.08);
      }
    `;

    const styleEl = document.createElement("style");
    styleEl.id = "patente-decoder-styles";
    styleEl.textContent = css;
    document.head.appendChild(styleEl);
  }
}

// Global instance
if (typeof window !== "undefined") {
  window.PatenteQuestionDecoder = PatenteQuestionDecoder;
  window.questionDecoder = new PatenteQuestionDecoder();
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = { PatenteQuestionDecoder };
}

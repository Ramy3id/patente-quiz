/**
 * =======================================================================
 * Patente B Pro - Trap Vault & Keyword Highlighter Engine
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محرك بنك الفخاخ وتمييز الكلمات الخادعة:
 *  - استخراج وتصفية الأسئلة ذات الفخاخ اللغوية
 *  - تمييز وإبراز الكلمات المخادعة (Pink Glow Highlight)
 *  - قوائم الكلمات المفتاحية الأكثر خداعاً في امتحانات الموتريزاتسيوني
 */

class PatenteTrapEngine {
  constructor() {
    // الكلمات المفتاحية الشهيرة في فخاخ الامتحان الإيطالي
    this.trapKeywords = [
      { it: "\\bsempre\\b", label: "دائماً (فخ إطلاق)", severity: "high" },
      { it: "\\bmai\\b", label: "أبداً (فخ نفي قاطع)", severity: "high" },
      { it: "\\bsolo\\b", label: "فقط (فخ حصر)", severity: "high" },
      { it: "\\bsoltanto\\b", label: "فحسب (فخ حصر)", severity: "high" },
      { it: "\\besclusivamente\\b", label: "حصراً", severity: "high" },
      { it: "\\bin ogni caso\\b", label: "في كل الأحوال", severity: "high" },
      { it: "\\bqualunque\\b", label: "أيّاً كان", severity: "med" },
      { it: "\\bobbligatoriamente\\b", label: "إلزامياً", severity: "med" },
      { it: "\\banche in\\b", label: "حتى في...", severity: "med" },
      { it: "\\bnon è mai\\b", label: "ليس أبداً", severity: "high" },
      { it: "\\bvietato in ogni\\b", label: "ممنوع في كل...", severity: "high" }
    ];
  }

  /**
   * فلترة الأسئلة التي تحتوي على فخاخ مؤكدة
   * @param {Array} questions
   */
  filterTraps(questions) {
    if (!Array.isArray(questions)) return [];
    return questions.filter((q) => {
      const tb = (q.trabocchetto || "").trim();
      const hasExplicitTrap = tb.length > 5 && !tb.includes("NO TRAP") && !tb.includes("لا يوجد فخ");
      
      // فحص وجود كلمات مفتاحية مفخخة
      const text = q.domanda || "";
      const hasKeyword = this.trapKeywords.some((k) => new RegExp(k.it, "i").test(text));

      return hasExplicitTrap || hasKeyword;
    });
  }

  /**
   * تمييز الكلمات المخادعة داخل نص السؤال الإيطالي عبر HTML Wrappers
   * @param {string} text النص الإيطالي للسؤال
   * @returns {string} النص بعد إحاطة الكلمات بـ span زجاجي وردي مضيء
   */
  highlightTrapWords(text) {
    if (!text) return "";
    let highlighted = text;

    this.trapKeywords.forEach((kw) => {
      const regex = new RegExp(`(${kw.it})`, "gi");
      highlighted = highlighted.replace(
        regex,
        `<mark class="trap-keyword-highlight" title="${kw.label}">$1</mark>`
      );
    });

    return highlighted;
  }

  /**
   * استخراج ملخص الفخ وتحليله بصرياً
   * @param {Object} question
   */
  analyzeTrap(question) {
    const text = question.domanda || "";
    const detectedWords = [];

    this.trapKeywords.forEach((kw) => {
      if (new RegExp(kw.it, "i").test(text)) {
        detectedWords.push(kw.label);
      }
    });

    return {
      hasTrap: detectedWords.length > 0 || Boolean(question.trabocchetto),
      detectedWords,
      trabocchettoText: question.trabocchetto || "انتبه للصيغة اللغوية الدقيقة للسؤال.",
      verdict: question.risposta ? "VERO" : "FALSO"
    };
  }
}

// تصدير المحرك
if (typeof window !== "undefined") {
  window.PatenteTrapEngine = PatenteTrapEngine;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PatenteTrapEngine;
}

/**
 * =======================================================================
 * Patente B Pro - Interactive Vehicle Anatomy Explorer (تشريح المركبة)
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description مستكشف تشريح وميكانيكا السيارة التفاعلي (للأبواب 18 و 25):
 *  - رسم هيكلي للسيارة بـ SVG يبرز نقاط التفاعل الهندسية والميكانيكية
 *  - نقاط لمس تفاعلية (Interactive Hotspots):
 *    (الفرامل والمكابح، الإطارات وضغط الهواء، زيت المحرك، سائل التبريد، الأضواء وعواكس النور)
 *  - عند النقر على أي مكون: يعرض الاسم الإيطالي، الوظيفة، وأسئلة وفخاخ الامتحان المتعلقة به
 */

class PatenteVehicleAnatomy {
  constructor(containerElement, options = {}) {
    this.container = typeof containerElement === "string"
      ? document.querySelector(containerElement)
      : containerElement;

    this.parts = [
      {
        id: "freni",
        nameIt: "Impianto Frenante (نظام الفرامل)",
        x: 290,
        y: 110,
        category: "sicurezza",
        desc: "نظام الفرامل الهيدروليكي المزدوج (Freno di servizio) وفرامل اليد (Freno di stazionamento).",
        quizTraps: "⚠️ فخ الامتحان: فرامل الخدمة تعمل بدواسة وتؤثر على جميع العجلات الأربع، بينما فرامل اليد تؤثر غالباً على العجلات الخلفية فقط.",
        article: "Art. 72 Codice della Strada"
      },
      {
        id: "pneumatici",
        nameIt: "Pneumatici e Battistrada (الإطارات ومداس العجلة)",
        x: 310,
        y: 180,
        category: "manutenzione",
        desc: "عمق مداس الإطار القانوني للسيارات يجب ألا يقل عن 1.6 مم، وضغط الهواء يُفحص على البارد.",
        quizTraps: "⚠️ فخ الامتحان: ضغط الهواء الزائد أو الناقص يؤدي لتآكل غير منتظم، وفحص الضغط يجب أن يكون عندما تكون الإطارات باردة (a freddo).",
        article: "Art. 79 Codice della Strada"
      },
      {
        id: "olio",
        nameIt: "Olio Motore e Lubrificazione (زيت المحرك والتشحيم)",
        x: 120,
        y: 90,
        category: "motore",
        desc: "فحص مستوى الزيت بواسطة مقياس الزيت (Asta graduata) على أرض مستوية والمحرك مطفأ وبارد.",
        quizTraps: "⚠️ فخ الامتحان: إضاءة لمبة الزيت الحمراء تعني انخفاض ضغط الزيت (Pressione insufficiente) وتتطلب الإيقاف الفوري للمحرك.",
        article: "Art. 161 Codice della Strada"
      },
      {
        id: "radiatore",
        nameIt: "Liquido di Raffreddamento (سائل التبريد)",
        x: 90,
        y: 120,
        category: "motore",
        desc: "دورة تبريد المحرك بالماء المضاف إليه مضاد التجمد (Antigelo) لمنع الغليان والتجمد.",
        quizTraps: "⚠️ فخ الامتحان: لا يجوز أبداً فتح غطاء قربة سائل التبريد والمحرك ساخن لتفادي خروج بخار حارق بضغط عالٍ.",
        article: "Elementi del veicolo"
      },
      {
        id: "luci",
        nameIt: "Dispositivi di Illuminazione (أنظمة الإضاءة)",
        x: 60,
        y: 100,
        category: "luci",
        desc: "أضواء الموضع (Posizione)، التقاطع (Anabbaglianti)، والإبهار (Abbaglianti) وضبط زاوية الإضاءة.",
        quizTraps: "⚠️ فخ الامتحان: أضواء التقاطع إجبارية خارج المدن نهاراً، ويحظر استخدام الأضواء العالية المبهرة داخل المناطق السكنية المضاءة.",
        article: "Art. 152 & 153 CdS"
      }
    ];

    this.selectedPart = this.parts[0];
    this.render();
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="anatomy-explorer-wrapper">
        <div class="anatomy-header">
          <div class="anatomy-title">🔧 التشريح التفاعلي للمركبة وأجزاء الميكانيكا</div>
          <div class="anatomy-subtitle">انقر على النقاط المضيئة بالسيارة لاستكشاف المكون وأهم فخاخ الامتحان</div>
        </div>

        <div class="anatomy-body">
          <div class="anatomy-diagram-view">
            <svg viewBox="0 0 400 240" class="car-anatomy-svg" id="carSvg">
              <!-- مجسم السيارة الزجاجي التجريدي -->
              <path d="M 50 140 L 90 90 L 150 80 L 250 80 L 320 100 L 360 140 L 370 170 L 40 170 Z" fill="#1E293B" stroke="#38BDF8" stroke-width="3" opacity="0.9" />
              <path d="M 100 90 L 150 85 L 240 85 L 290 105 L 100 105 Z" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5" />
              
              <!-- العجلات -->
              <circle cx="100" cy="175" r="28" fill="#0F172A" stroke="#94A3B8" stroke-width="6" />
              <circle cx="310" cy="175" r="28" fill="#0F172A" stroke="#94A3B8" stroke-width="6" />
              <circle cx="100" cy="175" r="10" fill="#38BDF8" />
              <circle cx="310" cy="175" r="10" fill="#38BDF8" />

              <!-- النقاط التفاعلية المضيئة (Hotspots) -->
              ${this.parts.map((p) => `
                <g class="hotspot-group" data-id="${p.id}" id="hotspot_${p.id}" style="cursor: pointer;">
                  <circle cx="${p.x}" cy="${p.y}" r="14" fill="rgba(56, 189, 248, 0.3)" class="hotspot-pulse" />
                  <circle cx="${p.x}" cy="${p.y}" r="8" fill="#38BDF8" stroke="#FFFFFF" stroke-width="2" class="hotspot-core" />
                  <text x="${p.x}" y="${p.y + 4}" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">⚡</text>
                </g>
              `).join("")}
            </svg>
          </div>

          <!-- لوحة التفاصيل والمعلومات الفورية -->
          <div class="anatomy-info-panel" id="anatomyInfoPanel">
            ${this.renderPartDetails(this.selectedPart)}
          </div>
        </div>
      </div>
    `;

    this.bindEvents();
  }

  renderPartDetails(part) {
    return `
      <div class="part-details-box">
        <div class="part-name-it">${part.nameIt}</div>
        <div class="part-article-tag">📜 ${part.article}</div>
        <div class="part-desc-ar">${part.desc}</div>
        <div class="part-trap-card">
          <div class="trap-card-label">🚨 فخ الموتريزاتسيوني في هذا الجزء:</div>
          <div class="trap-card-text">${part.quizTraps}</div>
        </div>
      </div>
    `;
  }

  bindEvents() {
    this.parts.forEach((p) => {
      const el = this.container.querySelector(`#hotspot_${p.id}`);
      if (el) {
        el.addEventListener("click", () => {
          this.selectedPart = p;
          const panel = this.container.querySelector("#anatomyInfoPanel");
          if (panel) panel.innerHTML = this.renderPartDetails(p);

          // تمييز النقطة المختارة
          this.container.querySelectorAll(".hotspot-core").forEach((c) => c.setAttribute("fill", "#38BDF8"));
          const activeCore = el.querySelector(".hotspot-core");
          if (activeCore) activeCore.setAttribute("fill", "#F59E0B");
        });
      }
    });
  }
}

// تصدير المحرك
if (typeof window !== "undefined") {
  window.PatenteVehicleAnatomy = PatenteVehicleAnatomy;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PatenteVehicleAnatomy;
}

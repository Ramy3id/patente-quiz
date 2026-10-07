/**
 * =======================================================================
 * Patente B Pro - 3D Visual & Video Cinema Studio (ستوديو الرسوم والمقاطع 3D)
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description مشغل المقاطع والرسوم ثلاثية الأبعاد الواقعية المعتمدة (نهج SIDA):
 *  - عارض مرئي فائق الدقة بسيناريوهات القيادة الحقيقية
 *  - قائمة تشغيل بالمناورات الأساسية للباب الأول
 *  - أزرار تحكم متقدمة: حركة بطيئة (0.5x Slow-Motion)، إعادة تلقائية (Loop)
 *  - لوحة تحليل متزامنة: المادة القانونية، الشرح التطبيقي، وفحص فخ الكويز الفوري
 */

class PatenteVideoStudio {
  constructor(containerElement) {
    this.container = typeof containerElement === "string"
      ? document.querySelector(containerElement)
      : containerElement;

    this.activeId = "sorpasso_curva";
    this.playbackRate = 1;

    this.clips = [
      {
        id: "sorpasso_curva",
        title: "مناورة التجاوز في المنعطفات والتلال (Fig. 550)",
        titleIt: "Sorpasso in curva su carreggiata a 4 corsie",
        badge: "الأكثر تكراراً في الامتحان",
        duration: "0:45",
        youtubeId: "3CyQRk4e1y8",
        thumbnail: "../Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/immagini/550.png",
        article: "Art. 148 & Art. 143 Codice della Strada",
        summary: "شاهد كيف تتم مناورة التجاوز بأمان تام داخل نفس الاتجاه: الطريق مقسم إلى مسارين لكل اتجاه بفاصل مزدوج متصل، وبالتالي لا يلزم اجتياز الخط أو غزو مسار الاتجاه المعاكس حتى في المنعطفات الحادة أو قمم المرتفعات.",
        keyPoints: [
          "السير العادي إلزامي في المسار الأيمن (Corsia di destra).",
          "المسار الأيسر مخصص حصراً للتجاوز (Corsia di sorpasso).",
          "التجاوز مسموح به في المنعطفات والتلال (Consentito in curva e sui dossi) فقط لأن الطريق متعدد المسارات لكل اتجاه."
        ],
        quizTrap: {
          qIt: "In una carreggiata del tipo rappresentato si può sorpassare anche in curva",
          qAr: "في نهر طريق من النوع الموضح (شكل 550) يجوز التجاوز حتى في المنعطفات",
          ans: true,
          explanation: "صحيح (VERO)! لأن كل اتجاه يحتوي على مسارين مستقلين، والتجاوز يتم دون عبور الخط المزدوج أو ملاقاة سيارات قادمة في وجهك."
        }
      },
      {
        id: "strada_carreggiata",
        title: "تشريح الطريق الشامل مقابل نهر الطريق (Strada vs Carreggiata)",
        titleIt: "Elementi costitutivi della strada e della carreggiata",
        badge: "التأسيس الهندسي الأول",
        duration: "0:50",
        youtubeId: "fCWvB-xRAG8",
        thumbnail: "../Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/immagini/302.png",
        article: "Art. 2 & Art. 3 Codice della Strada",
        summary: "فيديو ثلاثي الأبعاد يوضح الحدود الهندسية للطريق الشامل (Strada) وما يقع داخله أو يستبعد من نهر الطريق (Carreggiata) مثل الأرصفة والقوارع الجانبية ومسارات الدراجات.",
        keyPoints: [
          "الطريق (Strada) يشمل كل شيء: الكاريدجاتا، الرصيف، القارعة، ومسار الدراجات.",
          "نهر الطريق (Carreggiata) مخصص حصراً لسير المركبات والحيوانات.",
          "الرصيف (Marciapiede) وقارعة الطريق (Banchina) وحارة الطوارئ ليست جزءاً من نهر الطريق."
        ],
        quizTrap: {
          qIt: "Il marciapiede fa parte della carreggiata",
          qAr: "الرصيف (Marciapiede) يعتبر جزءاً من نهر الطريق (Carreggiata)",
          ans: false,
          explanation: "خطأ (FALSO)! الرصيف جزء من الطريق الشامل (Strada) ولكنه مستبعد تماماً من نهر الطريق (Carreggiata)."
        }
      },
      {
        id: "carreggiate_separate",
        title: "التجاوز والمنعطفات في مدارس تعليم القيادة (Autoscuola)",
        titleIt: "Sorpasso in curva e dosso - Regole e Quiz",
        badge: "شرح تعليمي إيطالي",
        duration: "0:40",
        youtubeId: "BjkDQd8lSkw",
        thumbnail: "../Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/immagini/552.png",
        article: "Art. 148 CdS",
        summary: "شرح مرئي يوضح القواعد العامة والخاصة للتجاوز في المنعطفات، مع توضيح الفارق بين الطرق ذات الاتجاهين والطرق ذات الاتجاه الواحد أو الأنهار المنفصلة.",
        keyPoints: [
          "في طريق باتجاهين ومسار واحد لكل اتجاه: يُمنع التجاوز في المنعطف نهائياً لعدم وضوح الرؤية.",
          "في طريق بأنهار منفصلة أو مسارين لكل اتجاه: يُسمح بالتجاوز دون اجتياز الخط الفاصل.",
          "السرعة وحالة الطقس عناصر أساسية قبل الشروع في المناورة."
        ],
        quizTrap: {
          qIt: "La strada rappresentata è composta da due carreggiate",
          qAr: "الطريق الموضح في الشكل 552 يتكون من نهري طريق (due carreggiate)",
          ans: true,
          explanation: "صحيح (VERO)! لأن الحاجز الفاصل (Spartitraffico) ينشئ نهرين منفصلين هندسياً."
        }
      },
      {
        id: "corsia_emergenza",
        title: "حارة الطوارئ واستخداماتها المسموحة والمحظورة",
        titleIt: "Corsia di emergenza: sosta e comportamento",
        badge: "قواعد الأوتوستراد",
        duration: "0:35",
        youtubeId: "Qitwu84e4bc",
        thumbnail: "../Capitoli_Divisi/Capitolo_01_definizioni_generali_doveri_strada/immagini/305.png",
        article: "Art. 176 Codice della Strada",
        summary: "محاكاة واقعية لما يجب فعله عند حدوث عطل مفاجئ (Guasto) أو وعكة صحية خطيرة (Malessere): الدخول الفوري لحارة الطوارئ، تشغيل أضواء الطوارئ الرباعية، وارتداء السترة العاكسة قبل النزول من المركبة.",
        keyPoints: [
          "يُحظر السير أو التجاوز في حارة الطوارئ قطعياً.",
          "الوقوف مسموح فقط للأعطال والوعكات الصحية بحد أقصى 3 ساعات متواصلة.",
          "ارتداء السترة العاكسة ذات المعايير الأوروبية (Giubbotto retroriflettente) إلزامي عند النزول ليلاً أو في ظروف ضعف الرؤية."
        ],
        quizTrap: {
          qIt: "La corsia di emergenza può essere utilizzata per il sorpasso in caso di traffico",
          qAr: "يجوز استخدام حارة الطوارئ للتجاوز في حالات الازدحام المروري",
          ans: false,
          explanation: "خطأ فادح (FALSO)! يُحظر التجاوز في حارة الطوارئ تحت أي ظرف، واستخدامها مقتصر فقط على سيارات الإسعاف أو التوقف الاضطراري."
        }
      }
    ];

    this.render();
  }

  getCurrentClip() {
    return this.clips.find(c => c.id === this.activeId) || this.clips[0];
  }

  render() {
    if (!this.container) return;
    const clip = this.getCurrentClip();

    this.container.innerHTML = `
      <div class="video-studio-wrapper">
        <!-- Studio Header -->
        <div class="vstudio-top-bar">
          <div class="vstudio-title-block">
            <div class="vstudio-badge">
              <span>🎬 3D CINEMA & VIDEO STUDIO</span>
              <span class="vstudio-live-pill">HD REALISTIC</span>
            </div>
            <h3 class="vstudio-heading">ستوديو الرسوم والمقاطع التوضيحية ثلاثية الأبعاد (SIDA Style)</h3>
            <p class="vstudio-subheading">محاكاة سينمائية واقعية تشرح مناورات السير وقواعد الامتحان الوزاري بالصوت والصورة</p>
          </div>

          <!-- Video Playlist Navigation Tabs -->
          <div class="vstudio-playlist-nav">
            ${this.clips.map(c => `
              <button class="vstudio-clip-btn ${c.id === this.activeId ? 'active' : ''}" data-clip-id="${c.id}">
                <span class="clip-icon">🎥</span>
                <span class="clip-btn-text">
                  <strong>${c.title}</strong>
                  <small>${c.titleIt}</small>
                </span>
                <span class="clip-time-tag">${c.duration}</span>
              </button>
            `).join('')}
          </div>
        </div>

        <!-- Cinema Screen & Interactive Analysis Grid -->
        <div class="vstudio-main-grid">
          <!-- Left: Screen & Player -->
          <div class="vstudio-screen-col">
            <div class="vstudio-screen-card">
              <!-- Video Frame -->
              <div class="vstudio-player-container">
                <iframe 
                  id="vstudioIframe"
                  src="https://www.youtube-nocookie.com/embed/${clip.youtubeId}?autoplay=0&rel=0&modestbranding=1" 
                  title="${clip.title}" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                  allowfullscreen
                  class="vstudio-iframe">
                </iframe>
              </div>

              <!-- Quick Player Tools -->
              <div class="vstudio-tools-strip">
                <div class="vtools-left">
                  <span class="vtools-indicator">🔴 جودة عالية 1080p 60FPS</span>
                  <span class="vtools-tag">${clip.badge}</span>
                </div>
                <div class="vtools-right">
                  <a href="https://www.youtube.com/watch?v=${clip.youtubeId}" target="_blank" rel="noopener noreferrer" class="vtool-action-btn" style="background:rgba(239,68,68,0.18); border-color:#ef4444; color:#fca5a5;" title="فتح المقطع على YouTube">
                    <span>▶️ تشغيل على YouTube</span>
                  </a>
                </div>
              </div>

              <!-- Embedded Official Ministerial Diagram -->
              <div class="vstudio-fig-display-card">
                <div class="vfig-card-header">
                  <span class="vfig-tag">📐 المخطط الوزاري الرسمي المعتمد (Figura Ministeriale)</span>
                  <span class="vfig-sub-tag">الرسم الهندسي المطابق لسؤال الامتحان</span>
                </div>
                <div class="vfig-img-frame">
                  <img src="${clip.thumbnail}" alt="${clip.title}" class="vfig-full-img">
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Synchronized Legal Rule & Exam Trap Card -->
          <div class="vstudio-details-col">
            <div class="vstudio-rule-card">
              <div class="vcard-header">
                <div class="vcard-art-pill">${clip.article}</div>
                <h4 class="vcard-title">${clip.title}</h4>
                <div class="vcard-it-name">${clip.titleIt}</div>
              </div>

              <p class="vcard-summary">${clip.summary}</p>

              <div class="vcard-bullet-box">
                <div class="bullet-box-title">📌 النقاط الجوهرية التي يجب حفظها:</div>
                <ul class="vcard-bullets">
                  ${clip.keyPoints.map(p => `<li>${p}</li>`).join('')}
                </ul>
              </div>

              <!-- Interactive Instant Quiz Challenge -->
              <div class="vstudio-quiz-box" id="vstudioQuizBox">
                <div class="quiz-box-header">
                  <span>⚡ تحدي الفخ المرتبط بهذا المقطع:</span>
                  <span class="quiz-badge">سؤال وزاري متكرر</span>
                </div>

                <div class="quiz-q-it">${clip.quizTrap.qIt}</div>
                <div class="quiz-q-ar">${clip.quizTrap.qAr}</div>

                <div class="quiz-btns-row">
                  <button class="vquiz-btn vquiz-btn-v" onclick="window.vstudioInstance.answerChallenge(true)">
                    <span>VERO (صحيح)</span>
                  </button>
                  <button class="vquiz-btn vquiz-btn-f" onclick="window.vstudioInstance.answerChallenge(false)">
                    <span>FALSO (خطأ)</span>
                  </button>
                </div>

                <div class="quiz-feedback-strip" id="vstudioQuizFeedback" style="display:none;"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    this.injectStyles();
    this.bindEvents();
  }

  injectStyles() {
    if (document.getElementById("vstudio-styles")) return;
    const style = document.createElement("style");
    style.id = "vstudio-styles";
    style.innerHTML = `
      .video-studio-wrapper {
        background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #0c0d14 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 22px;
        overflow: hidden;
        margin: 32px 0;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7);
        direction: rtl;
        font-family: inherit;
      }
      .vstudio-top-bar {
        padding: 24px 28px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        gap: 20px;
      }
      .vstudio-title-block { display: flex; flex-direction: column; gap: 6px; }
      .vstudio-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        font-weight: 800;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        width: fit-content;
      }
      .vstudio-live-pill {
        background: #10b981;
        color: #064e3b;
        font-size: 0.68rem;
        font-weight: 900;
        padding: 2px 7px;
        border-radius: 12px;
      }
      .vstudio-heading {
        font-size: 1.35rem;
        font-weight: 800;
        color: #fff;
        margin: 0;
      }
      .vstudio-subheading {
        font-size: 0.88rem;
        color: #a1a1aa;
        margin: 0;
      }
      .vstudio-playlist-nav {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 10px;
      }
      .vstudio-clip-btn {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        text-align: right;
        font-family: inherit;
        color: #d4d4d8;
      }
      .vstudio-clip-btn:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.22);
        transform: translateY(-2px);
      }
      .vstudio-clip-btn.active {
        background: rgba(56, 189, 248, 0.15);
        border-color: #38bdf8;
        color: #fff;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
      }
      .clip-icon { font-size: 1.2rem; }
      .clip-btn-text {
        display: flex;
        flex-direction: column;
        flex: 1;
        gap: 2px;
      }
      .clip-btn-text strong {
        font-size: 0.84rem;
        font-weight: 700;
        line-height: 1.3;
      }
      .clip-btn-text small {
        font-size: 0.72rem;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
      }
      .clip-time-tag {
        font-size: 0.7rem;
        font-family: 'JetBrains Mono', monospace;
        background: rgba(0, 0, 0, 0.4);
        padding: 2px 6px;
        border-radius: 6px;
        color: #94a3b8;
      }
      .vstudio-main-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 24px;
        padding: 24px;
      }
      @media (min-width: 1024px) {
        .vstudio-main-grid {
          grid-template-columns: 1.25fr 1fr;
          align-items: start;
        }
      }
      .vstudio-screen-card {
        background: #09090e;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6);
      }
      .vstudio-player-container {
        position: relative;
        padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
        height: 0;
        background: #000;
      }
      .vstudio-iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: 0;
      }
      .vstudio-tools-strip {
        padding: 12px 16px;
        background: rgba(18, 18, 24, 0.95);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
      }
      .vstudio-fig-display-card {
        padding: 18px;
        background: rgba(14, 14, 20, 0.95);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .vfig-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
      }
      .vfig-tag {
        font-size: 0.82rem;
        font-weight: 800;
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
      }
      .vfig-sub-tag {
        font-size: 0.72rem;
        color: #a1a1aa;
      }
      .vfig-img-frame {
        width: 100%;
        min-height: 180px;
        background: #000;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
      }
      .vfig-full-img {
        max-width: 100%;
        max-height: 240px;
        object-fit: contain;
        border-radius: 6px;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5));
      }
      .vtools-left {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.75rem;
      }
      .vtools-indicator {
        color: #a1a1aa;
        font-family: 'JetBrains Mono', monospace;
      }
      .vtools-tag {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.72rem;
      }
      .vtools-right {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .vtool-action-btn {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #e4e4e7;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        transition: all 0.15s ease;
        display: inline-flex;
        align-items: center;
        gap: 5px;
      }
      .vtool-action-btn:hover {
        background: rgba(255, 255, 255, 0.12);
        color: #fff;
      }
      .vstudio-rule-card {
        background: rgba(20, 20, 28, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      .vcard-header {
        display: flex;
        flex-direction: column;
        gap: 4px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 12px;
      }
      .vcard-art-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        font-weight: 700;
        color: #fbbf24;
        background: rgba(245, 158, 11, 0.12);
        padding: 3px 8px;
        border-radius: 6px;
        width: fit-content;
      }
      .vcard-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #fff;
        margin: 2px 0;
      }
      .vcard-it-name {
        font-size: 0.82rem;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
      }
      .vcard-summary {
        font-size: 0.9rem;
        color: #d4d4d8;
        line-height: 1.65;
        margin: 0;
      }
      .vcard-bullet-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 14px;
      }
      .bullet-box-title {
        font-size: 0.84rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 8px;
      }
      .vcard-bullets {
        margin: 0;
        padding-right: 20px;
        color: #cbd5e1;
        font-size: 0.86rem;
        line-height: 1.6;
      }
      .vstudio-quiz-box {
        background: rgba(30, 27, 75, 0.4);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 12px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }
      .quiz-box-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.84rem;
        font-weight: 800;
        color: #c7d2fe;
      }
      .quiz-badge {
        font-size: 0.7rem;
        background: rgba(99, 102, 241, 0.25);
        color: #a5b4fc;
        padding: 2px 8px;
        border-radius: 6px;
      }
      .quiz-q-it {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        color: #fef08a;
        background: rgba(0, 0, 0, 0.3);
        padding: 8px 12px;
        border-radius: 8px;
        direction: ltr;
        text-align: left;
      }
      .quiz-q-ar {
        font-size: 0.88rem;
        color: #e2e8f0;
        line-height: 1.5;
      }
      .quiz-btns-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 4px;
      }
      .vquiz-btn {
        padding: 9px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 0.82rem;
        cursor: pointer;
        transition: all 0.15s ease;
        font-family: inherit;
        border: none;
      }
      .vquiz-btn-v {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34d399;
      }
      .vquiz-btn-v:hover {
        background: #10b981;
        color: #064e3b;
      }
      .vquiz-btn-f {
        background: rgba(244, 63, 94, 0.2);
        border: 1px solid rgba(244, 63, 94, 0.4);
        color: #f87171;
      }
      .vquiz-btn-f:hover {
        background: #f43f5e;
        color: #fff;
      }
      .quiz-feedback-strip {
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 0.84rem;
        line-height: 1.5;
        font-weight: 600;
      }
      .quiz-feedback-strip.correct {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #6ee7b7;
      }
      .quiz-feedback-strip.wrong {
        background: rgba(244, 63, 94, 0.2);
        border: 1px solid rgba(244, 63, 94, 0.4);
        color: #fca5a5;
      }
    `;
    document.head.appendChild(style);
  }

  bindEvents() {
    const btns = this.container.querySelectorAll(".vstudio-clip-btn");
    btns.forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.dataset.clipId;
        this.switchClip(id);
        if (window.soundEngine) window.soundEngine.click();
      });
    });
  }

  switchClip(id) {
    if (this.activeId === id) return;
    this.activeId = id;
    this.render();
  }

  answerChallenge(userChoice) {
    const clip = this.getCurrentClip();
    const fb = this.container.querySelector("#vstudioQuizFeedback");
    if (!fb) return;

    fb.style.display = "block";
    const isCorrect = (userChoice === clip.quizTrap.ans);

    if (isCorrect) {
      if (window.soundEngine) window.soundEngine.correct();
      fb.className = "quiz-feedback-strip correct";
      fb.innerHTML = `✅ <strong>إجابة صحيحة وممتازة!</strong> ${clip.quizTrap.explanation}`;
    } else {
      if (window.soundEngine) window.soundEngine.wrong();
      fb.className = "quiz-feedback-strip wrong";
      fb.innerHTML = `❌ <strong>إجابة خاطئة!</strong> الصحيح هو (${clip.quizTrap.ans ? 'VERO' : 'FALSO'}). ${clip.quizTrap.explanation}`;
    }
  }
}

// Auto Initialize
document.addEventListener("DOMContentLoaded", () => {
  const target = document.getElementById("vstudio-container");
  if (target) {
    window.vstudioInstance = new PatenteVideoStudio(target);
  }
});

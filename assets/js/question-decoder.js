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
    this.contextRegex = /^(In una carreggiata[^,;]*|Nell['’]incrocio[^,;]*|In un incrocio[^,;]*|Sulle strade extraurbane[^,;]*|Sulle strade urbane[^,;]*|Sulle strade[^,;]*|Sulla carreggiata[^,;]*|In autostrada[^,;]*|Lungo le autostrade[^,;]*|In caso di[^,;]*|In presenza del segnale[^,;]*|In presenza di[^,;]*|Il segnale raffigurato[^,;]*|Il segnale in figura[^,;]*|Il pannello integrativo[^,;]*|Alla guida di[^,;]*|Di notte[^,;]*|Fuori dei centri abitati[^,;]*|Fuori dai centri abitati[^,;]*|Nei centri abitati[^,;]*|Sui dossi[^,;]*|In curva[^,;]*|Nelle curve[^,;]*|Nelle gallerie[^,;]*|Durante la marcia[^,;]*|Prima di[^,;]*|Quando si[^,;]*|Se si[^,;]*|Su strade[^,;]*|Nei passaggi a livello[^,;]*|A un passaggio a livello[^,;]*|In corrispondenza di[^,;]*|Per svoltare[^,;]*|Giungendo all['’]incrocio[^,;]*|Viaggiando[^,;]*|Dopo aver[^,;]*|Durante il[^,;]*|Nel caso in cui[^,;]*|Con la patente[^,;]*|Nei centri abitati[^,;]*|Nelle strade[^,;]*)/i;

    // 2. Judgment Matchers (الحكم القانوني - ماذا يقرر القانون)
    this.judgmentRegex = /(non è consentit[oa]|non è permess[oa]|non è vietat[oa]|non è obbligatori[oa]|è consentit[oa]|è permess[oa]|è vietat[oa]|è obbligatori[oa]|è facoltativ[oa]|non si può|non si possono|si può|si possono|non si deve|non si devono|si deve|si devono|non bisogna|bisogna|non occorre|occorre|impone di|prescrive di|obbliga a|vieta di|consente di|permette di|autorizza a|aumenta|diminuisce|raddoppia|si riduce|deve accertarsi|deve assicurarsi|deve verificare|deve moderare|deve rallentare|deve fermarsi|è tenuto a|è tenuto ad|ha l['’]obbligo di|non ha l['’]obbligo di|ha la precedenza|deve dare la precedenza|passa per primo|passa per ultimo|passa dopo|è di \d+ km\/h|è di \d+|non può superare|non deve superare|deve essere utilizzato|non deve essere|è opportuno|non è opportuno|è consigliabile|non è consigliabile|comporta la sospensione|comporta la revoca|comporta la decurtazione|costituisce reato|è punito|non fa parte|fa parte|è destinato a|non è destinato a)/i;

    // Prefixes context dictionary (قواعد المسرح والظرف القياسية)
    this.contextPrefixes = [
      { it: "sulle autostrade", ar: "على الطرق السريعة (الأوتوستراد)" },
      { it: "in autostrada", ar: "على الطريق السريع (الأوتوستراد)" },
      { it: "lungo le autostrade", ar: "على امتداد الطرق السريعة" },
      { it: "sulle strade extraurbane principali", ar: "على الطرق الخارجية الرئيسية" },
      { it: "sulle strade extraurbane secondarie", ar: "على الطرق الخارجية الثانوية" },
      { it: "fuori dei centri abitati", ar: "خارج المناطق السكنية" },
      { it: "fuori dai centri abitati", ar: "خارج التجمعات العمرانية" },
      { it: "nei centri abitati", ar: "داخل المناطق السكنية" },
      { it: "sulle strade urbane", ar: "على الطرق الحضرية (داخل المدن)" },
      { it: "in una carreggiata", ar: "في نهر الطريق (Carreggiata)" },
      { it: "sulla carreggiata", ar: "فوق نهر الطريق" },
      { it: "in un incrocio", ar: "عند التقاطع المروري" },
      { it: "nell'incrocio", ar: "عند التقاطع المروري" },
      { it: "giungendo all'incrocio", ar: "عند الوصول والاقتراب من التقاطع" },
      { it: "in presenza del segnale", ar: "عند وجود الإشارة المرورية" },
      { it: "il segnale raffigurato", ar: "الإشارة المرورية الموضحة بالرسم" },
      { it: "il segnale in figura", ar: "الإشارة الموضحة بالرسم" },
      { it: "il pannello integrativo", ar: "اللوحة الإضافية الملحقة" },
      { it: "in caso di nebbia fitta", ar: "في حالة وجود ضباب كثيف" },
      { it: "in caso di pioggia", ar: "في حالة هطول الأمطار" },
      { it: "in caso di neve", ar: "في حالة تساقط الثلوج" },
      { it: "in caso di incidente", ar: "عند وقوع حادث مروري" },
      { it: "di notte", ar: "أثناء القيادة ليلاً" },
      { it: "sui dossi", ar: "عند المطبات أو قمم المرتفعات (Dossi)" },
      { it: "in curva", ar: "عند المنعطفات" },
      { it: "nelle curve", ar: "في المنعطفات" },
      { it: "nelle gallerie", ar: "داخل الأنفاق المرورية" },
      { it: "nei passaggi a livello", ar: "عند مزلقان السكة الحديد" },
      { it: "a un passaggio a livello", ar: "عند مزلقان السكة الحديد" },
      { it: "durante la marcia", ar: "أثناء حركة السير" },
      { it: "con la patente b", ar: "لحامل رخصة القيادة فئة B" },
      { it: "con la patente a", ar: "لحامل رخصة الدراجات النارية فئة A" },
      { it: "alla guida di", ar: "أثناء قيادة مركبة" },
      { it: "prima di svoltare", ar: "قبل الشروع في الانعطاف" },
      { it: "prima di iniziare", ar: "قبل البدء بالمناورة" },
      { it: "norma generale", ar: "قاعدة سير وسلامة مرورية عامة" }
    ];

    // Comprehensive Patente B Glossary (Sorted descending by length for accurate compound matching)
    this.termsList = [
      { it: "limite massimo di velocità", ar: "الحد الأقصى للسرعة" },
      { it: "limite di velocità", ar: "حد السرعة المقررة" },
      { it: "distanza di sicurezza", ar: "مسافة الأمان القانونية" },
      { it: "inversione di marcia", ar: "الدوران للخلف (U-turn)" },
      { it: "cinture di sicurezza", ar: "أحزمة الأمان" },
      { it: "sistemi di ritenuta per bambini", ar: "مقاعد وأنظمة تثبيت الأطفال" },
      { it: "seggiolino per bambini", ar: "مقعد الأطفال المعتمد" },
      { it: "proiettori anabbaglianti", ar: "الأضواء المنخفضة (الكوديك)" },
      { it: "proiettori abbaglianti", ar: "الأضواء العالية (الفار)" },
      { it: "luci di posizione", ar: "أضواء الموضع (الصالصية)" },
      { it: "luci della targa", ar: "إضاءة لوحة السيارة" },
      { it: "indicatori di direzione", ar: "إشارات الاتجاه (الفليشر)" },
      { it: "segnalazione luminosa di pericolo", ar: "أضواء الانتظار الرباعية (4 فرود)" },
      { it: "anabbaglianti", ar: "الأضواء المنخفضة" },
      { it: "abbaglianti", ar: "الأضواء العالية" },
      { it: "passo carrabile", ar: "ممر عبور المركبات (الجراج)" },
      { it: "attraversamento pedonale", ar: "معبر المشاة" },
      { it: "attraversamento ciclabile", ar: "معبر راكبي الدراجات" },
      { it: "pista ciclabile", ar: "مسار الدراجات الهوائية" },
      { it: "corsia riservata", ar: "مسار مخصص لمركبات النقل" },
      { it: "corsia di emergenza", ar: "مسار الطوارئ" },
      { it: "corsia di accelerazione", ar: "مسار التسارع للدخول" },
      { it: "corsia di decelerazione", ar: "مسار التباطؤ للخروج" },
      { it: "dare la precedenza", ar: "إعطاء الأسبقية والتوقف إن لزم" },
      { it: "ha la precedenza", ar: "له حق الأسبقية في المرور" },
      { it: "precedenza a destra", ar: "الأسبقية للقادم من اليمين" },
      { it: "strada a senso unico", ar: "طريق ذو اتجاه واحد" },
      { it: "doppio senso di circolazione", ar: "اتجاهان لحركة السير" },
      { it: "doppia striscia continua", ar: "خط طولي مزدوج متصل" },
      { it: "striscia discontinua", ar: "خط طولي متقطع" },
      { it: "striscia continua", ar: "خط طولي متصل" },
      { it: "zona a traffico limitato", ar: "منطقة محدودة المرور (ZTL)" },
      { it: "area pedonale", ar: "منطقة مخصصة للمشاة" },
      { it: "isola di traffico", ar: "جزيرة تنظيم حركة المرور" },
      { it: "salvagente", ar: "رصيف أمان المشاة" },
      { it: "freno di stazionamento", ar: "فرامل التوقف (فرامل اليد)" },
      { it: "freno di servizio", ar: "فرامل الخدمة الأساسية (دواسة الفرامل)" },
      { it: "bloccaggio delle ruote", ar: "انغلاق العجلات أثناء الفرملة" },
      { it: "sistema antibloccaggio abs", ar: "نظام منع انغلاق المكابح ABS" },
      { it: "servosterzo", ar: "مساعد التوجيه (الباور ستيرينغ)" },
      { it: "tasso alcolemico", ar: "نسبة الكحول في الدم" },
      { it: "esame dell'etilometro", ar: "فحص قياس نسبة الكحول (الإيثيلومتر)" },
      { it: "tempo di reazione", ar: "زمن رد فعل السائق" },
      { it: "spazio di frenatura", ar: "مسافة الفرملة المقطوعة" },
      { it: "spazio totale di arresto", ar: "مسافة التوقف الكلية" },
      { it: "stato di shock", ar: "حالة الصدمة العصبية والدورانية" },
      { it: "posizione laterale di sicurezza", ar: "وضعية الإفاقة الجانبية للمصاب (PLS)" },
      { it: "massaggio cardiaco", ar: "الإنعاش القلبي الرئوي (CPR)" },
      { it: "corpo estraneo nell'occhio", ar: "دخول جسم غريب في عين المصاب" },
      { it: "ustioni", ar: "حروق الجلد وإصابات النار" },
      { it: "emorragia", ar: "النزيف الدموي الخارجي" },
      { it: "frattura", ar: "كسور العظام وتثبيت الأطراف" },
      { it: "assicurazione obbligatoria rca", ar: "التأمين الإلزامي ضد الغير (RCA)" },
      { it: "risarcimento del danno", ar: "التعويض المالي عن الأضرار" },
      { it: "constatazione amichevole cid", ar: "نموذج المعاينة الودية للحادث (CID)" },
      { it: "fondo di garanzia per le vittime", ar: "صندوق تعويض ضحايا حوادث الطرق" },
      { it: "patente a punti", ar: "نظام رصيد نقاط رخصة القيادة" },
      { it: "sospensione della patente", ar: "تعليق وسحب رخصة القيادة مؤقتاً" },
      { it: "revoca della patente", ar: "إلغاء وسحب رخصة القيادة نهائياً" },
      { it: "revisione della patente", ar: "إعادة الفحص الطبي أو النظري للرخصة" },
      { it: "ritiro della patente", ar: "سحب الرخصة فورياً بواسطة الشرطة" },
      { it: "carta di circolazione", ar: "رخصة سير المركبة (الكارت)" },
      { it: "certificato di proprietà", ar: "شهادة ملكية المركبة (CdP)" },
      { it: "revisione periodica", ar: "الفحص الفني الدوري للمركبة (Collaudo)" },
      { it: "contrassegno assicurativo", ar: "ملصق شهادة التأمين" },
      { it: "pannello per carichi sporgenti", ar: "لوحة الحمولة البارزة للخلف" },
      { it: "triangolo mobile di pericolo", ar: "مثلث الخطر العاكس المتنقل" },
      { it: "giubbotto retroriflettente", ar: "سترة الأمان العاكسة للضوء" },
      { it: "casco protettivo", ar: "الخوذة الواقية المعتمدة" },
      { it: "visiera del casco", ar: "قناع وواقي الخوذة" },
      { it: "abbigliamento protettivo", ar: "الملابس الواقية المعتمدة لسائقي الدراجات" },
      { it: "guanti protettivi", ar: "قفازات الحماية المعتمدة" },
      { it: "pneumatici invernali", ar: "الإطارات الشتوية (M+S)" },
      { it: "catene da neve", ar: "سلاسل الثلوج المعدنية" },
      { it: "spessore del battistrada", ar: "عمق نقشة الإطار (1.6 مم كحد أدنى للسيارات)" },
      { it: "pressione di gonfiaggio", ar: "ضغط نفخ الإطارات" },
      { it: "aquaplaning", ar: "ظاهرة الانزلاق المائي (فقدان التماسك)" },
      { it: "veicolo che precede", ar: "المركبة التي تسير في الأمام" },
      { it: "veicolo che segue", ar: "المركبة القادمة من الخلف" },
      { it: "sorpasso a destra", ar: "مناورة التجاوز من جهة اليمين" },
      { it: "svolta a sinistra", ar: "مناورة الانعطاف نحو اليسار" },
      { it: "svolta a destra", ar: "مناورة الانعطاف نحو اليمين" },
      { it: "cambio di corsia", ar: "مناورة الانتقال وتغيير المسار" },
      { it: "marcia per file parallele", ar: "السير في خطوط متوازية عند الازدحام" },
      { it: "marcia indietro", ar: "السير والتحرك إلى الخلف" },
      { it: "traino di un veicolo", ar: "عملية قطر أو سحب سيارة معطلة" },
      { it: "marmitta catalitica", ar: "المحول الحفاز وتقليل العادم (Catalizzatore)" },
      { it: "filtro antiparticolato", ar: "مرشح جسيمات الديزل (FAP)" },
      { it: "monossido di carbonio", ar: "غاز أول أكسيد الكربون السام (عديم الرائحة)" },
      { it: "inquinamento atmosferico", ar: "تلوث الهواء وانبعاثات العادم" },
      { it: "inquinamento acustico", ar: "التلوث الضوضائي واستخدام المنبه الصوتي" },
      { it: "consumo di carburante", ar: "معدل استهلاك الوقود" },
      { it: "resistenza dell'aria", ar: "مقاومة الهواء والديناميكا الهوائية" },
      { it: "portapacchi", ar: "شبكة وحامل الأمتعة فوق السقف" },
      { it: "carico sporgente", ar: "الحمولة البارزة خارج أبعاد السيارة" },
      { it: "massa complessiva", ar: "الكتلة الإجمالية للمركبة بحمولتها" },
      { it: "rimorchio leggero", ar: "المقطورة الخفيفة (حتى 750 كجم)" },
      { it: "freno ad inerzia", ar: "مكابح القصور الذاتي للمقطورات" },
      { it: "contemporaneamente", ar: "المرور في نفس الوقت معاً" },
      { it: "prima di impegnare", ar: "قبل احتلال والدخول إلى مفترق الطرق" },
      { it: "lasciare libero l'incrocio", ar: "ترك التقاطع خالياً وعدم إغلاقه" },
      { it: "dare la precedenza ai veicoli", ar: "إعطاء حق الأسبقية للمركبات الأخرى" },
      { it: "veicolo sosta", ar: "ركن وانتظار المركبة" },
      { it: "veicolo fermata", ar: "التوقف المؤقت لإنزال أو ركوب شخص" },
      { it: "strada extraurbana", ar: "الطريق الواقع خارج المدن" },
      { it: "strada urbana", ar: "الطريق داخل التجمعات السكنية" },
      { it: "veicolo a motore", ar: "المركبة ذات المحرك الآلي" },
      { it: "autovettura", ar: "سيارة الركوب الخاصة (الملاكي)" },
      { it: "autocarro", ar: "شاحنة نقل البضائع" },
      { it: "motociclo", ar: "الدراجة النارية (سعة تفوق 50 سم مكعب)" },
      { it: "ciclomotore", ar: "السكوتر والدراجة الآلية الخفيفة (حتى 50 سم مكعب)" },
      { it: "quadriciclo leggero", ar: "المركبة الخفيفة رباعية العجلات (Minicar)" },
      { it: "macchina agricola", ar: "الآلية الزراعية (الجرار)" },
      { it: "macchina operatrice", ar: "معدات الأشغال وآليات البناء" },
      { it: "utente debole della strada", ar: "مستخدم الطريق الضعيف (مشاة، دراجات، معاقين)" },
      { it: "pedone", ar: "المشاة الذين يعبرون الطريق" },
      { it: "ciclista", ar: "راكب الدراجة الهوائية" }
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
   * تفكيك أي سؤال وزاري إلى 3 كتل دقيقة ومعادلة رياضية منطقية
   */
  decode(qObj) {
    if (!qObj) return null;

    const rawIt = (qObj.q || qObj.domanda || "").trim();
    let rawAr = (qObj.tr || qObj.traduzione || "").trim();

    // استبعاد الاستامبات القديمة المعيبة إذا وجدت في الكائن
    if (rawAr.includes("سؤال يتناول موضوع") || rawAr.includes("بخصوص:")) {
      rawAr = "";
    }

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

    const b1Ar = this.extractContextArabic(b1It, rawAr);
    const b2Ar = this.extractSubjectArabic(b2It, rawAr);
    const b3Ar = this.extractJudgmentArabic(b3It, isTrue);

    const formulaText = `[📍 ${fCtx}] + [🎯 ${fObj}] ➔ [⚖️ ${fJdg}] = ${isTrue ? "✅ VERO (صح)" : "❌ FALSO (خطأ)"}`;

    return {
      rawAr: rawAr,
      rawIt: rawIt,
      b1: {
        titleAr: "المسرح والظرف",
        titleIt: "Il Contesto",
        icon: "📍",
        it: b1It,
        ar: b1Ar
      },
      b2: {
        titleAr: "الموضوع والمناورة",
        titleIt: "L'Oggetto",
        icon: "🎯",
        it: b2It,
        ar: b2Ar
      },
      b3: {
        titleAr: "الحكم القانوني",
        titleIt: "Il Giudizio",
        icon: "⚖️",
        it: b3It,
        ar: b3Ar
      },
      formula: {
        text: formulaText,
        ctx: fCtx,
        obj: fObj,
        jdg: fJdg,
        isTrue: isTrue
      },
      isTrue: isTrue,
      explanation: qObj.sp || qObj.spiegazione || qObj.r || "",
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
    const s = (itSnippet || "").toLowerCase();

    // 1. Check in context prefixes dictionary
    for (const item of this.contextPrefixes) {
      if (s.includes(item.it)) {
        return item.ar;
      }
    }

    // 2. Check in main terms glossary
    for (const item of this.termsList) {
      if (s.includes(item.it.toLowerCase())) {
        return item.ar;
      }
    }

    // 3. Extract opening contextual clause from authentic translation
    if (fullArabic) {
      const parts = fullArabic.split(/[,،؛]/);
      if (parts.length > 1 && parts[0].trim().length > 3) {
        return parts[0].trim();
      }
    }

    return "الظرف والسياق المروري المحدد";
  }

  extractSubjectArabic(itSnippet, fullArabic) {
    const s = (itSnippet || "").toLowerCase();

    // 1. Search against comprehensive terms glossary
    for (const item of this.termsList) {
      if (s.includes(item.it.toLowerCase())) {
        return item.ar;
      }
    }

    // 2. Fallback to smart clause extraction from fullArabic
    if (fullArabic) {
      const parts = fullArabic.split(/[,،؛]/);
      if (parts.length > 1) {
        // Return the main clause describing the maneuver or subject
        const mainPart = parts.slice(1).join("، ").trim();
        if (mainPart.length > 4 && mainPart.length < 80) {
          return mainPart;
        }
      }
      if (fullArabic.length < 80) {
        return fullArabic;
      }
    }

    return "المناورة أو المسألة القانونية المطروحة";
  }

  extractJudgmentArabic(itSnippet, isTrue) {
    const s = (itSnippet || "").toLowerCase();

    if (s.includes("vietat") || s.includes("non si può") || s.includes("non è consentit") || s.includes("non è permess") || s.includes("vieta di")) {
      return "🚫 محظور وممنوع قانوناً (Vietato)";
    }
    if (s.includes("obbligatori") || s.includes("si deve") || s.includes("si devono") || s.includes("impone") || s.includes("obbliga") || s.includes("deve accertarsi") || s.includes("ha l'obbligo")) {
      return "⚡ واجب وإلزامي قانوناً (Obbligatorio)";
    }
    if (s.includes("consentit") || s.includes("si può") || s.includes("si possono") || s.includes("permess") || s.includes("autorizza") || s.includes("permette")) {
      return "🟢 مسموح وجائز قانوناً (Consentito)";
    }
    if (s.includes("facoltativ")) {
      return "⚪ اختياري وغير إجباري (Facoltativo)";
    }
    if (s.includes("dare la precedenza")) {
      return "🛑 يلزم بإعطاء وتنازل عن حق الأسبقية";
    }
    if (s.includes("ha la precedenza")) {
      return "👑 يتمتع بحق الأسبقية في المرور";
    }
    if (s.includes("passa per primo")) {
      return "🥇 يمر أولاً في حركة التقاطع";
    }
    if (s.includes("passa per ultimo")) {
      return "⏳ يمر أخيراً بعد خلو مسار الجميع";
    }
    if (s.includes("passa dopo")) {
      return "↩️ يمر بعد عبور المركبة المعنية";
    }
    if (s.includes("aumenta")) {
      return "📈 يزداد ويرتفع";
    }
    if (s.includes("diminuisce") || s.includes("riduce")) {
      return "📉 ينخفض ويقل";
    }
    if (s.includes("raddoppia")) {
      return "✖️ يتضاعف إلى الضعف";
    }
    if (s.includes("comporta la sospensione")) {
      return "⛔ يترتب عليه سحب وتعليق الرخصة مؤقتاً";
    }
    if (s.includes("comporta la revoca")) {
      return "❌ يترتب عليه إلغاء وسحب الرخصة نهائياً";
    }
    if (s.includes("comporta la decurtazione")) {
      return "📉 يترتب عليه خصم نقاط من رصيد الرخصة";
    }
    if (s.includes("costituisce reato") || s.includes("punito con l'arresto")) {
      return "⚖️ يشكل جريمة جنائية يعاقب عليها القانون";
    }
    if (s.includes("è opportuno") || s.includes("è consigliabile")) {
      return "💡 إجراء مستحسن وموصى به لسلامة السير";
    }
    if (s.includes("non è opportuno") || s.includes("non è consigliabile")) {
      return "⚠️ إجراء غير مستحسن ومخاطرة غير مبررة";
    }
    if (s.includes("fa parte")) {
      return "✅ يُعد جزءاً لا يتجزأ من تكوين الطريق";
    }
    if (s.includes("non fa parte")) {
      return "❌ لا يُعد جزءاً من نهر الطريق";
    }

    return isTrue ? "✅ تصرف سليم ومطابق لقواعد كود السير" : "❌ ادعاء باطل ومخالف لقانون المرور";
  }

  /**
   * توليد بطاقة HTML متكاملة لتفكيك السؤال مع عرض الترجمة الأصيلة الكاملة
   */
  renderDecoderCard(qObj, options = {}) {
    const dec = this.decode(qObj);
    if (!dec) return "";

    const isCollapsed = options.collapsed || false;
    const cardId = "decCard_" + Math.random().toString(36).substring(2, 9);
    const hasFullArabic = Boolean(dec.rawAr && dec.rawAr.length > 2);

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
          <!-- شريط الترجمة السياقية الكاملة للسؤال -->
          ${hasFullArabic ? `
            <div class="pt-dec-full-trans">
              <div class="pt-dec-trans-label">
                <span class="pt-dec-trans-icon">📖</span>
                <span>الترجمة السياقية المعتمدة للسؤال:</span>
              </div>
              <div class="pt-dec-trans-body">${this.escapeHtml(dec.rawAr)}</div>
            </div>
          ` : ''}

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

          <!-- الشرح والفخ إن توفرا في الكائن -->
          ${dec.explanation ? `
            <div class="pt-dec-expl-box">
              <span class="pt-expl-icon">💡</span>
              <div class="pt-expl-body">
                <strong>التحليل البيداغوجي:</strong> ${this.escapeHtml(dec.explanation)}
              </div>
            </div>
          ` : ''}

          ${dec.trap ? `
            <div class="pt-dec-trap-box">
              <span class="pt-trap-icon">⚠️</span>
              <div class="pt-trap-body">
                <strong>فخ الامتحان:</strong> ${this.escapeHtml(dec.trap)}
              </div>
            </div>
          ` : ''}
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
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  injectStyles() {
    if (typeof document === "undefined") return;
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

      /* Full Question Translation Banner */
      .pt-dec-full-trans {
        margin-top: 12px;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 10px 14px;
      }
      html.light .pt-dec-full-trans {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
      }
      .pt-dec-trans-label {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.78rem;
        font-weight: 800;
        color: #38BDF8;
        margin-bottom: 4px;
      }
      html.light .pt-dec-trans-label {
        color: #0284C7;
      }
      .pt-dec-trans-body {
        font-size: 0.95rem;
        font-weight: 700;
        line-height: 1.55;
        color: #F8FAFC;
        direction: rtl;
        text-align: right;
      }
      html.light .pt-dec-trans-body {
        color: #0F172A;
      }

      /* Grid of 3 Blocks */
      .pt-dec-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 12px;
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
        font-size: 0.86rem;
        font-weight: 600;
        color: #CBD5E1;
        line-height: 1.45;
        direction: rtl;
        text-align: right;
      }
      html.light .pt-dec-ar {
        color: #334155;
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

      /* Explanation and Trap boxes */
      .pt-dec-expl-box {
        margin-top: 10px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 9px 12px;
        display: flex;
        gap: 8px;
        font-size: 0.85rem;
        line-height: 1.5;
        color: #E2E8F0;
      }
      html.light .pt-dec-expl-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        color: #334155;
      }
      .pt-dec-trap-box {
        margin-top: 8px;
        background: rgba(244, 63, 94, 0.08);
        border: 1px solid rgba(244, 63, 94, 0.25);
        border-radius: 12px;
        padding: 9px 12px;
        display: flex;
        gap: 8px;
        font-size: 0.85rem;
        line-height: 1.5;
        color: #FDA4AF;
      }
      html.light .pt-dec-trap-box {
        background: #FFF1F2;
        border: 1px solid #FECDD3;
        color: #BE123C;
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

/**
 * =======================================================================
 * Patente B Pro - Unified Navigation, Header, Footer & Search Suite (2026)
 * =======================================================================
 * @author Eng. Ramy Eid Saad Fahmy & Architecture Team
 * @description
 * - الهيدر الموحد الفاخر (10/10 Portal Header):
 *   1. تجميع الروابط الـ 12 في 4 تصنيفات رئيسية ذكية منسدلة (Mega Dropdowns):
 *      📖 المناهج | 🔬 المعامل الذكية | 🎮 التدريب والامتحانات | 📊 لوحة الإنجاز
 *   2. قائمة سريعة متطورة لتصفح الأبواب الـ 25 (تصفح الأبواب ▾) مع فلترة فورية وروابط أسئلة وشروحات.
 *   3. شارة الإنجاز العامة في زاوية الهيدر والموبايل مع حساب دقيق من 7,139 سؤالاً.
 *   4. نافذة البحث السريع الفوري بالمصطلحات (Quick Search Modal [Ctrl + K]).
 * - قائمة الموبايل الاحترافية (Categorized Mobile Drawer with Progress Banner).
 * - الفوتر الموحد (Developer Signature Footer).
 * - التوافقية والأمان: SafeStorage، High-Contrast Apple HIG (Dark/Light).
 */

(function () {
  'use strict';

  // 1. ==================== أمان البيانات وحماية المدخلات ====================
  const sanitizeStr = function (str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  };
  window.safeHtml = window.safeHtml || sanitizeStr;
  window.escapeHtml = window.escapeHtml || sanitizeStr;

  window.SafeStorage = {
    _mem: {},
    get: function (key, defVal) {
      if (defVal === undefined) defVal = null;
      try {
        const item = localStorage.getItem(key);
        if (item === null) return defVal;
        try {
          return JSON.parse(item);
        } catch (_) {
          return item;
        }
      } catch (err) {
        return this._mem[key] !== undefined ? this._mem[key] : defVal;
      }
    },
    set: function (key, val) {
      try {
        const strVal = typeof val === 'string' ? val : JSON.stringify(val);
        localStorage.setItem(key, strVal);
      } catch (err) {
        console.warn('[SafeStorage] Storage fallback to memory:', err);
        this._mem[key] = val;
      }
    },
    remove: function (key) {
      try {
        localStorage.removeItem(key);
      } catch (err) {
        delete this._mem[key];
      }
    }
  };

  // 2. ==================== تحديد مسارات الروابط تلقائياً ====================
  function getPathContext() {
    const rawPath = (window.location.pathname || '').replace(/\\/g, '/');
    const isFile = window.location.protocol === 'file:';

    // على الخوادم والاستضافة السحابية (Vercel / Localhost): نستخدم مسارات مطلقة آمنة 100% لمنع أي خطأ 404
    if (!isFile) {
      return {
        root: '/',
        interactive: '/interactive_pages/',
        capitoli: '/Capitoli_Divisi/',
        currentFile: rawPath.split('/').filter(Boolean).pop() || 'index.html',
        fullPath: rawPath
      };
    }

    const parts = rawPath.split('/').filter(Boolean);
    const currentFile = parts.length > 0 ? parts[parts.length - 1] : 'index.html';

    // داخل مجلد فرعي داخل Capitoli_Divisi
    if (/\/Capitoli_Divisi\/Capitolo_[^\/]+/i.test(rawPath)) {
      return {
        root: '../../',
        interactive: '../../interactive_pages/',
        capitoli: '../',
        currentFile: currentFile,
        fullPath: rawPath
      };
    }
    // في مجلد Capitoli_Divisi مباشرة
    if (/\/Capitoli_Divisi/i.test(rawPath)) {
      return {
        root: '../',
        interactive: '../interactive_pages/',
        capitoli: './',
        currentFile: currentFile,
        fullPath: rawPath
      };
    }
    // في مجلد interactive_pages
    if (/\/interactive_pages/i.test(rawPath)) {
      return {
        root: '../',
        interactive: './',
        capitoli: '../Capitoli_Divisi/',
        currentFile: currentFile,
        fullPath: rawPath
      };
    }
    // في المجلد الجذري (Root)
    return {
      root: './',
      interactive: './interactive_pages/',
      capitoli: './Capitoli_Divisi/',
      currentFile: currentFile,
      fullPath: rawPath
    };
  }

  // 3. ==================== بيانات الأبواب الـ 25 والأسئلة ====================
  const CHAPTERS_DATA = [
    { num: 1, questions: 215, title: 'المفاهيم العامة وواجبات الطريق', itTitle: 'Definizioni generali e doveri della strada', folder: 'Capitolo_01_definizioni_generali_doveri_strada', guide: 'دليل_الباب_01_المفاهيم_العامة_وواجبات_مستخدمي_الطريق.html', keywords: 'strada carreggiata corsia salvagente banchina marciapiede definizioni doveri' },
    { num: 2, questions: 412, title: 'إشارات الخطر', itTitle: 'Segnali di pericolo', folder: 'Capitolo_02_segnali_pericolo', guide: 'دليل_الباب_02_إشارات_الخطر.html', keywords: 'pericolo curve dossi cunette passaggio a livello discesa ponte mobile vento' },
    { num: 3, questions: 432, title: 'إشارات المنع', itTitle: 'Segnali di divieto', folder: 'Capitolo_03_segnali_divieto', guide: 'دليل_الباب_03_إشارات_المنع.html', keywords: 'divieto transito sosta senso vietato sorpasso distanza carico assi clacson' },
    { num: 4, questions: 279, title: 'إشارات الإلزام', itTitle: 'Segnali di obbligo', folder: 'Capitolo_04_segnali_obbligo', guide: 'دليل_الباب_04_إشارات_الإلزام.html', keywords: 'obbligo direzione consentita rotatoria catene neve velocita minima pedonale' },
    { num: 5, questions: 214, title: 'إشارات الأسبقية', itTitle: 'Segnali di precedenza', folder: 'Capitolo_05_segnali_precedenza', guide: 'دليل_الباب_05_إشارات_الأسبقية.html', keywords: 'precedenza dare precedenza stop dare via libera senso unico alternato' },
    { num: 6, questions: 379, title: 'العلامات الأرضية والمطبات', itTitle: 'Segnaletica orizzontale e ostacoli', folder: 'Capitolo_06_segnaletica_orizzontale_ostacoli', guide: 'دليل_الباب_06_العلامات_الأرضية_والإشارات_الأفقية.html', keywords: 'strisce continua discontinua zebrature corsie canalizzazione attraversamento pedonale' },
    { num: 7, questions: 265, title: 'إشارات المرور الضوئية والشرطي', itTitle: 'Semafori e segnali dei vigili', folder: 'Capitolo_07_semafori_vigili', guide: 'دليل_الباب_07_إشارات_المرور_الضوئية_ورجال_الشرطة.html', keywords: 'semafori luce rossa verde gialla corsie frecce vigile braccia fischietto' },
    { num: 8, questions: 387, title: 'إشارات الإرشاد والمعلومات والخدمات', itTitle: 'Segnali di indicazione e servizi', folder: 'Capitolo_08_segnali_indicazione', guide: 'دليل_الباب_08_إشارات_الإرشاد_والمعلومات.html', keywords: 'indicazione autostrada itinerario preavviso bivio localita sos pronto soccorso' },
    { num: 9, questions: 184, title: 'إشارات الورش والتحويلات المؤقتة', itTitle: 'Segnali complementari e cantiere', folder: 'Capitolo_09_segnali_complementari_cantiere', guide: 'دليل_الباب_09_الإشارات_التكميلية_وورش_العمل.html', keywords: 'cantiere stradale fondo giallo delineatori curve coni barriere deviazione' },
    { num: 10, questions: 221, title: 'اللوحات الإضافية الملحقة بالإشارات', itTitle: 'Pannelli integrativi', folder: 'Capitolo_10_pannelli_integrativi', guide: 'دليل_الباب_10_اللوحات_الإضافية_الملحقة_بالإشارات.html', keywords: 'pannelli integrativi distanza estesa orari validita rimozione ghiaccio andamento' },
    { num: 11, questions: 218, title: 'حدود السرعة ومخاطرها', itTitle: 'Limiti di velocità e pericoli', folder: 'Capitolo_11_limiti_di_velocita', guide: 'دليل_الباب_11_حدود_السرعة_ومخاطرها.html', keywords: 'velocita limiti 50 90 110 130 neopatentati sicurezza visibilita curve' },
    { num: 12, questions: 219, title: 'مسافة الأمان والعوامل المؤثرة', itTitle: 'Distanza di sicurezza', folder: 'Capitolo_12_distanza_di_sicurezza', guide: 'دليل_الباب_12_مسافة_الأمان_والعوامل_المؤثرة.html', keywords: 'distanza sicurezza spazio frenatura reazione arresto asfalto bagnato formula' },
    { num: 13, questions: 367, title: 'قواعد السير وتنظيم الحارات والمسارات', itTitle: 'Norme di circolazione e corsie', folder: 'Capitolo_13_norme_di_circolazione', guide: 'دليل_الباب_13_قواعد_السير_والمسارات.html', keywords: 'circolazione corsia marcia sorpasso svolta inversione cambio corsia' },
    { num: 14, questions: 278, title: 'أسبقية المرور وفك التقاطعات المعقدة', itTitle: 'Precedenza negli incroci', folder: 'Capitolo_14_precedenza_incroci', guide: 'دليل_الباب_14_أسبقية_المرور_وفك_التقاطعات.html', keywords: 'incroci precedenza destra ordine transito prima dopo impegno rotatoria' },
    { num: 15, questions: 265, title: 'مناورة التجاوز والتخطي', itTitle: 'Manovra di sorpasso', folder: 'Capitolo_15_sorpasso', guide: 'دليل_الباب_15_مناورة_التجاوز_والتخطي.html', keywords: 'sorpasso vietato sinistra destra curve dossi passaggi livello incroci' },
    { num: 16, questions: 308, title: 'الوقوف والتوقف والركن', itTitle: 'Fermata, sosta e arresto', folder: 'Capitolo_16_fermata_sosta_arresto', guide: 'دليل_الباب_16_الوقوف_والتوقف_والركن.html', keywords: 'fermata sosta arresto divieto passo carrabile disco orario marciapiede' },
    { num: 17, questions: 341, title: 'الأوتوستراد وسحب المقطورات والحمولة', itTitle: 'Autostrade, rimorchi e carico', folder: 'Capitolo_17_norme_varie_autostrade_pannelli', guide: 'دليل_الباب_17_الأوتوستراد_والحمولة_وسحب_المقطورات.html', keywords: 'autostrada extraurbana principale rimorchi traino carico sporgente pannello' },
    { num: 18, questions: 268, title: 'استخدام الأضواء ولمبات التابلوه', itTitle: 'Uso delle luci e spie cruscotto', folder: 'Capitolo_18_luci_dispositivi_acustici', guide: 'دليل_الباب_18_استخدام_الأضواء_ولمبات_التابلوه_والعواكس.html', keywords: 'luci anabbaglianti abbaglianti posizione frecce fendinebbia clacson spie' },
    { num: 19, questions: 265, title: 'أحزمة الأمان والخوذة ومقاعد الأطفال', itTitle: 'Cinture, casco e seggiolini', folder: 'Capitolo_19_cinture_casco_sicurezza', guide: 'دليل_الباب_19_أحزمة_الأمان_والخوذة_ومقاعد_الأطفال.html', keywords: 'cinture sicurezza airbag casco seggiolini bambini ritenuta esenzioni' },
    { num: 20, questions: 374, title: 'رخص القيادة والنقاط والعقوبات الرسمية', itTitle: 'Patenti di guida, punti e sanzioni', folder: 'Capitolo_20_patente_punti_documenti', guide: 'دليل_الباب_20_رخص_القيادة_والنقاط_والعقوبات.html', keywords: 'patente b b1 a a2 punti 20 revoca sospensione ritiro revisione' },
    { num: 21, questions: 302, title: 'حوادث السير وظروف الطقس الصعبة', itTitle: 'Incidenti stradali e maltempo', folder: 'Capitolo_21_incidenti_stradali_comportamenti', guide: 'دليل_الباب_21_حوادث_السير_وظروف_الطقس_الصعبة.html', keywords: 'incidenti pioggia aquaplaning neve ghiaccio nebbia triangolo gilet' },
    { num: 22, questions: 282, title: 'الكحول والمخدرات والإسعافات الأولية', itTitle: 'Alcool, droga e primo soccorso', folder: 'Capitolo_22_alcool_droga_primo_soccorso', guide: 'دليل_الباب_22_الكحول_والمخدرات_والإسعافات_الأولية.html', keywords: 'alcool droga tasso alcolemico soccorso ferito emorragia soffocamento shock' },
    { num: 23, questions: 263, title: 'المسؤولية المدنية والجنائية والتأمين RCA', itTitle: 'Responsabilità civile, penale e RCA', folder: 'Capitolo_23_responsabilita_civile_penale_e_assicurazione', guide: 'دليل_الباب_23_المسؤولية_والتأمين.html', keywords: 'responsabilita civile penale assicurazione rca cid constatazione amichevole' },
    { num: 24, questions: 233, title: 'استهلاك الوقود وحماية البيئة والتلوث', itTitle: 'Consumi ed inquinamento', folder: 'Capitolo_24_consumi_ambiente_inquinamento', guide: 'دليل_الباب_24_استهلاك_الوقود_وحماية_البيئة.html', keywords: 'consumi carburante inquinamento acustico atmosferico marmitta catalitica filtri' },
    { num: 25, questions: 400, title: 'الميكانيكا وصيانة المركبة وأجهزة الأمان', itTitle: 'Elementi del veicolo e manutenzione', folder: 'Capitolo_25_elementi_veicolo_manutenzione_comportamenti', guide: 'دليل_الباب_25_الميكانيكا_وصيانة_المركبة_وأجهزة_الأمان.html', keywords: 'freni abs pneumatici gomme olio motore radiatore sterzo sospensioni' }
  ];

  const TOTAL_QUESTIONS_COUNT = 7139;

  // 4. ==================== حساب التقدم العام والفردي ====================
  function getChapterProgress(capNum) {
    try {
      const raw = localStorage.getItem('patente_progress_cap_' + capNum);
      if (!raw) return { answered: 0, correct: 0, wrong: 0, pct: 0, completed: false };
      const parsed = JSON.parse(raw);
      const userAnswers = parsed.userAnswers || {};
      const answered = Object.keys(userAnswers).length;
      let c = 0, w = 0;
      Object.keys(userAnswers).forEach(k => {
        if (userAnswers[k] && userAnswers[k].isCorrect) c++;
        else if (userAnswers[k] && userAnswers[k].isCorrect === false) w++;
      });
      const chMeta = CHAPTERS_DATA.find(c => c.num === capNum);
      const totalQ = chMeta ? chMeta.questions : 200;
      const pct = Math.min(100, Math.round((answered / totalQ) * 100));
      return { answered, correct: c, wrong: w, pct, completed: pct >= 100 };
    } catch (_) {
      return { answered: 0, correct: 0, wrong: 0, pct: 0, completed: false };
    }
  }

  function getGlobalProgressStats() {
    let answered = 0;
    let correct = 0;
    try {
      for (let i = 1; i <= 25; i++) {
        const prog = getChapterProgress(i);
        answered += prog.answered;
        correct += prog.correct;
      }
    } catch (e) {
      console.warn('[GlobalProgress] calculation error', e);
    }
    const pct = Math.min(100, Math.round((answered / TOTAL_QUESTIONS_COUNT) * 100));
    return { answered, correct, total: TOTAL_QUESTIONS_COUNT, pct };
  }

  // 5. ==================== قاعدة بيانات البحث السريع الفوري ====================
  function buildSearchDatabase(ctx) {
    const items = [];

    // 1. الأبواب الـ 25
    CHAPTERS_DATA.forEach(ch => {
      const pad = ch.num < 10 ? '0' + ch.num : String(ch.num);
      items.push({
        type: 'chapter',
        category: 'chapters',
        categoryLabel: '📚 الأبواب الرسمية',
        title: `الباب ${pad}: ${ch.title}`,
        subtitle: `${ch.itTitle} (${ch.questions} سؤال)`,
        badge: `Cap. ${pad}`,
        hrefQuiz: `${ctx.capitoli}${ch.folder}/index.html`,
        hrefGuide: `${ctx.interactive}${ch.guide}`,
        href: `${ctx.capitoli}${ch.folder}/index.html`,
        tags: `${ch.num} ${pad} الباب ${ch.title} ${ch.itTitle} ${ch.keywords}`.toLowerCase()
      });
    });

    // 2. الأدوات والمعامل الـ 12
    const tools = [
      { id: 'mistakes', title: 'بنك أخطائي وتحدي التصحيح', it: 'Banca Errori e Correzione', desc: 'تجميع كافة أخطائك في كويز مخصص لإتقانها وتفادي الرسوب في الامتحان', icon: '⚠️', href: ctx.interactive + 'dashboard.html#mistakes', tags: 'اخطاء بنك اخطائي اسئلة خاطئة مراجعة تصحيح غلط غلطات errori sbagli srs' },
      { id: 'scheda', title: 'محاكي الامتحان الوزاري الرسمي', it: 'Scheda d’Esame Ministeriale', desc: '30 سؤال في 20 دقيقة بنظام الوزارة المحدث وتقييم النجاح', icon: '⏱️', href: ctx.interactive + 'scheda-esame.html', tags: 'محاكي امتحان تجريبي اختبار رسمي scheda esame timer وقت نتيجة' },
      { id: 'incroci', title: 'مفكك التقاطعات التفاعلي', it: 'Decodificatore Incroci', desc: 'تحليل أسبقية السير في الميادين وحساب مسار السيارات خطوة بخطوة', icon: '🔄', href: ctx.interactive + 'decodificatore-incroci.html', tags: 'تقاطعات مفكك اسبقية ميادين incroci precedenza rotatoria destra' },
      { id: 'parole', title: 'رادار الكلمات المفتاحية والفخاخ', it: 'Parole Spia e Trabocchetti', desc: 'كشف كلمات التأكيد (Sempre / Mai) وكلمات الخداع في أسئلة الباتنت', icon: '🎯', href: ctx.interactive + 'parole-spia.html', tags: 'رادار كلمات فخاخ مفتاحية sempre mai solo soltanto trabocchetti parole spia' },
      { id: 'numeri', title: 'معمل الأرقام وحساب المسافات', it: 'Laboratorio Numeri e Distanze', desc: 'حاسبة السرعات ومسافات الأمان وزمن رد الفعل وأبعاد المركبات', icon: '📏', href: ctx.interactive + 'laboratorio-numeri.html', tags: 'ارقام مسافات سرعة فرملة رد فعل مسافة الامان numeri distanza velocita' },
      { id: 'flashcards', title: 'الفلاش كاردز التفاعلية', it: 'Flashcards Segnali Stradali', desc: 'بطاقات بصرية ذكية لحفظ الإشارات ورموز الطريق وتكرارها', icon: '🗂️', href: ctx.interactive + 'flashcards.html', tags: 'فلاش كارد بطاقات اشارات حفظ مراجعة سريعة flashcards segnali' },
      { id: 'traps', title: 'بنك الفخاخ والألعاب التفاعلية', it: 'Banca Trappole e Sfide', desc: 'تحدي أصعب الأسئلة الوزارية وتدريبات التحدي الموقوتة', icon: '🎮', href: ctx.interactive + 'traps_and_games.html', tags: 'فخاخ العاب تحدي اسئلة صعبة traps games quiz' },
      { id: 'trucchi', title: 'خزينة التريكات وأسرار النجاح', it: 'Trucchi e Segreti d’Esame', desc: 'قواعد ذهبية واستراتيجيات استنتاج الإجابة الصحيحة بسرعة', icon: '💎', href: ctx.interactive + 'trucchi-esame.html', tags: 'تريكات حيل اسرار نصائح trucchi esame trucchi patente' },
      { id: 'soccorso', title: 'دليل الإسعافات الأولية والتصرف', it: 'Primo Soccorso Stradale', desc: 'خطوات الإنقاذ والتصرف السليم أثناء حوادث السير وإسعاف المصابين', icon: '🚑', href: ctx.interactive + 'primo-soccorso.html', tags: 'اسعافات اولية حوادث انقاذ صدمة تنفس primo soccorso ferito' },
      { id: 'piano', title: 'خطة الدراسة والجدول الزمني', it: 'Piano di Studio Personalizzato', desc: 'جدول زمني منظم لاجتياز اختبار الباتنت خلال 4 أو 8 أسابيع', icon: '📅', href: ctx.interactive + 'piano-studio.html', tags: 'خطة دراسة جدول برنامج زمني تنظيم وقت piano studio' },
      { id: 'dashboard', title: 'لوحة الإنجاز ومتابعة التقدم', it: 'Dashboard Statistiche Personali', desc: 'إحصائيات تفصيلية ونسبة الدقة ومؤشر الجاهزية لدخول الامتحان', icon: '📊', href: ctx.interactive + 'dashboard.html', tags: 'لوحة انجاز تقدم احصائيات نقاط dashboard statistiche progresso' },
      { id: 'hub', title: 'بنك أسئلة الأبواب الـ 25', it: 'Hub Capitoli Divisi (7,139 Domande)', desc: 'فهرس الوحدات التدريبية المباشرة لجميع أسئلة رخصة القيادة', icon: '📝', href: ctx.capitoli + 'index.html', tags: 'بنك اسئلة ابواب 7139 وحدة تدريب capitoli hub quiz' },
      { id: 'guide', title: 'شرح وأدلة الأبواب (1-25)', it: 'Guida Completa ai Capitoli', desc: 'الشرح الشامل باللغة العربية والرسوم التوضيحية لجميع الدروس', icon: '📖', href: ctx.interactive + 'index.html', tags: 'شرح ادلة دروس تلخيص كتاب guida spiegazione teoria' }
    ];

    tools.forEach(t => {
      items.push({
        type: 'tool',
        category: 'tools',
        categoryLabel: '🔬 المعامل والأدوات',
        title: t.title,
        subtitle: `${t.it} — ${t.desc}`,
        badge: t.icon,
        href: t.href,
        tags: `${t.title} ${t.it} ${t.desc} ${t.tags}`.toLowerCase()
      });
    });

    // 3. مصطلحات وفخاخ وقواعد هامة في الاختبار
    const glossary = [
      { it: 'Sempre', ar: 'دائماً', desc: 'غالباً خاطئة (Falso) في 90% من أسئلة الامتحانات باستثناء حالات محددة', href: ctx.interactive + 'parole-spia.html', tags: 'sempre دائما فخ كاذب falso' },
      { it: 'Mai', ar: 'أبداً / إطلاقاً', desc: 'غالباً خاطئة (Falso) في معظم الأسئلة الوزارية وتعد من أبرز كلمات الفخ', href: ctx.interactive + 'parole-spia.html', tags: 'mai ابدا اطلاقا فخ falso' },
      { it: 'Solo / Soltanto', ar: 'فقط / حصراً', desc: 'كلمة تقييد شديدة؛ تتطلب انتباهاً خاصاً وغالباً ما تكون إجابتها Falso', href: ctx.interactive + 'parole-spia.html', tags: 'solo soltanto فقط حصرا تقييد falso' },
      { it: 'Precedenza a destra', ar: 'أسبقية اليمين', desc: 'القاعدة العامة في التقاطعات ما لم توجد إشارة تنص على خلاف ذلك', href: ctx.interactive + 'decodificatore-incroci.html', tags: 'precedenza destra اسبقية اليمين تقاطع incrocio' },
      { it: 'Distanza di sicurezza', ar: 'مسافة الأمان', desc: 'المسافة الواجب تركها خلف المركبة التي أمامك لتفادي الاصطدام عند الفرملة', href: ctx.interactive + 'laboratorio-numeri.html', tags: 'distanza sicurezza مسافة الامان reazione frenatura' },
      { it: 'Tempo di reazione', ar: 'زمن رد الفعل', desc: 'يقدر بحوالي ثانية واحدة (1s)؛ تقطع فيه السيارة مسافة قبل بدء الفرملة', href: ctx.interactive + 'laboratorio-numeri.html', tags: 'tempo reazione زمن رد الفعل ثانية spazio reazione' },
      { it: 'Sorpasso vietato', ar: 'ممنوع التجاوز', desc: 'يمنع التجاوز في المنحنيات (Curve) والمرتفعات (Dossi) والتقاطعات غير المحمية', href: ctx.capitoli + 'Capitolo_15_sorpasso/index.html', tags: 'sorpasso vietato تجاوز ممنوع curve dossi' },
      { it: 'Fermata vs Sosta', ar: 'الفرق بين الوقوف المؤقت والركن', desc: 'الوقوف (Fermata) مؤقت والسائق جاهز للمغادرة، بينما الركن (Sosta) يترك فيه السائق السيارة', href: ctx.capitoli + 'Capitolo_16_fermata_sosta_arresto/index.html', tags: 'fermata sosta وقوف ركن marciapiede disco orario' },
      { it: 'Aquaplaning', ar: 'الانزلاق المائي', desc: 'فقدان تماسك الإطارات بسبب طبقة الماء على الطريق، وتزداد مع السرعة وتآكل المداس', href: ctx.capitoli + 'Capitolo_21_incidenti_stradali_comportamenti/index.html', tags: 'aquaplaning انزلاق مائي ماء مطر اطارات سرعة' },
      { it: 'Tasso alcolemico', ar: 'نسبة الكحول في الدم', desc: 'صفر (0.0 g/l) للجدد Neopatentati والمحترفين، و 0.5 g/l لعموم السائقين', href: ctx.capitoli + 'Capitolo_22_alcool_droga_primo_soccorso/index.html', tags: 'alcool tasso alcolemico كحول دم سكران neopatentati' },
      { it: 'Assicurazione RCA', ar: 'تأمين المسؤولية المدنية الإجباري', desc: 'يغطي الأضرار التي تلحقها مركبتك بالغير ولا يغطي أضرار السائق المتسبب', href: ctx.capitoli + 'Capitolo_23_responsabilita_civile_penale_e_assicurazione/index.html', tags: 'assicurazione rca تامين مسؤلية مدنية كفالة cid' },
      { it: 'Patente a punti', ar: 'نقاط رخصة القيادة', desc: 'تبدأ بـ 20 نقطة؛ تضاعف العقوبات للجدد Neopatentati خلال أول 3 سنوات', href: ctx.capitoli + 'Capitolo_20_patente_punti_documenti/index.html', tags: 'patente punti نقاط رخصة سحب نقاط عقوبات neopatentati' }
    ];

    glossary.forEach(g => {
      items.push({
        type: 'vocab',
        category: 'vocab',
        categoryLabel: '🔤 مصطلحات وفخاخ هامة',
        title: `${g.it} — ${g.ar}`,
        subtitle: g.desc,
        badge: '💡',
        href: g.href,
        tags: `${g.it} ${g.ar} ${g.desc} ${g.tags}`.toLowerCase()
      });
    });

    return items;
  }

  // 6. ==================== بناء الهيدر الموحد الفاخر (10/10) ====================
  function renderGlobalHeader(ctx) {
    const cur = (ctx.currentFile || '').toLowerCase();
    const full = (ctx.fullPath || '').toLowerCase();

    // حالات الصفحة النشطة
    const isGuide = (full.includes('interactive_pages') && (cur.includes('index') || cur === '' || cur === 'interactive_pages')) || 
                    cur.includes('دليل') || cur.includes('guida');
    const isHub = (full.includes('capitoli_divisi') && cur.includes('index')) || 
                  (!full.includes('interactive_pages') && cur.includes('index') && !isGuide);
    const isPiano = cur.includes('piano-studio');
    const isIncroci = cur.includes('decodificatore-incroci');
    const isParole = cur.includes('parole-spia');
    const isNumeri = cur.includes('laboratorio-numeri');
    const isSoccorso = cur.includes('primo-soccorso');
    const isScheda = cur.includes('scheda-esame');
    const isCards = cur.includes('flashcards');
    const isTraps = cur.includes('traps_and_games');
    const isTrucchi = cur.includes('trucchi-esame');
    const isDash = cur.includes('dashboard');
    const isAllenamento = cur.includes('allenamento-capitolo');

    // تصنيفات الهيدر
    const isCurriculumActive = isGuide || isHub || isPiano;
    const isLabsActive = isIncroci || isParole || isNumeri || isSoccorso;
    const isTrainingActive = isScheda || isCards || isTraps || isTrucchi;

    // حساب التقدم العام
    const globalStats = getGlobalProgressStats();

    // بناء بطاقات شبكة الأبواب الـ 25 لقائمة "تصفح الأبواب ▾"
    const chaptersGridHtml = CHAPTERS_DATA.map(ch => {
      const pad = ch.num < 10 ? '0' + ch.num : String(ch.num);
      const isCur = cur.includes(`capitolo_${pad}`) || 
                    cur.includes(`الباب_${pad}`) || 
                    cur.includes(`الباب_${ch.num}`);
      const prog = getChapterProgress(ch.num);
      const progBadge = prog.completed 
        ? `<span class="ch-prog-badge done" title="تم إنهاء جميع أسئلة الباب بنجاح">✅ 100%</span>`
        : (prog.answered > 0 ? `<span class="ch-prog-badge partial" title="تم حل ${prog.answered} من ${ch.questions}">${prog.pct}%</span>` : '');

      return `
        <div class="megamenu-ch-card ${isCur ? 'active' : ''}" data-ch="${ch.num}" data-search="${ch.num} ${pad} ${ch.title} ${ch.itTitle} ${ch.keywords}">
          <div class="megamenu-ch-info">
            <div class="megamenu-ch-meta">
              <span class="megamenu-ch-num">الباب ${pad}</span>
              ${progBadge}
              <span class="megamenu-ch-qcount">${ch.questions} سؤال</span>
            </div>
            <div class="megamenu-ch-title" title="${ch.title}">${ch.title}</div>
            <div class="megamenu-ch-it" title="${ch.itTitle}">${ch.itTitle}</div>
          </div>
          <div class="megamenu-ch-actions">
            <a href="${ctx.capitoli}${ch.folder}/index.html" class="megamenu-btn quiz" title="فتح بنك الأسئلة والتدريب الموديلار">
              <span>📝 أسئلة</span>
            </a>
            <a href="${ctx.interactive}${ch.guide}" class="megamenu-btn guide" title="فتح الشرح التفاعلي والقاموس">
              <span>📖 شرح</span>
            </a>
          </div>
        </div>
      `;
    }).join('');

    return `
      <header class="unified-portal-nav" id="globalPortalNav">
        <!-- 1. الشعار وزر تصفح الأبواب المنسدل السريع -->
        <div class="nav-brand-group">
          <a href="${ctx.capitoli}index.html" class="nav-brand" title="الرئيسية — Patente B Pro">
            <span class="brand-emoji">🚦</span>
            <span class="brand-text">Patente B Pro</span>
            <span class="badge-tag">2026</span>
          </a>

          <!-- زر تصفح الأبواب الـ 25 المنسدل السريع (ديسكتوب) -->
          <div class="nav-dropdown-wrapper nav-chapters-wrapper">
            <button class="nav-dropdown-btn nav-chapters-btn" id="btnToggleChaptersMenu" aria-expanded="false" title="تصفح جميع الأبواب الـ 25 والوصول اللحظي للأسئلة والشروحات">
              <span class="btn-icon">📚</span>
              <span class="btn-label">تصفح الأبواب (1-25)</span>
              <span class="dropdown-chevron">▾</span>
            </button>

            <!-- ميجا منيو الأبواب الـ 25 -->
            <div class="nav-dropdown-menu nav-chapters-megamenu" id="chaptersDropdownMenu">
              <div class="megamenu-topbar">
                <div class="megamenu-title-group">
                  <span class="megamenu-pill">25 باباً رسمياً</span>
                  <strong>فهرس أبواب رخصة القيادة الإيطالية (7,139 سؤال)</strong>
                </div>
                <div class="megamenu-search-wrapper">
                  <span class="input-search-icon">🔍</span>
                  <input type="text" id="chaptersMenuFilter" class="megamenu-filter-input" placeholder="تصفية بالرقم أو العنوان أو المصطلح الإيطالي..." autocomplete="off">
                  <button class="megamenu-clear-btn" id="btnClearChaptersFilter" style="display:none;" title="مسح التصفية">✕</button>
                </div>
              </div>
              <div class="megamenu-grid" id="chaptersMegamenuGrid">
                ${chaptersGridHtml}
              </div>
              <div class="megamenu-bottombar">
                <span class="bottombar-hint">💡 اختر "📝 أسئلة" للتدريب الموديلار وحفظ الإنجاز، أو "📖 شرح" لقاموس المفاهيم والرسوم.</span>
                <a href="${ctx.interactive}dashboard.html" class="bottombar-dash-link">📊 عرض لوحة الإنجاز العامة ⬅</a>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. التصنيفات الـ 4 الرئيسية المنسدلة (Desktop Mega Dropdowns) -->
        <nav class="nav-desktop-tabs" id="globalDesktopTabs">
          <!-- المجموعة 1: 📖 المناهج ▾ -->
          <div class="nav-dropdown-wrapper">
            <button class="nav-dropdown-tab ${isCurriculumActive ? 'active' : ''}" id="btnDropdownCurriculum">
              <span class="tab-icon">📖</span>
              <span>المناهج</span>
              <span class="dropdown-chevron">▾</span>
            </button>
            <div class="nav-dropdown-menu nav-category-menu">
              <div class="cat-menu-header">
                <span class="cat-menu-badge">المناهج والدروس</span>
                <span class="cat-menu-subtitle">المحتوى الأكاديمي الشامل لباتنت B</span>
              </div>
              <a href="${ctx.interactive}index.html" class="nav-cat-item ${isGuide ? 'active' : ''}">
                <div class="cat-item-icon">📖</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">شرح وتلخيص الأبواب (1-25)</div>
                  <div class="cat-item-desc">الدليل الشامل وترجمة المفاهيم الإيطالية بالرسوم التوضيحية</div>
                </div>
                ${isGuide ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
              <a href="${ctx.capitoli}index.html" class="nav-cat-item ${isHub ? 'active' : ''}">
                <div class="cat-item-icon">📝</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">بنك أسئلة الأبواب المقسمة</div>
                  <div class="cat-item-desc">7,139 سؤال رسمي مقسمة في 183 وحدة ذكية بحفظ الإنجاز</div>
                </div>
                ${isHub ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
              <a href="${ctx.interactive}piano-studio.html" class="nav-cat-item ${isPiano ? 'active' : ''}">
                <div class="cat-item-icon">📅</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">خطة الدراسة والجدول الزمني</div>
                  <div class="cat-item-desc">مسار زمني منظم لاجتياز الاختبار في 4 أو 8 أسابيع</div>
                </div>
                ${isPiano ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
            </div>
          </div>

          <!-- المجموعة 2: 🔬 المعامل الذكية ▾ -->
          <div class="nav-dropdown-wrapper">
            <button class="nav-dropdown-tab ${isLabsActive ? 'active' : ''}" id="btnDropdownLabs">
              <span class="tab-icon">🔬</span>
              <span>المعامل الذكية</span>
              <span class="dropdown-chevron">▾</span>
            </button>
            <div class="nav-dropdown-menu nav-category-menu">
              <div class="cat-menu-header">
                <span class="cat-menu-badge">المعامل التفاعلية</span>
                <span class="cat-menu-subtitle">أدوات ذكية متطورة لحل العقد وتفكيك القواعد</span>
              </div>
              <a href="${ctx.interactive}decodificatore-incroci.html" class="nav-cat-item ${isIncroci ? 'active' : ''}">
                <div class="cat-item-icon">🔄</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">مفكك التقاطعات التفاعلي</div>
                  <div class="cat-item-desc">تحليل أسبقية السير في الميادين وحساب مسار السيارات خطوة بخطوة</div>
                </div>
                ${isIncroci ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
              <a href="${ctx.interactive}parole-spia.html" class="nav-cat-item ${isParole ? 'active' : ''}">
                <div class="cat-item-icon">🎯</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">رادار الكلمات المفتاحية والفخاخ</div>
                  <div class="cat-item-desc">كشف الكلمات المؤكدة (Sempre / Mai) وكلمات الخداع في الاختبار</div>
                </div>
                ${isParole ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
              <a href="${ctx.interactive}laboratorio-numeri.html" class="nav-cat-item ${isNumeri ? 'active' : ''}">
                <div class="cat-item-icon">📏</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">معمل الأرقام وحساب المسافات</div>
                  <div class="cat-item-desc">حاسبة السرعات ومسافات الأمان وزمن رد الفعل وأوزان المركبات</div>
                </div>
                ${isNumeri ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
              <a href="${ctx.interactive}primo-soccorso.html" class="nav-cat-item ${isSoccorso ? 'active' : ''}">
                <div class="cat-item-icon">🚑</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">دليل الإسعافات الأولية (Primo Soccorso)</div>
                  <div class="cat-item-desc">خطوات الإنقاذ والتصرف السليم أثناء حوادث السير وإسعاف المصابين</div>
                </div>
                ${isSoccorso ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
            </div>
          </div>

          <!-- المجموعة 3: 🎮 التدريب والامتحانات ▾ -->
          <div class="nav-dropdown-wrapper">
            <button class="nav-dropdown-tab ${isTrainingActive ? 'active' : ''}" id="btnDropdownTraining">
              <span class="tab-icon">🎮</span>
              <span>التدريب والامتحانات</span>
              <span class="dropdown-chevron">▾</span>
            </button>
            <div class="nav-dropdown-menu nav-category-menu">
              <div class="cat-menu-header">
                <span class="cat-menu-badge">المحاكاة والتحديات</span>
                <span class="cat-menu-subtitle">تدريب مكثف بأحدث معايير وزارة النقل الإيطالية</span>
              </div>
              <a href="${ctx.interactive}scheda-esame.html" class="nav-cat-item ${isScheda ? 'active' : ''}">
                <div class="cat-item-icon">⏱️</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">محاكي الامتحان الوزاري الرسمي</div>
                  <div class="cat-item-desc">30 سؤال حقيقي في 20 دقيقة مع شاشة تصحيح وتقييم الأخطاء</div>
                </div>
                ${isScheda ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
              <a href="${ctx.interactive}flashcards.html" class="nav-cat-item ${isCards ? 'active' : ''}">
                <div class="cat-item-icon">🗂️</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">الفلاش كاردز التفاعلية</div>
                  <div class="cat-item-desc">بطاقات بصرية ذكية لحفظ الإشارات ورموز الطريق وتكرارها</div>
                </div>
                ${isCards ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
              <a href="${ctx.interactive}traps_and_games.html" class="nav-cat-item ${isTraps ? 'active' : ''}">
                <div class="cat-item-icon">🎮</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">بنك الفخاخ والألعاب التفاعلية</div>
                  <div class="cat-item-desc">تحدي أصعب الأسئلة الوزارية وتدريبات السرعة والتركيز</div>
                </div>
                ${isTraps ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
              <a href="${ctx.interactive}trucchi-esame.html" class="nav-cat-item ${isTrucchi ? 'active' : ''}">
                <div class="cat-item-icon">💎</div>
                <div class="cat-item-content">
                  <div class="cat-item-title">خزينة التريكات وأسرار النجاح</div>
                  <div class="cat-item-desc">قواعد ذهبية لاستنتاج الإجابة الصحيحة وتفادي الأخطاء الشائعة</div>
                </div>
                ${isTrucchi ? '<span class="cat-current-tag">أنت هنا</span>' : ''}
              </a>
              <a href="${ctx.interactive}dashboard.html#mistakes" class="nav-cat-item">
                <div class="cat-item-icon" style="background:rgba(239, 68, 68, 0.15); color:#F87171;">⚠️</div>
                <div class="cat-item-content">
                  <div class="cat-item-title" style="color:#FCA5A5;">بنك أخطائي وتحدي التصحيح</div>
                  <div class="cat-item-desc">تجميع أسئلتك الخاطئة في كويز مخصص لإتقانها وتفادي الرسوب</div>
                </div>
              </a>
            </div>
          </div>

          <!-- المجموعة 4: 📊 لوحة الإنجاز (Direct Tab) -->
          <a href="${ctx.interactive}dashboard.html" class="nav-direct-tab ${isDash ? 'active' : ''}" title="متابعة الإحصائيات ونسبة الدقة العامة">
            <span class="tab-icon">📊</span>
            <span>لوحة الإنجاز</span>
          </a>

          ${isAllenamento ? `
            <span class="nav-direct-tab active allenamento-pill" title="أنت تتمرن حالياً في هذا الباب">
              <span class="tab-icon">⚡</span>
              <span>تدريب الباب</span>
            </span>
          ` : ''}
        </nav>

        <!-- 3. أدوات الديسكتوب اليمنى: بحث سريع + شارة الإنجاز + الثيم -->
        <div class="nav-desktop-actions" id="globalDesktopActions">
          <!-- زر البحث السريع (Spotlight Search Button) -->
          <button class="nav-search-trigger" id="btnOpenGlobalSearch" title="بحث فوري في الأبواب والمصطلحات والمعامل [Ctrl + K]">
            <span class="search-icon">🔍</span>
            <span class="search-text">بحث سريع...</span>
            <kbd class="search-kbd">Ctrl K</kbd>
          </button>

          <!-- شارة الإنجاز العامة -->
          <a href="${ctx.interactive}dashboard.html" class="nav-progress-pill" id="globalProgressPill" title="إنجازك العام: تم حل ${globalStats.answered} من ${globalStats.total} سؤال (انقر لعرض لوحة التحكم)">
            <span class="prog-pill-icon">🎯</span>
            <div class="prog-pill-meta">
              <span class="prog-pill-label">إنجازك</span>
              <strong class="prog-pill-val" id="globalProgressPctVal">${globalStats.pct}%</strong>
            </div>
            <div class="prog-pill-bar-track">
              <div class="prog-pill-bar-fill" id="globalProgressMiniFill" style="width:${globalStats.pct}%;"></div>
            </div>
          </a>

          <!-- زر الحساب السحابي الموحد (Desktop Auth Pill) -->
          <div style="position:relative; display:inline-flex; align-items:center;">
            <button class="nav-auth-pill guest" id="globalAuthPill" title="تسجيل الدخول أو إنشاء حساب جديد لحفظ تقدمك سحابياً">
              <span>👤</span>
              <span>دخول / تسجيل</span>
            </button>
          </div>

          <!-- زر تبديل الوضع النهاري / الليلي -->
          <button class="nav-theme-btn" onclick="window.toggleTheme && window.toggleTheme()" title="تبديل الوضع (نهاري / ليلي) [Alt + T]">
            <span class="theme-icon-span">☀️</span>
            <span class="theme-label-span">الوضع</span>
          </button>
        </div>

        <!-- 4. عناصر تحكم الموبايل (<= 992px) -->
        <div class="nav-mobile-controls" id="globalMobileControls">
          <!-- شارة الإنجاز للموبايل -->
          <a href="${ctx.interactive}dashboard.html" class="mobile-prog-pill" id="globalMobileProgressPill" title="إنجازك العام">
            <span class="mob-prog-icon">🎯</span>
            <span class="mob-prog-text" id="globalMobileProgressVal">${globalStats.pct}%</span>
          </a>

          <!-- زر الحساب للموبايل -->
          <button class="nav-mobile-btn" id="btnOpenMobileAuth" title="حسابي والمزامنة السحابية" aria-label="حسابي">
            <span style="font-size:1.15rem;">👤</span>
          </button>

          <!-- زر البحث للموبايل -->
          <button class="nav-mobile-btn" id="btnOpenMobileSearch" title="بحث فوري" aria-label="بحث سريع">
            <span style="font-size:1.15rem;">🔍</span>
          </button>

          <!-- زر الثيم للموبايل -->
          <button class="nav-mobile-btn nav-mobile-theme-btn" onclick="window.toggleTheme && window.toggleTheme()" title="تبديل الوضع" aria-label="تبديل الوضع">
            <span class="theme-icon-span">☀️</span>
          </button>

          <!-- زر الهمبرغر المتطور -->
          <button class="nav-hamburger-btn nav-mobile-hamburger" id="btnToggleMobileDrawer" aria-label="فتح قائمة التنقل وتصفح الأبواب" aria-expanded="false">
            <div class="hamburger-box">
              <span class="hamburger-line line-top"></span>
              <span class="hamburger-line line-mid"></span>
              <span class="hamburger-line line-bot"></span>
            </div>
          </button>
        </div>
      </header>

      <!-- 5. نافذة البحث السريع الفوري المنبثقة (Spotlight Command Palette) -->
      <div class="global-search-backdrop" id="globalSearchModal" style="display:none;" aria-hidden="true">
        <div class="search-modal-container" role="dialog" aria-modal="true" aria-labelledby="globalSearchInput">
          <!-- شريط الإدخال الرئيسي -->
          <div class="search-modal-header">
            <span class="search-modal-icon">🔍</span>
            <input type="text" id="globalSearchInput" class="search-modal-input" placeholder="ابحث عن أي باب، إشارة، مفهوم، أو مصطلح إيطالي... (مثال: precedenza, سرعة, 14, sempre)" autocomplete="off">
            <button class="search-modal-close" id="btnCloseGlobalSearch" aria-label="إغلاق نافذة البحث" title="إغلاق [Esc]">⎋ Esc</button>
          </div>

          <!-- أزرار التصفية السريعة -->
          <div class="search-filter-pills" id="searchFilterPills">
            <button class="search-pill-btn active" data-filter="all">الكل</button>
            <button class="search-pill-btn" data-filter="chapters">📚 الأبواب الـ 25</button>
            <button class="search-pill-btn" data-filter="tools">🔬 المعامل والأدوات</button>
            <button class="search-pill-btn" data-filter="vocab">🔤 مصطلحات وفخاخ</button>
          </div>

          <!-- قائمة نتائج البحث -->
          <div class="search-results-list" id="globalSearchResults">
            <!-- Dynamic Items Injected Here -->
          </div>

          <!-- شريط معلومات وقواعد الاختصارات أسفل النافذة -->
          <div class="search-modal-footer">
            <div class="search-footer-shortcuts">
              <span><kbd class="footer-kbd">↑</kbd> <kbd class="footer-kbd">↓</kbd> للتنقل</span>
              <span><kbd class="footer-kbd">↵ Enter</kbd> للفتح الفوري</span>
              <span><kbd class="footer-kbd">Esc</kbd> للإغلاق</span>
            </div>
            <div class="search-footer-brand">
              <span>Patente B Pro Search Engine</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 6. قائمة الموبايل الاحترافية المقسمة (Mobile Drawer with Backdrop Blur) -->
      <div class="mobile-drawer-backdrop" id="mobileDrawerBackdrop">
        <aside class="mobile-drawer-pane" id="mobileDrawerPane">
          <div class="mobile-drawer-header">
            <div class="drawer-header-brand">
              <span style="font-size:1.4rem;">🚦</span>
              <div>
                <strong class="drawer-app-title">Patente B Pro</strong>
                <span class="drawer-app-subtitle">القائمة الموحدة وتصفح الأبواب</span>
              </div>
            </div>
            <button class="mobile-drawer-close" id="btnCloseMobileDrawer" aria-label="إغلاق القائمة">✕</button>
          </div>

          <!-- بطاقة الإنجاز في أعلى قائمة الموبايل -->
          <a href="${ctx.interactive}dashboard.html" class="drawer-progress-card">
            <div class="drawer-prog-top">
              <div class="drawer-prog-title">
                <span>🎯</span>
                <strong>تقدمك الإجمالي في المنهج</strong>
              </div>
              <span class="drawer-prog-pct" id="drawerProgressPctVal">${globalStats.pct}%</span>
            </div>
            <div class="drawer-prog-bar-track">
              <div class="drawer-prog-bar-fill" id="drawerProgressFill" style="width:${globalStats.pct}%;"></div>
            </div>
            <div class="drawer-prog-sub">
              <span>تمت الإجابة على <strong id="drawerAnsweredCount">${globalStats.answered}</strong> من ${globalStats.total} سؤال رسمي</span>
            </div>
          </a>

          <!-- زر البحث السريع في قائمة الموبايل -->
          <button class="drawer-search-trigger-btn" id="btnDrawerSearchTrigger">
            <span>🔍</span>
            <span>ابحث عن أي باب، إشارة أو مصطلح...</span>
            <kbd>بحث</kbd>
          </button>

          <div class="mobile-drawer-links-wrap">
            <!-- 1. المناهج -->
            <div class="mobile-drawer-section-label">📖 المناهج والدروس</div>
            <a href="${ctx.interactive}index.html" class="mobile-drawer-link ${isGuide ? 'active' : ''}">
              <span class="drawer-link-icon">📖</span>
              <span class="drawer-link-text">شرح وتلخيص الأبواب (1-25)</span>
              ${isGuide ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>
            <a href="${ctx.capitoli}index.html" class="mobile-drawer-link ${isHub ? 'active' : ''}">
              <span class="drawer-link-icon">📝</span>
              <span class="drawer-link-text">بنك أسئلة الأبواب المقسمة</span>
              ${isHub ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>
            <a href="${ctx.interactive}piano-studio.html" class="mobile-drawer-link ${isPiano ? 'active' : ''}">
              <span class="drawer-link-icon">📅</span>
              <span class="drawer-link-text">خطة الدراسة والجدول الزمني</span>
              ${isPiano ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>

            <!-- 2. المعامل الذكية -->
            <div class="mobile-drawer-divider"></div>
            <div class="mobile-drawer-section-label">🔬 المعامل الذكية</div>
            <a href="${ctx.interactive}decodificatore-incroci.html" class="mobile-drawer-link ${isIncroci ? 'active' : ''}">
              <span class="drawer-link-icon">🔄</span>
              <span class="drawer-link-text">مفكك التقاطعات التفاعلي</span>
              ${isIncroci ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>
            <a href="${ctx.interactive}parole-spia.html" class="mobile-drawer-link ${isParole ? 'active' : ''}">
              <span class="drawer-link-icon">🎯</span>
              <span class="drawer-link-text">رادار الكلمات المفتاحية والفخاخ</span>
              ${isParole ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>
            <a href="${ctx.interactive}laboratorio-numeri.html" class="mobile-drawer-link ${isNumeri ? 'active' : ''}">
              <span class="drawer-link-icon">📏</span>
              <span class="drawer-link-text">معمل الأرقام وحساب المسافات</span>
              ${isNumeri ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>
            <a href="${ctx.interactive}primo-soccorso.html" class="mobile-drawer-link ${isSoccorso ? 'active' : ''}">
              <span class="drawer-link-icon">🚑</span>
              <span class="drawer-link-text">دليل الإسعافات الأولية (Primo Soccorso)</span>
              ${isSoccorso ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>

            <!-- 3. التدريب والامتحانات -->
            <div class="mobile-drawer-divider"></div>
            <div class="mobile-drawer-section-label">🎮 التدريب والامتحانات</div>
            <a href="${ctx.interactive}scheda-esame.html" class="mobile-drawer-link ${isScheda ? 'active' : ''}">
              <span class="drawer-link-icon">⏱️</span>
              <span class="drawer-link-text">محاكي الامتحان الوزاري الرسمي</span>
              ${isScheda ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>
            <a href="${ctx.interactive}flashcards.html" class="mobile-drawer-link ${isCards ? 'active' : ''}">
              <span class="drawer-link-icon">🗂️</span>
              <span class="drawer-link-text">الفلاش كاردز التفاعلية</span>
              ${isCards ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>
            <a href="${ctx.interactive}traps_and_games.html" class="mobile-drawer-link ${isTraps ? 'active' : ''}">
              <span class="drawer-link-icon">🎮</span>
              <span class="drawer-link-text">بنك الفخاخ والألعاب التفاعلية</span>
              ${isTraps ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>
            <a href="${ctx.interactive}trucchi-esame.html" class="mobile-drawer-link ${isTrucchi ? 'active' : ''}">
              <span class="drawer-link-icon">💎</span>
              <span class="drawer-link-text">خزينة التريكات وأسرار النجاح</span>
              ${isTrucchi ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>
            <a href="${ctx.interactive}dashboard.html#mistakes" class="mobile-drawer-link">
              <span class="drawer-link-icon">⚠️</span>
              <span class="drawer-link-text">بنك أخطائي وتحدي التصحيح</span>
            </a>
            <a href="${ctx.interactive}dashboard.html" class="mobile-drawer-link ${isDash ? 'active' : ''}">
              <span class="drawer-link-icon">📊</span>
              <span class="drawer-link-text">لوحة الإنجاز ومتابعة التقدم</span>
              ${isDash ? '<span class="drawer-link-badge">أنت هنا</span>' : ''}
            </a>

            <!-- 4. الأكورديون الذكي للأبواب الـ 25 -->
            <div class="mobile-drawer-divider"></div>
            <div class="mobile-drawer-accordion-btn" id="btnToggleChaptersAccordion" role="button" tabindex="0">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:1.15rem;">📚</span>
                <span style="font-weight:800; color:var(--text-primary, #FFF);">تصفح الأبواب المقسمة (1 - 25)</span>
              </div>
              <span class="accordion-arrow" id="chaptersAccordionArrow" style="transition:transform 0.25s ease; font-size:0.9rem;">▾</span>
            </div>

            <div class="mobile-drawer-chapters-container" id="mobileChaptersContainer" style="display:none;">
              ${CHAPTERS_DATA.map(ch => {
                const chPad = ch.num < 10 ? '0' + ch.num : String(ch.num);
                const isCur = cur.includes(`capitolo_${chPad}`) || 
                              cur.includes(`الباب_${chPad}`) ||
                              cur.includes(`الباب_${ch.num}`);
                const prog = getChapterProgress(ch.num);
                const progBadge = prog.completed 
                  ? `<span class="drawer-prog-pill done">✅ مكتمل</span>`
                  : (prog.answered > 0 ? `<span class="drawer-prog-pill partial">${prog.pct}%</span>` : '');

                return `
                  <div class="mobile-drawer-chapter-row ${isCur ? 'active' : ''}">
                    <div class="drawer-ch-header">
                      <span class="drawer-ch-badge">الباب ${chPad}</span>
                      ${progBadge}
                      <span class="drawer-ch-name" title="${ch.title}">${ch.title}</span>
                    </div>
                    <div class="drawer-ch-pills">
                      <a href="${ctx.capitoli}${ch.folder}/index.html" class="drawer-ch-pill quiz" title="كويز وبنك أسئلة">
                        <span>📝 أسئلة</span>
                      </a>
                      <a href="${ctx.interactive}${ch.guide}" class="drawer-ch-pill guide" title="الشرح والقاموس">
                        <span>📖 شرح</span>
                      </a>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <div class="mobile-drawer-footer">
            <button class="mobile-control-btn" onclick="window.toggleTheme && window.toggleTheme()">
              <span class="theme-icon-span">☀️</span>
              <span class="theme-label-span">تبديل الوضع النهاري / الليلي</span>
            </button>
          </div>
        </aside>
      </div>
    `;
  }

  // 7. ==================== بناء الفوتر الموحد ====================
  function renderGlobalFooter(ctx) {
    return `
      <footer class="unified-portal-footer" id="globalPortalFooter">
        <div class="footer-inner-container">
          <div class="dev-footer-card">
            <div class="dev-info-left">
              <div class="dev-avatar-wrap">
                <span class="dev-avatar-icon">👨‍💻</span>
              </div>
              <div class="dev-text-details">
                <div class="dev-name-row">
                  <span class="dev-name">Eng. Ramy Eid Saad Fahmy</span>
                  <span class="dev-badge">Ingegnere Informatico</span>
                </div>
                <p class="dev-sub-desc">
                  Full Stack & Automation Developer • Brindisi, Italia
                </p>
              </div>
            </div>

            <div class="dev-links-right">
              <a href="https://portfolio-taupe-eight-84.vercel.app/" target="_blank" rel="noopener noreferrer" class="dev-pill-btn" title="Portfolio Personale">
                <span>🌐</span>
                <span>Portfolio</span>
              </a>
              <a href="https://github.com/Ramy3id" target="_blank" rel="noopener noreferrer" class="dev-pill-btn" title="GitHub Profile">
                <span>💻</span>
                <span>GitHub</span>
              </a>
              <a href="mailto:ramyeid.dev@gmail.com" class="dev-pill-btn" title="Email: ramyeid.dev@gmail.com">
                <span>✉️</span>
                <span>Email</span>
              </a>
              <a href="https://wa.me/393447044605" target="_blank" rel="noopener noreferrer" class="dev-pill-btn" title="WhatsApp: (+39) 3447044605">
                <span>💬</span>
                <span>WhatsApp</span>
              </a>
              <button class="footer-btn-scrolltop" onclick="window.scrollTo({top:0, behavior:'smooth'})" title="العودة لأعلى الصفحة (Scroll to top)">
                <span>⬆️</span>
              </button>
            </div>
          </div>

          <div class="dev-copyright-row">
            <span>Patente B Pro &copy; 2026 • Progettato e sviluppato da <strong>Eng. Ramy Eid Saad Fahmy</strong></span>
            <span class="dev-status-pill">⚡ Offline PWA Ready • 7,139 Domande</span>
          </div>
        </div>
      </footer>
    `;
  }

  // 8. ==================== التنسيقات المتكاملة (High-Contrast Apple HIG) ====================
  function injectStyles() {
    if (document.getElementById('unifiedNavCustomStyles')) return;
    const style = document.createElement('style');
    style.id = 'unifiedNavCustomStyles';
    style.textContent = `
      /* =========================================================
         1. شريط التنقل العلوي الموحد (Unified Portal Nav)
         ========================================================= */
      .unified-portal-nav {
        position: sticky;
        top: 0;
        z-index: 9999;
        min-height: 60px;
        background: rgba(11, 15, 25, 0.94);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 16px;
        gap: 12px;
        box-sizing: border-box;
        transition: background 0.25s ease, border-color 0.25s ease;
      }
      html.light .unified-portal-nav {
        background: rgba(255, 255, 255, 0.96);
        border-bottom: 1px solid rgba(15, 23, 42, 0.09);
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
      }

      /* الشعار والوسم */
      .nav-brand-group {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-shrink: 0;
      }
      .nav-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        text-decoration: none;
        white-space: nowrap;
      }
      .brand-emoji {
        font-size: 1.35rem;
        line-height: 1;
      }
      .brand-text {
        font-size: 1.05rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.2px;
      }
      html.light .brand-text {
        color: #0F172A;
      }
      .badge-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        padding: 2px 7px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38BDF8;
        border-radius: 6px;
        font-weight: 700;
      }
      html.light .badge-tag {
        background: rgba(2, 132, 199, 0.08);
        border-color: rgba(2, 132, 199, 0.25);
        color: #0284C7;
      }

      /* زر تصفح الأبواب المنسدل السريع (ديسكتوب) */
      .nav-chapters-btn {
        height: 36px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 12px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 9px;
        color: #38BDF8;
        font-size: 0.82rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: inherit;
        white-space: nowrap;
      }
      html.light .nav-chapters-btn {
        background: rgba(2, 132, 199, 0.08);
        border-color: rgba(2, 132, 199, 0.28);
        color: #0284C7;
      }
      .nav-chapters-btn:hover, .nav-chapters-btn.active {
        background: rgba(56, 189, 248, 0.2);
        border-color: rgba(56, 189, 248, 0.5);
        transform: translateY(-1px);
      }
      html.light .nav-chapters-btn:hover, html.light .nav-chapters-btn.active {
        background: rgba(2, 132, 199, 0.15);
        border-color: rgba(2, 132, 199, 0.45);
      }

      /* ميجا منيو الأبواب الـ 25 */
      .nav-chapters-megamenu {
        position: absolute;
        top: calc(100% + 8px);
        right: 0;
        width: 820px;
        max-width: 92vw;
        max-height: 82vh;
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65);
        padding: 0;
        display: none;
        flex-direction: column;
        z-index: 10005;
        overflow: hidden;
      }
      html.light .nav-chapters-megamenu {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.12);
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.18);
      }
      .nav-chapters-megamenu.show {
        display: flex;
        animation: menuFadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      }
      @keyframes menuFadeIn {
        from { opacity: 0; transform: translateY(-6px); }
        to { opacity: 1; transform: translateY(0); }
      }

      .megamenu-topbar {
        padding: 14px 18px;
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 14px;
        flex-wrap: wrap;
      }
      html.light .megamenu-topbar {
        background: #F8FAFC;
        border-bottom-color: rgba(15, 23, 42, 0.08);
      }
      .megamenu-title-group {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #F8FAFC;
        font-size: 0.92rem;
      }
      html.light .megamenu-title-group {
        color: #0F172A;
      }
      .megamenu-pill {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 2px 7px;
      }
      html.light .megamenu-pill {
        background: rgba(2, 132, 199, 0.08);
        color: #0284C7;
        border-color: rgba(2, 132, 199, 0.25);
      }
      .megamenu-search-wrapper {
        position: relative;
        flex: 1;
        max-width: 320px;
        min-width: 200px;
      }
      .input-search-icon {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 0.85rem;
        opacity: 0.6;
        pointer-events: none;
      }
      .megamenu-filter-input {
        width: 100%;
        height: 34px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #F8FAFC;
        padding: 0 32px 0 28px;
        font-size: 0.8rem;
        font-family: inherit;
        outline: none;
        box-sizing: border-box;
      }
      html.light .megamenu-filter-input {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.15);
        color: #0F172A;
      }
      .megamenu-filter-input:focus {
        border-color: #38BDF8;
        background: rgba(56, 189, 248, 0.05);
      }
      .megamenu-clear-btn {
        position: absolute;
        left: 8px;
        top: 50%;
        transform: translateY(-50%);
        background: transparent;
        border: none;
        color: #94A3B8;
        cursor: pointer;
        padding: 2px 4px;
      }

      /* شبكة الأبواب */
      .megamenu-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        padding: 14px 18px;
        overflow-y: auto;
        max-height: 58vh;
      }
      @media (min-width: 1200px) {
        .megamenu-grid {
          grid-template-columns: repeat(2, 1fr);
        }
      }
      .megamenu-ch-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 10px 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        transition: all 0.15s ease;
      }
      html.light .megamenu-ch-card {
        background: #F8FAFC;
        border-color: rgba(15, 23, 42, 0.07);
      }
      .megamenu-ch-card:hover {
        background: rgba(56, 189, 248, 0.06);
        border-color: rgba(56, 189, 248, 0.25);
        transform: translateY(-1px);
      }
      html.light .megamenu-ch-card:hover {
        background: rgba(2, 132, 199, 0.05);
        border-color: rgba(2, 132, 199, 0.25);
      }
      .megamenu-ch-card.active {
        border-color: rgba(56, 189, 248, 0.45);
        background: rgba(56, 189, 248, 0.1);
      }
      .megamenu-ch-info {
        flex: 1;
        min-width: 0;
      }
      .megamenu-ch-meta {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 3px;
      }
      .megamenu-ch-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 800;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        padding: 2px 6px;
        border-radius: 5px;
      }
      html.light .megamenu-ch-num {
        background: rgba(2, 132, 199, 0.08);
        color: #0284C7;
      }
      .ch-prog-badge {
        font-size: 0.68rem;
        font-weight: 800;
        padding: 1px 6px;
        border-radius: 5px;
      }
      .ch-prog-badge.done {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
      }
      .ch-prog-badge.partial {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
      }
      .megamenu-ch-qcount {
        font-size: 0.7rem;
        color: #94A3B8;
        margin-right: auto;
      }
      .megamenu-ch-title {
        font-size: 0.84rem;
        font-weight: 700;
        color: #F8FAFC;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      html.light .megamenu-ch-title {
        color: #0F172A;
      }
      .megamenu-ch-it {
        font-size: 0.72rem;
        color: #94A3B8;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-style: italic;
      }
      html.light .megamenu-ch-it {
        color: #64748B;
      }
      .megamenu-ch-actions {
        display: flex;
        flex-direction: column;
        gap: 4px;
        flex-shrink: 0;
      }
      .megamenu-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 3px;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        text-decoration: none;
        white-space: nowrap;
        transition: all 0.15s ease;
      }
      .megamenu-btn.quiz {
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.25);
      }
      .megamenu-btn.quiz:hover {
        background: rgba(16, 185, 129, 0.25);
      }
      .megamenu-btn.guide {
        background: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.25);
      }
      .megamenu-btn.guide:hover {
        background: rgba(56, 189, 248, 0.25);
      }
      .megamenu-bottombar {
        padding: 10px 18px;
        background: rgba(255, 255, 255, 0.02);
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        font-size: 0.78rem;
        color: #94A3B8;
      }
      html.light .megamenu-bottombar {
        background: #F1F5F9;
        border-top-color: rgba(15, 23, 42, 0.06);
        color: #64748B;
      }
      .bottombar-dash-link {
        color: #38BDF8;
        font-weight: 700;
        text-decoration: none;
      }
      html.light .bottombar-dash-link {
        color: #0284C7;
      }

      /* =========================================================
         2. ألسنة التبويب للديسكتوب والقوائم المنسدلة الذكية
         ========================================================= */
      .nav-desktop-tabs {
        display: flex;
        align-items: center;
        gap: 6px;
        flex: 1;
        justify-content: center;
        padding: 0 8px;
      }
      .nav-dropdown-wrapper {
        position: relative;
        display: inline-flex;
        align-items: center;
      }
      .nav-dropdown-tab {
        height: 36px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 12px;
        border-radius: 9px;
        color: #94A3B8;
        background: transparent;
        border: 1px solid transparent;
        font-size: 0.84rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s ease;
        white-space: nowrap;
        font-family: inherit;
      }
      html.light .nav-dropdown-tab {
        color: #334155;
      }
      .nav-dropdown-tab:hover {
        color: #FFFFFF;
        background: rgba(255, 255, 255, 0.06);
      }
      html.light .nav-dropdown-tab:hover {
        color: #0F172A;
        background: rgba(15, 23, 42, 0.05);
      }
      .nav-dropdown-tab.active {
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.12);
        border-color: rgba(56, 189, 248, 0.25);
      }
      html.light .nav-dropdown-tab.active {
        color: #0284C7;
        background: rgba(2, 132, 199, 0.1);
        border-color: rgba(2, 132, 199, 0.28);
      }
      .dropdown-chevron {
        font-size: 0.78rem;
        opacity: 0.7;
        transition: transform 0.2s ease;
      }
      .nav-dropdown-wrapper.open .dropdown-chevron {
        transform: rotate(180deg);
      }

      .nav-direct-tab {
        height: 36px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 12px;
        border-radius: 9px;
        color: #94A3B8;
        background: transparent;
        border: 1px solid transparent;
        font-size: 0.84rem;
        font-weight: 700;
        text-decoration: none;
        transition: all 0.15s ease;
        white-space: nowrap;
      }
      html.light .nav-direct-tab {
        color: #334155;
      }
      .nav-direct-tab:hover {
        color: #FFFFFF;
        background: rgba(255, 255, 255, 0.06);
      }
      html.light .nav-direct-tab:hover {
        color: #0F172A;
        background: rgba(15, 23, 42, 0.05);
      }
      .nav-direct-tab.active {
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.12);
        border-color: rgba(56, 189, 248, 0.25);
      }
      html.light .nav-direct-tab.active {
        color: #0284C7;
        background: rgba(2, 132, 199, 0.1);
        border-color: rgba(2, 132, 199, 0.28);
      }
      .allenamento-pill {
        border-color: rgba(245, 158, 11, 0.35) !important;
        background: rgba(245, 158, 11, 0.15) !important;
        color: #FBBF24 !important;
      }

      /* قوائم التصنيفات المنسدلة (Category Dropdowns) */
      .nav-category-menu {
        position: absolute;
        top: calc(100% + 8px);
        right: 0;
        width: 330px;
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.55);
        padding: 8px;
        display: none;
        flex-direction: column;
        gap: 4px;
        z-index: 10002;
      }
      html.light .nav-category-menu {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.12);
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.15);
      }
      .nav-category-menu.show {
        display: flex;
        animation: menuFadeIn 0.18s cubic-bezier(0.16, 1, 0.3, 1);
      }
      .cat-menu-header {
        padding: 8px 12px 6px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 4px;
      }
      html.light .cat-menu-header {
        border-bottom-color: rgba(15, 23, 42, 0.06);
      }
      .cat-menu-badge {
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        color: #38BDF8;
        letter-spacing: 0.04em;
        display: block;
      }
      html.light .cat-menu-badge {
        color: #0284C7;
      }
      .cat-menu-subtitle {
        font-size: 0.72rem;
        color: #94A3B8;
      }
      html.light .cat-menu-subtitle {
        color: #64748B;
      }
      .nav-cat-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 9px 12px;
        border-radius: 10px;
        text-decoration: none;
        transition: all 0.15s ease;
        border: 1px solid transparent;
      }
      .nav-cat-item:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.08);
      }
      html.light .nav-cat-item:hover {
        background: rgba(15, 23, 42, 0.04);
        border-color: rgba(15, 23, 42, 0.08);
      }
      .nav-cat-item.active {
        background: rgba(56, 189, 248, 0.12);
        border-color: rgba(56, 189, 248, 0.25);
      }
      html.light .nav-cat-item.active {
        background: rgba(2, 132, 199, 0.08);
        border-color: rgba(2, 132, 199, 0.25);
      }
      .cat-item-icon {
        font-size: 1.25rem;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }
      html.light .cat-item-icon {
        background: rgba(15, 23, 42, 0.05);
      }
      .cat-item-content {
        flex: 1;
        min-width: 0;
      }
      .cat-item-title {
        font-size: 0.84rem;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.3;
      }
      html.light .cat-item-title {
        color: #0F172A;
      }
      .cat-item-desc {
        font-size: 0.72rem;
        color: #94A3B8;
        line-height: 1.35;
        margin-top: 2px;
      }
      html.light .cat-item-desc {
        color: #64748B;
      }
      .cat-current-tag {
        font-size: 0.68rem;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 5px;
        background: #38BDF8;
        color: #0B0F19;
        margin-right: auto;
      }

      /* =========================================================
         3. الأدوات اليمنى: بحث سريع + شارة إنجاز + زر الثيم
         ========================================================= */
      .nav-desktop-actions {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
      }
      /* زر فتح البحث السريع */
      .nav-search-trigger {
        height: 36px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9px;
        color: #94A3B8;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.15s ease;
        font-family: inherit;
      }
      html.light .nav-search-trigger {
        background: rgba(15, 23, 42, 0.04);
        border-color: rgba(15, 23, 42, 0.1);
        color: #475569;
      }
      .nav-search-trigger:hover {
        background: rgba(255, 255, 255, 0.09);
        border-color: rgba(56, 189, 248, 0.3);
        color: #F8FAFC;
      }
      html.light .nav-search-trigger:hover {
        background: rgba(15, 23, 42, 0.07);
        border-color: rgba(2, 132, 199, 0.3);
        color: #0F172A;
      }
      .search-kbd {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        padding: 2px 5px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 5px;
        color: #CBD5E1;
      }
      html.light .search-kbd {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.15);
        color: #475569;
      }

      /* شارة الإنجاز العامة في الهيدر */
      .nav-progress-pill {
        height: 36px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0 10px;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 9px;
        text-decoration: none;
        transition: all 0.2s ease;
      }
      html.light .nav-progress-pill {
        background: rgba(5, 150, 105, 0.06);
        border-color: rgba(5, 150, 105, 0.25);
      }
      .nav-progress-pill:hover {
        background: rgba(16, 185, 129, 0.16);
        border-color: rgba(16, 185, 129, 0.45);
        transform: translateY(-1px);
      }
      .prog-pill-icon {
        font-size: 1rem;
        line-height: 1;
      }
      .prog-pill-meta {
        display: flex;
        flex-direction: column;
        line-height: 1.1;
      }
      .prog-pill-label {
        font-size: 0.62rem;
        color: #94A3B8;
        font-weight: 700;
        text-transform: uppercase;
      }
      html.light .prog-pill-label {
        color: #64748B;
      }
      .prog-pill-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 800;
        color: #34D399;
      }
      html.light .prog-pill-val {
        color: #059669;
      }
      .prog-pill-bar-track {
        width: 32px;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 99px;
        overflow: hidden;
      }
      html.light .prog-pill-bar-track {
        background: rgba(15, 23, 42, 0.1);
      }
      .prog-pill-bar-fill {
        height: 100%;
        background: #34D399;
        border-radius: 99px;
        transition: width 0.3s ease;
      }

      /* زر الثيم المتطور */
      .nav-theme-btn {
        height: 36px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9px;
        color: #CBD5E1;
        font-size: 0.8rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s ease;
        font-family: inherit;
      }
      html.light .nav-theme-btn {
        background: rgba(15, 23, 42, 0.04);
        border-color: rgba(15, 23, 42, 0.1);
        color: #334155;
      }
      .nav-theme-btn:hover {
        background: rgba(255, 255, 255, 0.09);
        color: #FFFFFF;
      }
      html.light .nav-theme-btn:hover {
        background: rgba(15, 23, 42, 0.08);
        color: #0F172A;
      }

      /* زر الحساب السحابي الموحد (Desktop & Mobile) */
      .nav-auth-pill {
        height: 36px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 12px;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 9px;
        color: #38BDF8;
        font-size: 0.8rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: inherit;
        white-space: nowrap;
        text-decoration: none;
        outline: none;
      }
      html.light .nav-auth-pill {
        background: rgba(2, 132, 199, 0.06);
        border-color: rgba(2, 132, 199, 0.25);
        color: #0284C7;
      }
      .nav-auth-pill:hover {
        background: rgba(56, 189, 248, 0.18);
        border-color: rgba(56, 189, 248, 0.5);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.2);
      }
      html.light .nav-auth-pill:hover {
        background: rgba(2, 132, 199, 0.12);
        border-color: rgba(2, 132, 199, 0.45);
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.15);
      }
      .nav-auth-pill.logged-in {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.35);
        color: #34D399;
      }
      html.light .nav-auth-pill.logged-in {
        background: rgba(5, 150, 105, 0.08);
        border-color: rgba(5, 150, 105, 0.3);
        color: #059669;
      }
      .auth-online-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 8px #10B981;
        display: inline-block;
      }
      .auth-online-dot.syncing {
        background: #F59E0B;
        box-shadow: 0 0 8px #F59E0B;
        animation: authPulse 0.8s infinite alternate;
      }

      /* عناصر تحكم الموبايل */
      .nav-mobile-controls {
        display: none;
      }
      .mobile-prog-pill {
        display: inline-flex;
        align-items: center;
        gap: 3px;
        padding: 4px 7px;
        border-radius: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #34D399;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        font-weight: 800;
        text-decoration: none;
        flex-shrink: 0;
      }
      html.light .mobile-prog-pill {
        background: rgba(5, 150, 105, 0.08);
        border-color: rgba(5, 150, 105, 0.25);
        color: #059669;
      }
      .nav-mobile-btn {
        width: 33px;
        height: 33px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #FFF;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        padding: 0;
        flex-shrink: 0;
      }
      html.light .nav-mobile-btn {
        background: rgba(15, 23, 42, 0.05);
        border-color: rgba(15, 23, 42, 0.1);
        color: #0F172A;
      }
      .nav-mobile-hamburger {
        width: 35px;
        height: 35px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #FFF;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        padding: 0;
        flex-shrink: 0;
      }
      html.light .nav-mobile-hamburger {
        background: rgba(15, 23, 42, 0.05);
        border-color: rgba(15, 23, 42, 0.1);
        color: #0F172A;
      }
      .hamburger-box {
        width: 17px;
        height: 12px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .hamburger-line {
        display: block;
        width: 100%;
        height: 2px;
        background-color: currentColor;
        border-radius: 2px;
        transition: transform 0.25s ease, opacity 0.2s ease;
      }
      .nav-mobile-hamburger.is-active .line-top {
        transform: translateY(5px) rotate(45deg);
        background-color: #38BDF8;
      }
      .nav-mobile-hamburger.is-active .line-mid {
        opacity: 0;
      }
      .nav-mobile-hamburger.is-active .line-bot {
        transform: translateY(-5px) rotate(-45deg);
        background-color: #38BDF8;
      }

      @media (max-width: 992px) {
        .unified-portal-nav {
          padding: 0 10px !important;
          gap: 6px !important;
        }
        .nav-chapters-wrapper { display: none !important; }
        .nav-desktop-tabs { display: none !important; }
        .nav-desktop-actions { display: none !important; }
        .nav-mobile-controls {
          display: flex !important;
          align-items: center;
          gap: 5px;
          flex-shrink: 0;
        }
      }

      @media (max-width: 480px) {
        .unified-portal-nav {
          padding: 0 8px !important;
          gap: 4px !important;
        }
        .nav-brand-group {
          gap: 6px !important;
          min-width: 0;
          overflow: hidden;
        }
        .nav-brand .badge-tag {
          display: none !important;
        }
        .nav-brand .brand-text {
          font-size: 0.95rem !important;
          text-overflow: ellipsis;
          overflow: hidden;
        }
        .nav-mobile-controls {
          gap: 4px !important;
        }
        .nav-mobile-theme-btn {
          display: none !important; /* توفير المساحة لشاشات الموبايل الضيقة لأن الثيم متاح داخل قائمة البرجر */
        }
      }

      /* =========================================================
         4. نافذة البحث السريع الفوري (Spotlight Command Palette)
         ========================================================= */
      .global-search-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.72);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        z-index: 999999;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        padding: 60px 16px 20px;
        box-sizing: border-box;
      }
      .search-modal-container {
        width: 100%;
        max-width: 650px;
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 16px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        animation: modalScaleUp 0.18s cubic-bezier(0.16, 1, 0.3, 1);
      }
      html.light .search-modal-container {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.15);
        box-shadow: 0 25px 60px rgba(15, 23, 42, 0.22);
      }
      @keyframes modalScaleUp {
        from { opacity: 0; transform: scale(0.96) translateY(-10px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
      }
      .search-modal-header {
        display: flex;
        align-items: center;
        padding: 14px 18px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        gap: 12px;
      }
      html.light .search-modal-header {
        border-bottom-color: rgba(15, 23, 42, 0.08);
      }
      .search-modal-icon {
        font-size: 1.25rem;
        opacity: 0.7;
      }
      .search-modal-input {
        flex: 1;
        background: transparent;
        border: none;
        outline: none;
        color: #F8FAFC;
        font-size: 1.05rem;
        font-weight: 600;
        font-family: inherit;
      }
      html.light .search-modal-input {
        color: #0F172A;
      }
      .search-modal-input::placeholder {
        color: #64748B;
        font-size: 0.95rem;
      }
      .search-modal-close {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #CBD5E1;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        cursor: pointer;
        font-family: inherit;
      }
      html.light .search-modal-close {
        background: rgba(15, 23, 42, 0.06);
        border-color: rgba(15, 23, 42, 0.12);
        color: #475569;
      }
      .search-filter-pills {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        overflow-x: auto;
      }
      html.light .search-filter-pills {
        background: #F8FAFC;
        border-bottom-color: rgba(15, 23, 42, 0.06);
      }
      .search-pill-btn {
        padding: 4px 10px;
        border-radius: 99px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: transparent;
        color: #94A3B8;
        font-size: 0.76rem;
        font-weight: 700;
        cursor: pointer;
        white-space: nowrap;
        font-family: inherit;
        transition: all 0.15s ease;
      }
      html.light .search-pill-btn {
        border-color: rgba(15, 23, 42, 0.1);
        color: #475569;
      }
      .search-pill-btn.active, .search-pill-btn:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: rgba(56, 189, 248, 0.35);
        color: #38BDF8;
      }
      html.light .search-pill-btn.active, html.light .search-pill-btn:hover {
        background: rgba(2, 132, 199, 0.1);
        border-color: rgba(2, 132, 199, 0.3);
        color: #0284C7;
      }
      .search-results-list {
        max-height: 420px;
        overflow-y: auto;
        padding: 8px 12px;
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      .search-result-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid transparent;
        text-decoration: none;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      html.light .search-result-row {
        background: #F8FAFC;
      }
      .search-result-row:hover, .search-result-row.selected {
        background: rgba(56, 189, 248, 0.12);
        border-color: rgba(56, 189, 248, 0.3);
        transform: translateX(-2px);
      }
      html.light .search-result-row:hover, html.light .search-result-row.selected {
        background: rgba(2, 132, 199, 0.08);
        border-color: rgba(2, 132, 199, 0.28);
      }
      .result-badge {
        font-size: 1.15rem;
        width: 34px;
        height: 34px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.06);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        color: #38BDF8;
      }
      html.light .result-badge {
        background: rgba(15, 23, 42, 0.06);
        color: #0284C7;
      }
      .result-info {
        flex: 1;
        min-width: 0;
      }
      .result-title-row {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .result-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #F8FAFC;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      html.light .result-title {
        color: #0F172A;
      }
      .result-cat-label {
        font-size: 0.68rem;
        padding: 1px 6px;
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.08);
        color: #94A3B8;
      }
      html.light .result-cat-label {
        background: rgba(15, 23, 42, 0.06);
        color: #64748B;
      }
      .result-subtitle {
        font-size: 0.74rem;
        color: #94A3B8;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-top: 2px;
      }
      html.light .result-subtitle {
        color: #64748B;
      }
      .result-jump-icon {
        font-size: 0.85rem;
        color: #94A3B8;
        opacity: 0.6;
      }
      .search-modal-footer {
        padding: 10px 18px;
        background: rgba(255, 255, 255, 0.02);
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        font-size: 0.74rem;
        color: #94A3B8;
      }
      html.light .search-modal-footer {
        background: #F8FAFC;
        border-top-color: rgba(15, 23, 42, 0.06);
        color: #64748B;
      }
      .search-footer-shortcuts {
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .footer-kbd {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        padding: 1px 4px;
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
      }
      html.light .footer-kbd {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.15);
      }
      .search-empty-state {
        padding: 36px 20px;
        text-align: center;
        color: #94A3B8;
        font-size: 0.88rem;
      }

      /* =========================================================
         5. قائمة الموبايل الاحترافية (Mobile Drawer)
         ========================================================= */
      .mobile-drawer-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        z-index: 99999;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1),
                    visibility 0.3s ease;
      }
      .mobile-drawer-backdrop.open {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
      }
      .mobile-drawer-pane {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        width: 86%;
        max-width: 360px;
        background: #0F172A;
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
        transform: translateX(100%);
        transition: transform 0.34s cubic-bezier(0.32, 0.72, 0, 1);
        box-shadow: -8px 0 35px rgba(0, 0, 0, 0.6);
        padding: 18px 16px;
        box-sizing: border-box;
      }
      html.light .mobile-drawer-pane {
        background: #FFFFFF;
        border-left-color: rgba(15, 23, 42, 0.12);
        box-shadow: -8px 0 35px rgba(15, 23, 42, 0.18);
      }
      .mobile-drawer-backdrop.open .mobile-drawer-pane {
        transform: translateX(0);
      }
      .mobile-drawer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 12px;
      }
      html.light .mobile-drawer-header {
        border-bottom-color: rgba(15, 23, 42, 0.08);
      }
      .drawer-header-brand {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .drawer-app-title {
        font-size: 1.05rem;
        color: #F8FAFC;
        display: block;
        line-height: 1.2;
      }
      html.light .drawer-app-title {
        color: #0F172A;
      }
      .drawer-app-subtitle {
        font-size: 0.72rem;
        color: #94A3B8;
      }
      .mobile-drawer-close {
        background: transparent;
        border: none;
        color: #94A3B8;
        font-size: 1.3rem;
        cursor: pointer;
        padding: 4px;
      }

      /* بطاقة الإنجاز في الموبايل */
      .drawer-progress-card {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.22);
        border-radius: 12px;
        padding: 12px;
        text-decoration: none;
        margin-bottom: 10px;
        display: block;
        transition: all 0.2s ease;
      }
      html.light .drawer-progress-card {
        background: rgba(5, 150, 105, 0.06);
        border-color: rgba(5, 150, 105, 0.2);
      }
      .drawer-prog-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
      }
      .drawer-prog-title {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.82rem;
        color: #F8FAFC;
      }
      html.light .drawer-prog-title {
        color: #0F172A;
      }
      .drawer-prog-pct {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        font-weight: 800;
        color: #34D399;
      }
      html.light .drawer-prog-pct {
        color: #059669;
      }
      .drawer-prog-bar-track {
        height: 6px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 99px;
        overflow: hidden;
        margin-bottom: 6px;
      }
      html.light .drawer-prog-bar-track {
        background: rgba(15, 23, 42, 0.08);
      }
      .drawer-prog-bar-fill {
        height: 100%;
        background: #34D399;
        border-radius: 99px;
        transition: width 0.3s ease;
      }
      .drawer-prog-sub {
        font-size: 0.72rem;
        color: #94A3B8;
      }
      html.light .drawer-prog-sub {
        color: #64748B;
      }

      /* زر البحث في قائمة الموبايل */
      .drawer-search-trigger-btn {
        width: 100%;
        height: 38px;
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 0 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #94A3B8;
        font-size: 0.8rem;
        cursor: pointer;
        margin-bottom: 12px;
        font-family: inherit;
      }
      html.light .drawer-search-trigger-btn {
        background: #F1F5F9;
        border-color: rgba(15, 23, 42, 0.1);
        color: #475569;
      }
      .drawer-search-trigger-btn kbd {
        margin-right: auto;
        font-size: 0.68rem;
        padding: 2px 6px;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border-radius: 4px;
      }

      .mobile-drawer-links-wrap {
        flex: 1;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
        scroll-behavior: smooth;
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding-left: 4px;
        scrollbar-width: thin;
        scrollbar-color: rgba(56, 189, 248, 0.3) transparent;
      }
      .mobile-drawer-links-wrap::-webkit-scrollbar {
        width: 5px;
      }
      .mobile-drawer-links-wrap::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 999px;
      }
      html.light .mobile-drawer-links-wrap::-webkit-scrollbar-thumb {
        background: rgba(15, 23, 42, 0.15);
      }
      .mobile-drawer-section-label {
        font-size: 0.74rem;
        font-weight: 800;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.04em;
        margin: 8px 4px 4px;
      }
      .mobile-drawer-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.06);
        margin: 8px 0;
      }
      html.light .mobile-drawer-divider {
        background: rgba(15, 23, 42, 0.06);
      }
      .mobile-drawer-link {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        border-radius: 10px;
        text-decoration: none;
        color: #CBD5E1;
        font-weight: 700;
        font-size: 0.88rem;
        transition: all 0.15s;
      }
      html.light .mobile-drawer-link {
        color: #334155;
      }
      .mobile-drawer-link:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #FFF;
      }
      html.light .mobile-drawer-link:hover {
        background: rgba(15, 23, 42, 0.04);
        color: #0F172A;
      }
      .mobile-drawer-link.active {
        background: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.25);
      }
      html.light .mobile-drawer-link.active {
        background: rgba(2, 132, 199, 0.08);
        color: #0284C7;
        border-color: rgba(2, 132, 199, 0.25);
      }
      .drawer-link-badge {
        margin-right: auto;
        font-size: 0.68rem;
        padding: 2px 6px;
        border-radius: 5px;
        background: #38BDF8;
        color: #0B0F19;
        font-weight: 800;
      }

      /* أكورديون الأبواب في الموبايل */
      .mobile-drawer-accordion-btn {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 12px;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 10px;
        cursor: pointer;
        font-size: 0.86rem;
        margin-bottom: 6px;
      }
      html.light .mobile-drawer-accordion-btn {
        background: rgba(2, 132, 199, 0.06);
        border-color: rgba(2, 132, 199, 0.2);
      }
      .mobile-drawer-chapters-container {
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding-top: 4px;
      }
      .mobile-drawer-chapter-row {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 8px 10px;
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      html.light .mobile-drawer-chapter-row {
        background: #F8FAFC;
        border-color: rgba(15, 23, 42, 0.06);
      }
      .mobile-drawer-chapter-row.active {
        border-color: rgba(56, 189, 248, 0.35);
        background: rgba(56, 189, 248, 0.08);
      }
      .drawer-ch-header {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .drawer-ch-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 800;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        padding: 2px 5px;
        border-radius: 4px;
      }
      .drawer-prog-pill {
        font-size: 0.65rem;
        font-weight: 800;
        padding: 1px 5px;
        border-radius: 4px;
      }
      .drawer-prog-pill.done {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
      }
      .drawer-prog-pill.partial {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
      }
      .drawer-ch-name {
        font-size: 0.8rem;
        font-weight: 700;
        color: #E4E4E7;
        flex: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      html.light .drawer-ch-name {
        color: #1E293B;
      }
      .drawer-ch-pills {
        display: flex;
        gap: 6px;
      }
      .drawer-ch-pill {
        flex: 1;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        padding: 4px 6px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        text-decoration: none;
      }
      .drawer-ch-pill.quiz {
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.25);
      }
      .drawer-ch-pill.guide {
        background: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.25);
      }
      .mobile-drawer-footer {
        padding-top: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 6px;
      }
      html.light .mobile-drawer-footer {
        border-top-color: rgba(15, 23, 42, 0.08);
      }
      .mobile-control-btn {
        width: 100%;
        height: 38px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #CBD5E1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-size: 0.84rem;
        font-weight: 700;
        cursor: pointer;
        font-family: inherit;
      }
      html.light .mobile-control-btn {
        background: #F1F5F9;
        border-color: rgba(15, 23, 42, 0.1);
        color: #334155;
      }

      /* =========================================================
         6. الفوتر الموحد (Developer Signature Footer)
         ========================================================= */
      .unified-portal-footer {
        margin-top: 50px;
        background: rgba(11, 15, 25, 0.95);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px 20px 20px;
        color: #94A3B8;
        box-sizing: border-box;
      }
      html.light .unified-portal-footer {
        background: #FFFFFF;
        border-top: 1px solid rgba(15, 23, 42, 0.09);
        color: #475569;
      }
      .footer-inner-container {
        max-width: 1100px;
        margin: 0 auto;
      }
      .dev-footer-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
        padding-bottom: 18px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      }
      html.light .dev-footer-card {
        border-bottom-color: rgba(15, 23, 42, 0.06);
      }
      .dev-info-left {
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .dev-avatar-wrap {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.35rem;
        flex-shrink: 0;
      }
      html.light .dev-avatar-wrap {
        background: rgba(2, 132, 199, 0.08);
        border-color: rgba(2, 132, 199, 0.2);
      }
      .dev-text-details {
        display: flex;
        flex-direction: column;
        gap: 2px;
      }
      .dev-name-row {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }
      .dev-name {
        font-size: 1.02rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.2px;
      }
      html.light .dev-name {
        color: #0F172A;
      }
      .dev-badge {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 6px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
      }
      html.light .dev-badge {
        background: rgba(5, 150, 105, 0.1);
        border-color: rgba(5, 150, 105, 0.25);
        color: #059669;
      }
      .dev-sub-desc {
        font-size: 0.82rem;
        color: #94A3B8;
        margin: 0;
      }
      html.light .dev-sub-desc {
        color: #64748B;
      }
      .dev-links-right {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }
      .dev-pill-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 12px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #94A3B8;
        text-decoration: none;
        font-size: 0.82rem;
        font-weight: 700;
        transition: all 0.2s ease;
      }
      html.light .dev-pill-btn {
        background: rgba(15, 23, 42, 0.04);
        border-color: rgba(15, 23, 42, 0.09);
        color: #334155;
      }
      .dev-pill-btn:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: rgba(56, 189, 248, 0.35);
        color: #38BDF8;
        transform: translateY(-2px);
      }
      html.light .dev-pill-btn:hover {
        background: rgba(2, 132, 199, 0.1);
        border-color: rgba(2, 132, 199, 0.3);
        color: #0284C7;
      }
      .footer-btn-scrolltop {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #38BDF8;
        padding: 7px 12px;
        border-radius: 10px;
        font-family: inherit;
        font-size: 0.88rem;
        font-weight: 800;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
      }
      html.light .footer-btn-scrolltop {
        background: rgba(15, 23, 42, 0.04);
        border-color: rgba(15, 23, 42, 0.1);
        color: #0284C7;
      }
      .footer-btn-scrolltop:hover {
        background: rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
      }
      .dev-copyright-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        padding-top: 14px;
        font-size: 0.8rem;
        color: #64748B;
        direction: ltr;
      }
      .dev-status-pill {
        font-size: 0.72rem;
        font-weight: 700;
        color: #34D399;
        direction: ltr;
      }
      @media (max-width: 768px) {
        .dev-footer-card {
          flex-direction: column;
          align-items: flex-start;
        }
        .dev-links-right {
          width: 100%;
          justify-content: flex-start;
        }
      }
    `;
    document.head.appendChild(style);
  }

  // 9. ==================== إدارة الأحداث والتفاعل الذكي ====================
  function setupInteractiveEvents(ctx) {
    const searchDatabase = buildSearchDatabase(ctx);

    // 1. تفعيل دروبداون الأبواب والتصنيفات (Mega Dropdowns)
    function closeAllDropdowns() {
      document.querySelectorAll('.nav-dropdown-menu').forEach(m => m.classList.remove('show'));
      document.querySelectorAll('.nav-dropdown-wrapper').forEach(w => w.classList.remove('open'));
    }

    document.addEventListener('click', function (e) {
      // هل تم النقر على زر دروبداون؟
      const trigger = e.target.closest('.nav-dropdown-tab, .nav-chapters-btn');
      if (trigger) {
        e.stopPropagation();
        const wrapper = trigger.closest('.nav-dropdown-wrapper');
        const menu = wrapper ? wrapper.querySelector('.nav-dropdown-menu') : null;
        const wasOpen = menu && menu.classList.contains('show');

        closeAllDropdowns();

        if (!wasOpen && menu) {
          menu.classList.add('show');
          wrapper.classList.add('open');
          // صوت نقر اختياري
          if (window.soundEngine && typeof window.soundEngine.click === 'function') {
            try { window.soundEngine.click(); } catch (_) {}
          }
          // تركيز الإدخال عند فتح ميجا منيو الأبواب
          if (menu.id === 'chaptersDropdownMenu') {
            const filterInput = document.getElementById('chaptersMenuFilter');
            if (filterInput) setTimeout(() => filterInput.focus(), 50);
          }
        }
      } else if (!e.target.closest('.nav-dropdown-menu')) {
        closeAllDropdowns();
      }
    });

    // 2. تصفية قائمة الأبواب الـ 25 داخل الميجا منيو
    const chaptersFilter = document.getElementById('chaptersMenuFilter');
    const clearChaptersFilterBtn = document.getElementById('btnClearChaptersFilter');
    if (chaptersFilter) {
      chaptersFilter.addEventListener('input', function () {
        const q = this.value.trim().toLowerCase();
        if (clearChaptersFilterBtn) clearChaptersFilterBtn.style.display = q ? 'block' : 'none';
        const cards = document.querySelectorAll('.megamenu-ch-card');
        cards.forEach(card => {
          const haystack = (card.getAttribute('data-search') || '').toLowerCase();
          card.style.display = (!q || haystack.includes(q)) ? 'flex' : 'none';
        });
      });
    }
    if (clearChaptersFilterBtn) {
      clearChaptersFilterBtn.addEventListener('click', function () {
        if (chaptersFilter) {
          chaptersFilter.value = '';
          chaptersFilter.dispatchEvent(new Event('input'));
          chaptersFilter.focus();
        }
      });
    }

    // 3. نافذة البحث السريع الفوري (Spotlight Modal)
    const searchModal = document.getElementById('globalSearchModal');
    const searchInput = document.getElementById('globalSearchInput');
    const searchResults = document.getElementById('globalSearchResults');
    const btnOpenSearch = document.getElementById('btnOpenGlobalSearch');
    const btnOpenMobileSearch = document.getElementById('btnOpenMobileSearch');
    const btnDrawerSearch = document.getElementById('btnDrawerSearchTrigger');
    const btnCloseSearch = document.getElementById('btnCloseGlobalSearch');
    let currentFilterType = 'all';
    let selectedResultIndex = -1;

    function openSearchModal() {
      if (!searchModal) return;
      closeAllDropdowns();
      searchModal.style.display = 'flex';
      searchModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      if (searchInput) {
        searchInput.value = '';
        setTimeout(() => searchInput.focus(), 60);
        renderSearchResults('');
      }
      if (window.soundEngine && typeof window.soundEngine.click === 'function') {
        try { window.soundEngine.click(); } catch (_) {}
      }
    }

    function closeSearchModal() {
      if (!searchModal) return;
      searchModal.style.display = 'none';
      searchModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    if (btnOpenSearch) btnOpenSearch.addEventListener('click', openSearchModal);
    if (btnOpenMobileSearch) btnOpenMobileSearch.addEventListener('click', openSearchModal);
    if (btnDrawerSearch) {
      btnDrawerSearch.addEventListener('click', function () {
        const drawerBackdrop = document.getElementById('mobileDrawerBackdrop');
        if (drawerBackdrop) drawerBackdrop.classList.remove('open');
        document.querySelectorAll('.nav-hamburger-btn, .nav-mobile-hamburger').forEach(b => b.classList.remove('is-active'));
        openSearchModal();
      });
    }
    if (btnCloseSearch) btnCloseSearch.addEventListener('click', closeSearchModal);

    if (searchModal) {
      searchModal.addEventListener('click', function (e) {
        if (e.target === searchModal) closeSearchModal();
      });
    }

    // فلترة النتائج ديناميكياً
    function renderSearchResults(query) {
      if (!searchResults) return;
      const q = query.trim().toLowerCase();
      let filtered = searchDatabase.filter(item => {
        if (currentFilterType !== 'all' && item.category !== currentFilterType) return false;
        if (!q) return true;
        return item.tags.includes(q) || item.title.toLowerCase().includes(q) || item.subtitle.toLowerCase().includes(q);
      });

      if (!q && currentFilterType === 'all') {
        // عرض مقترحات سريعة عند فتح البحث وهو فارغ
        filtered = filtered.slice(0, 10);
      }

      if (filtered.length === 0) {
        searchResults.innerHTML = `
          <div class="search-empty-state">
            <span style="font-size:2rem; display:block; margin-bottom:8px;">🔍</span>
            <strong>لم يتم العثور على نتائج مطابقة لـ "${window.escapeHtml(q)}"</strong>
            <p style="margin:6px 0 0; font-size:0.78rem; opacity:0.8;">جرّب البحث برقم الباب (مثال: 14)، أو اسم الإشارة، أو كلمة إيطالية (precedenza, sempre, velocità).</p>
          </div>
        `;
        selectedResultIndex = -1;
        return;
      }

      selectedResultIndex = 0;
      searchResults.innerHTML = filtered.map((item, idx) => `
        <a href="${item.href}" class="search-result-row ${idx === 0 ? 'selected' : ''}" data-idx="${idx}">
          <div class="result-badge">${item.badge}</div>
          <div class="result-info">
            <div class="result-title-row">
              <span class="result-title">${window.escapeHtml(item.title)}</span>
              <span class="result-cat-label">${window.escapeHtml(item.categoryLabel)}</span>
            </div>
            <div class="result-subtitle">${window.escapeHtml(item.subtitle)}</div>
          </div>
          <span class="result-jump-icon">↵</span>
        </a>
      `).join('');

      // مستمع للنقر
      searchResults.querySelectorAll('.search-result-row').forEach(row => {
        row.addEventListener('click', function () {
          closeSearchModal();
        });
      });
    }

    if (searchInput) {
      searchInput.addEventListener('input', function () {
        renderSearchResults(this.value);
      });

      // مفاتيح الأسهم والانتقال
      searchInput.addEventListener('keydown', function (e) {
        const rows = searchResults ? searchResults.querySelectorAll('.search-result-row') : [];
        if (!rows.length) return;

        if (e.key === 'ArrowDown') {
          e.preventDefault();
          selectedResultIndex = (selectedResultIndex + 1) % rows.length;
          updateSelectedRow(rows);
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          selectedResultIndex = (selectedResultIndex - 1 + rows.length) % rows.length;
          updateSelectedRow(rows);
        } else if (e.key === 'Enter') {
          e.preventDefault();
          if (selectedResultIndex >= 0 && selectedResultIndex < rows.length) {
            rows[selectedResultIndex].click();
          }
        }
      });
    }

    function updateSelectedRow(rows) {
      rows.forEach((r, idx) => {
        if (idx === selectedResultIndex) {
          r.classList.add('selected');
          r.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        } else {
          r.classList.remove('selected');
        }
      });
    }

    // تصفية الفئات في مودال البحث
    const filterPills = document.querySelectorAll('.search-pill-btn');
    filterPills.forEach(pill => {
      pill.addEventListener('click', function () {
        filterPills.forEach(p => p.classList.remove('active'));
        this.classList.add('active');
        currentFilterType = this.getAttribute('data-filter') || 'all';
        if (searchInput) renderSearchResults(searchInput.value);
      });
    });

    // اختصار لوحة المفاتيح العام: Ctrl + K أو Cmd + K أو /
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        if (searchModal && searchModal.style.display === 'flex') {
          closeSearchModal();
        } else {
          openSearchModal();
        }
      } else if (e.key === 'Escape') {
        closeAllDropdowns();
        closeSearchModal();
        const drawerBackdrop = document.getElementById('mobileDrawerBackdrop');
        if (drawerBackdrop && drawerBackdrop.classList.contains('open')) {
          drawerBackdrop.classList.remove('open');
          document.querySelectorAll('.nav-hamburger-btn, .nav-mobile-hamburger').forEach(b => b.classList.remove('is-active'));
          document.body.style.overflow = '';
        }
      }
    });

    // 4. تفعيل قائمة الموبايل الاحترافية (Mobile Drawer)
    const btnOpenDrawer = document.getElementById('btnToggleMobileDrawer');
    const btnCloseDrawer = document.getElementById('btnCloseMobileDrawer');
    const drawerBackdrop = document.getElementById('mobileDrawerBackdrop');
    const allHamburgerBtns = document.querySelectorAll('.nav-hamburger-btn, .nav-mobile-hamburger');

    function openDrawer() {
      if (drawerBackdrop) drawerBackdrop.classList.add('open');
      allHamburgerBtns.forEach(btn => {
        btn.classList.add('is-active');
        btn.setAttribute('aria-expanded', 'true');
      });
      document.body.style.overflow = 'hidden';
      if (window.soundEngine && typeof window.soundEngine.click === 'function') {
        try { window.soundEngine.click(); } catch (_) {}
      }
    }

    function closeDrawer() {
      if (drawerBackdrop) drawerBackdrop.classList.remove('open');
      allHamburgerBtns.forEach(btn => {
        btn.classList.remove('is-active');
        btn.setAttribute('aria-expanded', 'false');
      });
      document.body.style.overflow = '';
    }

    if (btnOpenDrawer) {
      btnOpenDrawer.addEventListener('click', function (e) {
        e.stopPropagation();
        if (drawerBackdrop && drawerBackdrop.classList.contains('open')) {
          closeDrawer();
        } else {
          openDrawer();
        }
      });
    }
    if (btnCloseDrawer) btnCloseDrawer.addEventListener('click', closeDrawer);
    if (drawerBackdrop) {
      drawerBackdrop.addEventListener('click', function (e) {
        if (e.target === drawerBackdrop) closeDrawer();
      });
    }

    // أكورديون الأبواب في الموبايل
    const btnAcc = document.getElementById('btnToggleChaptersAccordion');
    const containerAcc = document.getElementById('mobileChaptersContainer');
    const arrowAcc = document.getElementById('chaptersAccordionArrow');
    if (btnAcc && containerAcc) {
      btnAcc.addEventListener('click', function (e) {
        e.stopPropagation();
        const isClosed = containerAcc.style.display === 'none';
        containerAcc.style.display = isClosed ? 'flex' : 'none';
        if (arrowAcc) arrowAcc.style.transform = isClosed ? 'rotate(180deg)' : 'rotate(0deg)';
      });
    }

    // إغلاق الموبايل دروة عند النقر على أي رابط
    document.querySelectorAll('.mobile-drawer-link, .drawer-ch-pill').forEach(link => {
      link.addEventListener('click', closeDrawer);
    });

    // 5. تأمين الروابط الخارجية (Link Hardening)
    document.querySelectorAll('a[href^="http"]').forEach(link => {
      if (!link.href.includes(window.location.hostname)) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
      }
    });

    // 6. تحديث حي ومستمر لشارات الإنجاز عند العودة للنافذة
    window.addEventListener('focus', function () {
      updateAllProgressBadges();
    });

    // 7. زر حساب المستخدم والمزامنة (Desktop & Mobile)
    const openAuthFn = function (e) {
      if (e) e.preventDefault();
      if (window.PatenteAuth && window.PatenteAuth.openAuthModal) {
        window.PatenteAuth.openAuthModal();
      } else {
        const m = document.getElementById('patenteAuthModal');
        if (m) m.classList.add('open');
      }
    };
    const deskAuthBtn = document.getElementById('globalAuthPill');
    if (deskAuthBtn) deskAuthBtn.onclick = openAuthFn;

    const mobAuthBtn = document.getElementById('btnOpenMobileAuth');
    if (mobAuthBtn) mobAuthBtn.onclick = openAuthFn;
  }

  // 10. ==================== تحديث فوري لشارات الإنجاز ====================
  function updateAllProgressBadges() {
    const stats = getGlobalProgressStats();
    // Desktop Pill
    const pctVal = document.getElementById('globalProgressPctVal');
    const fill = document.getElementById('globalProgressMiniFill');
    const pill = document.getElementById('globalProgressPill');
    if (pctVal) pctVal.textContent = `${stats.pct}%`;
    if (fill) fill.style.width = `${stats.pct}%`;
    if (pill) pill.setAttribute('title', `إنجازك العام: تم حل ${stats.answered} من ${stats.total} سؤال رسمي`);

    // Mobile Pill
    const mobVal = document.getElementById('globalMobileProgressVal');
    if (mobVal) mobVal.textContent = `${stats.pct}%`;

    // Mobile Drawer Banner
    const dPct = document.getElementById('drawerProgressPctVal');
    const dFill = document.getElementById('drawerProgressFill');
    const dCount = document.getElementById('drawerAnsweredCount');
    if (dPct) dPct.textContent = `${stats.pct}%`;
    if (dFill) dFill.style.width = `${stats.pct}%`;
    if (dCount) dCount.textContent = stats.answered;
  }
  window.updatePortalProgress = updateAllProgressBadges;

  // 11. ==================== التهيئة التلقائية ====================
  function initUnifiedPortalUI() {
    injectStyles();
    const ctx = getPathContext();

    // 1. تنظيف أي عناصر قديمة مكررة
    const oldDrawerPanel = document.getElementById('mobile-drawer-panel') || document.querySelector('.mobile-drawer-panel');
    const oldDrawerOverlay = document.getElementById('mobile-drawer-overlay') || document.querySelector('.mobile-drawer-overlay');
    if (oldDrawerPanel) oldDrawerPanel.remove();
    if (oldDrawerOverlay) oldDrawerOverlay.remove();

    // 2. تركيب الهيدر الموحد
    let globalNav = document.getElementById('globalPortalNav');
    if (!globalNav) {
      let oldNav = document.querySelector('.unified-portal-nav') || 
                   document.querySelector('.inc-navbar') || 
                   document.querySelector('.tr-navbar');

      const wrapper = document.createElement('div');
      wrapper.innerHTML = renderGlobalHeader(ctx);

      const newHeaderEl = wrapper.querySelector('#globalPortalNav');
      const searchModalEl = wrapper.querySelector('#globalSearchModal');
      const drawerEl = wrapper.querySelector('#mobileDrawerBackdrop');

      if (oldNav) oldNav.remove();

      const headerContainer = document.getElementById('unified-header') || document.getElementById('app-header');
      if (headerContainer) {
        headerContainer.innerHTML = '';
        headerContainer.appendChild(newHeaderEl);
      } else if (document.body.insertAdjacentElement) {
        document.body.insertAdjacentElement('afterbegin', newHeaderEl);
      } else {
        document.body.insertBefore(newHeaderEl, document.body.firstChild);
      }

      if (searchModalEl) document.body.appendChild(searchModalEl);
      if (drawerEl) document.body.appendChild(drawerEl);

      // إزالة أي أزرار رجوع قديمة مكررة
      document.querySelectorAll('.action-btn.home-btn').forEach(btn => btn.remove());
    }

    // 3. تركيب الفوتر الموحد
    let globalFooter = document.getElementById('globalPortalFooter');
    if (!globalFooter) {
      const footerContainer = document.getElementById('unified-footer') || document.getElementById('app-footer');
      if (footerContainer) {
        footerContainer.innerHTML = renderGlobalFooter(ctx);
      } else {
        document.body.insertAdjacentHTML('beforeend', renderGlobalFooter(ctx));
      }
    }

    // 4. ربط الأحداث
    setupInteractiveEvents(ctx);

    // 5. تحميل محرك المصادقة والمزامنة السحابية (Firebase Auth Engine)
    if (!window.PatenteAuth && !document.querySelector('script[src*="firebase-auth-engine.js"]')) {
      const authScript = document.createElement('script');
      authScript.src = ctx.root + 'assets/js/firebase-auth-engine.js?v=20261022_v7';
      authScript.defer = true;
      document.head.appendChild(authScript);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUnifiedPortalUI);
  } else {
    initUnifiedPortalUI();
  }

})();

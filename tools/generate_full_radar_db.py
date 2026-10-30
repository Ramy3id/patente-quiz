# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

def sanitize_q(q):
    return {
        'id': q['id'],
        'ch': q['ch'],
        'ch_name': q['ch_name'],
        'sub': q.get('sub', ''),
        'q': q['q'],
        'a': q['a'],
        'img': q.get('img', ''),
        'tr': q.get('tr', ''),
        'sp': q.get('sp', ''),
        'tb': q.get('tb', '')
    }

SIGN_RULES_INPUT = [
    {
        "id": "sign_85_consente",
        "fig": "85.png",
        "category": "divieto",
        "title_it": "Divieto di fermata (Fig. 85)",
        "title_ar": "ممنوع التوقف المؤقت والانتظار (Fig. 85)",
        "sub": "Divieto di fermata",
        "ch": 3,
        "keyword_it": "consente / permette",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ السماح بالتوقف المؤقت: الدائرة الزرقاء بإطار وشريطين متقاطعين (X) تمنع منعاً باتاً ومطلقاً كلاً من التوقف المؤقت (Fermata) والانتظار (Sosta) على مدار 24 ساعة دون أي استثناء.",
        "rule_ar": "أي سؤال يزعم أن هذه اللوحة 'consente' أو 'permette la fermata' أو تسمح بإنزال راكب فهو FALSO بنسبة 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/85.png",
        "match": lambda q: q.get('ch') == 3 and ('85.png' in q.get('img', '') or 'fermata' in q.get('sub', '').lower()) and re.search(r'\b(consente|permette)\b', q['q'], re.I) and not q['a']
    },
    {
        "id": "sign_84_fermata",
        "fig": "84.png",
        "category": "divieto",
        "title_it": "Divieto di sosta (Fig. 84)",
        "title_ar": "ممنوع الانتظار (Fig. 84)",
        "sub": "Divieto sosta",
        "ch": 3,
        "keyword_it": "consente la fermata",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "المفتاح السحري للانتظار: اللوحة بشريط أحمر مائل واحد تمنع الـ Sosta (ترك السيارة)، لكنها تسمح دائماً بالـ Fermata (التوقف المؤقت لصعود ونزول الركاب) بشرط بقاء السائق خلف المقود.",
        "rule_ar": "السؤال الذي ينص على أنها تسمح بالتوقف المؤقت (consente la fermata) هو VERO 100%. أما السؤال الذي يدعي منع الـ Fermata فهو FALSO.",
        "img": "Capitolo_03_segnali_divieto/immagini/946.png",
        "match": lambda q: q.get('ch') == 3 and ('946.png' in q.get('img', '') or '84.png' in q.get('img', '') or 'sosta' in q.get('sub', '').lower()) and re.search(r'\bfermata\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_14_filobus",
        "fig": "14.png",
        "category": "pericolo",
        "title_it": "Attraversamento tranviario (Fig. 14)",
        "title_ar": "تقاطع مع خط ترامواي (Fig. 14)",
        "sub": "Attraversamento tram",
        "ch": 2,
        "keyword_it": "filobus / filoviaria",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الترولي باص: اللوحة تحذر من خط ترام يسير على قضبان حديدية مدمجة في نهر الطريق (su rotaie)؛ وأسئلة الوزارة تخدعك بكلمة filobus (حافلة كهربائية تسير على عجلات مطاطية).",
        "rule_ar": "أي سؤال يذكر filobus أو linea filoviaria مع هذه اللوحة فهو خطأ FALSO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/14.png",
        "match": lambda q: q.get('ch') == 2 and ('14.png' in q.get('img', '') or 'tram' in q.get('sub', '').lower()) and re.search(r'filob', q['q'], re.I)
    },
    {
        "id": "sign_14_sorpasso",
        "fig": "14.png",
        "category": "pericolo",
        "title_it": "Attraversamento tranviario (Fig. 14)",
        "title_ar": "تقاطع مع خط ترامواي (Fig. 14)",
        "sub": "Attraversamento tram",
        "ch": 2,
        "keyword_it": "sorpasso a destra vietato / mai",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ حظر التجاوز المطلق: تجاوز الترام مسموح قانوناً على اليمين إذا توقف لنزول الركاب وكان هناك رصيف حماية (Salvagente)، ومسموح على اليمين أثناء سيره إذا اتسع الشارع.",
        "rule_ar": "أي سؤال يزعم أن التجاوز على اليمين ممنوع دائماً هو FALSO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/14.png",
        "match": lambda q: q.get('ch') == 2 and ('14.png' in q.get('img', '') or 'tram' in q.get('sub', '').lower()) and re.search(r'\bsorpass', q['q'], re.I) and not q['a']
    },
    {
        "id": "sign_1_dossi",
        "fig": "1.png",
        "category": "pericolo",
        "title_it": "Strada dissestata (Fig. 1)",
        "title_ar": "طريق وعر / غير مستوي (Fig. 1)",
        "sub": "Strada dissestata",
        "ch": 2,
        "keyword_it": "dossi artificiali / serie di dossi",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ المطبات الصناعية: هذه الإشارة تحذر من هبوط وتعرج وتلف طبيعي في طبقة الرصف (pavimentazione irregolare)، وليست مطبات صناعية لتهدئة السرعة إطلاقاً!",
        "rule_ar": "أي سؤال يربط هذه الإشارة بـ 'dossi artificiali' هو FALSO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/902.png",
        "match": lambda q: q.get('ch') == 2 and ('902.png' in q.get('img', '') or '1.png' in q.get('img', '') or 'dissestata' in q.get('sub', '').lower()) and re.search(r'\b(dossi|artificial)\b', q['q'], re.I) and not q['a']
    },
    {
        "id": "sign_2_visibilita",
        "fig": "2.png",
        "category": "pericolo",
        "title_it": "Dosso stradale (Fig. 2)",
        "title_ar": "مطب طبيعي محدب يحجب الرؤية (Fig. 2)",
        "sub": "Dosso",
        "ch": 2,
        "keyword_it": "visibilità limitata / ridotta",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "المفتاح الأساسي: الخطر الجوهري للـ Dosso هو حجب الرؤية في الصعود (visibilità limitata)، لذا تنخفض السرعة لحظر رؤية المركبات القادمة خلف القمة.",
        "rule_ar": "الأسئلة التي تذكر ضعف الرؤية (visibilità limitata) أو صعود يليه نزول هي VERO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/2.png",
        "match": lambda q: q.get('ch') == 2 and ('2.png' in q.get('img', '') or 'dosso' in q.get('sub', '').lower()) and re.search(r'\b(visibilit|limitata|salita)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_3_cunetta",
        "fig": "3.png",
        "category": "pericolo",
        "title_it": "Cunetta (Fig. 3)",
        "title_ar": "منخفض طريق / مجرى سيل مقعر (Fig. 3)",
        "sub": "Cunetta",
        "ch": 2,
        "keyword_it": "allagamento / accumulo d'acqua",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "مفتاح تجمع المياه: الـ Cunetta هبوط مقعر تتجمع فيه مياه الأمطار أو الطين مسببة انزلاقاً خطيراً وتطاير مياه على الزجاج.",
        "rule_ar": "الأسئلة التي تذكر تجمع المياه (accumulo d'acqua) أو الغمر (allagamento) أو نزول يليه صعود هي VERO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/3.png",
        "match": lambda q: q.get('ch') == 2 and ('3.png' in q.get('img', '') or 'cunetta' in q.get('sub', '').lower()) and re.search(r'\b(acqua|allagament|discesa)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_8_croce",
        "fig": "8.png",
        "category": "pericolo",
        "title_it": "Passaggio a livello con barriere (Fig. 8)",
        "title_ar": "مزلقان قطار بحواجز كاملة (Fig. 8)",
        "sub": "Passaggio livello barriere",
        "ch": 2,
        "keyword_it": "Croce di S. Andrea",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ صليب أندريا: صليب سان أندريا (Croce di S. Andrea) يوضع حصرياً أمام المزلقان الخالي من الحواجز (SENZA barriere). وجوده مع مزلقان البوابات خطأ وزاري فادح!",
        "rule_ar": "أي سؤال يضع صليب أندريا مع لوحة المزلقان ذي الحواجز فهو FALSO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/8.png",
        "match": lambda q: q.get('ch') == 2 and ('8.png' in q.get('img', '') or 'barriere' in q.get('sub', '').lower()) and re.search(r'\b(croce|andrea)\b', q['q'], re.I)
    },
    {
        "id": "sign_9_croce",
        "fig": "9.png",
        "category": "pericolo",
        "title_it": "Passaggio a livello senza barriere (Fig. 9)",
        "title_ar": "مزلقان قطار بدون حواجز (Fig. 9)",
        "sub": "Ferrovia senza barriere",
        "ch": 2,
        "keyword_it": "Croce di S. Andrea / due luci rosse",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "المفتاح الصريح: المزلقان المكشوف بدون بوابات تتبعه مباشرة لوحة صليب سان أندريا ومصباحان أحمران يومضان بالتبادل.",
        "rule_ar": "الأسئلة التي تذكر صليب أندريا أو وميض الضوءين الأحمرين مع هذه اللوحة هي VERO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/9.png",
        "match": lambda q: q.get('ch') == 2 and ('9.png' in q.get('img', '') or 'senza barriere' in q.get('sub', '').lower()) and re.search(r'\b(croce|due luci|lampeggianti)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_17_discesa_folle",
        "fig": "17.png",
        "category": "pericolo",
        "title_it": "Discesa pericolosa (Fig. 17)",
        "title_ar": "منحدر خطر بنسبة انحدار محددة (Fig. 17)",
        "sub": "Discesa pericolosa",
        "ch": 2,
        "keyword_it": "in folle / frizione abbassata / spento",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الدبرياج والمور: السير في المنحدر والدبرياج مضغوط أو على المور (in folle) أو مع إطفاء المحرك يفصل فرامل الموتور ويسخن الفرامل حتى تحترق وتفشل تماماً!",
        "rule_ar": "أي سؤال يطلب الضغط على الدبرياج أو وضع الفتيس في المور أو إطفاء المحرك في المنحدر هو FALSO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/17.png",
        "match": lambda q: q.get('ch') == 2 and ('17.png' in q.get('img', '') or '18.png' in q.get('img', '') or 'discesa' in q.get('sub', '').lower()) and re.search(r'\b(folle|frizione|spento)\b', q['q'], re.I)
    },
    {
        "id": "sign_17_discesa_marcia_bassa",
        "fig": "17.png",
        "category": "pericolo",
        "title_it": "Discesa pericolosa (Fig. 17)",
        "title_ar": "منحدر خطر بنسبة انحدار محددة (Fig. 17)",
        "sub": "Discesa pericolosa",
        "ch": 2,
        "keyword_it": "marcia bassa / freno motore",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "القاعدة الذهبية للمنحدر: النزول يجب أن يكون بغيار منخفض مناسب (marcia bassa) لتفعيل فرملة المحرك وحماية فرامل العجلات من ارتفاع الحرارة والتلف.",
        "rule_ar": "الأسئلة التي توصي بـ marcia bassa أو استخدام freno motore في المنحدر هي VERO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/17.png",
        "match": lambda q: q.get('ch') == 2 and ('17.png' in q.get('img', '') or '18.png' in q.get('img', '') or 'discesa' in q.get('sub', '').lower()) and re.search(r'\b(marcia bassa|freno motore|adeguatamente)\b', q['q'], re.I)
    },
    {
        "id": "sign_54_divieto_transito",
        "fig": "54.png",
        "category": "divieto",
        "title_it": "Divieto di transito (Fig. 54)",
        "title_ar": "ممنوع مرور جميع المركبات في الاتجاهين (Fig. 54)",
        "sub": "Divieto di transito",
        "ch": 3,
        "keyword_it": "entrambi i sensi / tutti i veicoli",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "المفتاح الصارم: الدائرة الحمراء البيضاء الفارغة تمنع المرور من كلا الاتجاهين (entrambi i sensi) لجميع أنواع المركبات.",
        "rule_ar": "السؤال الذي ينص على المنع في الاتجاهين (da entrambi i sensi) هو VERO 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/54.png",
        "match": lambda q: q.get('ch') == 3 and ('54.png' in q.get('img', '') or 'divieto di transito' in q.get('sub', '').lower()) and re.search(r'\bentrambi\b', q['q'], re.I)
    },
    {
        "id": "sign_55_senso_vietato",
        "fig": "55.png",
        "category": "divieto",
        "title_it": "Senso vietato (Fig. 55)",
        "title_ar": "ممنوع الدخول / اتجاه واحد قادم (Fig. 55)",
        "sub": "Senso vietato",
        "ch": 3,
        "keyword_it": "entrambi i sensi",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الاتجاهين: القرص الأحمر مع شريط أبيض أفقي يمنع الدخول من هذه الجهة فقط لأن الطريق باتجاه واحد قادم نحوك (senso unico)؛ فلا يمنع الاتجاهين!",
        "rule_ar": "أي سؤال يدعي أن هذه اللوحة تمنع السير في كلا الاتجاهين فهو FALSO 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/55.png",
        "match": lambda q: q.get('ch') == 3 and ('55.png' in q.get('img', '') or 'senso vietato' in q.get('sub', '').lower()) and re.search(r'\bentrambi\b', q['q'], re.I)
    },
    {
        "id": "sign_56_divieto_sorpasso",
        "fig": "56.png",
        "category": "divieto",
        "title_it": "Divieto di sorpasso (Fig. 56)",
        "title_ar": "ممنوع التجاوز للسيارات (Fig. 56)",
        "sub": "Divieto sorpasso",
        "ch": 3,
        "keyword_it": "senza motore / ciclomotori / motocicli",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "استثناء التجاوز المسموح: رغم منع التجاوز، يُسمح لك بتجاوز المركبات عديمة المحرك (عربات الخيل، الدراجات) والسيكلوموتوري والموتوسيكل بشرط عدم تخطي الخط المتصل وعدم غزو المسار المعاكس!",
        "rule_ar": "السؤال الذي يجيز تجاوز veicoli sprovvisti di motore أو ciclomotori senza superare la striscia continua هو VERO 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/56.png",
        "match": lambda q: q.get('ch') == 3 and ('56.png' in q.get('img', '') or 'sorpasso' in q.get('sub', '').lower()) and re.search(r'\b(senza motore|sprovvisti|ciclomotori|due ruote|motocicli)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_68_merci_autobus",
        "fig": "68.png",
        "category": "divieto",
        "title_it": "Divieto veicoli merci oltre 3,5 t (Fig. 68)",
        "title_ar": "ممنوع لشاحنات نقل البضائع فوق 3.5 طن (Fig. 68)",
        "sub": "Transito autocarri 3.5 t",
        "ch": 3,
        "keyword_it": "autobus / persone",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الأوتوبيس: الرمز يمثل شاحنة بضائع، لذا ينطبق فقط على نقل البضائع (trasporto merci/cose)؛ ولا ينطبق إطلاقاً على أوتوبيسات الركاب أو الكرفانات حتى لو زادت عن 3.5 طن!",
        "rule_ar": "أي سؤال يدعي أن هذه اللوحة تنطبق على الأوتوبيس (autobus) هو FALSO 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/68.png",
        "match": lambda q: q.get('ch') == 3 and ('68.png' in q.get('img', '') or '3.5 t' in q.get('sub', '').lower()) and re.search(r'\b(autobus|persone)\b', q['q'], re.I)
    },
    {
        "id": "sign_101_passaggio_obbligatorio",
        "fig": "101.png",
        "category": "obbligo",
        "title_it": "Passaggio obbligatorio a sinistra (Fig. 101)",
        "title_ar": "مرور إلزامي من يسار العائق (Fig. 101)",
        "sub": "Passaggio sinistra",
        "ch": 4,
        "keyword_it": "svoltare a sinistra / incrocio",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الانعطاف في التقاطع: السهم المائل 45 درجة يلزمك بالمرور من يسار عائق أو جزيرة طريق (ostacolo)، ولا يلزمك بالانعطاف يساراً في تقاطع كما تدعي الأسئلة الخادعة!",
        "rule_ar": "أي سؤال يزعم أن السهم المائل يلزمك بالدوران (svoltare a sinistra) في تقاطع هو FALSO 100%.",
        "img": "Capitolo_04_segnali_obbligo/immagini/101.png",
        "match": lambda q: q.get('ch') == 4 and ('101.png' in q.get('img', '') or 'passaggio' in q.get('sub', '').lower()) and re.search(r'\b(svoltare)\b', q['q'], re.I)
    },
    {
        "id": "sign_41_stop_arrestarsi",
        "fig": "41.png",
        "category": "precedenza",
        "title_it": "Fermarsi e dare precedenza - STOP (Fig. 41)",
        "title_ar": "قف وأعطِ الأسبقية - STOP (Fig. 41)",
        "sub": "Segnale stop",
        "ch": 5,
        "keyword_it": "arrestarsi / linea trasversale",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "القاعدة الذهبية المطلقة لـ STOP: يجب التوقف التام للعجلات عند خط الوقوف المستعرض (striscia trasversale di arresto) وإعطاء الأسبقية لليمين واليسار حتى لو كان الطريق خالياً تماماً!",
        "rule_ar": "الأسئلة التي تفرض التوقف التام (arrestarsi) عند خط التوقف هي VERO 100%. وأي سؤال يقول يكفي التهدئة بدون توقف هو FALSO.",
        "img": "Capitolo_05_segnali_precedenza/immagini/41.png",
        "match": lambda q: q.get('ch') == 5 and ('41.png' in q.get('img', '') or 'stop' in q.get('sub', '').lower()) and re.search(r'\b(arrestarsi|striscia trasversale)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_45_sensi_unici_diritto",
        "fig": "45.png",
        "category": "precedenza",
        "title_it": "Dare precedenza nei sensi unici alternati (Fig. 45)",
        "title_ar": "إعطاء الأسبقية في المسار التبادلي (Fig. 45)",
        "sub": "Sensi unici alternati",
        "ch": 5,
        "keyword_it": "diritto di precedenza",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ حق الأسبقية: اللوحة الدائرية بالحد الأحمر تلزمك بالتنازل عن الأسبقية للقادم في مواجهتك؛ بينما اللوحة المربعة الزرقاء (Fig. 53) هي التي تمنحك حق الأسبقية.",
        "rule_ar": "أي سؤال يدعي أن اللوحة الدائرية تمنحك حق الأسبقية (diritto di precedenza) هو FALSO 100%.",
        "img": "Capitolo_05_segnali_precedenza/immagini/45.png",
        "match": lambda q: q.get('ch') == 5 and ('45.png' in q.get('img', '') or 'sensi unici' in q.get('sub', '').lower()) and re.search(r'\b(diritto di precedenza)\b', q['q'], re.I)
    },
    {
        "id": "sign_509_doppia_striscia",
        "fig": "509.png",
        "category": "orizzontale",
        "title_it": "Doppia striscia continua (Fig. 509)",
        "title_ar": "الخط المزدوج الأبيض المتصل (Fig. 509)",
        "sub": "Doppia striscia continua",
        "ch": 6,
        "keyword_it": "oltrepassare / sormontare / a cavallo",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "محرمات الخط المزدوج: الخط المزدوج كالجدار الخرساني؛ لا يجوز تخطيه أو ركوبه بالعجلات (a cavallo) أو الالتفاف منه بتاتاً في أي ظرف.",
        "rule_ar": "أي سؤال يدعي جواز دهس الخط المزدوج أو السير راكباً عليه فهو FALSO 100%.",
        "img": "Capitolo_06_segnaletica_orizzontale_ostacoli/immagini/509.png",
        "match": lambda q: q.get('ch') == 6 and ('509.png' in q.get('img', '') or 'doppia striscia' in q.get('sub', '').lower()) and re.search(r'\b(superata|cavallo|oltrepassar)\b', q['q'], re.I) and not q['a']
    }
]

THEORY_RULES_INPUT = [
    {
        "id": "theory_soccorso_bere",
        "topic": "🚑 الإسعافات الأولية (Primo Soccorso)",
        "category": "soccorso",
        "ch": 22,
        "title_ar": "محرّمات الإسعاف: إعطاء السوائل أو الكحول أو الطعام",
        "title_it": "Divieto assoluto di somministrare bevande o alcool",
        "keywords_it": "dare da bere / acqua / bevande alcoliche / superalcolici",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "قاعدة إنقاذ الحياة: يُمنع منعاً باتاً ومطلقاً إعطاء المصاب في حادث سير أي ماء أو سوائل أو كحول، لتفادي الاختناق وارتجاع السوائل إلى الرئتين خاصة عند فقدان الوعي أو الصدمة.",
        "why_trap_ar": "الوزارة تحاول استدراج تعاطفك بعبارات إنسانية خادعة مثل 'إعطاء الماء لتهدئة المصاب' أو 'إعطاء جرعة كحول لتدفئته' - احذر، كلها FALSO فوري!",
        "match": lambda q: q.get('ch') == 22 and re.search(r'\b(bere|bevande|acqua|superalcolic)\b', q['q'], re.I) and not q['a']
    },
    {
        "id": "theory_soccorso_shock_gambe",
        "topic": "🚑 الإسعافات الأولية (Primo Soccorso)",
        "category": "soccorso",
        "ch": 22,
        "title_ar": "علاج الصدمة (Shock): التمديد ورفع القدمين وتغطيته",
        "title_it": "Ferito in stato di shock: disteso con gambe sollevate e coperto",
        "keywords_it": "stato di shock / gambe sollevate / coperto",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "إسعاف الصدمة الصحيح: المصاب بالصدمة يعاني من هبوط حاد في ضغط الدم وبرودة أطراف، لذا يجب تمديده على ظهره ورفع ساقيه للأعلى لإعادة تدفق الدم للدماغ، وتغطيته لتدفئته.",
        "why_trap_ar": "الأسئلة التي تطلب رفع الساقين (gambe sollevate) أو تغطية المصاب (coperto per evitare che si raffreddi) هي VERO 100%. وأي سؤال يطلب جعله يمشي أو ضربه كفوف هو FALSO.",
        "match": lambda q: q.get('ch') == 22 and re.search(r'\b(gambe sollevate|coperto|evitare che si raffreddi)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "theory_soccorso_ustioni",
        "topic": "🚑 الإسعافات الأولية (Primo Soccorso)",
        "category": "soccorso",
        "ch": 22,
        "title_ar": "إسعاف الحروق: الماء البارد وعدم نزع الملابس الملتصقة",
        "title_it": "Ustioni: acqua fredda e non togliere i vestiti attaccati",
        "keywords_it": "ustioni / acqua fredda / vestiti attaccati",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "قواعد الحروق الصارمة: يُستعمل الماء البارد فقط لتخفيف ألم الحرق، ويُمنع منعاً باتاً نزع الملابس الملتصقة بالجلد المحروق لتفادي سلخ الأنسجة، ويُمنع وضع الكحول أو المراهم.",
        "why_trap_ar": "الأسئلة التي تنصح بعدم نزع الملابس الملتصقة واستخدام الماء البارد هي VERO 100%.",
        "match": lambda q: q.get('ch') == 22 and 'ustion' in q.get('sub', '').lower()
    },
    {
        "id": "theory_soccorso_fratture",
        "topic": "🚑 الإسعافات الأولية (Primo Soccorso)",
        "category": "soccorso",
        "ch": 22,
        "title_ar": "إسعاف الكسور: تثبيت العضو ومنع تحريكه مطلقاً",
        "title_it": "Fratture: bloccare gli arti senza muoverli",
        "keywords_it": "fratture agli arti / non muovere / bloccarli",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "تثبيت الكسر: المصاب بكسور في أطرافه يجب تثبيت العضو المكسور (bloccarlo) دون تحريكه، وتغطية الجرح إن وجد، وانتظار سيارة الإسعاف لتجنب قطع الأعصاب أو الشرايين.",
        "why_trap_ar": "الأسئلة التي تطلب تثبيت الكسر وعدم تحريكه هي VERO 100%. وأي سؤال يطلب إعادة العظم البارز لمكانه أو المشي هو FALSO.",
        "match": lambda q: q.get('ch') == 22 and 'fratture' in q.get('sub', '').lower()
    },
    {
        "id": "theory_soccorso_corpo_estraneo",
        "topic": "🚑 الإسعافات الأولية (Primo Soccorso)",
        "category": "soccorso",
        "ch": 22,
        "title_ar": "جسم غريب في العين أو الجسد: التضميد دون محاولة النزع",
        "title_it": "Corpo estraneo: bendare senza rimuovere o toccare",
        "keywords_it": "corpo estraneo / bendare / non toccare",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "المسعف لا ينزع الأجسام الغريبة: إذا دخل جسم غريب في العين أو انغرس في الجسم، يجب فقط تضميده بشاش نظيف لمنع حركته، وتركه للمتخصصين في المستشفى.",
        "why_trap_ar": "الأسئلة التي توصي بتضميد العين وعدم لمسها هي VERO 100%، بينما محاولة استخراجه بالقوة هي FALSO.",
        "match": lambda q: q.get('ch') == 22 and 'corpo estraneo' in q.get('sub', '').lower()
    },
    {
        "id": "theory_assicurazione_penale",
        "topic": "🛡️ التأمين والمسؤولية (Assicurazione RCA)",
        "category": "assicurazione",
        "ch": 23,
        "title_ar": "المسؤولية الجنائية شخصية لا يغطيها التأمين إطلاقاً",
        "title_it": "Responsabilità penale è personale (non coperta da RCA)",
        "keywords_it": "responsabilità penale / coperta dall'assicurazione",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "مبدأ دستوري إيطالي: المسؤولية الجنائية شخصية (La responsabilità penale è personale)؛ تأمين السيارات RCA يغطي فقط المسؤولية المدنية والأضرار المادية للغير، ولا يحمي من الحبس أو العقوبة الجنائية إطلاقاً.",
        "why_trap_ar": "أي سؤال يزعم أن التأمين يعفي السائق من المسؤولية الجنائية أو يدفع عقوبتها هو FALSO 100%.",
        "match": lambda q: q.get('ch') == 23 and 'penale' in q.get('sub', '').lower()
    },
    {
        "id": "theory_assicurazione_fondo",
        "topic": "🛡️ التأمين والمسؤولية (Assicurazione RCA)",
        "category": "assicurazione",
        "ch": 23,
        "title_ar": "صندوق ضمان ضحايا الطريق لتعويض حوادث الهاربين وغير المؤمنين",
        "title_it": "Fondo di garanzia per le vittime della strada",
        "keywords_it": "Fondo di garanzia per le vittime della strada",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "حماية الضحايا: أنشئ هذا الصندوق لتعويض الأضرار الجسدية عندما تكون المركبة المتسببة مجهولة وهربت (veicolo non identificato) أو غير مؤمنة (non coperto da assicurazione).",
        "why_trap_ar": "الأسئلة التي تصف دور صندوق Fondo di garanzia في تعويض هذه الحالات صحيحة VERO 100%.",
        "match": lambda q: q.get('ch') == 23 and 'fondo garanzia' in q.get('sub', '').lower()
    },
    {
        "id": "theory_assicurazione_scaduta",
        "topic": "🛡️ التأمين والمسؤولية (Assicurazione RCA)",
        "category": "assicurazione",
        "ch": 23,
        "title_ar": "انتهاء التأمين: حظر السير والوقوف في الشارع العام ومصادرة السيارة",
        "title_it": "Assicurazione scaduta: divieto di circolazione e sosta, confisca",
        "keywords_it": "assicurazione scaduta / sanzione / confisca / vietato sosta",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "لا استثناء للمركبة غير المؤمنة: يُمنع منعاً باتاً قيادتها أو حتى ركنها (sosta) في أي طريق عام، وتتعرض للغرامة والمصادرة (confisca). ولا يُسمح بها حتى للمشاوير القصيرة.",
        "why_trap_ar": "الأسئلة التي تبيح استخدامها للمشاوير القصيرة أو ركنها في الشارع هي FALSO 100%.",
        "match": lambda q: q.get('ch') == 23 and 'assicurazione scaduta' in q.get('sub', '').lower()
    },
    {
        "id": "theory_cinture_purché",
        "topic": "💺 أحزمة الأمان والخوذة (Cinture e Casco)",
        "category": "cinture",
        "ch": 19,
        "title_ar": "أفخاخ استثناءات الحزام الوهمية: بشرط السرعة المنخفضة أو المشاوير القصيرة",
        "title_it": "Falsi esoneri cinture (purché a bassa velocità / percorso breve)",
        "keywords_it": "purché / bassa velocità / breve percorso / solo in città",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "إلزامية الحزام المطلقة: الحزام إجباري داخل وخارج المدينة، وعلى أي سرعة حتى لو كانت 10 كم/س، وفي كل مشوار مهما كان قصيراً.",
        "why_trap_ar": "الأسئلة التي تضع شرط 'purché' (بشرط ألا تتجاوز السرعة 30 كم/س، أو بشرط السير في المدينة) كلها مصائد كاذبة FALSO 100%.",
        "match": lambda q: q.get('ch') == 19 and re.search(r'\b(purché|bassa velocità|breve percorso)\b', q['q'], re.I) and not q['a']
    },
    {
        "id": "theory_airbag_caratteristiche",
        "topic": "💺 أحزمة الأمان والوسائد الهوائية (Airbag)",
        "category": "cinture",
        "ch": 19,
        "title_ar": "الوسادة الهوائية (Airbag): تنتفخ في أجزاء من الألف من الثانية وتعمل مع الحزام",
        "title_it": "Caratteristiche airbag: millisecondi, complementare alla cintura",
        "keywords_it": "millisecondi / non va usato insieme / premendo un pulsante",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "حقائق الأيرباج: ينتفخ الأيرباج آلياً عبر حساس في أجزاء من الألف من الثانية (millisecondi)، وهو خطير إذا لم يُربط الحزام، ولا يغني عن الحزام بل يكمله.",
        "why_trap_ar": "الأسئلة التي تزعم أنه ينتفخ في بضع ثوانٍ (secondi) أو بضغط زر أو يلغي الحزام هي FALSO 100%.",
        "match": lambda q: q.get('ch') == 19 and 'airbag' in q.get('sub', '').lower()
    },
    {
        "id": "theory_distanza_quadruplica",
        "topic": "📏 السرعة ومسافة الأمان (Velocità e Distanza)",
        "category": "distanza",
        "ch": 11,
        "title_ar": "العلاقة التربيعية: مضاعفة السرعة تضاعف مسافة الفرملة 4 مرات",
        "title_it": "Raddoppio velocità comporta quadruplicazione spazio frenatura",
        "keywords_it": "quadruplica / se la velocità raddoppia",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "القاعدة الفيزيائية: مسافة الفرملة تتناسب طردياً مع مربع السرعة (v²). إذا ضاعفت سرعتك من 50 إلى 100 كم/س، فمسافة الفرملة لا تتضاعف مرتين بل تتضاعف 4 مرات (quadruplica)!",
        "why_trap_ar": "السؤال الذي يقول 'quadruplica' صحيح VERO 100%، بينما السؤال الذي يقول تتضاعف مرتين 'raddoppia' خطأ FALSO 100%.",
        "match": lambda q: (q.get('ch') in [11, 12]) and re.search(r'\bquadruplica\b', q['q'], re.I)
    },
    {
        "id": "theory_alcool_caffe",
        "topic": "🍷 الكحول والمخدرات (Alcool e Droga)",
        "category": "alcool",
        "ch": 22,
        "title_ar": "خرافات القضاء على الكحول: القهوة والدش البارد والأطعمة المالحة",
        "title_it": "Miti falsi: caffè, doccia fredda o cibi non eliminano l'alcool",
        "keywords_it": "caffè / doccia fredda / cibi salati / recuperare velocemente",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "الحقيقة البيولوجية: الكبد وحده هو الذي يفتت الكحول في الدم بمعدل بطيء ثابت. شرب قهوة مركزة أو أخذ دش بارد أو أكل أطعمة مالحة لا يقلل نسبة الكحول إطلاقاً ولا يسرع تخلص الجسم منه.",
        "why_trap_ar": "أي سؤال يدعي أن فنجان قهوة أو هواء بارداً يتيح لك القيادة أو يخفض الكحول هو FALSO 100%.",
        "match": lambda q: q.get('ch') == 22 and re.search(r'\b(caffè|doccia|salati)\b', q['q'], re.I)
    },
    {
        "id": "theory_patente_punti_perdita",
        "topic": "📋 رخص القيادة والنقاط (Patente e Punti)",
        "category": "patente",
        "ch": 20,
        "title_ar": "قواعد خصم النقاط: السرعة والتجاوز والهاتف وحزام الأمان",
        "title_it": "Perdita punti patente per infrazioni gravi",
        "keywords_it": "perdita di punti / decurtazione / raddoppiano per neopatentati",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "نظام النقاط: تجاوز السرعة بأكثر من 10 كم/س، استخدام الهاتف باليد، عدم ربط الحزام، أو عدم ارتداء الخوذة كلها مخالفات تسحب نقاطاً من الرصيد (20 نقطة مبدئياً)، وتتضاعف للجدد في أول 3 سنوات.",
        "why_trap_ar": "الأسئلة التي تذكر خصم النقاط لهذه المخالفات هي VERO 100%.",
        "match": lambda q: q.get('ch') == 20 and 'perdita punti' in q.get('sub', '').lower()
    },
    {
        "id": "theory_patente_revisione",
        "topic": "📋 رخص القيادة والنقاط (Patente e Punti)",
        "category": "patente",
        "ch": 20,
        "title_ar": "إعادة الفحص (Revisione della patente): عند تصفير النقاط أو الشك في الأهلية",
        "title_it": "Revisione della patente per azzeramento punti o incidente grave",
        "keywords_it": "revisione della patente / esame di idoneità / visita medica",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "شروط مراجعة الرخصة: تفرض الـ Motorizzazione أو المحافظ (Prefetto) إعادة الفحص الطبي أو النظري/العملي عند فقدان جميع النقاط (صفر) أو وقوع حادث بإصابات جسيمة.",
        "why_trap_ar": "الأسئلة التي تصف أسباب فرض الـ Revisione هي VERO 100%.",
        "match": lambda q: q.get('ch') == 20 and 'revisione patente' in q.get('sub', '').lower()
    },
    {
        "id": "theory_sosta_salvo_diversa",
        "topic": "🛑 الوقوف والتوقف (Sosta e Fermata)",
        "category": "sosta",
        "ch": 16,
        "title_ar": "قاعدة الاستثناء الموثقة: ما لم توجد إشارة مخالفة (Salvo diversa segnalazione)",
        "title_it": "Regola generale 'salvo diversa segnalazione'",
        "keywords_it": "salvo diversa segnalazione",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "صيغة المرونة القانونية: عبارة 'salvo diversa segnalazione' تؤكد أن القاعدة العامة تسري ما لم توضع لوحة استثنائية في المكان، وهي إحدى أشهر العبارات الوزارية التي تأتي VERO دائماً.",
        "why_trap_ar": "أي سؤال في باب التوقف والانتظار يتضمن عبارة 'salvo diversa segnalazione' هو VERO 100%.",
        "match": lambda q: q.get('ch') == 16 and re.search(r'\bsalvo diversa\b', q['q'], re.I)
    },
    {
        "id": "theory_meccanica_pneumatici",
        "topic": "🔧 الميكانيكا والصيانة (Meccanica e Manutenzione)",
        "category": "meccanica",
        "ch": 25,
        "title_ar": "سلامة الإطارات: فحص الضغط دورياً (بما فيها عجلة الطوارئ) وعمق النقشة 1.6 مم",
        "title_it": "Pressione periodica compresa ruota di scorta, spessore 1,6 mm",
        "keywords_it": "ruota di scorta / 1,6 millimetri / periodica",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "قواعد الإطارات الصارمة: يجب فحص ضغط الهواء دورياً بما فيها عجلة الاحتياط (ruota di scorta)، والحد الأدنى لنقشة الإطار للسيارات هو 1.6 مم، وللدراجات 1.0 مم، وللسيكلوموتوري 0.5 مم.",
        "why_trap_ar": "السؤال الذي يذكر شمول عجلة الطوارئ (ruota di scorta) أو حد 1.6 مم للسيارات هو VERO 100%.",
        "match": lambda q: (q.get('ch') == 25 and re.search(r'\b(ruota di scorta|1,6 millimetri)\b', q['q'], re.I)) or ('battistrada degli pneumatici di un autoveicolo' in q['q'])
    },
    {
        "id": "theory_meccanica_olio",
        "topic": "🔧 الميكانيكا والصيانة (Meccanica e Manutenzione)",
        "category": "meccanica",
        "ch": 25,
        "title_ar": "فحص مستوى زيت المحرك: المحرك مطفأ تماماً وعلى أرض مستوية",
        "title_it": "Controllo livello olio a motore spento e in piano",
        "keywords_it": "motore spento / in piano / motore acceso",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "فحص الزيت: يُفحص مقاس الزيت والمحرك مطفأ منذ بضع دقائق (spento da alcuni minuti) والسيارة على أرض مستوية (in piano) ليركد الزيت في الكارتير. فحصه والمحرك يدور خطأ فادح يعطي قراءة فارغة.",
        "why_trap_ar": "الأسئلة التي تطلب الفحص a motore spento e in piano صحيحة VERO 100%، بينما a motore in moto هي FALSO 100%.",
        "match": lambda q: q.get('ch') == 25 and 'livello olio' in q.get('sub', '').lower()
    }
]

print("Compiling Sign Rules...")
total_sign_qs = 0
for r in SIGN_RULES_INPUT:
    matched = [sanitize_q(q) for q in questions if r['match'](q)]
    r['questions'] = matched
    r['count'] = len(matched)
    total_sign_qs += len(matched)
    del r['match']
    print(f" - [{r['category']}] {r['id']}: {r['count']} questions")

print(f"\nTotal Sign Questions: {total_sign_qs}")

print("\nCompiling Theory Rules...")
total_theory_qs = 0
for r in THEORY_RULES_INPUT:
    matched = [sanitize_q(q) for q in questions if r['match'](q)]
    r['questions'] = matched
    r['count'] = len(matched)
    total_theory_qs += len(matched)
    del r['match']
    print(f" - [{r['category']}] {r['id']}: {r['count']} questions")

print(f"\nTotal Theory Questions: {total_theory_qs}")

js_code = f"""// Auto-generated Expanded Radar Dataset
// Tab 2: Sign-Trap Radar (Chapters 1 - 10)
// Tab 3: Theoretical Golden Rules (Chapters 11 - 25)

const RADAR_SIGN_TRAPS = {json.dumps(SIGN_RULES_INPUT, ensure_ascii=False, indent=2)};

const RADAR_THEORY_RULES = {json.dumps(THEORY_RULES_INPUT, ensure_ascii=False, indent=2)};
"""

with open('R:/Ramy/PATENTE/assets/js/data-radar-expanded.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("\nSuccessfully compiled R:/Ramy/PATENTE/assets/js/data-radar-expanded.js")

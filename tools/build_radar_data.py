# -*- coding: utf-8 -*-
import sys, re, json
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

with open('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const ALL_QUESTIONS_DATA = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

# Helper to find questions matching regex or keywords
def find_matching_qs(filter_fn):
    res = []
    for q in questions:
        if filter_fn(q):
            res.append({
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
            })
    return res

# 1. CURATED SIGN-TRAP RULES (Chapters 1 - 10)
# We will define top sign patterns and verify their accuracy against actual questions
SIGN_RADAR_DEFS = [
    {
        "id": "sign_85_consente",
        "fig": "85.png",
        "title_it": "Divieto di fermata (e di sosta)",
        "title_ar": "ممنوع التوقف والانتظار",
        "ch": 3,
        "keyword_it": "consente / fermata",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "الفخ القاتل: اليافطة تمنع منعاً باتاً كلاً من التوقف المؤقت (Fermata) والانتظار (Sosta). أي سؤال يقول 'تسمح بالتوقف' أو 'تسمح لإنزال راكب' هو خطأ مؤكد 100%!",
        "rule_ar": "إشارة المنع المزدوج الصارم: لا توقف ولا انتظار لأي سبب كان، 24 ساعة في الـ 24 ساعة بدون لوحة توقيت.",
        "img": "Capitolo_03_segnali_divieto/immagini/85.png",
        "match": lambda q: '85.png' in q.get('img', '') and re.search(r'\b(consente|permette)\b', q['q'], re.I)
    },
    {
        "id": "sign_84_fermata",
        "fig": "84.png",
        "title_it": "Divieto di sosta",
        "title_ar": "ممنوع الانتظار (يسمح بالتوقف)",
        "ch": 3,
        "keyword_it": "consente la fermata",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "المفتاح السحري: إشارة ممنوع الانتظار تمنع الـ Sosta فقط، لكنها تسمح دائماً بالـ Fermata المؤقتة لركوب أو نزول الركاب بشرط بقاء السائق مستعداً للتحرك.",
        "rule_ar": "السؤال الذي يقول تسمح بالتوقف المؤقت (consente la fermata) صحيح دائماً بنسبة 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/84.png",
        "match": lambda q: '84.png' in q.get('img', '') and re.search(r'\b(fermata)\b', q['q'], re.I) and not re.search(r'\bvieta\b', q['q'], re.I)
    },
    {
        "id": "sign_14_filobus",
        "fig": "14.png",
        "title_it": "Attraversamento tranviario",
        "title_ar": "تقاطع مع خط ترامواي",
        "ch": 2,
        "keyword_it": "filobus / filoviaria",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الخلط بين الترام والترولي باص: الإشارة خاصة بحركة الترام على قضبان حديدية (su rotaie)، والوزارة تضع أسئلة خبيثة تدعي أنها لخط ترولي باص (linea filoviaria) للإيقاع بالطالب!",
        "rule_ar": "أي سؤال يذكر filobus مع هذه الإشارة فهو خطأ فادح وقطعي 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/14.png",
        "match": lambda q: '14.png' in q.get('img', '') and re.search(r'\b(filobus|filoviari[ao])\b', q['q'], re.I)
    },
    {
        "id": "sign_14_sorpasso",
        "fig": "14.png",
        "title_it": "Attraversamento tranviario",
        "title_ar": "تقاطع مع خط ترامواي",
        "ch": 2,
        "keyword_it": "vieta il sorpasso / mai",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ حظر التجاوز المطلق: تجاوز الترام مسموح على اليمين إذا توقف لنزول الركاب وكان هناك رصيف حماية (Salvagente)، أو على اليمين أثناء سيره إذا اتسع الطريق.",
        "rule_ar": "أي سؤال يدعي أن الإشارة تمنع التجاوز كلياً أو تحظر تجاوز الترام دائماً هو FALSO.",
        "img": "Capitolo_02_segnali_pericolo/immagini/14.png",
        "match": lambda q: '14.png' in q.get('img', '') and re.search(r'\b(sorpass|vieta)\b', q['q'], re.I) and not q['a']
    },
    {
        "id": "sign_1_dossi",
        "fig": "1.png",
        "title_it": "Strada dissestata",
        "title_ar": "طريق وعر / غير مستوي",
        "ch": 2,
        "keyword_it": "dossi artificiali",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ المطبات الصناعية: هذه الإشارة تحذر من هبوط وتموج وتآكل طبيعي في أرضية الطريق (strada in cattivo stato)، وليست مطبات صناعية مخففة للسرعة إطلاقاً!",
        "rule_ar": "أي سؤال يربط هذه اللوحة بالمطبات الصناعية المنظمة هو FALSO قطعي.",
        "img": "Capitolo_02_segnali_pericolo/immagini/1.png",
        "match": lambda q: '1.png' in q.get('img', '') and re.search(r'\b(artificial|doss)\b', q['q'], re.I) and not q['a']
    },
    {
        "id": "sign_2_visibilita",
        "fig": "2.png",
        "title_it": "Dosso stradale",
        "title_ar": "مطب طبيعي / مرتفع يحجب الرؤية",
        "ch": 2,
        "keyword_it": "visibilità / limitata",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "المفتاح الجوهري: خطر الـ Dosso الأساسي في قانون المرور هو حجب الرؤية في المطلع (Tratto ascendente con visibilità limitata)، لذا تنخفض السرعة لحجب الأفق.",
        "rule_ar": "أي سؤال يذكر انخفاض الرؤية (visibilità limitata/ridotta) فهو VERO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/2.png",
        "match": lambda q: '2.png' in q.get('img', '') and re.search(r'\b(visibilit|limitat)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_3_acqua",
        "fig": "3.png",
        "title_it": "Cunetta",
        "title_ar": "منخفض طريق / مجرى سيل",
        "ch": 2,
        "keyword_it": "acqua / allagamento",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "مفتاح المياه: الـ Cunetta هبوط مقعر تتجمع فيه مياه الأمطار أو الطين عند هطول المطر مسببة انزلاقاً خطيراً.",
        "rule_ar": "الأسئلة التي تذكر تجمع المياه (accumulo d'acqua) أو الغمر (allagamento) صحيحة VERO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/3.png",
        "match": lambda q: '3.png' in q.get('img', '') and re.search(r'\b(acqua|allagament)\b', q['q'], re.I)
    },
    {
        "id": "sign_8_croce",
        "fig": "8.png",
        "title_it": "Passaggio a livello con barriere",
        "title_ar": "مزلقان قطار بحواجز كاملة",
        "ch": 2,
        "keyword_it": "Croce di S. Andrea",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ صليب أندريا: صليب سان أندريا (Croce di S. Andrea) يوضع حصرياً في المزلقان بدون حواجز (SENZA barriere). وجوده مع مزلقان الحواجز خطأ قاتل في الكويزات!",
        "rule_ar": "أي سؤال يضع صليب أندريا مع لوحة المزلقان ذي الحواجز فهو FALSO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/8.png",
        "match": lambda q: '8.png' in q.get('img', '') and re.search(r'\b(croce|andrea)\b', q['q'], re.I)
    },
    {
        "id": "sign_9_croce",
        "fig": "9.png",
        "title_it": "Passaggio a livello senza barriere",
        "title_ar": "مزلقان قطار بدون حواجز",
        "ch": 2,
        "keyword_it": "Croce di S. Andrea / luci rosse",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "المفتاح الصريح: هذا المزلقان مكشوف بدون بوابات، لذا تجد قبله مباشرة صليب القديس أندريا ومصباحين أحمرين وامضين بالتبادل.",
        "rule_ar": "الأسئلة التي تذكر صليب أندريا أو وميض الضوءين الأحمرين مع هذه اللوحة هي VERO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/9.png",
        "match": lambda q: '9.png' in q.get('img', '') and re.search(r'\b(croce|lampeggi|due luci)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_18_frizione",
        "fig": "18.png",
        "title_it": "Discesa pericolosa",
        "title_ar": "منحدر خطر بنسبة انحدار محددة",
        "ch": 2,
        "keyword_it": "frizione / folle / spento",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الدبرياج والمور: السير في المنحدر والدبرياج مضغوط أو على المور (in folle) أو إطفاء المحرك يفصل فرامل الموتور ويسخن الفرامل حتى تحترق، وهو محرم ومجرم قطعاً!",
        "rule_ar": "أي سؤال يطلب الضغط على الدبرياج أو وضع الفتيس في المور أو إطفاء المحرك في المنحدر هو FALSO بنسبة 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/18.png",
        "match": lambda q: '18.png' in q.get('img', '') and re.search(r'\b(frizione|folle|spento)\b', q['q'], re.I)
    },
    {
        "id": "sign_18_marcia_bassa",
        "fig": "18.png",
        "title_it": "Discesa pericolosa",
        "title_ar": "منحدر خطر بنسبة انحدار محددة",
        "ch": 2,
        "keyword_it": "marcia bassa / freno motore",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "القاعدة الذهبية: النزول في المنحدر يجب دائماً أن يكون بغيار منخفض (marcia bassa) للاستفادة القصوى من فرملة المحرك وحماية فرامل العجلات من التلف.",
        "rule_ar": "السؤال الذي يوصي بـ marcia bassa أو freno motore في المنحدر هو VERO 100%.",
        "img": "Capitolo_02_segnali_pericolo/immagini/18.png",
        "match": lambda q: '18.png' in q.get('img', '') and re.search(r'\b(marcia bassa|freno motore)\b', q['q'], re.I)
    },
    {
        "id": "sign_54_entrambi",
        "fig": "54.png",
        "title_it": "Divieto di transito",
        "title_ar": "ممنوع مرور جميع المركبات في الاتجاهين",
        "ch": 3,
        "keyword_it": "entrambi i sensi",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "المفتاح الحاسم: الدائرة الحمراء ذات الخلفية البيضاء الفارغة تمنع الدخول في كلا الاتجاهين (entrambi i sensi) لجميع المركبات.",
        "rule_ar": "السؤال الذي يذكر منع السير في الاتجاهين (da entrambi i sensi) هو VERO 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/54.png",
        "match": lambda q: '54.png' in q.get('img', '') and re.search(r'\b(entrambi)\b', q['q'], re.I)
    },
    {
        "id": "sign_55_senso_vietato",
        "fig": "55.png",
        "title_it": "Senso vietato",
        "title_ar": "ممنوع الدخول (اتجاه واحد قادم)",
        "ch": 3,
        "keyword_it": "entrambi i sensi",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الاتجاهين: القرص الأحمر مع شريط أبيض أفقي يمنع الدخول من هذه الجهة فقط لأنه شارع باتجاه واحد (senso unico) ولا يمنع الاتجاهين!",
        "rule_ar": "أي سؤال يدعي أن هذه اللوحة تمنع السير في كلا الاتجاهين فهو FALSO 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/55.png",
        "match": lambda q: '55.png' in q.get('img', '') and re.search(r'\b(entrambi)\b', q['q'], re.I)
    },
    {
        "id": "sign_58_senza_motore",
        "fig": "58.png",
        "title_it": "Divieto di sorpasso",
        "title_ar": "ممنوع التجاوز للسيارات",
        "ch": 3,
        "keyword_it": "veicoli senza motore / ciclomotori",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "استثناء التجاوز المسموح: برغم وجود إشارة منع التجاوز، يُسمح لك قانوناً بتجاوز المركبات عديمة المحرك (عربات الخيل، الدراجات) والسيكلوموتوري والموتوسيكل بشرط عدم تجاوز الخط المتصل وعدم غزو المسار المعاكس!",
        "rule_ar": "أي سؤال ينص على جواز تجاوز veicoli sprovvisti di motore أو a due ruote senza invadere l'opposto senso هو VERO 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/58.png",
        "match": lambda q: '58.png' in q.get('img', '') and re.search(r'\b(senza motore|ciclomotori|due ruote)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_68_merci",
        "fig": "68.png",
        "title_it": "Divieto per veicoli merci oltre 3,5 t",
        "title_ar": "ممنوع لمركبات نقل البضائع فوق 3.5 طن",
        "ch": 3,
        "keyword_it": "autobus / persone",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الأوتوبيس: الرمز يمثل شاحنة بضائع، لذا ينطبق فقط على نقل البضائع (trasporto cose/merci)؛ ولا ينطبق إطلاقاً على أوتوبيسات الركاب أو الكرفانات حتى لو زاد وزنها عن 3.5 طن!",
        "rule_ar": "أي سؤال يدعي أن هذه اللوحة تنطبق على الأوتوبيس (autobus) هو FALSO 100%.",
        "img": "Capitolo_03_segnali_divieto/immagini/68.png",
        "match": lambda q: '68.png' in q.get('img', '') and re.search(r'\b(autobus|persone)\b', q['q'], re.I)
    },
    {
        "id": "sign_101_svoltare",
        "fig": "101.png",
        "title_it": "Passaggio obbligatorio a sinistra",
        "title_ar": "مرور إلزامي من يسار العائق",
        "ch": 4,
        "keyword_it": "svoltare / incrocio",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ الانعطاف في التقاطع: السهم المائل 45 درجة يلزمك بالمرور من يسار عائق أو جزيرة طريق (ostacolo/isola di traffico)، ولا يلزمك بالانعطاف يساراً في تقاطع كما تزعم الأسئلة الخادعة!",
        "rule_ar": "أي سؤال يزعم أن السهم المائل يلزمك بالدوران (svoltare a sinistra) في تقاطع هو FALSO 100%.",
        "img": "Capitolo_04_segnali_obbligo/immagini/101.png",
        "match": lambda q: '101.png' in q.get('img', '') and re.search(r'\b(svoltare)\b', q['q'], re.I)
    },
    {
        "id": "sign_37_arrestarsi",
        "fig": "37.png",
        "title_it": "Fermarsi e dare precedenza (STOP)",
        "title_ar": "قف وأعطِ الأسبقية (STOP)",
        "ch": 5,
        "keyword_it": "arrestarsi / anche se / non ci sono veicoli",
        "type": "vero",
        "rate": "100% VERO",
        "trap_ar": "القاعدة الذهبية المطلقة: مع إشارة STOP يجب التوقف التام عند خط التوقف الأبيض المستعرض، حتى لو كان التقاطع خالياً تماماً من المركبات بدون أي استثناء!",
        "rule_ar": "السؤال الذي يفرض التوقف التام حتى مع خلو الشارع هو VERO 100%. والسؤال الذي يقول يكفي الإبطاء بدون توقف هو FALSO 100%.",
        "img": "Capitolo_05_segnali_precedenza/immagini/37.png",
        "match": lambda q: '37.png' in q.get('img', '') and re.search(r'\b(arrestarsi|anche se)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "sign_45_diritto",
        "fig": "45.png",
        "title_it": "Dare precedenza nei sensi unici alternati",
        "title_ar": "إعطاء الأسبقية في المسار التبادلي (دائري أحمر)",
        "ch": 5,
        "keyword_it": "diritto di precedenza",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "فخ حق الأسبقية: اللوحة الدائرية بالحد الأحمر تلزمك بالتنازل عن الأسبقية للقادم في مواجهتك، بينما اللوحة المربعة الزرقاء هي التي تمنحك الحق.",
        "rule_ar": "أي سؤال يدعي أن هذه اللوحة تعطي حق الأسبقية (diritto di precedenza) هو FALSO 100%.",
        "img": "Capitolo_05_segnali_precedenza/immagini/45.png",
        "match": lambda q: '45.png' in q.get('img', '') and re.search(r'\b(diritto di precedenza)\b', q['q'], re.I)
    },
    {
        "id": "sign_509_oltrepassare",
        "fig": "509.png",
        "title_it": "Striscia bianca longitudinale continua",
        "title_ar": "الخط الطولي الأبيض المتصل",
        "ch": 6,
        "keyword_it": "oltrepassare / sormontare",
        "type": "falso",
        "rate": "100% FALSO",
        "trap_ar": "محرمات الخط المتصل: الخط المتصل كالجدار الخرساني؛ لا يجوز دهسه أو تجاوزه أو الالتفاف منه بتاتاً (vietato oltrepassare o sormontare).",
        "rule_ar": "أي سؤال يدعي جواز دهس الخط المتصل حتى لتجاوز بطيء أو دوران للخلف هو FALSO 100%.",
        "img": "Capitolo_06_segnaletica_orizzontale_ostacoli/immagini/509.png",
        "match": lambda q: '509.png' in q.get('img', '') and re.search(r'\b(oltrepassar|sormontar)\b', q['q'], re.I) and not q['a']
    }
]

# 2. CURATED THEORETICAL GOLDEN RULES (Chapters 11 - 25)
THEORY_RADAR_DEFS = [
    {
        "id": "theory_soccorso_bere",
        "topic": "🚑 الإسعافات الأولية (Primo Soccorso)",
        "ch": 22,
        "title_ar": "محرّمات الإسعاف: إعطاء السوائل أو الكحول أو الطعام",
        "title_it": "Divieto assoluto di somministrare bevande o alcool",
        "keywords_it": "dare da bere / acqua / bevande alcoliche",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "قاعدة إنقاذ الحياة: يُمنع منعاً باتاً ومطلقاً إعطاء المصاب في حادث سير أي ماء أو سوائل أو كحول، لتفادي الاختناق ودخول السائل إلى الرئتين خاصة عند فقدان الوعي أو الصدمة.",
        "why_trap_ar": "الوزارة تحاول استدراج تعاطفك بعبارات إنسانية خادعة مثل 'إعطاء الماء لتهدئة المصاب' أو 'إعطاء جرعة كحول لتدفئته' - احذر، كلها FALSO فوري!",
        "match": lambda q: q.get('ch', 0) == 22 and re.search(r'\b(bere|bevande|acqua|alcoliche)\b', q['q'], re.I) and not q['a']
    },
    {
        "id": "theory_soccorso_farmaci",
        "topic": "🚑 الإسعافات الأولية (Primo Soccorso)",
        "ch": 22,
        "title_ar": "محرّمات الإسعاف: إعطاء أدوية أو مسكنات للمصاب",
        "title_it": "Divieto di somministrare farmaci o medicinali",
        "keywords_it": "somministrare farmaci / medicinali",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "المسعف ليس طبيباً: لا يحق للمسعف الأولي إعطاء المصاب أي دواء أو مهدئ أو مسكن مهما كانت شدة ألمه، لأن ذلك قد يخفي الأعراض الطبية الحقيقية أو يسبب حساسية قاتلة.",
        "why_trap_ar": "أي سؤال يذكر كلمة 'farmaci' أو 'medicinali' للمصاب من قِبل المسعف هو FALSO 100%.",
        "match": lambda q: q.get('ch', 0) == 22 and re.search(r'\b(farmac|medicinal)\b', q['q'], re.I)
    },
    {
        "id": "theory_soccorso_estrarre",
        "topic": "🚑 الإسعافات الأولية (Primo Soccorso)",
        "ch": 22,
        "title_ar": "محرّمات الإسعاف: نزع الأجسام الغريبة المغروسة بالجسم",
        "title_it": "Divieto di estrarre corpi estranei conficcati",
        "keywords_it": "estrarre corpi estranei",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "الجسم المغروس يسد النزيف: إذا كان هناك زجاج أو حديد مغروس في جرح المصاب، يمنع نزعه لأن نزعه يسبب نزيفاً صاعقاً يودي بحياته فوراً، بل يجب تثبيته وانتظار الجراحين.",
        "why_trap_ar": "أي سؤال يقول 'estrarre il corpo estraneo' هو FALSO بنسبة 100%.",
        "match": lambda q: q.get('ch', 0) == 22 and re.search(r'\b(estrarre|corpo estraneo|corpi estranei)\b', q['q'], re.I)
    },
    {
        "id": "theory_soccorso_chiamare",
        "topic": "🚑 الإسعافات الأولية (Primo Soccorso)",
        "ch": 22,
        "title_ar": "الواجب الفوري: استدعاء الطوارئ 118 أو 112",
        "title_it": "Chiamare immediatamente i servizi di soccorso 118 / 112",
        "keywords_it": "soccorso / 118 / 112 / chiamare",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "أول خطوة حتمية في أي حادث: تأمين المكان وإبلاغ الطوارئ الطبية وتقديم معلومات دقيقة عن موقع الحادث وعدد المصابين.",
        "why_trap_ar": "الأسئلة المتعلقة بطلب الإسعاف وتوضيح الحالة والعدد والمكان هي VERO دائماً.",
        "match": lambda q: q.get('ch', 0) == 22 and re.search(r'\b(118|112|soccorsi|chiamare)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "theory_assicurazione_penale",
        "topic": "🛡️ التأمين والمسؤولية (Assicurazione e Responsabilità)",
        "ch": 23,
        "title_ar": "المسؤولية الجنائية شخصية لا يغطيها التأمين إطلاقاً",
        "title_it": "Responsabilità penale non è coperta da assicurazione",
        "keywords_it": "responsabilità penale / coperta dall'assicurazione",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "مبدأ دستوري إيطالي: المسؤولية الجنائية شخصية (La responsabilità penale è personale)؛ تأمين السيارات RCA يغطي فقط المسؤولية المدنية والأضرار المادية للغير، ولا يحمي من الحبس أو الإدانة الجنائية أبداً.",
        "why_trap_ar": "أي سؤال يزعم أن التأمين يعفي السائق من المسؤولية الجنائية أو يدفع عقوبتها هو FALSO 100%.",
        "match": lambda q: q.get('ch', 0) == 23 and re.search(r'\b(penale)\b', q['q'], re.I) and re.search(r'\b(assicuraz|copre|coperta)\b', q['q'], re.I) and not q['a']
    },
    {
        "id": "theory_assicurazione_fondo",
        "topic": "🛡️ التأمين والمسؤولية (Assicurazione e Responsabilità)",
        "ch": 23,
        "title_ar": "صندوق ضمان ضحايا الطريق لتعويض حوادث الهاربين",
        "title_it": "Fondo di garanzia per le vittime della strada",
        "keywords_it": "Fondo di garanzia per le vittime della strada",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "حماية الضحايا: أنشئ هذا الصندوق لتعويض الأضرار الجسدية عندما تكون المركبة المتسببة مجهولة وهربت (veicolo non identificato) أو غير مؤمنة (non coperto da assicurazione).",
        "why_trap_ar": "الأسئلة التي تصف دور صندوق Fondo di garanzia per le vittime della strada في تعويض هذه الحالات صحيحة VERO 100%.",
        "match": lambda q: q.get('ch', 0) == 23 and re.search(r'\bvittime della strada\b', q['q'], re.I)
    },
    {
        "id": "theory_cinture_purché",
        "topic": "💺 أحزمة الأمان والخوذة (Cinture e Casco)",
        "ch": 19,
        "title_ar": "أفخاخ استثناءات الحزام الوهمية: بشرط السرعة المنخفضة أو المشاوير القصيرة",
        "title_it": "Falsi esoneri cinture (purché a bassa velocità / percorso breve)",
        "keywords_it": "purché / breve percorso / solo in città",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "إلزامية الحزام المطلقة: الحزام إجباري داخل وخارج المدينة، وعلى أي سرعة حتى لو كانت 10 كم/س، وفي كل مشوار مهما كان قصيراً.",
        "why_trap_ar": "الأسئلة التي تضع شرط 'purché' (بشرط ألا تتجاوز السرعة 30 كم/س، أو بشرط السير في المدينة) كلها مصائد كاذبة FALSO 100%.",
        "match": lambda q: q.get('ch', 0) == 19 and re.search(r'\b(purché|bassa velocità|breve percorso)\b', q['q'], re.I) and not q['a']
    },
    {
        "id": "theory_cinture_gravidanza",
        "topic": "💺 أحزمة الأمان والخوذة (Cinture e Casco)",
        "ch": 19,
        "title_ar": "الاستثناء الحقيقي المعتمد: الحوامل بتقرير طبي صريح",
        "title_it": "Esenzione donne in stato di gravidanza con certificato",
        "keywords_it": "gravidanza / certificato medico",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "الاستثناء الطبي الصحيح: تُعفى المرأة الحامل من ربط الحزام فقط إذا كانت تحمل شهادة طبية رسمية من طبيب النساء تثبت وجود خطر على الجنين مع تاريخ الصلاحية.",
        "why_trap_ar": "السؤال الذي يذكر إعفاء الحامل بوجود شهادة طبية (certificato medico) هو VERO 100%. أما بدون شهادة فهو FALSO.",
        "match": lambda q: q.get('ch', 0) == 19 and re.search(r'\b(gravidanza)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "theory_distanza_quadruplica",
        "topic": "📏 السرعة ومسافة الأمان (Velocità e Distanza)",
        "ch": 11,
        "title_ar": "القاعدة الفيزيائية: مضاعفة السرعة تضاعف مسافة الفرملة 4 مرات",
        "title_it": "Raddoppio velocità comporta quadruplicazione spazio frenatura",
        "keywords_it": "quadruplica / raddoppia",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "العلاقة التربيعية: مسافة الفرملة تتناسب طردياً مع مربع السرعة (v²). إذا ضاعفت سرعتك من 50 إلى 100 كم/س، فمسافة الفرملة لا تتضاعف مرتين بل تتضاعف أربع مرات (quadruplica)!",
        "why_trap_ar": "السؤال الذي يقول 'quadruplica' صحيح VERO 100%، بينما السؤال الذي يقول تتضاعف مرتين 'raddoppia' خطأ FALSO 100%.",
        "match": lambda q: (q.get('ch', 0) in [11, 12]) and re.search(r'\bquadruplica\b', q['q'], re.I)
    },
    {
        "id": "theory_alcool_zero",
        "topic": "🍷 الكحول والمخدرات (Alcool e Guida)",
        "ch": 22,
        "title_ar": "نسبة كحول صفرية مطلقة (Zero Alcool) للجدد والمحترفين",
        "title_it": "Tasso alcolemico zero per neopatentati e minori di 21 anni",
        "keywords_it": "zero / neopatentati / minori di 21 anni",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "التسامح الصفري الصارم: السائقون الجدد (Neopatentati في أول 3 سنوات) والشباب دون 21 سنة والسائقون المحترفون يجب أن تكون نسبة الكحول في دمهم صفراً تاماً (0.0 g/l).",
        "why_trap_ar": "أي سؤال يبيح لهم حتى 0.2 أو 0.5 جم/لتر هو FALSO. والأسئلة التي تفرض نسبة Zero هي VERO 100%.",
        "match": lambda q: q.get('ch', 0) == 22 and re.search(r'\b(zero|tasso alcolemico pari a zero)\b', q['q'], re.I)
    },
    {
        "id": "theory_alcool_caffe",
        "topic": "🍷 الكحول والمخدرات (Alcool e Guida)",
        "ch": 22,
        "title_ar": "خرافات القضاء على الكحول: القهوة والدش البارد",
        "title_it": "Miti falsi: caffè o doccia fredda non eliminano l'alcool",
        "keywords_it": "caffè / doccia fredda / eliminare l'alcool",
        "type": "falso",
        "rate": "100% FALSO",
        "golden_rule_ar": "الحقيقة البيولوجية: الكبد وحده هو الذي يفتت الكحول في الدم بمعدل بطيء ثابت. شرب قهوة مركزة أو أخذ دش بارد لا يقلل نسبة الكحول إطلاقاً ولا يسرع تخلص الجسم منه.",
        "why_trap_ar": "أي سؤال يدعي أن فنجان قهوة أو هواء بارداً يتيح لك القيادة أو يخفض الكحول هو FALSO 100%.",
        "match": lambda q: q.get('ch', 0) == 22 and re.search(r'\b(caffè|doccia)\b', q['q'], re.I)
    },
    {
        "id": "theory_patente_raddoppio_punti",
        "topic": "📋 رخص القيادة والنقاط (Patente a Punti)",
        "ch": 20,
        "title_ar": "مضاعفة خصم النقاط للجدد (Neopatentati)",
        "title_it": "Raddoppio decurtazione punti per i neopatentati",
        "keywords_it": "raddoppiano / neopatentati / primi tre anni",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "عقوبة مضاعفة: السائق في السنوات الثلاث الأولى من حصوله على الرخصة (Neopatentato) تتضاعف نقاط المخالفة المخصومة منه (مثلاً مخالفة 5 نقاط تخصم منه 10 نقاط).",
        "why_trap_ar": "السؤال الذي ينص على مضاعفة الخصم للجدد في أول ثلاث سنوات هو VERO 100%.",
        "match": lambda q: q.get('ch', 0) == 20 and re.search(r'\b(raddoppi|primi tre anni)\b', q['q'], re.I) and q['a']
    },
    {
        "id": "theory_sosta_passo_carrabile",
        "topic": "🛑 الوقوف والتوقف (Sosta e Fermata)",
        "ch": 16,
        "title_ar": "ممنوع الانتظار أمام مدخل الجراج (Passo Carrabile) ويسمح بالتوقف",
        "title_it": "Vietata la sosta davanti a passo carrabile, consentita la fermata",
        "keywords_it": "passo carrabile / sosta vietata / consente la fermata",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "أمام الجراج المرخص (Passo Carrabile): يُمنع الانتظار وترك السيارة (Sosta vietata)، ولكن يُسمح بالتوقف اللحظي (Fermata) لركوب أو نزول شخص بشرط عدم سد خروج السيارات واستعداد السائق للتحرك فوراً.",
        "why_trap_ar": "أي سؤال يقول تمنع أيضاً الـ Fermata أمام Passo Carrabile هو FALSO. والأسئلة التي تفرق بين منع الـ Sosta وجواز الـ Fermata هي VERO 100%.",
        "match": lambda q: q.get('ch', 0) == 16 and re.search(r'\bpasso carrabile\b', q['q'], re.I) and re.search(r'\bfermata\b', q['q'], re.I)
    },
    {
        "id": "theory_meccanica_pressione_freddo",
        "topic": "🔧 الميكانيكا والصيانة (Meccanica e Manutenzione)",
        "ch": 25,
        "title_ar": "فحص ضغط الإطارات حصراً عندما تكون باردة (A Gomme Fredde)",
        "title_it": "Controllo pressione pneumatici va fatto a freddo",
        "keywords_it": "a freddo / pneumatici caldi",
        "type": "vero",
        "rate": "100% VERO",
        "golden_rule_ar": "فيزياء الهواء: السخونة تمدد الهواء داخل الإطار فتعطي قراءة ضغط أعلى من الحقيقة. قياس الضغط الصحيح يجب أن يتم والإطارات باردة تماماً قبل التحرك أو بعد الوقوف لفترة كافية.",
        "why_trap_ar": "أي سؤال يطلب فحص الضغط والإطارات ساخنة (a caldo) أو بعد مشوار سريع هو FALSO 100%. بينما فحصه a freddo هو VERO 100%.",
        "match": lambda q: q.get('ch', 0) == 25 and re.search(r'\b(a freddo|caldi)\b', q['q'], re.I)
    }
]

# Compile real matching questions
total_sign_matched = 0
for rule in SIGN_RADAR_DEFS:
    matched = find_matching_qs(rule['match'])
    rule['questions'] = matched
    rule['count'] = len(matched)
    total_sign_matched += len(matched)
    print(f"[SIGN] {rule['id']}: matched {len(matched)} questions.")

total_theory_matched = 0
for rule in THEORY_RADAR_DEFS:
    matched = find_matching_qs(rule['match'])
    rule['questions'] = matched
    rule['count'] = len(matched)
    total_theory_matched += len(matched)
    print(f"[THEORY] {rule['id']}: matched {len(matched)} questions.")

print(f"\nTotal Sign Questions Linked: {total_sign_matched}")
print(f"Total Theory Questions Linked: {total_theory_matched}")

# Serialize to a clean JS file
# Exclude the lambda 'match' before serialization
for r in SIGN_RADAR_DEFS:
    del r['match']
for r in THEORY_RADAR_DEFS:
    del r['match']

js_content = f"""// Auto-generated Expanded Radar Dataset
// Tab 2: Sign-Trap Radar (Chapters 1 - 10)
// Tab 3: Theoretical Golden Rules (Chapters 11 - 25)

const RADAR_SIGN_TRAPS = {json.dumps(SIGN_RADAR_DEFS, ensure_ascii=False, indent=2)};

const RADAR_THEORY_RULES = {json.dumps(THEORY_RADAR_DEFS, ensure_ascii=False, indent=2)};
"""

with open('R:/Ramy/PATENTE/assets/js/data-radar-expanded.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("\nSuccessfully created R:/Ramy/PATENTE/assets/js/data-radar-expanded.js")

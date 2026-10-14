# -*- coding: utf-8 -*-
"""
Inject 12 Ministerial Trap Quiz Cards and CSS into Chapters 17, 18, and 19
Aligning them 100% with Chapter 20 benchmark standard.
"""

import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# CSS styles needed for Trap Quiz Cards if not already present
TRAP_CSS = '''
  /* 12 Trap Quiz Cards (Ministerial Radar) */
  .traps-section { margin-bottom: 50px; }
  .traps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 20px;
  }
  .trap-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .trap-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .card-tag-pill {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
  }
  .tag-vero { background: rgba(16, 185, 129, 0.2); color: var(--emerald-primary); }
  .tag-falso { background: rgba(244, 63, 94, 0.2); color: var(--rose-primary); }
  .trap-quiz-text {
    font-family: var(--font-mono);
    font-size: 0.85rem;
    color: #e4e4e7;
    background: rgba(0, 0, 0, 0.35);
    border-radius: 8px;
    padding: 10px;
    direction: ltr;
    text-align: left;
    line-height: 1.5;
  }
  .trap-quiz-trans {
    font-size: 0.88rem;
    color: var(--sky-primary);
    font-weight: 600;
    line-height: 1.6;
  }
  .trap-explanation {
    font-size: 0.86rem;
    color: var(--text-secondary);
    line-height: 1.6;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 8px;
    padding: 10px;
    border-right: 3px solid var(--amber-primary);
  }
'''

# 12 Traps for Chapter 17 (Autostrade e Rimorchi)
CH17_TRAPS = '''
  <!-- 12 TRAP QUIZ CARDS SECTION (RADAR TRAPS) -->
  <section class="traps-section">
    <div class="section-heading">
      <div class="section-badge">رادار فخاخ الامتحان (12 سؤالاً حاسماً)</div>
      <h2 class="section-title">أخطر الأسئلة الوزارية المخادعة في الأوتوستراد والحمولة وسحب المقطورات</h2>
    </div>

    <div class="traps-grid">

      <!-- Trap 1 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ الدوران للخلف في الأوتوستراد</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"In autostrada è consentito fare inversione di marcia in corrispondenza dei varchi dello spartitraffico in caso di errore di corsia"</p>
        <p class="trap-quiz-trans">«في الأوتوستراد يجوز الدوران للخلف (U-turn) عند فتحات الحاجز الأوسط في حال الخطأ في المسار»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). الدوران للخلف (Inversione) أو الرجوع للخلف على الأوتوستراد جريمة مرورية جسيمة محظورة تماماً، وتؤدي فوراً إلى سحب وإلغاء رخصة القيادة (Revoca) وغرامة مالية باهظة وحجز المركبة!
        </div>
      </div>

      <!-- Trap 2 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ الحد الأقصى للوقوف في حارة الطوارئ</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"La corsia di emergenza in autostrada può essere utilizzata per la sosta fino a un massimo di 3 ore in caso di malessere o guasto"</p>
        <p class="trap-quiz-trans">«يجوز استخدام حارة الطوارئ في الأوتوستراد للوقوف لمدة أقصاها 3 ساعات في حالة الوعكة الصحية أو العطل»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). القاعدة القانونية الصارمة (Art. 176 CdS) تحدد 3 ساعات كحد أقصى مطلق للوقوف الاضطراري في حارة الطوارئ، وبعد انقضاء هذه المدة يتم سحب المركبة بالونش على نفقة المالك.
        </div>
      </div>

      <!-- Trap 3 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ الحارة الثالثة للمركبات الطويلة (>7m)</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"I veicoli o complessi di veicoli di lunghezza superiore a 7 metri possono impegnare qualsiasi corsia in un'autostrada a tre o più corsie"</p>
        <p class="trap-quiz-trans">«يجوز للمركبات أو قاطرات المركبات التي يتجاوز طولها 7 أمتار استخدام أي حارة في أوتوستراد بثلاث حارات أو أكثر»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). قاعدة الـ 7 أمتار: قوافل المركبات (السيارة + المقطورة) أو الشاحنات التي يزيد طولها الإجمالي عن 7 أمتار يحظر عليها قطعياً استخدام الحارة الثالثة أو ما يليها، ويلزمها القانون باستخدام الحارتين الأوليين فقط (Corsia 1 e 2)!
        </div>
      </div>

      <!-- Trap 4 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ بروز الحمولة من الأمام</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"Il carico può sporgere anteriormente dalla sagoma del veicolo fino a 3/10 della lunghezza del veicolo stesso"</p>
        <p class="trap-quiz-trans">«يجوز للحمولة أن تبرز من الأمام عن هيكل السيارة حتى 3 أعشار طول السيارة»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). البروز بمقدار 3/10 (30%) مسموح به حصرياً من <strong>الخلف (Posteriormente)</strong> وللحمولة غير القابلة للتجزئة! أما من الأمام (Anteriormente) فيحظر بروز أي حمولة تتجاوز مقدمة السيارة نهائياً لحماية المشاة والمركبات!
        </div>
      </div>

      <!-- Trap 5 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ وضع لوحة الحمولة البارزة ليلاً فقط</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"Il pannello per carichi sporgenti deve essere applicato solo di notte o in caso di scarsa visibilità"</p>
        <p class="trap-quiz-trans">«لوحة الحمولة البارزة يجب وضعها ليلاً فقط أو في حالات ضعف الرؤية»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). اللوحة المربعة ذات الخطوط البيضاء والحمراء العاكسة (Pannello carichi sporgenti - Fig. 302) إلزامية دائماً في كل وقت (Sempre, sia di giorno che di notte) متى ما كانت هناك حمولة تبرز خلف السيارة ولو لسنتيمترات قليلة!
        </div>
      </div>

      <!-- Trap 6 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ سحب سيارة معطلة بالحبل في الأوتوستراد</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"Il traino di un veicolo in avaria sull'autostrada è consentito purché si utilizzi una fune o una catena robusta e ben segnalata"</p>
        <p class="trap-quiz-trans">«يسمح بسحب سيارة معطلة في الأوتوستراد بشرط استخدام حبل أو جنزير قوي وواضح الإشارة»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). على الأوتوستراد والطرق السريعة الرئيسية، يحظر منعاً باتاً سحب أي سيارة بواسطة سيارة خاصة أخرى! السحب محصور حصرياً بمركبات الإنقاذ والشاحنات المرخصة رسمياً (Soccorso Stradale ACI / Carro Attrezzi)!
        </div>
      </div>

      <!-- Trap 7 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ سحب مقطورة غير خفيفة برخصة B</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"La patente della categoria B abilita a guidare autoveicoli trainanti un rimorchio non leggero (superiore a 750 kg), purché la massa massima autorizzata del complesso non superi 3.500 kg"</p>
        <p class="trap-quiz-trans">«تتيح رخصة B قيادة سيارة تجر مقطورة غير خفيفة (أكثر من 750 كجم) بشرط ألا يتجاوز الوزن الإجمالي الكلي 3500 كجم»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). برخصة B العادية، يجوز جر مقطورة خفيفة (حتى 750 كجم) دائماً، أو مقطورة ثقيلة بشرط ألا يتجاوز مجموع السيارتين (Massa massima del complesso) 3.500 كجم.
        </div>
      </div>

      <!-- Trap 8 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ كود التدريب العملي B96 حتى 4250 كجم</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"Il codice armonizzato 96 sulla patente B consente di condurre complessi di veicoli con massa massima compresa tra 3.500 kg e 4.250 kg superando una prova pratica di guida"</p>
        <p class="trap-quiz-trans">«يتيح الكود 96 على رخصة B قيادة قواطر سيارات بوزن كلي بين 3500 و 4250 كجم بعد اجتياز اختبار قيادة عملي»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). كود 96 هو ترقية عملية لرخصة B لا تتطلب امتحاناً نظرياً جديداً، وتوسع حد السحب حتى 4.250 كجم للمجموع الإجمالي.
        </div>
      </div>

      <!-- Trap 9 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ دخول دراجات 125 cc للأوتوستراد</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"È consentito circolare in autostrada con motocicli aventi cilindrata di 125 cm3 se guidati da conducenti maggiorenni"</p>
        <p class="trap-quiz-trans">«يسمح بالسير في الأوتوستراد بالدراجات النارية سعة 125 سم مكعب إذا كان السائق بالغاً»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). يمنع دخول الأوتوستراد لجميع الدراجات النارية التي تقل سعة محركها عن 150 سم مكعب (حتى لو كانت 125 أو 149 cc)، كما يمنع السيكلوموتوري وعربات الميني كار.
        </div>
      </div>

      <!-- Trap 10 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ سلك الأمان الفولاذي للمقطورة (Cavetto di sicurezza)</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"Il cavetto di sicurezza in acciaio collegato al gancio di traino attiva automaticamente la frenatura del rimorchio in caso di distacco accidentale"</p>
        <p class="trap-quiz-trans">«يقوم سلك الأمان الفولاذي المتصل بكرة السحب بتفعيل فرامل المقطورة تلقائياً في حال انفصالها العرضي»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). وظيفة سلك الأمان الفولاذي (Cavetto a strappo) هي شد فرامل الطوارئ للمقطورة لإيقافها ذاتياً وتفادي كارثة مرورية إذا أفلتت وصلة السحب.
        </div>
      </div>

      <!-- Trap 11 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ نقل بضائع عامة في مقطورات T.A.T.S.</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"I rimorchi per trasporto di attrezzature turistiche e sportive (T.A.T.S.) possono essere utilizzati per il trasporto di merci commerciali generiche"</p>
        <p class="trap-quiz-trans">«مقطورات المعدات الرياضية والسياحية T.A.T.S. يجوز استخدامها لنقل بضائع تجارية عامة»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). مقطورات T.A.T.S. مخصصة حصرياً وحسب الترخيص لنقل معدات سياحية أو رياضية محددة (مثل القوارب، الخيول، الدراجات الشراعية) ويحظر استخدامها لنقل بضائع تجارية عادية!
        </div>
      </div>

      <!-- Trap 12 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ مسافة مثلث الخطر في الأوتوستراد (100m)</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"Il segnale mobile di pericolo (triangolo) deve essere posizionato in modo da essere visibile da almeno 100 metri dai conducenti che sopraggiungono"</p>
        <p class="trap-quiz-trans">«يجب وضع مثلث الخطر بحيث يكون مرئياً من مسافة 100 متر على الأقل للسائقين القادمين خلفه»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). يوضع المثلث على بعد 50 متراً على الأقل خلف السيارة على الطرق السريعة و 100 متر في الأوتوستراد، ويشترط أن يراه السائقون القادمون من مسافة 100 متر على الأقل.
        </div>
      </div>

    </div>
  </section>
'''

# 12 Traps for Chapter 18 (Luci e Spie)
CH18_TRAPS = '''
  <!-- 12 TRAP QUIZ CARDS SECTION (RADAR TRAPS) -->
  <section class="traps-section">
    <div class="section-heading">
      <div class="section-badge">رادار فخاخ الامتحان (12 سؤالاً حاسماً)</div>
      <h2 class="section-title">أخطر الأسئلة الوزارية المخادعة في الأضواء ولمبات التابلوه والعواكس</h2>
    </div>

    <div class="traps-grid">

      <!-- Trap 1 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ إضاءة المصابيح نهاراً خارج المدن</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"I fari anabbaglianti devono essere tenuti accesi anche di giorno su autostrade e strade extraurbane da tutti i veicoli a motore"</p>
        <p class="trap-quiz-trans">«المصابيح الخافتة (الواطية) يجب أن تظل مضاءة نهاراً على الأوتوستراد والطرق خارج المدن لكافة المركبات الآلية»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). إلزام قانوني صارم: خارج المدن وعلى الأوتوستراد يجب إضاءة المصابيح الخافتة (Anabbaglianti) نهاراً وليلاً، أما الدراجات النارية فيلزمها إضاءتها دائماً حتى داخل المدن.
        </div>
      </div>

      <!-- Trap 2 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ الأضواء العالية (Abbaglianti) داخل المدن</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"L'uso dei fari abbaglianti è consentito nei centri abitati quando la strada è scarsamente illuminata"</p>
        <p class="trap-quiz-trans">«يسمح باستخدام المصابيح الكاشفة العالية (العالي) داخل المدن إذا كان الشارع قليل الإضاءة»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). داخل المدن (Centri abitati) يحظر استخدام المصابيح العالية تماماً وبشكل مستمر حتى لو كان الشارع مظلماً؛ يجب استخدام الأضواء الخافتة (Anabbaglianti) فقط لتجنب إبهار الآخرين!
        </div>
      </div>

      <!-- Trap 3 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ التنبيه المتقطع بالضوء العالي (Lampeggio) للتجاوز</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"È consentito l'uso intermittente dei fari abbaglianti per segnalare al veicolo che precede l'intenzione di sorpassare, sia di giorno che di notte"</p>
        <p class="trap-quiz-trans">«يجوز استخدام المصابيح العالية بشكل متقطع (تكبيس النور) لإعلام المركبة التي في الأمام بالرغبة في التجاوز نهاراً وليلاً»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). التنبيه المتقطع الخاطف (Lampeggio) مسموح به قانوناً كإشارة بصرية بديلة للمنبه الصوتي عند التجاوز أو للتحذير من خطر وشيك.
        </div>
      </div>

      <!-- Trap 4 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ الشكل المثلث لعواكس المقطورة الخلفية</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"I catadiottri installati sulla parte posteriore dei rimorchi devono essere di forma triangolare con vertice rivolto verso l'alto"</p>
        <p class="trap-quiz-trans">«العواكس المثبتة في الجزء الخلفي للمقطورات يجب أن تكون مثلثة الشكل ورأسها لأعلى»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). قاعدة تصنيف العواكس: العواكس الخلفية المثلثة الحمراء (Catadiottri triangolari) حصرية ومخصصة فقط للمقطورات وشبه المقطورات لتمييزها فوراً في الظلام!
        </div>
      </div>

      <!-- Trap 5 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ مدلول اللمبات الحمراء في التابلوه</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"La spia di colore rosso nel quadro strumenti indica semplicemente un'avvertenza di manutenzione programmata senza pericolo immediato"</p>
        <p class="trap-quiz-trans">«اللمبة ذات اللون الأحمر في التابلوه تشير ببساطة إلى تنبيه لصيانة دورية دون خطر فوري»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). اللمبات الحمراء (Spie rosse) تدل على عطل خطير أو خطر وشيك يوجب إيقاف السيارة فوراً (مثل ضغط الزيت، حرارة المبرد، عطل الفرامل)؛ أما التحذيرات البسيطة فتكون صفراء برتقالية!
        </div>
      </div>

      <!-- Trap 6 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ إضاءة لوحة الأرقام متزامنة مع أضواء الموضع</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"La luce della targa deve accendersi contemporaneamente alle luci di posizione"</p>
        <p class="trap-quiz-trans">«ضوء لوحة الأرقام الخلفية يجب أن يضاء بالتزامن مع أضواء الموضع (المارش)»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). لمبة اللوحة الخلفية متصلة بدائرة أضواء الموضع وتعمل معها تلقائياً لتكون أرقام اللوحة مقروءة بوضوح من مسافة لا تقل عن 20 متراً.
        </div>
      </div>

      <!-- Trap 7 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ استخدام الضوء العالي في الضباب الكثيف</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"In caso di nebbia fitta, l'uso dei proiettori abbaglianti migliora la visibilità rispetto agli anabbaglianti"</p>
        <p class="trap-quiz-trans">«في حالة الضباب الكثيف، استخدام المصابيح العالية يحسن الرؤية مقارنة بالمصابيح الخافتة»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). الضوء العالي في الضباب يصطدم بقطرات الماء المعلقة في الهواء وينعكس كالمرآة مشكلاً جداراً ضوئياً مبهراً يعمي السائق! يجب استخدام أضواء الضباب الخافضة أو الأنوار الواطية فقط.
        </div>
      </div>

      <!-- Trap 8 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ تشغيل الأضواء الرباعية في التباطؤ المفاجئ</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"La segnalazione luminosa di pericolo (quattro frecce) deve essere utilizzata in caso di improvviso e forte rallentamento del traffico in autostrada"</p>
        <p class="trap-quiz-trans">«إشارة الخطر الضوئية (الأربعة غمازات) يجب استخدامها في حال التباطؤ المفاجئ والشديد لحركة المرور في الأوتوستراد»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). إحدى الحالات الإلزامية لتشغيل الأضواء الرباعية هي تحذير السائقين القادمين من الخلف عند الدخول فجأة في طابور متوقف أو تباطؤ حاد على الطرق السريعة.
        </div>
      </div>

      <!-- Trap 9 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ استبدال الأنوار الخافتة بمصابيح الضباب الأمامية</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"I proiettori fendinebbia anteriori possono sostituire gli anabbaglianti in caso di nebbia fitta, fumo o forte nevicata"</p>
        <p class="trap-quiz-trans">«يجوز لمصابيح الضباب الأمامية أن تحل محل الأضواء الخافتة في حالة الضباب الكثيف أو الدخان أو تساقط الثلوج الشديد»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). مصابيح الضباب الأمامية مصممة لتسليط شعاع مسطح عريض تحت طبقة الضباب، لذا يجوز أن تحل محل الأنوار الواطية في ظروف الطقس شديدة السوء.
        </div>
      </div>

      <!-- Trap 10 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ استخدام كلاكسون المرور لتحية الأصدقاء</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"L'uso del segnalatore acustico (clacson) nei centri abitati è consentito per sollecitare il veicolo che precede a ripartire al semaforo verde"</p>
        <p class="trap-quiz-trans">«يسمح باستخدام كلاكسون السيارة داخل المدن لحث السيارة التي في الأمام على الانطلاق عند الإشارة الخضراء»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). داخل المدن، المنبه الصوتي محظور قطعياً إلا في حالتين حصريتين: 1) تفادي خطر حادث وشيك على السلامة، 2) أثناء نقل جريح أو مريض في حالة طوارئ قصوى!
        </div>
      </div>

      <!-- Trap 11 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ عمل العواكس ببطارية كهربائية</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"I catadiottri funzionano a batteria autonoma e si accendono insieme alle luci di posizione del veicolo"</p>
        <p class="trap-quiz-trans">«تعمل العواكس ببطارية مستقلة وتضاء مع أضواء الموضع للسيارة»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). العواكس (Catadiottri) هي أجهزة بصرية سالبة تعكس ضوء مصابيح المركبات الأخرى دون أي استهلاك للكهرباء ودون وجود لمبات أو بطاريات داخلها!
        </div>
      </div>

      <!-- Trap 12 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ لمبة زيت المحرك ومستوى مياه التبريد</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"La spia rossa dell'olio motore indica che la temperatura del liquido di raffreddamento ha raggiunto un livello pericoloso"</p>
        <p class="trap-quiz-trans">«لمبة زيت المحرك الحمراء تشير إلى أن درجة حرارة سائل التبريد بلغت مستوى خطيراً»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). لمبة الزيت الحمراء تشير إلى انخفاض ضغط دورة تزييت المحرك (Pressione insufficiente)، بينما حرارة سائل التبريد لها لمبة مستقلة على شكل مقياس حرارة يطفو في سائل!
        </div>
      </div>

    </div>
  </section>
'''

# 12 Traps for Chapter 19 (Cinture, Casco, Seggiolini)
CH19_TRAPS = '''
  <!-- 12 TRAP QUIZ CARDS SECTION (RADAR TRAPS) -->
  <section class="traps-section">
    <div class="section-heading">
      <div class="section-badge">رادار فخاخ الامتحان (12 سؤالاً حاسماً)</div>
      <h2 class="section-title">أخطر الأسئلة الوزارية المخادعة في أحزمة الأمان والخوذة ومقاعد الأطفال</h2>
    </div>

    <div class="traps-grid">

      <!-- Trap 1 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ إعفاء ركاب المقاعد الخلفية من الحزام</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"L'uso delle cinture di sicurezza non è obbligatorio per i passeggeri che occupano i sedili posteriori dell'autovettura"</p>
        <p class="trap-quiz-trans">«استخدام أحزمة الأمان ليس إجبارياً للركاب الذين يشغلون المقاعد الخلفية للسيارة»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). حزام الأمان إلزامي قانوناً لجميع ركاب السيارة في المقاعد الأمامية والخلفية على حد سواء متى كانت السيارة مزودة بها، وعدم ربطه في الخلف مخالفة مشددة وغرامة!
        </div>
      </div>

      <!-- Trap 2 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ شروط إعفاء النساء الحوامل من الحزام</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"Le donne in stato di gravidanza sono esentate dall'uso della cintura solo sulla base di certificazione medica attestante condizioni di rischio"</p>
        <p class="trap-quiz-trans">«تعفى النساء الحوامل من استخدام حزام الأمان فقط بناءً على شهادة طبية رسمية تثبت وجود مخاطر»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). الحمل بحد ذاته لا يعفي تلقائياً من الحزام؛ الإعفاء القانوني يتطلب شهادة خطية من طبيب النساء والتوليد تثبت وجود خطر خاص، ويجب إبرازها عند طلب الشرطة.
        </div>
      </div>

      <!-- Trap 3 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ مقاعد الأطفال للأطوال أقل من 150 سم</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"I bambini di statura inferiore a 1,50 metri devono essere assicurati con un sistema di ritenuta per bambini omologato, adeguato al loro peso"</p>
        <p class="trap-quiz-trans">«الأطفال الذين يقل طولهم عن 1.50 متراً يجب تأمينهم بنظام تثبيت مقاعد أطفال معتمد يتناسب مع أوزانهم»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). معيار الإلزام هو طول القامة (1.50 م)؛ فكل طفل يقل طوله عن 150 سم يمنع جلوسه بحزام السيارة العادي فقط، ويلزم وضعه في مقعد أطفال معتمد (Seggiolino / Adattatore).
        </div>
      </div>

      <!-- Trap 4 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ وضع مقعد الطفل المعاكس أمام الإيرباج</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"È consentito posizionare il seggiolino per bambini in senso contrario alla marcia sul sedile anteriore senza disattivare l'airbag"</p>
        <p class="trap-quiz-trans">«يجوز وضع مقعد الطفل بالاتجاه المعاكس للسير في المقعد الأمامي دون تعطيل الوسادة الهوائية (الإيرباج)»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). هذا خطر مميت ومخالفة جسيمة! انتفاخ الوسادة الهوائية الأمامية بسرعة 300 كم/س سيصدم مقعد الطفل بقوة تسحق رأس الرضيع! يجب تعطيل إيرباج الراكب الأمامي حتماً قبل وضع المقعد المعاكس!
        </div>
      </div>

      <!-- Trap 5 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ إغلاق خوذة الدراجة النارية بإحكام</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"Il casco da motociclista deve essere sempre allacciato correttamente; viaggiare con il casco slacciato equivale a non indossarlo"</p>
        <p class="trap-quiz-trans">«يجب ربط خوذة الدراجة النارية دائماً بإحكام؛ والقيادة بخوذة غير مربوطة تعادل عدم ارتدائها تماماً»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). الخوذة المفكوكة أو المربوطة بشكل رخو تطير عن الرأس في اللحظة الأولى لأي اصطدام، ويعاقب عليها القانون بنفس عقوبة عدم ارتداء الخوذة مع حجز المركبة لمدة 60 يوماً!
        </div>
      </div>

      <!-- Trap 6 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ إعادة استخدام خوذة تعرضت لصدمة</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"Un casco che ha subito un forte urto può essere regolarmente riutilizzato se la calotta esterna non presenta crepe o rotture visibili"</p>
        <p class="trap-quiz-trans">«يجوز إعادة استخدام خوذة تعرضت لصدمة قوية طالما أن الهيكل الخارجي لا يحتوي على شروخ ظاهرة»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). بطانة الخوذة الداخلية الماصة للصدمات (من البوليسترين الممدد) تنضغط وتتدمر ميكانيكياً بعد أول صدمة وتفقد قدرتها على حماية الجمجمة حتى لو بدا الغلاف الخارجي سليماً؛ يجب استبدالها فوراً!
        </div>
      </div>

      <!-- Trap 7 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ إعفاء البالغين من خوذة السيكلوموتوري</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"I conducenti di ciclomotori a due ruote sono esentati dall'obbligo del casco se sono maggiorenni"</p>
        <p class="trap-quiz-trans">«يعفى سائقو الدراجات الصغيرة (السيكلوموتوري) من الخوذة إذا كانوا بالغين»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). الخوذة المعتمدة إجبارية لجميع سائقي وركاب الدراجات النارية والسيكلوموتوري ذات العجلتين دون أي استثناء للسن أو سرعة المركبة!
        </div>
      </div>

      <!-- Trap 8 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ استغناء الإيرباج عن حزام الأمان</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"La presenza dell'airbag rende superfluo l'uso delle cinture di sicurezza per i passeggeri anteriori"</p>
        <p class="trap-quiz-trans">«وجود الوسادة الهوائية (الإيرباج) يجعل استخدام أحزمة الأمان غير ضروري لركاب المقاعد الأمامية»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). الإيرباج نظام أمان تكميلي مساعد (Sistema supplementare) ولا يعمل بكفاءة إلا بوجود الحزام؛ فبدون الحزام يندفع جسم السائق نحو الوسادة أثناء انفجارها مما يسبب كسوراً وإصابات قاتلة!
        </div>
      </div>

      <!-- Trap 9 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ عمل شداد الحزام (Pretensionatore) بعد الإيرباج</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"Il pretensionatore pirotecnico della cintura di sicurezza interviene solo dopo che l'airbag si è completamente sgonfiato"</p>
        <p class="trap-quiz-trans">«يتدخل الشداد الناري لحزام الأمان فقط بعد تفريغ الوسادة الهوائية من الهواء بالكامل»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). شداد الحزام (Pretensionatore) ينفجر ويسحب شريط الحزام للخلف في غضون أجزاء من الألف من الثانية لحظة الصدمة ليثبت جسم الراكب في ظهر المقعد قبل أو مع بداية انتفاخ الإيرباج!
        </div>
      </div>

      <!-- Trap 10 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--rose-primary);">❌ فخ مسند الرأس كأداة راحة فقط</span>
          <span class="card-tag-pill tag-falso">FALSO</span>
        </div>
        <p class="trap-quiz-text">"Il poggiatesta ha esclusivamente una funzione di comfort per rilassare i muscoli del collo durante la guida"</p>
        <p class="trap-quiz-trans">«مسند الرأس له وظيفة راحة حصرية لإرخاء عضلات الرقبة أثناء القيادة»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة خاطئة (FALSO). مسند الرأس (Poggiatesta) هو جهاز أمان خامل أساسي يمنع الارتداد العنيف للرقبة (Colpo di frusta) وكسر الفقرات العنقية في حوادث الصدم الخلفي!
        </div>
      </div>

      <!-- Trap 11 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ وجوب اعتماد ملابس سائق الدراجة (CE)</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"L'abbigliamento protettivo per motociclisti (giacca con protezioni, stivali, guanti) deve essere omologato e recare il marchio CE"</p>
        <p class="trap-quiz-trans">«الملابس الواقية لسائقي الدراجات (السترة بالواقيات، الحذاء، القفازات) يجب أن تكون معتمدة وتحمل علامة CE»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). يضمن اعتماد CE مطابقة المواد لمقاومة التمزق والاحتكاك بالأسفلت وقدرة الواقيات المدمجة على امتصاص قوة الصدمات المباشرة.
        </div>
      </div>

      <!-- Trap 12 -->
      <div class="trap-card">
        <div class="trap-header">
          <span style="font-weight:800; color:var(--emerald-primary);">✅ إعفاء سائقي التاكسي داخل المدن أثناء الخدمة</span>
          <span class="card-tag-pill tag-vero">VERO</span>
        </div>
        <p class="trap-quiz-text">"I conducenti dei taxi e dei veicoli a noleggio con conducente sono esentati dall'obbligo di indossare la cintura durante il servizio nei centri abitati"</p>
        <p class="trap-quiz-trans">«سائقو سيارات الأجرة (التاكسي) وسيارات التأجير بسائق يعفون من حزام الأمان أثناء أداء الخدمة داخل المدن»</p>
        <div class="trap-explanation">
          💡 <strong>التحليل الوزاري:</strong> العبارة صحيحة (VERO). استثناء قانوني واضح في المادة 172 من كود السير: يعفى سائقو التاكسي وسيارات NCC من ربط الحزام حصرياً داخل المراكز العمرانية (Nei centri abitati) وأثناء العمل الفعلي مع الركاب.
        </div>
      </div>

    </div>
  </section>
'''

def upgrade_chapter(file_path, traps_html):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Ensure Trap CSS is in <style>
    if '.traps-section' not in content:
        content = content.replace('</style>', TRAP_CSS + '\n</style>')
    
    # 2. Replace old quiz section or inject right before pagination
    # Search for quiz-section or chapter-pagination
    if '<section class="quiz-section"' in content:
        # replace the quiz-section up to </section>
        pattern = r'<section class="quiz-section"[^>]*>.*?</section>'
        content = re.sub(pattern, traps_html.strip(), content, flags=re.DOTALL)
        print(f"Replaced old quiz section with 12 Trap Quiz Cards in {file_path}")
    elif '<nav class="chapter-pagination"' in content:
        content = content.replace('<nav class="chapter-pagination"', traps_html.strip() + '\n\n  <nav class="chapter-pagination"')
        print(f"Injected 12 Trap Quiz Cards before pagination in {file_path}")
    else:
        print(f"Warning: Neither quiz-section nor chapter-pagination found in {file_path}")
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

upgrade_chapter('interactive_pages/دليل_الباب_17_الأوتوستراد_والحمولة_وسحب_المقطورات.html', CH17_TRAPS)
upgrade_chapter('interactive_pages/دليل_الباب_18_استخدام_الأضواء_ولمبات_التابلوه_والعواكس.html', CH18_TRAPS)
upgrade_chapter('interactive_pages/دليل_الباب_19_أحزمة_الأمان_والخوذة_ومقاعد_الأطفال.html', CH19_TRAPS)

print("Upgrade of Chapters 17, 18, and 19 completed successfully!")

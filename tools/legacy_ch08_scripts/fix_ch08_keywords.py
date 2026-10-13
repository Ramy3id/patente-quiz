import json
p = r'Capitoli_Divisi/Capitolo_08_segnali_indicazione/domande.json'
d = json.load(open(p, encoding='utf-8'))
m = {
 'Svolta sinistra': 'Svolta a sinistra indiretta (انعطاف غير مباشر لليسار)',
 'Inversione marcia': 'Inversione di marcia (الدوران للخلف)',
 'Piazzola sosta': 'Piazzola di sosta (فسحة توقف)',
 'Corsia autobus': 'Corsia riservata autobus (مسار مخصص للحافلات)',
 'Aumento corsie': 'Aumento corsie (زيادة المسارات)',
 'Diminuzione corsie': 'Diminuzione corsie (انخفاض المسارات)',
 'Deviazione autocarri': 'Deviazione consigliata (تحويلة منصوح بها)',
 'Cartello autobus': 'Fermata autobus extraurbano (موقف حافلات خارجي)',
 'Scambio autobus': 'Parcheggio di scambio (موقف تبادلي)',
 'Auto seguito': 'Auto al seguito (سيارة بصحبة المسافر على القطار)',
 'Impianti scarico': 'Impianti di scarico (مرافق تفريغ الصرف)',
 'Officina meccanica': 'Officina meccanica (ورشة ميكانيكية)',
 'Confine stato ue': 'Confine UE (حدود الاتحاد الأوروبي)',
 'Preavviso confine': 'Preavviso confine UE (إخطار مسبق بالحدود الأوروبية)',
 'Direzione obbligatoria': 'Direzione obbligatoria temporanea (اتجاه إجباري مؤقت)',
}
n = 0
for q in d['domande']:
    pk = q.get('parole_chiave') or []
    if len(pk) < 2:
        k = m.get(q['sotto_argomento'])
        if k and k not in pk:
            pk.append(k); q['parole_chiave'] = pk; n += 1
        else:
            print('unmapped', q['id'], q['sotto_argomento'])
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('fixed', n)

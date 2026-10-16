const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

const concepts = [
  'retromarcia',
  'prefetto',
  'prefettura',
  'ministero',
  'sospensione della patente',
  'revoca della patente',
  'revisione della patente',
  'conducenti minorenni',
  'traino',
  'soccorso',
  'spartitraffico',
  'segnalazione visiva a luce lampeggiante',
  'faro',
  'fari',
  'abbaglianti',
  'anabbaglianti',
  'quattro frecce',
  'frecce',
  'triangolo',
  'giubbotto',
  'catadiottri',
  'visiera',
  'casco',
  'ruotino',
  'abs',
  'airbag',
  'freno a mano',
  'freno di stazionamento',
  'freno di servizio',
  'aquaplaning',
  'aderenza',
  'frenatura',
  'spazio di frenatura',
  'spazio totale di arresto',
  'tempo di reazione'
];

console.log('=== TRAFFIC CONCEPTS ACCURACY CHECK ===');
concepts.forEach(term => {
  const reg = new RegExp('\\b' + term.replace(/ /g, '\\s+') + '\\b', 'i');
  const matched = all.filter(q => reg.test(q.q));
  if (matched.length >= 4) {
    const v = matched.filter(q => q.a === true).length;
    const f = matched.filter(q => q.a === false).length;
    const vPct = ((v / matched.length) * 100).toFixed(1);
    const fPct = ((f / matched.length) * 100).toFixed(1);
    console.log(`${term.padEnd(35)} | Total: ${String(matched.length).padStart(2)} | V: ${String(v).padStart(2)} (${vPct}%) | F: ${String(f).padStart(2)} (${fPct}%)`);
  }
});

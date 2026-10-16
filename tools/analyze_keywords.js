const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

const keywords = [
  'esclusivamente',
  'in ogni caso',
  'mai',
  'soltanto',
  'qualsiasi',
  'qualunque',
  'sempre',
  'tutti',
  'tutte',
  'solo',
  'obbligatoriamente',
  'moderare',
  'invita',
  'salvo diversa segnalazione',
  'potrebbero',
  'accertarsi che',
  'richiede',
  'differenziale',
  'frizione',
  'chiusa',
  'vanno',
  'affiancati',
  'facoltativo',
  'quanti',
  'pagamento'
];

console.log('=== KEYWORDS ANALYSIS ===');
keywords.forEach(kw => {
  const reg = new RegExp('\\b' + kw.replace(/ /g, '\\s+') + '\\b', 'i');
  const matched = all.filter(q => reg.test(q.q));
  const vero = matched.filter(q => q.a === true);
  const falso = matched.filter(q => q.a === false);
  const vRate = matched.length ? ((vero.length / matched.length) * 100).toFixed(1) : 0;
  const fRate = matched.length ? ((falso.length / matched.length) * 100).toFixed(1) : 0;
  console.log(`${kw.padEnd(28)} | Total: ${String(matched.length).padStart(3)} | V: ${String(vero.length).padStart(3)} (${vRate}%) | F: ${String(falso.length).padStart(3)} (${fRate}%)`);
});

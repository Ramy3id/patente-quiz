const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

const wordStats = {};
all.forEach(q => {
  const words = q.q.toLowerCase().match(/\b[a-zàèéìòù']{4,}\b/g) || [];
  new Set(words).forEach(w => {
    if (!wordStats[w]) wordStats[w] = { total: 0, v: 0, f: 0 };
    wordStats[w].total++;
    if (q.a === true) wordStats[w].v++;
    else wordStats[w].f++;
  });
});

console.log('=== UNKNOWN 100% FALSO WORDS (Total between 4 and 6) ===');
Object.keys(wordStats)
  .map(w => ({ word: w, ...wordStats[w] }))
  .filter(w => w.total >= 4 && w.f === w.total)
  .forEach(w => console.log(`FALSO: ${w.word.padEnd(20)} | Total: ${w.total}`));

console.log('\n=== UNKNOWN 100% VERO WORDS (Total between 4 and 6) ===');
Object.keys(wordStats)
  .map(w => ({ word: w, ...wordStats[w] }))
  .filter(w => w.total >= 4 && w.v === w.total)
  .forEach(w => console.log(`VERO:  ${w.word.padEnd(20)} | Total: ${w.total}`));

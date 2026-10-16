const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

// Analyze all individual words in the questions
const wordStats = {};

all.forEach(q => {
  // tokenize words (letters and apostrophes)
  const words = q.q.toLowerCase().match(/\b[a-zàèéìòù']{4,}\b/g) || [];
  const uniqueInQ = new Set(words);
  uniqueInQ.forEach(w => {
    if (!wordStats[w]) wordStats[w] = { total: 0, v: 0, f: 0 };
    wordStats[w].total++;
    if (q.a === true) wordStats[w].v++;
    else wordStats[w].f++;
  });
});

const candidates = Object.keys(wordStats).map(w => {
  const s = wordStats[w];
  const vPct = (s.v / s.total) * 100;
  const fPct = (s.f / s.total) * 100;
  return { word: w, total: s.total, v: s.v, f: s.f, vPct, fPct };
});

console.log('=== 100% PURE FALSO WORDS (Total >= 6) ===');
candidates
  .filter(c => c.total >= 6 && c.fPct === 100)
  .sort((a,b) => b.total - a.total)
  .slice(0, 30)
  .forEach(c => console.log(`${c.word.padEnd(20)} | Total: ${c.total} | 100% FALSO`));

console.log('\n=== 100% PURE VERO WORDS (Total >= 6) ===');
candidates
  .filter(c => c.total >= 6 && c.vPct === 100)
  .sort((a,b) => b.total - a.total)
  .slice(0, 30)
  .forEach(c => console.log(`${c.word.padEnd(20)} | Total: ${c.total} | 100% VERO`));

console.log('\n=== WORDS WITH HIGH BIAS (Total >= 10, Bias >= 85% & < 100%) ===');
candidates
  .filter(c => c.total >= 10 && ((c.vPct >= 85 && c.vPct < 100) || (c.fPct >= 85 && c.fPct < 100)))
  .sort((a,b) => b.total - a.total)
  .forEach(c => {
    const isVero = c.vPct >= 85;
    console.log(`${c.word.padEnd(20)} | Total: ${c.total} | V: ${c.v} | F: ${c.f} | ${isVero ? c.vPct.toFixed(1) + '% VERO' : c.fPct.toFixed(1) + '% FALSO'}`);
  });

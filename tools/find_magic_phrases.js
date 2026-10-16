const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

const phraseStats = {};

all.forEach(q => {
  const norm = q.q.toLowerCase().replace(/[^a-zàèéìòù\s]/g, ' ').replace(/\s+/g, ' ');
  const tokens = norm.trim().split(' ');
  // Generate 2-word and 3-word n-grams
  const seenInQ = new Set();
  for (let i = 0; i < tokens.length - 1; i++) {
    const bi = tokens[i] + ' ' + tokens[i+1];
    seenInQ.add(bi);
    if (i < tokens.length - 2) {
      const tri = tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2];
      seenInQ.add(tri);
    }
  }

  seenInQ.forEach(p => {
    if (!phraseStats[p]) phraseStats[p] = { total: 0, v: 0, f: 0 };
    phraseStats[p].total++;
    if (q.a === true) phraseStats[p].v++;
    else phraseStats[p].f++;
  });
});

const pList = Object.keys(phraseStats).map(p => {
  const s = phraseStats[p];
  return { phrase: p, total: s.total, v: s.v, f: s.f, vPct: (s.v / s.total) * 100, fPct: (s.f / s.total) * 100 };
});

console.log('=== 100% FALSO PHRASES (Total >= 5) ===');
pList
  .filter(p => p.total >= 5 && p.fPct === 100)
  .sort((a,b) => b.total - a.total)
  .slice(0, 30)
  .forEach(p => console.log(`${p.phrase.padEnd(35)} | Total: ${p.total} | 100% FALSO`));

console.log('\n=== 100% VERO PHRASES (Total >= 5) ===');
pList
  .filter(p => p.total >= 5 && p.vPct === 100)
  .sort((a,b) => b.total - a.total)
  .slice(0, 30)
  .forEach(p => console.log(`${p.phrase.padEnd(35)} | Total: ${p.total} | 100% VERO`));

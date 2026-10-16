const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

console.log('=== HUNT 1: REPEATED QUESTIONS (100% FALSO) ===');
// Find duplicate/repeated question texts
const qMap = {};
all.forEach(q => {
  const norm = q.q.trim().toLowerCase().replace(/[.,;:?!]/g, '').replace(/\s+/g, ' ');
  if (!qMap[norm]) qMap[norm] = [];
  qMap[norm].push(q);
});

const repeatedFalso = Object.keys(qMap)
  .map(k => ({ text: k, items: qMap[k], count: qMap[k].length, allFalso: qMap[k].every(x => x.a === false) }))
  .filter(x => x.count > 1 && x.allFalso)
  .sort((a,b) => b.count - a.count);

console.log(`Found ${repeatedFalso.length} identical question texts that are repeated >1 time and ALWAYS FALSO!`);
repeatedFalso.slice(0, 15).forEach((rf, i) => {
  console.log(`[#${i+1}] Repeated ${rf.count} times (Chapters: ${rf.items.map(x=>x.ch).join(', ')}):`);
  console.log(`   IT: ${rf.items[0].q}`);
  console.log(`   AR: ${rf.items[0].tr}`);
});

console.log('\n=== HUNT 2: TWO WORDS THAT MEET -> 100% FALSO (CO-OCCURRENCE) ===');
// Let's test combinations of common words
const candidateWords = [
  'sempre', 'solo', 'soltanto', 'anche', 'deve', 'possono', 'può', 'corsia',
  'sorpasso', 'precedenza', 'velocità', 'veicolo', 'strada', 'segnale',
  'arresto', 'fermata', 'sosta', 'clacson', 'segnalazione', 'pannello',
  'autostrada', 'distanza', 'inversione', 'marcia', 'luci', 'notte', 'pioggia'
];

const pairs = [];
for (let i = 0; i < candidateWords.length; i++) {
  for (let j = i + 1; j < candidateWords.length; j++) {
    const w1 = candidateWords[i];
    const w2 = candidateWords[j];
    const r1 = new RegExp('\\b' + w1 + '\\b', 'i');
    const r2 = new RegExp('\\b' + w2 + '\\b', 'i');

    const matched = all.filter(q => r1.test(q.q) && r2.test(q.q));
    if (matched.length >= 6) {
      const fCount = matched.filter(q => q.a === false).length;
      if (fCount === matched.length) {
        pairs.push({ w1, w2, count: matched.length });
      }
    }
  }
}

pairs.sort((a,b) => b.count - a.count);
console.log(`Found ${pairs.length} pairs of words that when meeting together are 100% FALSO (Min count >= 6):`);
pairs.slice(0, 15).forEach((p, i) => {
  console.log(`[#${i+1}] ("${p.w1}" + "${p.w2}") -> ${p.count} questions, ALL 100% FALSO!`);
});

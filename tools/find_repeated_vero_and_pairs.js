const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

console.log('=== HUNT: REPEATED QUESTIONS (100% VERO) ===');
const qMap = {};
all.forEach(q => {
  const norm = q.q.trim().toLowerCase().replace(/[.,;:?!]/g, '').replace(/\s+/g, ' ');
  if (!qMap[norm]) qMap[norm] = [];
  qMap[norm].push(q);
});

const repeatedVero = Object.keys(qMap)
  .map(k => ({ text: k, items: qMap[k], count: qMap[k].length, allVero: qMap[k].every(x => x.a === true) }))
  .filter(x => x.count > 1 && x.allVero)
  .sort((a,b) => b.count - a.count);

console.log(`Found ${repeatedVero.length} identical question texts that are repeated >1 time and ALWAYS VERO!`);
repeatedVero.slice(0, 20).forEach((rv, i) => {
  console.log(`[#${i+1}] Repeated ${rv.count} times (Chapters: ${rv.items.map(x=>x.ch).join(', ')}):`);
  console.log(`   IT: ${rv.items[0].q}`);
  console.log(`   AR: ${rv.items[0].tr}`);
});

console.log('\n=== HUNT: GOLDEN WORD PAIRS (100% VERO, Min count >= 6) ===');
const wordCounts = {};
const stopWords = new Set(['il', 'lo', 'la', 'i', 'gli', 'le', 'un', 'uno', 'una', 'di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra', 'del', 'dello', 'della', 'dei', 'degli', 'delle', 'al', 'allo', 'alla', 'ai', 'agli', 'alle', 'dal', 'dallo', 'dalla', 'dai', 'dagli', 'dalle', 'nel', 'nello', 'nella', 'nei', 'negli', 'nelle', 'sul', 'sullo', 'sulla', 'sui', 'sugli', 'sulle', 'ed', 'ad', 'od', 'e', 'o', 'se', 'che', 'non', 'si', 'è', 'ha', 'ci', 'ne', 'vi', 'anche', 'come', 'più']);

all.forEach(q => {
  const words = q.q.toLowerCase().match(/\b[a-zàèéìòù']{3,}\b/g) || [];
  new Set(words).forEach(w => {
    if (!stopWords.has(w)) {
      wordCounts[w] = (wordCounts[w] || 0) + 1;
    }
  });
});

const topWords = Object.keys(wordCounts)
  .filter(w => wordCounts[w] >= 20)
  .sort((a,b) => wordCounts[b] - wordCounts[a])
  .slice(0, 120);

const goldenPairs = [];
for (let i = 0; i < topWords.length; i++) {
  for (let j = i + 1; j < topWords.length; j++) {
    const w1 = topWords[i];
    const w2 = topWords[j];
    const r1 = new RegExp('\\b' + w1 + '\\b', 'i');
    const r2 = new RegExp('\\b' + w2 + '\\b', 'i');

    const matched = all.filter(q => r1.test(q.q) && r2.test(q.q));
    if (matched.length >= 6) {
      const vCount = matched.filter(q => q.a === true).length;
      if (vCount === matched.length) {
        goldenPairs.push({ w1, w2, count: matched.length });
      }
    }
  }
}

goldenPairs.sort((a,b) => b.count - a.count);
console.log(`Found ${goldenPairs.length} golden pairs of words that when meeting together are 100% VERO (Min count >= 6):`);
goldenPairs.forEach((p, idx) => {
  console.log(`[#${idx+1}] ("${p.w1}" + "${p.w2}") -> ${p.count} questions (100% VERO)`);
});

const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

// Extract top 150 most frequent meaningful words in Patente questions
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
  .filter(w => wordCounts[w] >= 25)
  .sort((a,b) => wordCounts[b] - wordCounts[a])
  .slice(0, 100);

console.log('Testing pairs among top', topWords.length, 'words...');

const fatalPairs = [];

for (let i = 0; i < topWords.length; i++) {
  for (let j = i + 1; j < topWords.length; j++) {
    const w1 = topWords[i];
    const w2 = topWords[j];
    const r1 = new RegExp('\\b' + w1 + '\\b', 'i');
    const r2 = new RegExp('\\b' + w2 + '\\b', 'i');

    const matched = all.filter(q => r1.test(q.q) && r2.test(q.q));
    if (matched.length >= 5) {
      const fCount = matched.filter(q => q.a === false).length;
      if (fCount === matched.length) {
        fatalPairs.push({ w1, w2, count: matched.length });
      }
    }
  }
}

fatalPairs.sort((a,b) => b.count - a.count);
console.log(`\n=== FATAL WORD PAIRS (Co-occurrence = 100% FALSO, Min 8 questions) ===`);
fatalPairs.forEach((p, idx) => {
  console.log(`[#${idx+1}] "${p.w1}" + "${p.w2}" -> ${p.count} questions (100% FALSO)`);
});

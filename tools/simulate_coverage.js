// Run simulation using Node.js directly
const fs = require('fs');

// Read data_all_questions.js
let allQFile = fs.readFileSync('R:/Ramy/PATENTE/Capitoli_Divisi/data_all_questions.js', 'utf8');
allQFile = allQFile.replace('const CHAPTERS_META', 'global.CHAPTERS_META');
allQFile = allQFile.replace('const ALL_QUESTIONS_DATA', 'global.ALL_QUESTIONS_DATA');
eval(allQFile);

// Read data-radar-expanded.js
let radarFile = fs.readFileSync('R:/Ramy/PATENTE/assets/js/data-radar-expanded.js', 'utf8');
radarFile = radarFile.replace('const RADAR_SIGN_TRAPS', 'global.RADAR_SIGN_TRAPS');
radarFile = radarFile.replace('const RADAR_THEORY_RULES', 'global.RADAR_THEORY_RULES');
eval(radarFile);

// Read MAGIC_WORDS_DB from parole-spia.html
const psHtml = fs.readFileSync('R:/Ramy/PATENTE/interactive_pages/parole-spia.html', 'utf8');
const idx1 = psHtml.indexOf('const MAGIC_WORDS_DB = [');
const idx2 = psHtml.indexOf('];', idx1);
if (idx1 === -1 || idx2 === -1) {
  console.log("Could not find MAGIC_WORDS_DB range");
  process.exit(1);
}
let mwCode = psHtml.substring(idx1, idx2 + 2);
mwCode = mwCode.replace('const MAGIC_WORDS_DB', 'global.MAGIC_WORDS_DB');
eval(mwCode);

console.log("Total DB Questions:", ALL_QUESTIONS_DATA.length);
console.log("Tab 1 Magic Words Count:", MAGIC_WORDS_DB.length);
console.log("Tab 2 Sign Traps Count:", RADAR_SIGN_TRAPS.length);
console.log("Tab 3 Theory Rules Count:", RADAR_THEORY_RULES.length);

// 1. Tab 1 Covered Questions
const tab1Set = new Set();
MAGIC_WORDS_DB.forEach(mw => {
  if (!mw.regex) return;
  try {
    const re = new RegExp(mw.regex, 'i');
    ALL_QUESTIONS_DATA.forEach(q => {
      if (re.test(q.q || "")) {
        tab1Set.add(`${q.ch}_${q.id}`);
      }
    });
  } catch(e) {}
});

// 2. Tab 2 Covered Questions
const tab2Set = new Set();
RADAR_SIGN_TRAPS.forEach(r => {
  (r.questions || []).forEach(q => {
    tab2Set.add(`${q.ch}_${q.id}`);
  });
});

// 3. Tab 3 Covered Questions
const tab3Set = new Set();
RADAR_THEORY_RULES.forEach(r => {
  (r.questions || []).forEach(q => {
    tab3Set.add(`${q.ch}_${q.id}`);
  });
});

// Combined Unique Set
const allRadarSet = new Set([...tab1Set, ...tab2Set, ...tab3Set]);

console.log("\n=== Direct Bank Coverage ===");
console.log("Questions covered by Tab 1 (General Spy Words):", tab1Set.size);
console.log("Questions covered by Tab 2 (Sign Traps):", tab2Set.size);
console.log("Questions covered by Tab 3 (Theory Rules):", tab3Set.size);
console.log("Total UNIQUE questions covered across all 3 tabs:", allRadarSet.size);
console.log("Percentage of whole bank (7,139 qs):", (allRadarSet.size / ALL_QUESTIONS_DATA.length * 100).toFixed(2) + "%");

// 4. Simulate 10,000 real ministerial exams (30 questions each)
const chaptersMap = {};
ALL_QUESTIONS_DATA.forEach(q => {
  if (!chaptersMap[q.ch]) chaptersMap[q.ch] = [];
  chaptersMap[q.ch].push(`${q.ch}_${q.id}`);
});

const simCount = 10000;
const hits = [];
const extraChapters = [1, 2, 3, 8, 14];

for (let i = 0; i < simCount; i++) {
  const exam = [];
  // 1 question from each of chapters 1..25
  for (let ch = 1; ch <= 25; ch++) {
    const pool = chaptersMap[ch] || [];
    if (pool.length > 0) {
      exam.push(pool[Math.floor(Math.random() * pool.length)]);
    }
  }
  // 5 extra questions from major chapters to make 30
  extraChapters.forEach(ch => {
    const pool = chaptersMap[ch] || [];
    if (pool.length > 0) {
      exam.push(pool[Math.floor(Math.random() * pool.length)]);
    }
  });

  // Count how many questions in this exam are hit by the radar
  let hit = 0;
  exam.forEach(qKey => {
    if (allRadarSet.has(qKey)) hit++;
  });
  hits.push(hit);
}

const avg = hits.reduce((a, b) => a + b, 0) / hits.length;
const min = Math.min(...hits);
const max = Math.max(...hits);

console.log("\n=== 10,000 Real Exam Simulations (30 questions each) ===");
console.log(`Average questions solved by Radar per exam: ${avg.toFixed(2)} out of 30 (${(avg/30*100).toFixed(1)}%)`);
console.log(`Minimum solved in any exam: ${min} out of 30`);
console.log(`Maximum solved in any exam: ${max} out of 30`);

// Frequency table
const freq = {};
hits.forEach(h => freq[h] = (freq[h] || 0) + 1);

console.log("\nProbability of questions solved per 30-question exam:");
Object.keys(freq).map(Number).sort((a,b)=>a-b).forEach(k => {
  const pct = (freq[k] / simCount * 100).toFixed(2);
  const bar = "█".repeat(Math.round(pct / 2));
  console.log(`  ${k} questions: ${pct}% ${bar}`);
});

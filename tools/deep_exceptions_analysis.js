const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

function analyzeWords(targetWords) {
  targetWords.forEach(w => {
    const reg = new RegExp('\\b' + w.replace(/ /g, '\\s+') + '\\b', 'i');
    const matched = all.filter(q => reg.test(q.q));
    const vero = matched.filter(q => q.a === true);
    const falso = matched.filter(q => q.a === false);
    console.log(`\n======================================================`);
    console.log(`ANALYSIS FOR: "${w}" (Total: ${matched.length} | V: ${vero.length} | F: ${falso.length})`);
    console.log(`======================================================`);
    
    console.log(`--- VERO Questions (${vero.length}) ---`);
    vero.forEach((q, i) => console.log(`  [V#${i+1}] Ch:${q.ch} | ${q.q}`));

    console.log(`\n--- FALSO Questions Sample (${Math.min(5, falso.length)} of ${falso.length}) ---`);
    falso.slice(0, 5).forEach((q, i) => console.log(`  [F#${i+1}] Ch:${q.ch} | ${q.q}`));
  });
}

analyzeWords(['soltanto', 'qualsiasi', 'qualunque', 'salvo diversa segnalazione']);

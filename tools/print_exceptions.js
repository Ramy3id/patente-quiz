const fs = require('fs');

const code = fs.readFileSync('./Capitoli_Divisi/data_all_questions.js', 'utf8');
eval(code.replace(/const ALL_QUESTIONS_DATA/g, 'global.ALL_QUESTIONS_DATA').replace(/const CHAPTERS_META/g, 'global.CHAPTERS_META'));
const all = global.ALL_QUESTIONS_DATA;

function inspectExceptions(kw, targetAnswer) {
  const reg = new RegExp('\\b' + kw.replace(/ /g, '\\s+') + '\\b', 'i');
  const matched = all.filter(q => reg.test(q.q));
  const exceptions = matched.filter(q => q.a === targetAnswer);
  console.log(`\n======================================================`);
  console.log(`KW: "${kw}" -> Showing ${exceptions.length} EXCEPTIONS (Expected: ${!targetAnswer ? 'VERO' : 'FALSO'}, Exception is: ${targetAnswer ? 'VERO' : 'FALSO'})`);
  console.log(`======================================================`);
  exceptions.forEach((q, idx) => {
    console.log(`[#${idx+1}] ID:${q.id} | Ch:${q.ch} | Ans:${q.a ? 'VERO' : 'FALSO'}`);
    console.log(`  IT: ${q.q}`);
    console.log(`  TR: ${q.tr}`);
    console.log(`  SP: ${q.sp.slice(0, 150)}...`);
  });
}

inspectExceptions('esclusivamente', true);
inspectExceptions('mai', true);
inspectExceptions('in ogni caso', true);
inspectExceptions('moderare', false);
inspectExceptions('invita', false);
inspectExceptions('potrebbero', false);
inspectExceptions('accertarsi che', false);
inspectExceptions('salvo diversa segnalazione', false);
inspectExceptions('trombe', true);

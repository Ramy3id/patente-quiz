path = r'R:\Ramy\PATENTE\assets\js\data-simulatore-questions.js'

with open(path, 'a', encoding='utf-8') as f:
    f.write('''
// Security: Freeze question datasets to prevent DevTools memory tampering
if (typeof Object.freeze === 'function') {
  try {
    ALL_QUESTIONS.forEach(q => Object.freeze(q));
    Object.freeze(ALL_QUESTIONS);
    Object.freeze(CHAPTERS_META);
  } catch (_) {}
}
''')

print("Frozen datasets appended to data-simulatore-questions.js!")

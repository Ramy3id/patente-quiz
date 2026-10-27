path = r'R:\Ramy\PATENTE\assets\js\quiz-engine.js'

with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

target1 = '''  recordAnswer(questionId, value) {
    if (this.isSubmitted) return;
    this.answers[questionId] = Boolean(value);
  }'''

replacement1 = '''  recordAnswer(questionId, value) {
    if (this.isSubmitted) return;
    this.answers[questionId] = Boolean(value);
    
    // Haptic Feedback for Mobile Touch (Apple HIG & Android Haptics)
    if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
      try { navigator.vibrate(12); } catch (_) {}
    }
  }'''

target2 = '''    analysis.passed = analysis.errors <= this.maxAllowedErrors;'''

replacement2 = '''    analysis.passed = analysis.errors <= this.maxAllowedErrors;

    // Haptic Feedback based on Exam Result (Pass vs Fail)
    if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
      try {
        if (analysis.passed) {
          navigator.vibrate([20, 30, 40]);
        } else {
          navigator.vibrate([40, 60, 40]);
        }
      } catch (_) {}
    }'''

if target1 in code:
    code = code.replace(target1, replacement1, 1)
    if target2 in code:
        code = code.replace(target2, replacement2, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("quiz-engine.js updated with Haptic Feedback!")
else:
    print("target1 not found in quiz-engine.js")

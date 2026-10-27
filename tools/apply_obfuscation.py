import base64
import json
import re

# 1. Transform data-simulatore-questions.js
js_path = r"R:\Ramy\PATENTE\assets\js\data-simulatore-questions.js"
with open(js_path, "r", encoding="utf-8") as f:
    js_text = f.read()

# Find ALL_QUESTIONS = [...]
m = re.search(r"const ALL_QUESTIONS = (\[.*?\]);", js_text)
if m:
    questions = json.loads(m.group(1))
    print(f"Loaded {len(questions)} questions from data-simulatore-questions.js")
    
    salt = "_PATENTE_PRO_2026_"
    obfuscated_count = 0
    for q in questions:
        if "a" in q:
            is_v = bool(q["a"])
            raw = f"{q['id']}_{'VERO' if is_v else 'FALSO'}{salt}"
            q["sig"] = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
            del q["a"]
            obfuscated_count += 1
    
    print(f"Obfuscated answers for {obfuscated_count} questions into salted signatures!")
    new_questions_json = json.dumps(questions, ensure_ascii=False)
    js_text = js_text[:m.start(1)] + new_questions_json + js_text[m.end(1):]
    
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_text)
    print("data-simulatore-questions.js written successfully!")
else:
    print("Could not find ALL_QUESTIONS in data-simulatore-questions.js")

# 2. Update Simulatore_Esame.html
html_path = r"R:\Ramy\PATENTE\Simulatore_Esame.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Add helper functions right before initSetup() or after soundEngine
helpers = '''
  // Secure Answer Verification (Salted Token Checksum)
  const _SEC_SALT = "_PATENTE_PRO_2026_";
  function getQuestionCorrectAnswer(q) {
    if (!q) return false;
    if (q.sig) {
      return q.sig === btoa(q.id + "_VERO" + _SEC_SALT);
    }
    return q.a === true;
  }
  function verifyStudentAnswer(q, studentChoice) {
    if (!q || studentChoice === undefined) return false;
    if (q.sig) {
      const expected = btoa(q.id + (studentChoice ? "_VERO" : "_FALSO") + _SEC_SALT);
      return q.sig === expected;
    }
    return q.a === studentChoice;
  }
'''

if 'function getQuestionCorrectAnswer' not in html:
    html = html.replace('// Initialize Setup', helpers + '\n  // Initialize Setup', 1)

# Replace occurrences of q.a
html = html.replace('const isVero = q.a === true;', 'const isVero = getQuestionCorrectAnswer(q);')
html = html.replace('const curVero = selected.filter(q => q.a === true).length;', 'const curVero = selected.filter(q => getQuestionCorrectAnswer(q)).length;')
html = html.replace('if (userAns === q.a) {', 'if (verifyStudentAnswer(q, userAns)) {')
html = html.replace('const correctIds = examQuestions.filter((q, idx) => userAnswers[idx] === q.a).map(q => q.id);', 'const correctIds = examQuestions.filter((q, idx) => verifyStudentAnswer(q, userAnswers[idx])).map(q => q.id);')
html = html.replace('const isCorrect = (userAns === q.a);', 'const isCorrect = (userAns !== undefined && verifyStudentAnswer(q, userAns));')
html = html.replace('const realText = q.a ? \'VERO\' : \'FALSO\';', 'const realText = getQuestionCorrectAnswer(q) ? \'VERO\' : \'FALSO\';')
html = html.replace('${q.a ? \'#34d399\' : \'#f87171\'}', '${getQuestionCorrectAnswer(q) ? \'#34d399\' : \'#f87171\'}')

# Dynamic alt tag for image
img_old = "imgElem.src = q.img;\n      imgElem.onerror = function() {"
img_new = "imgElem.src = q.img;\n      imgElem.alt = `Quiz Patente B - Segnale Capitolo ${q.ch || ''} domanda ${q.id} - إشارة رخصة القيادة الإيطالية`;\n      imgElem.onerror = function() {"
if img_old in html:
    html = html.replace(img_old, img_new, 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Simulatore_Esame.html updated with answer obfuscation & dynamic image alt tags!")

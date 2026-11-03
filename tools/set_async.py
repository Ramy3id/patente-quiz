file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\parole-spia.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Change data_all_questions.js from defer to async
text = text.replace('src="../Capitoli_Divisi/data_all_questions.js" defer', 'src="../Capitoli_Divisi/data_all_questions.js" async')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated data_all_questions.js to async")

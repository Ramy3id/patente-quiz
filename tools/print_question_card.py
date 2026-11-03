import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\allenamento-capitolo.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect from questionCard down to the end of questionCard
p_start = content.find('id="questionCard"')
if p_start == -1:
    p_start = content.find('class="tr-question-card"')

print("Question Card Start at:", p_start)
p_end = content.find('</main>', p_start)
print("Question Card End at:", p_end)
print(content[p_start:p_end+10])

import shutil
import os

src = r"R:\Ramy\PATENTE\Simulatore_Esame.html"
bak = r"R:\Ramy\PATENTE\Simulatore_Esame.html.bak"
if not os.path.exists(bak):
    shutil.copyfile(src, bak)

js_target = r"R:\Ramy\PATENTE\assets\js\data-simulatore-questions.js"

with open(bak, "r", encoding="utf-8") as f:
    lines = f.readlines()

line_2250 = lines[2249]
line_2251 = lines[2250]

with open(js_target, "w", encoding="utf-8") as f_out:
    f_out.write("// Patente B Pro - Ministerial Exam Dataset Cached Assets\n")
    f_out.write(line_2250.lstrip())
    f_out.write(line_2251.lstrip())

lines[2249] = "  // Questions pool loaded from external cached bundle: data-simulatore-questions.js\n"
lines[2250] = "\n"
lines.insert(2248, '<script src="assets/js/data-simulatore-questions.js"></script>\n')

with open(src, "w", encoding="utf-8") as f:
    f.writelines(lines)

new_size = os.path.getsize(src)
js_size = os.path.getsize(js_target)
print(f"Done! New Simulatore_Esame.html size: {new_size/1024:.2f} KB (was 7047 KB)")
print(f"data-simulatore-questions.js size: {js_size/(1024*1024):.2f} MB")

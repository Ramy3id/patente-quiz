import os

# 1. Update theme-engine.js
theme_engine_path = r"R:\Ramy\PATENTE\assets\js\theme-engine.js"
with open(theme_engine_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Change default to light
js_content = js_content.replace("// Default to dark mode for Patente B Pro\n    return 'dark';", "// Default to light mode for Patente B Pro\n    return 'light';")
js_content = js_content.replace("return 'dark';", "return 'light';")

with open(theme_engine_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("theme-engine.js default theme set to LIGHT!")

# 2. Update all HTML files from class="dark" to class="light"
base_dir = r"R:\Ramy\PATENTE"
updated_count = 0

for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".html"):
            fp = os.path.join(root, f)
            try:
                with open(fp, "r", encoding="utf-8") as fl:
                    html_content = fl.read()
                
                # Check for class="dark"
                if 'class="dark"' in html_content or "class='dark'" in html_content:
                    html_content = html_content.replace('class="dark"', 'class="light"')
                    html_content = html_content.replace("class='dark'", "class='light'")
                    with open(fp, "w", encoding="utf-8") as fl:
                        fl.write(html_content)
                    updated_count += 1
            except Exception as e:
                print(f"Error on {f}: {e}")

print(f"Updated {updated_count} HTML files to have class='light' by default!")

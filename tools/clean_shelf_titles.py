import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\parole-quiz.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Strip parentheses from the button text so it never truncates on mobile
old_snippet = """    shelf.innerHTML = PATENTE_THESAURUS.map(item => {
      // Create concise title by stripping long parenthesized text if needed, keeping icon + Arabic
      let shortCat = item.categoria;
      return `
        <button class="family-pill" onclick="selectThesaurusFamily('${item.id}')" title="${item.categoria}">
          <span>${shortCat}</span>
        </button>
      `;
    }).join('');"""

new_snippet = """    shelf.innerHTML = PATENTE_THESAURUS.map(item => {
      // Clean Arabic title by removing latin parenthesis from button face for crisp 2-col mobile grid
      const cleanTitle = item.categoria.replace(/\\s*\\([^)]*\\)/g, '').trim();
      return `
        <button class="family-pill" onclick="selectThesaurusFamily('${item.id}')" title="${item.categoria}">
          <span>${cleanTitle}</span>
        </button>
      `;
    }).join('');"""

if old_snippet in content:
    content = content.replace(old_snippet, new_snippet)
    print("Cleaned title snippet applied.")
else:
    print("Warning: old snippet not found directly, checking regex...")
    import re
    content = re.sub(r'let shortCat = item\.categoria;[\s\S]*?<span>\$\{shortCat\}</span>', r"const cleanTitle = item.categoria.replace(/\\s*\\([^)]*\\)/g, '').trim();\n      return `\n        <button class=\"family-pill\" onclick=\"selectThesaurusFamily('${item.id}')\" title=\"${item.categoria}\">\n          <span>${cleanTitle}</span>", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved.")

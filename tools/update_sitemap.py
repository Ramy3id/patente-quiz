import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r'R:\Ramy\PATENTE_PRO_APP\sitemap.xml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

count = content.count('https://patente-quiz-livid.vercel.app')
print(f"Found {count} occurrences of old Vercel URL in sitemap.xml")

content = content.replace('https://patente-quiz-livid.vercel.app', 'https://ramy3id.github.io/patente-quiz')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated sitemap.xml to official GitHub Pages domain successfully!")

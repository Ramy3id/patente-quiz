with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\scheda-esame.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's check opening and closing braces in style tags
import re
style_blocks = re.findall(r'<style[^>]*>([\s\S]*?)</style>', html)
for i, block in enumerate(style_blocks):
    open_b = block.count('{')
    close_b = block.count('}')
    print(f"Style block {i}: open={open_b}, close={close_b}, diff={open_b - close_b}")

# Also check around motoScreenWrap
idx = html.find('id="motoScreenWrap"')
print("motoScreenWrap in HTML:")
print(html[idx:idx+1500])

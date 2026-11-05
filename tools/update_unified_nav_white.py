with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_rule = """  html.light #globalPortalNav::before {
    background: linear-gradient(to right, 
      #009246 0%, #009246 33.33%, 
      #cbd5e1 33.33%, #cbd5e1 66.66%, 
      #ce2b37 66.66%, #ce2b37 100%
    ) !important;
    box-shadow: 0 0 12px rgba(206, 43, 55, 0.08) !important;
  }"""

new_rule = """  html.light #globalPortalNav::before {
    background: linear-gradient(to right, 
      #009246 0%, #009246 33.33%, 
      #ffffff 33.33%, #ffffff 66.66%, 
      #ce2b37 66.66%, #ce2b37 100%
    ) !important;
    box-shadow: 0 0 14px rgba(206, 43, 55, 0.12) !important;
  }"""

assert old_rule in js, "old_rule not found in unified-nav.js"
js = js.replace(old_rule, new_rule)

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated unified-nav.js successfully!")

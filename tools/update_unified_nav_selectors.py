with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_nav_block = """@media (min-width: 993px) {
  #globalPortalNav {
    position: fixed !important;
  }
  #globalPortalNav::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    border-radius: 18px !important;
    padding: 2.5px !important;
    background: linear-gradient(to right, 
      #009246 0%, #009246 33.33%, 
      #ffffff 33.33%, #ffffff 66.66%, 
      #ce2b37 66.66%, #ce2b37 100%
    ) !important;
    -webkit-mask: 
       linear-gradient(#fff 0 0) content-box, 
       linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    pointer-events: none !important;
    z-index: 10 !important;
    clip-path: polygon(0 0, 100% 0, 100% 22px, 0 22px) !important;
    box-shadow: 0 2px 10px rgba(206, 43, 55, 0.12) !important;
  }
  html.light #globalPortalNav::before {
    background: linear-gradient(to right, 
      #009246 0%, #009246 33.33%, 
      #ffffff 33.33%, #ffffff 66.66%, 
      #ce2b37 66.66%, #ce2b37 100%
    ) !important;
    box-shadow: 0 2px 10px rgba(206, 43, 55, 0.08) !important;
  }
}"""

new_nav_block = """@media (min-width: 993px) {
  #globalPortalNav,
  .unified-portal-nav,
  #portal-nav {
    position: fixed !important;
    height: 64px !important;
    max-height: 64px !important;
    border-radius: 18px !important;
  }
  #globalPortalNav::before,
  .unified-portal-nav::before,
  #portal-nav::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    border-radius: 18px !important;
    padding: 2.5px !important;
    background: linear-gradient(to right, 
      #009246 0%, #009246 33.33%, 
      #ffffff 33.33%, #ffffff 66.66%, 
      #ce2b37 66.66%, #ce2b37 100%
    ) !important;
    -webkit-mask: 
       linear-gradient(#fff 0 0) content-box, 
       linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    pointer-events: none !important;
    z-index: 10 !important;
    clip-path: polygon(0 0, 100% 0, 100% 22px, 0 22px) !important;
    box-shadow: 0 2px 10px rgba(206, 43, 55, 0.12) !important;
  }
  html.light #globalPortalNav::before,
  html.light .unified-portal-nav::before,
  html.light #portal-nav::before {
    background: linear-gradient(to right, 
      #009246 0%, #009246 33.33%, 
      #ffffff 33.33%, #ffffff 66.66%, 
      #ce2b37 66.66%, #ce2b37 100%
    ) !important;
    box-shadow: 0 2px 10px rgba(206, 43, 55, 0.08) !important;
  }
}"""

assert old_nav_block in js, "old_nav_block not found in unified-nav.js"
js = js.replace(old_nav_block, new_nav_block)

with open(r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated unified-nav.js with universal selectors!")

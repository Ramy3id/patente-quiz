with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_rule = '''    html.light #guestDashboardNotice span {
      color: #475569 !important;
    }'''

new_rule = '''    html.light #guestDashboardNotice span.banner-subtext {
      color: #475569 !important;
    }
    #guestDashboardNotice button,
    #guestDashboardNotice button span {
      color: #FFFFFF !important;
    }'''

text = text.replace(old_rule, new_rule)
text = text.replace('<span style="font-size: 0.78rem;', '<span class="banner-subtext" style="font-size: 0.78rem;')

with open(r'R:\Ramy\PATENTE_PRO_APP\interactive_pages\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated banner styles successfully.')

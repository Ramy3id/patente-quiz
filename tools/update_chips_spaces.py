with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_chips_markup = '''      <button class="chip-btn" data-cat="segnali" onclick="setCategory('segnali')">
        <span class="chip-title">الإشارات</span>
        <span class="chip-sub">02-10</span>
      </button>
      <button class="chip-btn" data-cat="norme" onclick="setCategory('norme')">
        <span class="chip-title">القواعد</span>
        <span class="chip-sub">11-13</span>
      </button>
      <button class="chip-btn" data-cat="precedenze" onclick="setCategory('precedenze')">
        <span class="chip-title">التقاطعات</span>
        <span class="chip-sub">14-16</span>
      </button>
      <button class="chip-btn" data-cat="sicurezza" onclick="setCategory('sicurezza')">
        <span class="chip-title">السلامة</span>
        <span class="chip-sub">17-20</span>
      </button>
      <button class="chip-btn" data-cat="meccanica" onclick="setCategory('meccanica')">
        <span class="chip-title">الميكانيكا</span>
        <span class="chip-sub">21-25</span>
      </button>'''

new_chips_markup = '''      <button class="chip-btn" data-cat="segnali" onclick="setCategory('segnali')">
        <span class="chip-title">الإشارات</span>
        <span class="chip-sub">02 - 10</span>
      </button>
      <button class="chip-btn" data-cat="norme" onclick="setCategory('norme')">
        <span class="chip-title">القواعد</span>
        <span class="chip-sub">11 - 13</span>
      </button>
      <button class="chip-btn" data-cat="precedenze" onclick="setCategory('precedenze')">
        <span class="chip-title">التقاطعات</span>
        <span class="chip-sub">14 - 16</span>
      </button>
      <button class="chip-btn" data-cat="sicurezza" onclick="setCategory('sicurezza')">
        <span class="chip-title">السلامة</span>
        <span class="chip-sub">17 - 20</span>
      </button>
      <button class="chip-btn" data-cat="meccanica" onclick="setCategory('meccanica')">
        <span class="chip-title">الميكانيكا</span>
        <span class="chip-sub">21 - 25</span>
      </button>'''

if old_chips_markup in c:
    c = c.replace(old_chips_markup, new_chips_markup)
    with open(r'R:\Ramy\PATENTE_PRO_APP\Capitoli_Divisi\index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated chip-sub texts in Capitoli_Divisi/index.html successfully!")
else:
    print("Warning: old_chips_markup not found")

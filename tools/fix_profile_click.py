# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update firebase-auth-engine.js
auth_file = 'R:/Ramy/PATENTE/assets/js/firebase-auth-engine.js'
with open(auth_file, 'r', encoding='utf-8') as f:
    auth_code = f.read()

# Replace toggleProfileDropdown and export it
old_toggle_start = '  function toggleProfileDropdown(profile) {'
old_toggle_end = '  function updateSyncIndicator(isSync) {'

p1 = auth_code.find(old_toggle_start)
p2 = auth_code.find(old_toggle_end)

if p1 != -1 and p2 != -1:
    new_toggle_func = '''  function toggleProfileDropdown(profile) {
    const active = userProfile || profile || {};
    let drop = document.getElementById('authProfileDropdown');
    const pill = document.getElementById('globalAuthPill');
    const mobBtn = document.getElementById('btnOpenMobileAuth');

    // Use document.body to prevent parent container clipping/overflow issues
    if (!drop) {
      drop = document.createElement('div');
      drop.className = 'auth-profile-dropdown';
      drop.id = 'authProfileDropdown';
      document.body.appendChild(drop);
    }

    const isCurrentlyOpen = drop.classList.contains('open');
    if (isCurrentlyOpen) {
      drop.classList.remove('open');
      return;
    }

    const fullName = active.fullName || `${active.firstName || ''} ${active.lastName || ''}`.trim() || active.displayName || 'طالب رخصة القيادة';
    const email = active.email || (currentUser ? currentUser.email : '');
    const phone = active.phone || 'غير مسجل';
    const bdate = active.birthDate || 'غير مسجل';
    const genderStr = active.gender === 'male' ? 'ذكر 👨' : active.gender === 'female' ? 'أنثى 👩' : 'غير محدد / آخر 👤';
    const firstLetter = (active.firstName || active.fullName || 'ط').trim().charAt(0).toUpperCase();

    drop.innerHTML = `
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px; padding-bottom:12px; border-bottom:1px solid rgba(255,255,255,0.08);">
        <div style="width:44px; height:44px; border-radius:50%; background:#10B981; color:#FFF; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.15rem; flex-shrink:0; box-shadow:0 2px 8px rgba(16,185,129,0.3);">
          ${escapeHtml(firstLetter)}
        </div>
        <div style="overflow:hidden; flex:1;">
          <div style="font-weight:800; font-size:0.98rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:var(--text-primary, inherit);">${escapeHtml(fullName)}</div>
          <div style="font-size:0.75rem; color:#94A3B8; direction:ltr; text-align:right; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHtml(email)}</div>
        </div>
      </div>

      <div style="font-size:0.8rem; margin-bottom:14px; line-height:1.75; color:inherit;">
        <div style="display:flex; justify-content:space-between;"><span>📱 <strong>الهاتف:</strong></span> <span dir="ltr">${escapeHtml(phone)}</span></div>
        <div style="display:flex; justify-content:space-between;"><span>🎂 <strong>الميلاد:</strong></span> <span>${escapeHtml(bdate)}</span></div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:2px;">
          <span>👤 <strong>النوع:</strong> ${genderStr}</span>
          <button id="btnDeleteAccountInline" title="حذف الحساب وجميع البيانات نهائياً من السحابة" style="background:transparent; border:none; color:#EF4444; font-size:0.72rem; cursor:pointer; padding:1px 4px; border-radius:4px; opacity:0.85; font-family:inherit; transition:all 0.2s; display:inline-flex; align-items:center; gap:3px;">
            <span>🗑️</span>
            <span>حذف الحساب</span>
          </button>
        </div>
      </div>

      <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.22); border-radius:10px; padding:10px 12px; margin-bottom:12px; font-size:0.76rem;">
        <div id="dropdownSyncStatusText" style="color:#10B981; font-weight:800;">🟢 الحساب متصل ومتزامن سحابياً</div>
        <div style="color:#64748B; font-size:0.7rem; margin-top:3px;">يتم حفظ تقدمك تلقائياً بعد كل باب وامتحان.</div>
      </div>

      <button id="btnManualSyncNow" style="width:100%; height:36px; border-radius:10px; background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.3); color:#0284C7; font-weight:700; font-size:0.82rem; cursor:pointer; font-family:inherit; margin-bottom:8px; display:flex; align-items:center; justify-content:center; gap:6px;">
        <span>🔄 مزامنة سحابية فورية الآن</span>
      </button>

      <button id="btnAuthLogout" style="width:100%; height:36px; border-radius:10px; background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.28); color:#EF4444; font-weight:700; font-size:0.82rem; cursor:pointer; font-family:inherit; display:flex; align-items:center; justify-content:center; gap:6px;">
        <span>🚪 تسجيل الخروج</span>
      </button>
    `;

    // Position dynamically relative to trigger button
    const targetTrigger = (window.innerWidth <= 992 && mobBtn) ? mobBtn : (pill || mobBtn);
    if (targetTrigger) {
      const rect = targetTrigger.getBoundingClientRect();
      const dropWidth = 300;
      
      if (window.innerWidth <= 640) {
        drop.style.position = 'fixed';
        drop.style.top = (rect.bottom + 8) + 'px';
        drop.style.left = '12px';
        drop.style.right = '12px';
        drop.style.width = 'auto';
      } else {
        drop.style.position = 'fixed';
        drop.style.top = (rect.bottom + 8) + 'px';
        let leftPos = rect.left;
        if (leftPos + dropWidth > window.innerWidth - 12) {
          leftPos = window.innerWidth - dropWidth - 12;
        }
        if (leftPos < 12) leftPos = 12;
        drop.style.left = leftPos + 'px';
        drop.style.right = 'auto';
        drop.style.width = dropWidth + 'px';
      }
    }

    drop.classList.add('open');

    // زر المزامنة الفورية
    const syncBtn = document.getElementById('btnManualSyncNow');
    if (syncBtn) {
      syncBtn.onclick = async () => {
        syncBtn.innerHTML = 'جاري المزامنة... ⏳';
        syncBtn.disabled = true;
        if (currentUser && currentUser.uid) {
          await uploadLocalProgressToCloud(currentUser.uid);
        }
        syncBtn.innerHTML = '✅ تمت المزامنة بنجاح!';
        setTimeout(() => {
          syncBtn.innerHTML = '<span>🔄 مزامنة سحابية فورية الآن</span>';
          syncBtn.disabled = false;
        }, 1500);
      };
    }

    // زر تسجيل الخروج
    const logoutBtn = document.getElementById('btnAuthLogout');
    if (logoutBtn) {
      logoutBtn.onclick = async () => {
        if (confirm('هل تريد تسجيل الخروج من حسابك؟')) {
          await logoutAccount();
          drop.classList.remove('open');
        }
      };
    }

    // زر حذف الحساب نهائياً
    const delBtn = document.getElementById('btnDeleteAccountInline');
    if (delBtn) {
      delBtn.onclick = async () => {
        const confirmed = confirm(
          '⚠️ تحذير نهائي:\\n\\n' +
          'هل أنت متأكد تماماً من حذف حسابك وكافة سجلاتك وتقدمك السحابي نهائياً؟\\n\\n' +
          '• سيتم مسح ملفك وجميع سجلاتك من خوادم السحابة فوراً.\\n' +
          '• لن تتمكن من استرجاع تقدمك في الأسئلة أو الامتحانات بعد الحذف.\\n' +
          '• يمكنك إنشاء حساب جديد بنفس البريد لاحقاً في أي وقت.'
        );
        if (!confirmed) return;

        delBtn.innerHTML = 'جاري الحذف... ⏳';
        delBtn.disabled = true;

        try {
          await deleteCurrentAccount();
          drop.classList.remove('open');
          alert('✅ تم حذف حسابك وكافة بياناتك السحابية نهائياً بنجاح.');
        } catch (err) {
          delBtn.innerHTML = '<span>🗑️</span> <span>حذف الحساب</span>';
          delBtn.disabled = false;
          if (err && err.code === 'auth/requires-recent-login') {
            alert('🔒 لأسباب أمنية مشددة، يتطلب حذف الحساب إعادة تسجيل الدخول حديثاً. يرجى تسجيل الخروج ثم الدخول مرة أخرى والمحاولة مجدداً.');
          } else {
            alert('تعذر حذف الحساب حالياً: ' + ((err && err.message) || 'يرجى المحاولة لاحقاً.'));
          }
        }
      };
    }

    // إغلاق عند النقر بالخارج
    const closeListener = (evt) => {
      if (!drop.contains(evt.target) && (!pill || !pill.contains(evt.target)) && (!mobBtn || !mobBtn.contains(evt.target))) {
        drop.classList.remove('open');
        document.removeEventListener('click', closeListener);
      }
    };
    setTimeout(() => document.addEventListener('click', closeListener), 10);
  }

  '''
    auth_code = auth_code[:p1] + new_toggle_func + auth_code[p2:]
    print("toggleProfileDropdown rewritten successfully in firebase-auth-engine.js!")

# Expose toggleProfileDropdown in window.PatenteAuth
if 'toggleProfileDropdown: toggleProfileDropdown' not in auth_code:
    auth_code = auth_code.replace('openAuthModal: openAuthModal', 'openAuthModal: openAuthModal,\n    toggleProfileDropdown: toggleProfileDropdown')
    print("toggleProfileDropdown exposed in window.PatenteAuth!")

# Update light mode styling in firebase-auth-engine.js for dropdown
old_dropdown_css = '''.auth-profile-dropdown {
        position: absolute;'''
new_dropdown_css = '''.auth-profile-dropdown {
        position: fixed;
        color: #F8FAFC;'''

if old_dropdown_css in auth_code:
    auth_code = auth_code.replace(old_dropdown_css, new_dropdown_css, 1)

old_light_dropdown = '''      html.light .auth-profile-dropdown {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.1);
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.15);
      }'''

new_light_dropdown = '''      html.light .auth-profile-dropdown {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.12);
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.18), 0 4px 12px rgba(15, 23, 42, 0.08);
        color: #0F172A;
      }
      html.light .auth-profile-dropdown #btnManualSyncNow {
        color: #0284C7 !important;
        background: rgba(2, 132, 199, 0.08) !important;
        border-color: rgba(2, 132, 199, 0.25) !important;
      }
      html.light .auth-profile-dropdown div[style*="background:rgba(16,185,129,0.08)"] {
        background: rgba(16, 185, 129, 0.06) !important;
        border-color: rgba(16, 185, 129, 0.2) !important;
      }'''

if old_light_dropdown in auth_code:
    auth_code = auth_code.replace(old_light_dropdown, new_light_dropdown, 1)

with open(auth_file, 'w', encoding='utf-8') as f:
    f.write(auth_code)
print("firebase-auth-engine.js saved!")

# 2. Update unified-nav.js
nav_file = 'R:/Ramy/PATENTE/assets/js/unified-nav.js'
with open(nav_file, 'r', encoding='utf-8') as f:
    nav_code = f.read()

old_open_auth = '''    // 7. زر حساب المستخدم والمزامنة (Desktop & Mobile)
    const openAuthFn = function (e) {
      if (e) e.preventDefault();
      if (window.PatenteAuth && window.PatenteAuth.openAuthModal) {
        window.PatenteAuth.openAuthModal();
      } else {
        const m = document.getElementById('patenteAuthModal');
        if (m) m.classList.add('open');
      }
    };
    const deskAuthBtn = document.getElementById('globalAuthPill');
    if (deskAuthBtn) deskAuthBtn.onclick = openAuthFn;

    const mobAuthBtn = document.getElementById('btnOpenMobileAuth');
    if (mobAuthBtn) mobAuthBtn.onclick = openAuthFn;'''

new_open_auth = '''    // 7. زر حساب المستخدم والمزامنة (Desktop & Mobile)
    const openAuthFn = function (e) {
      if (e) e.preventDefault();
      if (window.PatenteAuth) {
        if (window.PatenteAuth.isLoggedIn && window.PatenteAuth.isLoggedIn()) {
          if (window.PatenteAuth.toggleProfileDropdown) {
            window.PatenteAuth.toggleProfileDropdown();
            return;
          }
        }
        if (window.PatenteAuth.openAuthModal) {
          window.PatenteAuth.openAuthModal();
          return;
        }
      }
      const m = document.getElementById('patenteAuthModal');
      if (m) m.classList.add('open');
    };
    const deskAuthBtn = document.getElementById('globalAuthPill');
    if (deskAuthBtn) deskAuthBtn.onclick = openAuthFn;

    const mobAuthBtn = document.getElementById('btnOpenMobileAuth');
    if (mobAuthBtn) mobAuthBtn.onclick = openAuthFn;

    // Listen to patente:auth-changed to wire dynamic profile dropdown
    window.addEventListener('patente:auth-changed', function (ev) {
      const detail = ev.detail || {};
      const mobBtn = document.getElementById('btnOpenMobileAuth');
      const deskPill = document.getElementById('globalAuthPill');
      if (detail.loggedIn) {
        const profile = detail.user || (window.PatenteAuth && window.PatenteAuth.getUserProfile && window.PatenteAuth.getUserProfile());
        if (mobBtn) {
          mobBtn.classList.add('logged-in');
          mobBtn.onclick = (e) => {
            e.stopPropagation();
            if (window.PatenteAuth && window.PatenteAuth.toggleProfileDropdown) {
              window.PatenteAuth.toggleProfileDropdown(profile);
            }
          };
        }
      }
    });'''

if old_open_auth in nav_code:
    nav_code = nav_code.replace(old_open_auth, new_open_auth, 1)
    with open(nav_file, 'w', encoding='utf-8') as f:
        f.write(nav_code)
    print("unified-nav.js updated with auth-aware handlers!")
else:
    print("Warning: old_open_auth not found in unified-nav.js directly!")

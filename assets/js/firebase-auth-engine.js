/**
 * =======================================================================
 * Patente B Pro - Cloud Authentication & Firestore Sync Engine (2026)
 * =======================================================================
 * @author Eng. Ramy Eid Saad Fahmy & Architecture Team
 * @description
 * - المحرك السحابي المتكامل للحسابات والمزامنة الفورية عبر Google Firebase.
 * - التسجيل الكامل بالبيانات: (الاسم، اللقب، البريد، كلمة المرور، الهاتف، تاريخ الميلاد، النوع).
 * - تسجيل الدخول بالبريد الإلكتروني أو حساب Google بنقرة واحدة.
 * - مزامنة إنجاز الـ 25 باباً، بنك الأخطاء، وسجل الامتحانات تلقائياً عبر الأجهزة.
 * - تصميم Apple HIG كامل التجاوب مع الثيم الليلي والنهاري (Light/Dark Mode).
 */

(function () {
  'use strict';

  // 1. مفاتيح إعدادات مشروع Firebase الرسمي
  const FIREBASE_CONFIG = {
    apiKey: "AIzaSyBvnl-gy7sGsdG5M6dTmhYU7ZI5VUblH7s",
    authDomain: "patente-b-pro.firebaseapp.com",
    projectId: "patente-b-pro",
    storageBucket: "patente-b-pro.firebasestorage.app",
    messagingSenderId: "170993396640",
    appId: "1:170993396640:web:14024c306960017f9d52c5",
    measurementId: "G-0XKH713DCV"
  };

  // حالة النظام والمستخدم الحالي
  let authApp = null;
  let authInstance = null;
  let firestoreInstance = null;
  let currentUser = null;
  let userProfile = null;
  let isSyncing = false;
  let lastSyncTime = null;

  // 2. تحميل مكتبات Firebase SDK ديناميكياً بشكل متسلسل آمن
  function loadSingleScript(src) {
    return new Promise((resolve, reject) => {
      if (document.querySelector(`script[src="${src}"]`)) return resolve();
      const script = document.createElement('script');
      script.src = src;
      script.onload = () => resolve();
      script.onerror = (err) => {
        console.warn('تعذر تحميل السكربت:', src, err);
        reject(err);
      };
      document.head.appendChild(script);
    });
  }

  async function loadFirebaseSDKs() {
    if (window.firebase && window.firebase.auth && window.firebase.firestore) {
      return window.firebase;
    }

    // 1. يجب تحميل app-compat أولاً لتعريف window.firebase
    await loadSingleScript('https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js');

    // 2. تحميل auth و firestore معاً
    await Promise.all([
      loadSingleScript('https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js'),
      loadSingleScript('https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore-compat.js')
    ]);

    return window.firebase;
  }

  // 3. تهيئة النظام السحابي
  async function initFirebase() {
    try {
      const fb = await loadFirebaseSDKs();
      if (!fb.apps.length) {
        authApp = fb.initializeApp(FIREBASE_CONFIG);
      } else {
        authApp = fb.app();
      }

      authInstance = fb.auth();
      firestoreInstance = fb.firestore();

      // تفعيل الكاش الداخلي بدون إنترنت
      try {
        firestoreInstance.enablePersistence({ synchronizeTabs: true }).catch(() => {});
      } catch (_) {}

      // الاستماع لتغير حالة الدخول
      authInstance.onAuthStateChanged(handleAuthStateChange);

      return true;
    } catch (err) {
      console.warn('PatenteAuth: يعمل التطبيق في الوضع المحلي (Offline Mode)');
      updateAuthUiLoggedOut();
      return false;
    }
  }

  // 4. معالجة تغير حالة المصادقة (Auth State Change)
  async function handleAuthStateChange(user) {
    currentUser = user;
    if (user) {
      try {
        // جلب بيانات ملف الطالب من Firestore
        const docRef = firestoreInstance.collection('users').doc(user.uid);
        const docSnap = await docRef.get();
        if (docSnap.exists) {
          userProfile = docSnap.data();
        } else {
          // ملف مبدئي لحسابات Google الجديدة
          const nameParts = (user.displayName || 'طالب جديد').split(' ');
          userProfile = {
            uid: user.uid,
            firstName: nameParts[0] || 'طالب',
            lastName: nameParts.slice(1).join(' ') || '',
            email: user.email || '',
            phone: user.phoneNumber || '',
            birthDate: '',
            gender: 'unspecified',
            createdAt: window.firebase.firestore.FieldValue.serverTimestamp()
          };
          await docRef.set(userProfile, { merge: true });
        }

        updateAuthUiLoggedIn(userProfile || { displayName: user.displayName, email: user.email });

        // مزامنة تلقائية هادئة مع السحابة عند الدخول
        syncBidirectional(user.uid);
      } catch (err) {
        console.error('Error fetching user profile:', err);
        updateAuthUiLoggedIn({ displayName: user.displayName || user.email, email: user.email });
      }
    } else {
      userProfile = null;
      updateAuthUiLoggedOut();
    }
  }

  // 5. تسجيل حساب جديد (Register)
  async function registerAccount({ firstName, lastName, email, password, phone, birthDate, gender }) {
    if (!authInstance) throw new Error('خدمة السحابة غير مهيأة بعد');
    if (!email || !password) throw new Error('يرجى ملء البريد الإلكتروني وكلمة المرور');
    if (password.length < 6) throw new Error('كلمة المرور يجب ألا تقل عن 6 خانات');

    // إنشاء الحساب في Firebase Auth
    const cred = await authInstance.createUserWithEmailAndPassword(email, password);
    const user = cred.user;

    // تحديث الاسم المعروض في Firebase Auth
    const fullName = `${firstName.trim()} ${lastName.trim()}`.trim();
    await user.updateProfile({ displayName: fullName });

    // حفظ تفاصيل الملف الشخصي الكاملة في Firestore
    const profileData = {
      uid: user.uid,
      firstName: firstName.trim(),
      lastName: lastName.trim(),
      fullName: fullName,
      email: email.trim().toLowerCase(),
      phone: (phone || '').trim(),
      birthDate: birthDate || '',
      gender: gender || 'unspecified',
      createdAt: window.firebase.firestore.FieldValue.serverTimestamp(),
      lastLoginAt: window.firebase.firestore.FieldValue.serverTimestamp(),
      platform: 'Patente B Pro 2026'
    };

    await firestoreInstance.collection('users').doc(user.uid).set(profileData);
    userProfile = profileData;

    // رفع التقدم المحلي الحالي تلقائياً إلى الحساب الجديد لمنع ضياع أي إنجاز سابق
    await uploadLocalProgressToCloud(user.uid);

    return user;
  }

  // 6. تسجيل الدخول (Email & Password)
  async function loginAccount(email, password) {
    if (!authInstance) throw new Error('خدمة السحابة غير مهيأة بعد');
    const cred = await authInstance.signInWithEmailAndPassword(email.trim(), password);
    
    // تحديث تاريخ آخر دخول
    try {
      await firestoreInstance.collection('users').doc(cred.user.uid).update({
        lastLoginAt: window.firebase.firestore.FieldValue.serverTimestamp()
      });
    } catch (_) {}

    return cred.user;
  }

  // 7. الدخول عبر Google
  async function loginWithGoogle() {
    if (!authInstance) throw new Error('خدمة السحابة غير مهيأة بعد');
    const provider = new window.firebase.auth.GoogleAuthProvider();
    provider.setCustomParameters({ prompt: 'select_account' });
    const res = await authInstance.signInWithPopup(provider);
    return res.user;
  }

  // 8. تسجيل الخروج (Logout)
  async function logoutAccount() {
    if (!authInstance) return;
    await authInstance.signOut();
    userProfile = null;
    currentUser = null;
    updateAuthUiLoggedOut();
  }

  // 9. استرجاع كلمة المرور
  async function resetPassword(email) {
    if (!authInstance) throw new Error('خدمة السحابة غير مهيأة');
    await authInstance.sendPasswordResetEmail(email.trim());
  }

  // 10. تجميع التقدم المحلي من المتصفح (Local Data Collector)
  function collectLocalProgress() {
    const chaptersData = {};
    for (let ch = 1; ch <= 25; ch++) {
      try {
        const raw = localStorage.getItem('patente_progress_cap_' + ch);
        if (raw) chaptersData[ch] = JSON.parse(raw);
      } catch (_) {}
    }

    let examHistory = [];
    try {
      const rawHist = localStorage.getItem('patente_exam_history');
      if (rawHist) examHistory = JSON.parse(rawHist);
    } catch (_) {}

    let srsVault = {};
    try {
      const rawSrs = localStorage.getItem('patente_b_pro_srs_vault');
      if (rawSrs) srsVault = JSON.parse(rawSrs);
    } catch (_) {}

    return {
      chapters: chaptersData,
      examHistory,
      srsVault,
      theme: localStorage.getItem('patente_app_theme') || 'dark',
      savedAt: Date.now()
    };
  }

  // 11. رفع التقدم المحلي إلى Firestore
  async function uploadLocalProgressToCloud(uid) {
    if (!firestoreInstance || !uid) return;
    isSyncing = true;
    updateSyncIndicator(true);

    try {
      const localData = collectLocalProgress();
      const progressDocRef = firestoreInstance.collection('users').doc(uid).collection('userData').doc('progress');
      
      await progressDocRef.set({
        ...localData,
        updatedAt: window.firebase.firestore.FieldValue.serverTimestamp()
      }, { merge: true });

      lastSyncTime = new Date();
      updateSyncStatusText(`تمت المزامنة سحابياً: ${lastSyncTime.toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' })} 🟢`);
    } catch (err) {
      console.error('Error uploading progress to cloud:', err);
      updateSyncStatusText('تعذرت المزامنة السحابية حالياً ⚠️');
    } finally {
      isSyncing = false;
      updateSyncIndicator(false);
    }
  }

  // 12. جلب التقدم السحابي وتطبيقه محلياً (Cloud to Local Pull)
  async function pullCloudProgressToLocal(uid) {
    if (!firestoreInstance || !uid) return;
    isSyncing = true;
    updateSyncIndicator(true);

    try {
      const docRef = firestoreInstance.collection('users').doc(uid).collection('userData').doc('progress');
      const snap = await docRef.get();

      if (snap.exists) {
        const cloudData = snap.data();

        // دمج الأبواب الـ 25
        if (cloudData.chapters) {
          Object.keys(cloudData.chapters).forEach(ch => {
            const capData = cloudData.chapters[ch];
            if (capData) {
              localStorage.setItem('patente_progress_cap_' + ch, JSON.stringify(capData));
            }
          });
        }

        // دمج سجل الامتحانات
        if (Array.isArray(cloudData.examHistory) && cloudData.examHistory.length > 0) {
          localStorage.setItem('patente_exam_history', JSON.stringify(cloudData.examHistory));
        }

        // دمج بنك الأخطاء
        if (cloudData.srsVault && Object.keys(cloudData.srsVault).length > 0) {
          localStorage.setItem('patente_b_pro_srs_vault', JSON.stringify(cloudData.srsVault));
        }

        // تحديث شارات الهيدر واللوحة الحالية
        if (typeof window.updatePortalProgress === 'function') {
          window.updatePortalProgress();
        }

        window.dispatchEvent(new CustomEvent('patente:cloud-synced', { detail: cloudData }));

        lastSyncTime = new Date();
        updateSyncStatusText(`تمت المزامنة سحابياً: ${lastSyncTime.toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' })} 🟢`);
      }
    } catch (err) {
      console.error('Error pulling cloud progress:', err);
    } finally {
      isSyncing = false;
      updateSyncIndicator(false);
    }
  }

  // 13. المزامنة الذكية ثنائية الاتجاه (Bidirectional Sync)
  async function syncBidirectional(uid) {
    if (!firestoreInstance || !uid) return;
    try {
      const docRef = firestoreInstance.collection('users').doc(uid).collection('userData').doc('progress');
      const snap = await docRef.get();

      if (!snap.exists) {
        // لا يوجد بيانات سحابية سابقة: ارفع البيانات المحلية فوراً
        await uploadLocalProgressToCloud(uid);
      } else {
        const cloudData = snap.data();
        const localData = collectLocalProgress();

        // مقارنة التحديث الأحدث أو الدمج
        const cloudTime = cloudData.savedAt || 0;
        const localTime = localData.savedAt || 0;

        if (cloudTime > localTime) {
          await pullCloudProgressToLocal(uid);
        } else {
          await uploadLocalProgressToCloud(uid);
        }
      }
    } catch (e) {
      console.warn('Sync bidirectional warning:', e);
    }
  }

  // =========================================================
  // 14. واجهة المستخدم والتصميم (UI & Apple HIG Modal Suite)
  // =========================================================

  function injectAuthStyles() {
    if (document.getElementById('patenteAuthStyles')) return;
    const style = document.createElement('style');
    style.id = 'patenteAuthStyles';
    style.textContent = `
      /* زر الحساب في الهيدر */
      .nav-auth-pill {
        height: 36px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 12px;
        border-radius: 9px;
        font-family: inherit;
        font-size: 0.8rem;
        font-weight: 700;
        cursor: pointer;
        border: 1px solid rgba(56, 189, 248, 0.28);
        background: rgba(56, 189, 248, 0.08);
        color: #38BDF8;
        transition: all 0.2s ease;
        position: relative;
        white-space: nowrap;
        outline: none;
        text-decoration: none;
      }
      .nav-auth-pill:hover {
        background: rgba(56, 189, 248, 0.18);
        border-color: rgba(56, 189, 248, 0.5);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.2);
      }
      html.light .nav-auth-pill {
        background: rgba(2, 132, 199, 0.06);
        border-color: rgba(2, 132, 199, 0.25);
        color: #0284C7;
      }
      html.light .nav-auth-pill:hover {
        background: rgba(2, 132, 199, 0.12);
        border-color: rgba(2, 132, 199, 0.45);
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.15);
      }
      .nav-auth-pill.logged-in {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.35);
        color: #34D399;
      }
      html.light .nav-auth-pill.logged-in {
        background: rgba(5, 150, 105, 0.08);
        border-color: rgba(5, 150, 105, 0.3);
        color: #059669;
      }
      .auth-online-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 8px #10B981;
        display: inline-block;
      }
      .auth-online-dot.syncing {
        background: #F59E0B;
        box-shadow: 0 0 8px #F59E0B;
        animation: authPulse 0.8s infinite alternate;
      }
      @keyframes authPulse {
        from { opacity: 0.4; transform: scale(0.85); }
        to { opacity: 1; transform: scale(1.2); }
      }

      /* نافذة المصادقة المنبثقة الفاخرة */
      .auth-modal-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        z-index: 100000;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 16px;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.25s ease;
      }
      .auth-modal-backdrop.open {
        opacity: 1;
        pointer-events: auto;
      }
      .auth-modal-card {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        width: 100%;
        max-width: 480px;
        max-height: 90vh;
        overflow-y: auto;
        padding: 28px 24px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
        transform: scale(0.95) translateY(12px);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        color: #F8FAFC;
        position: relative;
        direction: rtl;
        text-align: right;
      }
      html.light .auth-modal-card {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.1);
        color: #0F172A;
        box-shadow: 0 25px 60px rgba(15, 23, 42, 0.15);
      }
      .auth-modal-backdrop.open .auth-modal-card {
        transform: scale(1) translateY(0);
      }
      .auth-close-btn {
        position: absolute;
        top: 20px;
        left: 20px;
        background: rgba(255, 255, 255, 0.08);
        border: none;
        color: #94A3B8;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        transition: all 0.2s ease;
      }
      html.light .auth-close-btn { background: #F1F5F9; color: #475569; }
      .auth-close-btn:hover { background: #EF4444; color: #FFF; }

      /* تبويبات التبديل دخول / تسجيل */
      .auth-tabs-nav {
        display: flex;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 4px;
        margin-bottom: 22px;
        border: 1px solid rgba(255, 255, 255, 0.08);
      }
      html.light .auth-tabs-nav { background: #F1F5F9; border-color: rgba(15, 23, 42, 0.08); }
      .auth-tab-btn {
        flex: 1;
        padding: 10px;
        border: none;
        background: transparent;
        color: #94A3B8;
        font-size: 0.9rem;
        font-weight: 700;
        cursor: pointer;
        border-radius: 10px;
        transition: all 0.2s ease;
        font-family: inherit;
      }
      html.light .auth-tab-btn { color: #64748B; }
      .auth-tab-btn.active {
        background: #38BDF8;
        color: #0F172A;
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.35);
      }
      html.light .auth-tab-btn.active {
        background: #0284C7;
        color: #FFFFFF;
      }

      /* حقول الإدخال */
      .auth-field-group {
        margin-bottom: 14px;
      }
      .auth-label {
        display: block;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 6px;
        color: #94A3B8;
      }
      html.light .auth-label { color: #475569; }
      .auth-input, .auth-select {
        width: 100%;
        height: 44px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #FFF;
        padding: 0 14px;
        font-family: inherit;
        font-size: 0.9rem;
        outline: none;
        transition: all 0.2s ease;
      }
      html.light .auth-input, html.light .auth-select {
        background: #F8FAFC;
        border-color: rgba(15, 23, 42, 0.15);
        color: #0F172A;
      }
      .auth-input:focus, .auth-select:focus {
        border-color: #38BDF8;
        background: rgba(56, 189, 248, 0.05);
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.18);
      }
      .auth-row-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
      }

      /* زر الإجراء الأساسي */
      .auth-submit-btn {
        width: 100%;
        height: 46px;
        border-radius: 12px;
        background: #10B981;
        color: #FFFFFF;
        border: none;
        font-size: 0.95rem;
        font-weight: 800;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: inherit;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin-top: 18px;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
      }
      .auth-submit-btn:hover {
        background: #059669;
        transform: translateY(-1px);
      }
      .auth-submit-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }

      /* زر الدخول بجوجل */
      .auth-google-btn {
        width: 100%;
        height: 44px;
        border-radius: 12px;
        background: #FFFFFF;
        color: #0F172A;
        border: 1px solid rgba(15, 23, 42, 0.15);
        font-size: 0.88rem;
        font-weight: 700;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-top: 12px;
        font-family: inherit;
        transition: all 0.2s ease;
      }
      .auth-google-btn:hover {
        background: #F8FAFC;
        transform: translateY(-1px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      }

      /* تنبيهات الأخطاء والنجاح */
      .auth-alert-msg {
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 14px;
        display: none;
      }
      .auth-alert-msg.error {
        display: block;
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
      }
      .auth-alert-msg.success {
        display: block;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
      }

      /* قائمة الملف الشخصي المنسدلة */
      .auth-profile-dropdown {
        position: absolute;
        top: calc(100% + 10px);
        left: 0;
        width: 290px;
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
        display: none;
        z-index: 99999;
        direction: rtl;
        text-align: right;
      }
      html.light .auth-profile-dropdown {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.1);
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.15);
      }
      .auth-profile-dropdown.open { display: block; }
    `;
    document.head.appendChild(style);
  }

  // 15. حقن نافذة تسجيل الدخول في الصفحة
  function injectAuthModalHtml() {
    if (document.getElementById('patenteAuthModal')) return;

    const modal = document.createElement('div');
    modal.className = 'auth-modal-backdrop';
    modal.id = 'patenteAuthModal';
    modal.innerHTML = `
      <div class="auth-modal-card" role="dialog" aria-modal="true">
        <button class="auth-close-btn" id="btnAuthClose" title="إغلاق">✕</button>

        <div style="text-align:center; margin-bottom:18px;">
          <div style="font-size:2rem; margin-bottom:4px;">🚦</div>
          <h2 style="font-size:1.25rem; font-weight:800; margin:0;" id="authModalTitle">تسجيل الدخول إلى Patente B Pro</h2>
          <p style="font-size:0.78rem; color:#94A3B8; margin-top:4px;">احفظ إنجازك في السحابة وزامنه عبر جميع أجهزتك</p>
        </div>

        <div class="auth-tabs-nav">
          <button class="auth-tab-btn active" id="tabBtnLogin">تسجيل الدخول</button>
          <button class="auth-tab-btn" id="tabBtnRegister">حساب جديد</button>
        </div>

        <div class="auth-alert-msg" id="authAlertMsg"></div>

        <!-- فورم تسجيل الدخول -->
        <form id="authLoginForm">
          <div class="auth-field-group">
            <label class="auth-label">البريد الإلكتروني</label>
            <input type="email" class="auth-input" id="loginEmail" placeholder="name@example.com" required dir="ltr">
          </div>
          <div class="auth-field-group">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <label class="auth-label">كلمة المرور</label>
              <a href="#" id="btnForgotPassword" style="font-size:0.75rem; color:#38BDF8; text-decoration:none;">نسيت كلمة المرور؟</a>
            </div>
            <input type="password" class="auth-input" id="loginPassword" placeholder="••••••••" required dir="ltr">
          </div>
          <button type="submit" class="auth-submit-btn" id="btnSubmitLogin">
            <span>تسجيل الدخول</span>
            <span>⬅</span>
          </button>
        </form>

        <!-- فورم إنشاء حساب جديد -->
        <form id="authRegisterForm" style="display:none;">
          <div class="auth-row-2">
            <div class="auth-field-group">
              <label class="auth-label">الاسم الأول</label>
              <input type="text" class="auth-input" id="regFirstName" placeholder="رامي" required>
            </div>
            <div class="auth-field-group">
              <label class="auth-label">اللقب / العائلة</label>
              <input type="text" class="auth-input" id="regLastName" placeholder="المصري" required>
            </div>
          </div>

          <div class="auth-field-group">
            <label class="auth-label">البريد الإلكتروني</label>
            <input type="email" class="auth-input" id="regEmail" placeholder="name@example.com" required dir="ltr">
          </div>

          <div class="auth-field-group">
            <label class="auth-label">كلمة المرور</label>
            <input type="password" class="auth-input" id="regPassword" placeholder="6 خانات على الأقل" required minlength="6" dir="ltr">
          </div>

          <div class="auth-field-group">
            <label class="auth-label">رقم الهاتف</label>
            <div style="display:flex; gap:8px; direction:ltr;">
              <select class="auth-select" id="regPhoneCountryCode" style="width:148px; flex-shrink:0; font-family:inherit; font-size:0.82rem; padding:0 6px;">
                <option value="+39" selected>🇮🇹 إيطاليا (+39)</option>
                <option value="+20">🇪🇬 مصر (+20)</option>
                <option value="+212">🇲🇦 المغرب (+212)</option>
                <option value="+216">🇹🇳 تونس (+216)</option>
                <option value="+213">🇩🇿 الجزائر (+213)</option>
                <option value="+218">🇱🇾 ليبيا (+218)</option>
                <option value="+249">🇸🇩 السودان (+249)</option>
                <option value="+966">🇸🇦 السعودية (+966)</option>
                <option value="+971">🇦🇪 الإمارات (+971)</option>
                <option value="+49">🇩🇪 ألمانيا (+49)</option>
                <option value="+33">🇫🇷 فرنسا (+33)</option>
                <option value="+34">🇪🇸 إسبانيا (+34)</option>
                <option value="+41">🇨🇭 سويسرا (+41)</option>
                <option value="+44">🇬🇧 بريطانيا (+44)</option>
                <option value="">🌍 أخرى</option>
              </select>
              <input type="tel" class="auth-input" id="regPhone" placeholder="345 123 4567" style="flex:1;" dir="ltr">
            </div>
          </div>

          <div class="auth-row-2">
            <div class="auth-field-group">
              <label class="auth-label">تاريخ الميلاد</label>
              <input type="date" class="auth-input" id="regBirthDate" required>
            </div>
            <div class="auth-field-group">
              <label class="auth-label">النوع</label>
              <select class="auth-select" id="regGender" required>
                <option value="male">ذكر (Maschio)</option>
                <option value="female">أنثى (Femmina)</option>
                <option value="other">غير محدد / أفضل عدم الإفصاح (Altro / Non specificato)</option>
              </select>
            </div>
          </div>

          <button type="submit" class="auth-submit-btn" id="btnSubmitRegister">
            <span>إنشاء الحساب ومزامنة الإنجاز</span>
            <span>🎉</span>
          </button>
        </form>

        <!-- فاصل أو الدخول بجوجل -->
        <div style="display:flex; align-items:center; gap:10px; margin:16px 0 6px;">
          <div style="flex:1; height:1px; background:rgba(255,255,255,0.1);"></div>
          <span style="font-size:0.75rem; color:#64748B;">أو عبر</span>
          <div style="flex:1; height:1px; background:rgba(255,255,255,0.1);"></div>
        </div>

        <button type="button" class="auth-google-btn" id="btnGoogleAuth">
          <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.15z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.35 24 12 24z"/><path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.17 0 9.98 0 12s.45 3.83 1.25 5.42l4.03-3.15z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.35 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/></svg>
          <span>المتابعة باستخدام Google</span>
        </button>
      </div>
    `;

    document.body.appendChild(modal);
    wireAuthModalEvents();
  }

  // 16. ربط أحداث النوافذ والأزرار
  function wireAuthModalEvents() {
    const modal = document.getElementById('patenteAuthModal');
    const closeBtn = document.getElementById('btnAuthClose');
    const tabLogin = document.getElementById('tabBtnLogin');
    const tabReg = document.getElementById('tabBtnRegister');
    const formLogin = document.getElementById('authLoginForm');
    const formReg = document.getElementById('authRegisterForm');
    const alertBox = document.getElementById('authAlertMsg');

    function showAlert(msg, isSuccess = false) {
      alertBox.textContent = msg;
      alertBox.className = 'auth-alert-msg ' + (isSuccess ? 'success' : 'error');
    }

    function clearAlert() {
      alertBox.textContent = '';
      alertBox.className = 'auth-alert-msg';
    }

    closeBtn.onclick = () => modal.classList.remove('open');
    modal.onclick = (e) => {
      if (e.target === modal) modal.classList.remove('open');
    };

    tabLogin.onclick = () => {
      tabLogin.classList.add('active');
      tabReg.classList.remove('active');
      formLogin.style.display = 'block';
      formReg.style.display = 'none';
      clearAlert();
    };

    tabReg.onclick = () => {
      tabReg.classList.add('active');
      tabLogin.classList.remove('active');
      formLogin.style.display = 'none';
      formReg.style.display = 'block';
      clearAlert();
    };

    // إرسال تسجيل الدخول
    formLogin.onsubmit = async (e) => {
      e.preventDefault();
      clearAlert();
      const email = document.getElementById('loginEmail').value;
      const pass = document.getElementById('loginPassword').value;
      const submitBtn = document.getElementById('btnSubmitLogin');

      submitBtn.disabled = true;
      submitBtn.innerHTML = 'جاري التحقق... ⏳';

      try {
        await loginAccount(email, pass);
        showAlert('تم تسجيل الدخول بنجاح! مرحباً بك 🚀', true);
        setTimeout(() => modal.classList.remove('open'), 900);
      } catch (err) {
        showAlert(translateFirebaseError(err.code || err.message));
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>تسجيل الدخول</span> <span>⬅</span>';
      }
    };

    // إرسال إنشاء الحساب
    formReg.onsubmit = async (e) => {
      e.preventDefault();
      clearAlert();
      const submitBtn = document.getElementById('btnSubmitRegister');

      const phoneCode = document.getElementById('regPhoneCountryCode') ? document.getElementById('regPhoneCountryCode').value : '+39';
      const phoneNum = (document.getElementById('regPhone').value || '').trim();
      const combinedPhone = phoneCode ? `${phoneCode} ${phoneNum}`.trim() : phoneNum;

      const data = {
        firstName: document.getElementById('regFirstName').value,
        lastName: document.getElementById('regLastName').value,
        email: document.getElementById('regEmail').value,
        password: document.getElementById('regPassword').value,
        phone: combinedPhone,
        birthDate: document.getElementById('regBirthDate').value,
        gender: document.getElementById('regGender').value
      };

      submitBtn.disabled = true;
      submitBtn.innerHTML = 'جاري إنشاء الحساب ومزامنة بياناتك... ⏳';

      try {
        await registerAccount(data);
        showAlert('🎉 تم إنشاء حسابك بنجاح وربط إنجازك بالسحابة!', true);
        setTimeout(() => modal.classList.remove('open'), 1200);
      } catch (err) {
        showAlert(translateFirebaseError(err.code || err.message));
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>إنشاء الحساب ومزامنة الإنجاز</span> <span>🎉</span>';
      }
    };

    // الدخول بجوجل
    document.getElementById('btnGoogleAuth').onclick = async () => {
      clearAlert();
      try {
        await loginWithGoogle();
        showAlert('تم الدخول بنجاح بحساب Google! 🎉', true);
        setTimeout(() => modal.classList.remove('open'), 900);
      } catch (err) {
        showAlert(translateFirebaseError(err.code || err.message));
      }
    };

    // نسيت كلمة المرور
    document.getElementById('btnForgotPassword').onclick = async (e) => {
      e.preventDefault();
      const email = document.getElementById('loginEmail').value;
      if (!email) {
        showAlert('يرجى كتابة بريدك الإلكتروني في الحقل أولاً لإرسال رابط الاسترجاع.');
        return;
      }
      try {
        await resetPassword(email);
        showAlert('تم إرسال رابط استعادة كلمة المرور إلى بريدك الإلكتروني بنجاح! 📧', true);
      } catch (err) {
        showAlert(translateFirebaseError(err.code || err.message));
      }
    };
  }

  // 17. ترجمة أخطاء Firebase للعربية بشكل مفهوم
  function translateFirebaseError(code) {
    if (!code) return 'حدث خطأ غير متوقع، يرجى المحاولة مرة أخرى.';
    if (code.includes('user-not-found') || code.includes('wrong-password') || code.includes('invalid-credential')) {
      return 'البريد الإلكتروني أو كلمة المرور غير صحيحة.';
    }
    if (code.includes('email-already-in-use')) {
      return 'هذا البريد الإلكتروني مسجل بالفعل بحساب آخر.';
    }
    if (code.includes('invalid-email')) {
      return 'صيغة البريد الإلكتروني غير صالحة.';
    }
    if (code.includes('weak-password')) {
      return 'كلمة المرور ضعيفة جداً، يرجى كتابة 6 خانات على الأقل.';
    }
    if (code.includes('popup-closed-by-user')) {
      return 'تم إلغاء نافذة الدخول بواسطة المستخدم.';
    }
    return code;
  }

  // 18. تحديث واجهة المستخدم عند تسجيل الخروج (Guest Mode)
  function updateAuthUiLoggedOut() {
    const pill = document.getElementById('globalAuthPill');
    if (pill) {
      pill.className = 'nav-auth-pill guest';
      pill.innerHTML = '<span>👤</span> <span>دخول / تسجيل</span>';
      pill.title = 'تسجيل الدخول أو إنشاء حساب جديد لحفظ تقدمك سحابياً';
      pill.onclick = () => {
        document.getElementById('patenteAuthModal').classList.add('open');
      };
    }

    const drop = document.getElementById('authProfileDropdown');
    if (drop) drop.classList.remove('open');
  }

  // 19. تحديث واجهة المستخدم عند تسجيل الدخول (Logged In)
  function updateAuthUiLoggedIn(profile) {
    const pill = document.getElementById('globalAuthPill');
    const name = profile.firstName || profile.displayName || profile.email.split('@')[0];

    if (pill) {
      pill.className = 'nav-auth-pill logged-in';
      pill.innerHTML = `
        <span class="auth-online-dot" id="authSyncDot"></span>
        <span>👤 ${window.escapeHtml ? window.escapeHtml(name) : name}</span>
        <span style="font-size:0.7rem;">▾</span>
      `;
      pill.title = `مسجل كـ: ${profile.email} (انقر لعرض الملف الشخصي والمزامنة)`;
      pill.onclick = (e) => {
        e.stopPropagation();
        toggleProfileDropdown(profile);
      };
    }
  }

  // 20. إدارة القائمة المنسدلة للملف الشخصي (Profile Dropdown)
  function toggleProfileDropdown(profile) {
    let drop = document.getElementById('authProfileDropdown');
    const pill = document.getElementById('globalAuthPill');
    if (!pill) return;

    if (!drop) {
      drop = document.createElement('div');
      drop.className = 'auth-profile-dropdown';
      drop.id = 'authProfileDropdown';
      pill.parentElement.appendChild(drop);
    }

    const isCurrentlyOpen = drop.classList.contains('open');
    if (isCurrentlyOpen) {
      drop.classList.remove('open');
      return;
    }

    const fullName = profile.fullName || `${profile.firstName || ''} ${profile.lastName || ''}`.trim() || profile.displayName || 'طالب رخصة القيادة';
    const email = profile.email || '';
    const phone = profile.phone || 'غير مسجل';
    const bdate = profile.birthDate || 'غير مسجل';
    const genderStr = profile.gender === 'male' ? 'ذكر 👨' : profile.gender === 'female' ? 'أنثى 👩' : 'غير محدد / آخر 👤';

    drop.innerHTML = `
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px; padding-bottom:12px; border-bottom:1px solid rgba(255,255,255,0.08);">
        <div style="width:42px; height:42px; border-radius:50%; background:#10B981; color:#FFF; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.1rem;">
          ${(profile.firstName || 'ط').charAt(0)}
        </div>
        <div>
          <div style="font-weight:800; font-size:0.95rem;">${window.escapeHtml(fullName)}</div>
          <div style="font-size:0.75rem; color:#94A3B8; direction:ltr; text-align:right;">${window.escapeHtml(email)}</div>
        </div>
      </div>

      <div style="font-size:0.78rem; color:#94A3B8; margin-bottom:12px; line-height:1.7;">
        <div>📱 <strong>الهاتف:</strong> <span dir="ltr">${window.escapeHtml(phone)}</span></div>
        <div>🎂 <strong>الميلاد:</strong> ${window.escapeHtml(bdate)}</div>
        <div>👤 <strong>النوع:</strong> ${genderStr}</div>
      </div>

      <div style="background:rgba(255,255,255,0.04); border-radius:10px; padding:10px; margin-bottom:12px; font-size:0.75rem;">
        <div id="dropdownSyncStatusText" style="color:#34D399; font-weight:700;">🟢 الحساب متصل ومتزامن سحابياً</div>
        <div style="color:#64748B; font-size:0.7rem; margin-top:2px;">يتم حفظ تقدمك تلقائياً بعد كل باب وامتحان.</div>
      </div>

      <button id="btnManualSyncNow" style="width:100%; height:36px; border-radius:10px; background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.3); color:#38BDF8; font-weight:700; font-size:0.82rem; cursor:pointer; font-family:inherit; margin-bottom:8px; display:flex; align-items:center; justify-content:center; gap:6px;">
        <span>🔄 مزامنة سحابية فورية الآن</span>
      </button>

      <button id="btnAuthLogout" style="width:100%; height:36px; border-radius:10px; background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.3); color:#EF4444; font-weight:700; font-size:0.82rem; cursor:pointer; font-family:inherit; display:flex; align-items:center; justify-content:center; gap:6px;">
        <span>🚪 تسجيل الخروج</span>
      </button>
    `;

    drop.classList.add('open');

    // زر المزامنة الفورية
    document.getElementById('btnManualSyncNow').onclick = async () => {
      const btn = document.getElementById('btnManualSyncNow');
      btn.innerHTML = 'جاري المزامنة... ⏳';
      btn.disabled = true;
      await uploadLocalProgressToCloud(currentUser.uid);
      btn.innerHTML = '✅ تمت المزامنة بنجاح!';
      setTimeout(() => {
        btn.innerHTML = '<span>🔄 مزامنة سحابية فورية الآن</span>';
        btn.disabled = false;
      }, 1500);
    };

    // زر تسجيل الخروج
    document.getElementById('btnAuthLogout').onclick = async () => {
      if (confirm('هل تريد تسجيل الخروج من حسابك؟')) {
        await logoutAccount();
        drop.classList.remove('open');
      }
    };

    // إغلاق عند النقر بالخارج
    const closeListener = (evt) => {
      if (!drop.contains(evt.target) && evt.target !== pill) {
        drop.classList.remove('open');
        document.removeEventListener('click', closeListener);
      }
    };
    setTimeout(() => document.addEventListener('click', closeListener), 10);
  }

  function updateSyncIndicator(isSync) {
    const dot = document.getElementById('authSyncDot');
    if (dot) {
      dot.className = isSync ? 'auth-online-dot syncing' : 'auth-online-dot';
    }
  }

  function updateSyncStatusText(text) {
    const el = document.getElementById('dropdownSyncStatusText');
    if (el) el.textContent = text;
  }

  // 21. الواجهة البرمجية العامة المعرضة للتطبيق (Global API)
  window.PatenteAuth = {
    init: initFirebase,
    register: registerAccount,
    login: loginAccount,
    loginWithGoogle: loginWithGoogle,
    logout: logoutAccount,
    resetPassword: resetPassword,
    syncToCloud: () => currentUser ? uploadLocalProgressToCloud(currentUser.uid) : Promise.resolve(),
    pullFromCloud: () => currentUser ? pullCloudProgressToLocal(currentUser.uid) : Promise.resolve(),
    getCurrentUser: () => currentUser,
    getUserProfile: () => userProfile,
    openAuthModal: () => {
      const modal = document.getElementById('patenteAuthModal');
      if (modal) modal.classList.add('open');
    }
  };

  // تهيئة وتشغيل المحرك فورياً
  function startEngine() {
    injectAuthStyles();
    injectAuthModalHtml();
    initFirebase();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startEngine);
  } else {
    startEngine();
  }

})();
